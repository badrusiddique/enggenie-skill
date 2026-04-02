# Multi-Component Debugging

Reference guide for debugging issues that span multiple components, services, or layers. When the bug is not in one place but somewhere between places, this technique finds it.

---

## The Problem

In multi-component systems, data flows through several boundaries: API gateway to service, service to database, service to external API, frontend to backend. A bug at any boundary can produce symptoms elsewhere. Without systematic diagnosis, you guess which component is broken and waste time investigating the wrong one.

---

## The Technique: Boundary Logging

Add diagnostic logging at EACH component boundary. Log data entering and exiting every component. Run the failing scenario once. Read the logs. The bug is at the boundary where correct input produces wrong output.

### Step 1: Map the Component Chain

Before adding any logging, draw the data flow:

```
Client Request
    |
    v
API Gateway  -->  Auth Middleware  -->  Route Handler
                                            |
                                            v
                                      Service Layer  -->  Database
                                            |
                                            v
                                      External API (payment gateway)
```

Identify every boundary where data crosses from one component to another.

### Step 2: Add Entry/Exit Logging at Each Boundary

For each component, log what goes in and what comes out.

```typescript
// API Route Handler
app.post("/orders", async (req, res) => {
  console.log("[BOUNDARY] Route handler ENTRY:", {
    body: req.body,
    headers: { authorization: req.headers.authorization ? "present" : "missing" },
    userId: req.user?.id,
  });

  const result = await orderService.create(req.body, req.user);

  console.log("[BOUNDARY] Route handler EXIT:", {
    status: result.status,
    orderId: result.order?.id,
    error: result.error,
  });

  res.status(result.status).json(result);
});
```

```typescript
// Service Layer
class OrderService {
  async create(input: OrderInput, user: User): Promise<OrderResult> {
    console.log("[BOUNDARY] OrderService.create ENTRY:", {
      itemCount: input.items?.length,
      userId: user?.id,
      total: input.total,
    });

    // Validate
    const validated = this.validate(input);
    console.log("[BOUNDARY] OrderService validation result:", {
      valid: validated.valid,
      errors: validated.errors,
    });

    // Save to database
    const saved = await this.repository.save(validated.order);
    console.log("[BOUNDARY] Database save result:", {
      savedId: saved?.id,
      savedStatus: saved?.status,
    });

    // Call payment gateway
    const payment = await this.paymentClient.charge(saved);
    console.log("[BOUNDARY] Payment gateway result:", {
      paymentId: payment?.id,
      paymentStatus: payment?.status,
      error: payment?.error,
    });

    return { status: 200, order: saved };
  }
}
```

```typescript
// Database Repository
class OrderRepository {
  async save(order: Order): Promise<Order> {
    console.log("[BOUNDARY] Repository.save ENTRY:", {
      orderId: order.id,
      itemCount: order.items.length,
      status: order.status,
    });

    const result = await this.db.insert("orders", order);

    console.log("[BOUNDARY] Repository.save EXIT:", {
      insertedId: result.insertedId,
      acknowledged: result.acknowledged,
    });

    return { ...order, id: result.insertedId };
  }
}
```

### Step 3: Verify Environment and Config Propagation

Components often share configuration: database URLs, API keys, feature flags. Log these at startup and verify they match expectations.

```typescript
console.log("[CONFIG] Service startup:", {
  dbHost: config.database.host,
  dbName: config.database.name,
  paymentGatewayUrl: config.payment.url,
  paymentEnv: config.payment.environment, // "sandbox" vs "production"
  featureFlags: config.features,
});
```

Config mismatches between components are a common source of "works locally, fails in staging" bugs.

### Step 4: Check State at Each Layer

If the system maintains state (caches, sessions, queues), log state before and after operations.

```typescript
console.log("[STATE] Cache before lookup:", {
  cacheSize: cache.size,
  hasKey: cache.has(userId),
});

const cached = cache.get(userId);

console.log("[STATE] Cache lookup result:", {
  found: cached !== undefined,
  value: cached,
});
```

### Step 5: Run Once, Analyze, Focus

Run the failing scenario exactly once with all boundary logging active. Then read the logs in order.

Look for the first boundary where things go wrong:

```
[BOUNDARY] Route handler ENTRY: { body: { items: [{ id: 1 }], total: 25.00 }, userId: 42 }
[BOUNDARY] OrderService.create ENTRY: { itemCount: 1, userId: 42, total: 25.00 }
[BOUNDARY] OrderService validation result: { valid: true, errors: [] }
[BOUNDARY] Database save result: { savedId: 101, savedStatus: "pending" }
[BOUNDARY] Payment gateway result: { paymentId: null, paymentStatus: null, error: "invalid_amount" }
```

The data was correct through validation and database save. The payment gateway returned an error. Now investigate only the payment integration - not the route handler, not the database.

---

## Example: Diagnosing a Missing Order

**Symptom:** User creates an order, gets a success response, but the order does not appear in their order history.

**Boundary logging reveals:**

```
[BOUNDARY] Route handler ENTRY: { userId: 42, items: [...] }
[BOUNDARY] OrderService.create ENTRY: { userId: 42 }
[BOUNDARY] Database save result: { savedId: 101, savedStatus: "pending" }
[BOUNDARY] Route handler EXIT: { status: 200, orderId: 101 }
```

Order was saved. Now check the read path:

```
[BOUNDARY] OrderService.listForUser ENTRY: { userId: 42 }
[BOUNDARY] Repository.findByUser ENTRY: { userId: 42, statusFilter: "completed" }
[BOUNDARY] Repository.findByUser EXIT: { count: 0, query: "SELECT * FROM orders WHERE user_id=42 AND status='completed'" }
```

Found it. The read query filters by `status='completed'`, but the order was saved with `status='pending'`. The order exists but is excluded by the filter. The bug is in the query, not in the save logic.

---

## Cleanup

After identifying the failing component:

1. Remove all `[BOUNDARY]` diagnostic logging
2. Fix the identified component
3. Add permanent structured logging at key boundaries (not the verbose diagnostic kind, but enough to trace issues in production)
4. Add a test that covers the specific failure mode you found
