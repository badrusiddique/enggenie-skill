# Condition-Based Waiting

Reference guide for replacing arbitrary timeouts with polling that checks actual conditions. Arbitrary timeouts are the leading cause of flaky tests and unreliable async code.

---

## The Problem with Arbitrary Timeouts

```typescript
// Bad: assumes 500ms is enough, but sometimes it is not
setTimeout(() => {
  expect(document.querySelector(".loaded")).toBeTruthy();
}, 500);
```

This fails on slow CI machines. On fast machines, it wastes 400ms of unnecessary waiting. The timeout duration is a guess, not a contract.

---

## The Pattern: Poll for a Condition

Instead of waiting a fixed duration, poll repeatedly until the condition is true or a timeout expires.

```typescript
async function waitFor(
  condition: () => boolean | Promise<boolean>,
  options: { timeout?: number; interval?: number; description?: string } = {}
): Promise<void> {
  const { timeout = 5000, interval = 10, description = "condition" } = options;
  const start = Date.now();

  while (true) {
    const result = await condition();
    if (result) return;

    if (Date.now() - start >= timeout) {
      throw new Error(
        `waitFor timed out after ${timeout}ms waiting for: ${description}`
      );
    }

    await new Promise((resolve) => setTimeout(resolve, interval));
  }
}
```

### Usage

```typescript
// Wait for an element to appear
await waitFor(
  () => document.querySelector(".loaded") !== null,
  { description: "loaded class to appear" }
);

// Wait for a value to be set
await waitFor(
  () => store.getState().user !== undefined,
  { description: "user to be loaded into store" }
);

// Wait for an async condition
await waitFor(
  async () => {
    const response = await fetch("/api/status");
    const data = await response.json();
    return data.status === "ready";
  },
  { timeout: 10000, description: "API to report ready status" }
);
```

---

## Key Rules

### Poll Every 10ms, Not Faster

Polling faster than 10ms wastes CPU without meaningfully reducing wait time. Most async operations resolve in tens or hundreds of milliseconds. A 10ms poll interval means you detect completion within 10ms of it happening.

```typescript
// Bad: polling too fast, burns CPU
const interval = 1; // 1ms poll = 1000 checks per second

// Good: 10ms poll catches most events nearly instantly
const interval = 10;
```

### Always Include a Timeout

Never poll forever. A missing timeout turns a test failure into a test hang, which is worse.

```typescript
// Bad: polls forever if condition never becomes true
while (!condition()) {
  await sleep(10);
}

// Good: fails with a clear message after timeout
const start = Date.now();
while (!condition()) {
  if (Date.now() - start >= 5000) {
    throw new Error("Timed out waiting for condition");
  }
  await sleep(10);
}
```

The timeout should be generous enough to never trigger on correct code (5-10 seconds for most operations), but short enough to fail fast when something is actually broken.

### Call the Getter Inside the Loop

The condition function must fetch fresh data on each call. Capturing a stale reference defeats the purpose.

```typescript
// Bad: captured stale reference
const element = document.querySelector(".status");
await waitFor(() => element?.textContent === "Done");
// element was captured once — even if the DOM updates, this checks the old reference

// Good: fresh query each poll
await waitFor(() => {
  const element = document.querySelector(".status");
  return element?.textContent === "Done";
});
```

### Include a Description

When the wait times out, the error message should say what was being waited for. Without a description, you get "timed out" with no context.

```typescript
// Bad: no context on failure
await waitFor(() => result !== undefined);
// Error: "waitFor timed out after 5000ms waiting for: condition"

// Good: clear failure message
await waitFor(() => result !== undefined, {
  description: "payment processing result to be available",
});
// Error: "waitFor timed out after 5000ms waiting for: payment processing result to be available"
```

---

## When an Arbitrary Timeout IS Correct

Sometimes a fixed delay is the right choice, but only when you know the specific timing and can document why.

Valid cases:
- **Debounce tests:** You are testing a 300ms debounce. Waiting 350ms is correct because the debounce duration is a known, fixed value.
- **Animation tests:** An animation takes exactly 200ms per the CSS. Waiting 250ms is correct.
- **Rate limit tests:** The rate limiter resets every 1000ms. Waiting 1100ms is correct.

In all valid cases, the timeout is derived from a known constant, not a guess.

```typescript
// Valid: debounce is a known 300ms, wait slightly longer
const DEBOUNCE_MS = 300;
await triggerInput("search term");
await sleep(DEBOUNCE_MS + 50); // 50ms buffer for execution
expect(fetchSpy).toHaveBeenCalledTimes(1);
// Document WHY this timeout exists:
// The search input has a 300ms debounce. We wait 350ms to ensure
// the debounced handler has fired exactly once.
```

If you cannot point to a specific, documented timing constant that justifies the delay, use condition-based waiting instead.

---

## Framework-Specific Equivalents

Most testing frameworks provide built-in condition-based waiting:

```typescript
// React Testing Library
await waitFor(() => {
  expect(screen.getByText("Loaded")).toBeInTheDocument();
});

// Playwright
await page.waitForSelector(".loaded");
await expect(page.locator(".status")).toHaveText("Done");

// Cypress
cy.get(".loaded").should("exist");
cy.get(".status").should("have.text", "Done");
```

Use framework utilities when available. They handle polling intervals, timeouts, and error messages correctly. Write a custom `waitFor` only when the framework does not cover your case.

---

## Checklist

1. Replace every `setTimeout` in tests with condition-based waiting
2. Poll at 10ms intervals, not faster
3. Always set a timeout (5-10 seconds for most operations)
4. Query fresh data inside the condition function, not captured references
5. Include a description for clear timeout error messages
6. If using a fixed delay, document the specific timing constant it is based on
