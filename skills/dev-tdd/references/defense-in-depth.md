# Defense-in-Depth Validation

Reference guide for layered validation that makes bugs structurally impossible rather than merely caught at one checkpoint.

The principle: no single validation layer is trusted. Each layer assumes the previous one might have failed or been bypassed.

---

## The Four Layers

### Layer 1: Entry Point Validation

Validate everything that enters the system from the outside. API inputs, user form data, file uploads, query parameters, webhook payloads. Trust nothing.

```typescript
// API endpoint - validate shape, type, and constraints
function createUser(req: Request, res: Response) {
  const { name, email, age } = req.body;

  if (typeof name !== "string" || name.trim().length === 0) {
    return res.status(400).json({ error: "name is required" });
  }
  if (typeof email !== "string" || !email.includes("@")) {
    return res.status(400).json({ error: "valid email is required" });
  }
  if (typeof age !== "number" || age < 0 || age > 150) {
    return res.status(400).json({ error: "age must be 0-150" });
  }

  // Only clean, validated data passes to business logic
  return userService.create({ name: name.trim(), email, age });
}
```

This layer rejects garbage early. It should never assume the caller is well-behaved.

---

### Layer 2: Business Logic Validation

Enforce invariants and state transitions. Even if Layer 1 passed valid-shaped data, the business rules might reject it.

```typescript
class OrderService {
  cancel(order: Order): Order {
    // State transition guard
    if (order.status === "shipped") {
      throw new InvalidOperationError(
        `Cannot cancel order ${order.id}: already shipped`
      );
    }
    if (order.status === "cancelled") {
      throw new InvalidOperationError(
        `Order ${order.id} is already cancelled`
      );
    }

    // Invariant: only pending or confirmed orders can be cancelled
    const cancellable = ["pending", "confirmed"];
    if (!cancellable.includes(order.status)) {
      throw new InvalidOperationError(
        `Order ${order.id} in non-cancellable state: ${order.status}`
      );
    }

    return { ...order, status: "cancelled", cancelledAt: new Date() };
  }
}
```

This layer catches logic errors that pass input validation. A well-formed request to cancel a shipped order is syntactically valid but logically wrong.

---

### Layer 3: Environment Guards

Verify that configuration, feature flags, and permissions are correct before executing. Do not assume the environment is properly set up.

```typescript
function processPayment(order: Order, config: AppConfig): PaymentResult {
  // Config guard
  if (!config.paymentGatewayUrl) {
    throw new ConfigurationError("paymentGatewayUrl is not configured");
  }
  if (!config.paymentApiKey) {
    throw new ConfigurationError("paymentApiKey is not configured");
  }

  // Feature flag guard
  if (!config.features.paymentsEnabled) {
    throw new FeatureDisabledError("Payments are currently disabled");
  }

  // Permission guard
  if (!order.user.permissions.includes("make_purchases")) {
    throw new PermissionError(
      `User ${order.user.id} lacks make_purchases permission`
    );
  }

  return gateway.charge(order.total, config.paymentApiKey);
}
```

Environment guards catch deployment mistakes: missing env vars, disabled features, and misconfigured permissions. Without them, the code runs with bad assumptions and produces confusing failures downstream.

---

### Layer 4: Debug Instrumentation

Logging, monitoring, and alerts that make problems visible when they happen. This layer does not prevent bugs - it ensures you find them fast.

```typescript
function processOrder(order: Order): ProcessedOrder {
  logger.info("Processing order", {
    orderId: order.id,
    userId: order.user.id,
    itemCount: order.items.length,
    total: order.total,
  });

  const result = orderPipeline.run(order);

  if (result.status === "failed") {
    logger.error("Order processing failed", {
      orderId: order.id,
      failureReason: result.reason,
      failedAtStep: result.failedStep,
    });
    metrics.increment("order.processing.failure", {
      reason: result.reason,
    });
  } else {
    logger.info("Order processed successfully", { orderId: order.id });
    metrics.increment("order.processing.success");
  }

  return result;
}
```

Log enough to reconstruct what happened. Include identifiers (order ID, user ID) so you can trace a specific request. Alert on failure rates, not individual failures.

---

## The Pattern: Trace, Map, Validate, Test

Apply defense-in-depth to any feature by following this sequence:

1. **Trace data flow.** Follow the data from where it enters the system to where it produces output. Draw the path.

2. **Map checkpoints.** At each boundary (API handler, service method, database call, external API call), mark a checkpoint.

3. **Add validation at each checkpoint.** Each checkpoint validates what it receives, independent of what previous checkpoints did.

4. **Test each layer independently.** Unit test each validation layer. Then integration test the full flow to verify layers work together.

```
Request  -->  [Layer 1: Input]  -->  [Layer 2: Logic]  -->  [Layer 3: Env]  -->  Execute
                  |                      |                      |
              Rejects bad shape     Rejects bad state     Rejects bad config
                  |                      |                      |
              [Layer 4: Log]        [Layer 4: Log]        [Layer 4: Log]
```

---

## Testing Each Layer

Each layer gets its own tests:

```typescript
// Layer 1: bad input is rejected
test("rejects missing name", () => { ... });
test("rejects invalid email format", () => { ... });

// Layer 2: business rules enforced
test("cannot cancel shipped order", () => { ... });
test("cannot cancel already-cancelled order", () => { ... });

// Layer 3: environment problems caught
test("throws when payment gateway URL missing", () => { ... });
test("throws when payments feature disabled", () => { ... });

// Integration: full flow works when all layers pass
test("creates order end-to-end with valid input and config", () => { ... });
```

---

## Goal

Make bugs structurally impossible. If bad data cannot reach the business logic, the business logic cannot produce wrong results from bad data. If the environment is verified before execution, missing config cannot cause silent failures.

Each layer is a fence. One fence can be jumped. Four fences, each checking different things, are much harder to bypass.
