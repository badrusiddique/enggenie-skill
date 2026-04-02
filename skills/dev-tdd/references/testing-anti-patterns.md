# Testing Anti-Patterns

Reference guide for common testing mistakes that erode test suite value. Each pattern includes what goes wrong and how to fix it.

---

## 1. Testing Mock Behavior Instead of Real Code

Mocks are scaffolding. They exist to isolate the unit under test. If your assertions verify what the mock did, you are testing your test setup, not your code.

**Bad - asserting on mock calls:**
```typescript
const mockRepo = jest.fn().mockReturnValue({ id: 1, name: "Alice" });
const service = new UserService(mockRepo);
service.getUser(1);
expect(mockRepo).toHaveBeenCalledWith(1); // tests the mock, not the service
```

**Good - asserting on real behavior:**
```typescript
const mockRepo = jest.fn().mockReturnValue({ id: 1, name: "Alice" });
const service = new UserService(mockRepo);
const result = service.getUser(1);
expect(result.name).toBe("Alice"); // tests what the service actually returns
```

The mock enables the test. The assertion targets the real code.

---

## 2. Adding Test-Only Methods to Production Classes

If you need a `getInternalState()` method just for testing, your design is wrong. Test-only methods bloat the public API, create maintenance burden, and signal that behavior is not observable through normal interfaces.

**Bad:**
```typescript
class OrderProcessor {
  private queue: Order[] = [];
  processOrder(order: Order) { this.queue.push(order); }
  // exists only for tests
  getQueueForTesting(): Order[] { return this.queue; }
}
```

**Good - test through observable behavior:**
```typescript
class OrderProcessor {
  private queue: Order[] = [];
  processOrder(order: Order) { this.queue.push(order); }
  pendingCount(): number { return this.queue.length; }
}

// Test uses the real public API
processor.processOrder(order);
expect(processor.pendingCount()).toBe(1);
```

If there is no way to observe the behavior through public API, either the behavior does not matter or the class needs a design change.

---

## 3. Mocking Without Understanding What You Replace

Every mock is an assumption about the replaced component. If you mock a database client without understanding its error handling, retry logic, or return shape, your test is built on a fantasy.

Before mocking, answer:
- What does the real component return on success?
- What does it return on failure?
- Does it throw, return null, or return an error object?
- Are there side effects (logging, metrics, state changes)?

If you cannot answer these, read the real implementation first.

---

## 4. Partial Mock Data Structures

Returning `{ id: 1 }` when the real object has 12 fields hides bugs. Code that accesses `user.email` will get `undefined` in the test but a real value in production. The test passes. Production breaks.

**Bad - partial mock hides missing field access:**
```typescript
const mockUser = { id: 1, name: "Alice" };
// Real User has: id, name, email, role, createdAt, preferences...
const result = formatUserCard(mockUser);
expect(result).toContain("Alice");
// formatUserCard also uses user.email - undefined here, but test passes
```

**Good - complete mock data:**
```typescript
function createTestUser(overrides: Partial<User> = {}): User {
  return {
    id: 1,
    name: "Alice",
    email: "alice@example.com",
    role: "member",
    createdAt: new Date("2024-01-01"),
    preferences: { theme: "light", notifications: true },
    ...overrides,
  };
}

const result = formatUserCard(createTestUser());
expect(result).toContain("Alice");
expect(result).toContain("alice@example.com");
```

Use factory functions that return complete objects. Override only what the specific test cares about.

---

## 5. Integration Tests as an Afterthought

Integration tests verify that components work together. Bolting them on after everything is built means you discover integration failures late, when they are expensive to fix.

**Plan integration tests alongside unit tests:**
- Unit tests: Does each function do its job?
- Integration tests: Do the functions work together with real dependencies?

Write at least one integration test per user-facing flow before calling the feature done. If you wait, you will not write them at all.

---

## 6. Testing Implementation Details Instead of Behavior

If renaming a private method breaks your test, the test is coupled to implementation. Tests should describe what the code does, not how it does it.

**Bad - coupled to internal method name:**
```typescript
const spy = jest.spyOn(service, "internalCalculate" as any);
service.processPayment(100);
expect(spy).toHaveBeenCalled();
```

**Good - tests observable output:**
```typescript
const result = service.processPayment(100);
expect(result.charged).toBe(100);
expect(result.status).toBe("completed");
```

Refactoring should not break tests. If it does, the tests are testing the wrong thing.

---

## 7. Flaky Tests with Arbitrary Timeouts

`setTimeout(() => expect(...), 500)` is a coin flip. On a slow CI machine, 500ms is not enough. On a fast machine, it wastes time.

**Bad - arbitrary wait:**
```typescript
setTimeout(() => {
  expect(element.textContent).toBe("Loaded");
}, 500);
```

**Good - condition-based waiting:**
```typescript
await waitFor(() => {
  expect(element.textContent).toBe("Loaded");
});
```

Replace every `setTimeout` in tests with a polling mechanism that checks the actual condition. See the `condition-based-waiting` reference for the full pattern.

---

## Quick Checklist

Before merging any test, verify:

1. Assertions target real code output, not mock behavior
2. No test-only methods exist on production classes
3. Mocked components are understood and fully shaped
4. Mock data structures are complete, not partial
5. Integration tests exist for the flow, not just unit tests
6. Tests break only when behavior changes, not when implementation changes
7. No arbitrary timeouts - all waits are condition-based
