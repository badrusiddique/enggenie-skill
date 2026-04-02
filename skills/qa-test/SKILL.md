---
name: qa-test
description: Use for QA-perspective testing - Playwright automation or manual browser testing focused on user journeys, not implementation details
---

# enggenie:qa-test

## Announcement

When this skill is invoked, announce:

> I'm using enggenie:qa-test for [automation/manual] QA testing.

Replace `[automation/manual]` with the appropriate mode based on user request or context.

---

## Key Distinction

- **enggenie:qa-verify** asks: "Does my code work?"
- **enggenie:qa-test** asks: "Does the product work for users?"

qa-verify is developer-facing - unit tests, integration tests, type checks, lint passes. qa-test is user-facing - can a real person accomplish their goal using this product? The difference matters. A feature can pass every unit test and still be broken for users.

---

## Automation Mode (Playwright)

### Reading Acceptance Criteria

Before writing any tests, check if `pm-refine` produced a spec for this feature. If a spec exists, extract the acceptance criteria and map each criterion to one or more test scenarios. If no spec exists, ask the user for the expected behavior or derive it from the feature description.

### Writing Tests for User Journeys

QA tests what the user does, not what the code does. Every test should represent a real user scenario - navigating, clicking, filling forms, waiting for results.

```python
# QA tests what the user does, not what the code does
def test_user_can_filter_by_team():
    page.goto('http://localhost:3000/dashboard')
    page.wait_for_load_state('networkidle')
    page.click('text=Filter')
    page.click('text=Team A')
    items = page.locator('.item-row').all()
    assert all('Team A' in item.text_content() for item in items)
```

Do not test internal functions, database queries, or API response shapes. Test what the user sees and does.

### Server Lifecycle Management

Use `scripts/with_server.py` for server lifecycle management. This script handles:

- Starting the application server
- Waiting for the server to be ready (health check)
- Running the test suite
- Stopping the server after tests complete (regardless of pass/fail)

This avoids orphaned server processes and ensures clean test runs.

### Recon-Then-Action Pattern

Always follow this sequence when interacting with pages:

```
1. Navigate to target page
2. Wait for networkidle
3. Take screenshot or inspect DOM
4. Identify correct selectors from actual page content
5. THEN execute actions
```

Never: guess selectors, skip waiting, act on stale state.

This pattern prevents flaky tests caused by racing against page loads, dynamic content, or incorrect assumptions about the DOM structure.

---

## Manual Mode (Browser-Assisted)

### Test Plan Source

Take the QA test plan from the spec (if `pm-refine` produced one) or directly from the user. The test plan should list scenarios with steps and expected outcomes.

### Execution Process

For each test scenario:

1. **Navigate** to the page under test.
2. **Screenshot** the initial state before any interaction.
3. **Execute** the steps - click, fill, submit, scroll, hover, whatever the scenario requires.
4. **Screenshot** the result after the steps complete.
5. **Compare** the actual result against the expected result from the test plan.
6. **Report** the outcome as PASS or FAIL with screenshot evidence attached.

### Generate Test Matrix Report

After all scenarios are executed, compile the results into a test matrix.

---

## Recon-Then-Action Pattern (Detailed)

This pattern is the foundation of reliable browser testing, whether automated or manual. It applies everywhere.

```
1. Navigate to target page
2. Wait for networkidle
3. Take screenshot or inspect DOM
4. Identify correct selectors from actual page content
5. THEN execute actions
```

### Why This Matters

- Pages load asynchronously. Content may not be present when the URL resolves.
- Selectors guessed from code may not match the rendered DOM (dynamic classes, conditional rendering, lazy loading).
- Screenshots provide ground truth. If you can see it, you can interact with it. If you cannot see it, do not try.

### Common Violations

- Clicking a button immediately after `goto()` without waiting.
- Using a CSS class from the source code that gets transformed at build time.
- Assuming an element exists because the route loaded.
- Retrying a failed action without re-inspecting the page state.

---

## QA Mindset

Think like a QA engineer, not a developer. Developers test the happy path and move on. QA engineers ask uncomfortable questions:

- **Empty data:** What happens when there are no items, no results, no history? Does the UI show a helpful empty state or crash?
- **Maximum data:** What happens with 1000 rows, a 500-character name, a deeply nested structure? Does it paginate, truncate, or break?
- **Double-click:** What if the user clicks the submit button twice quickly? Does it submit twice? Does it disable after the first click?
- **Slow network:** What if the API takes 5 seconds to respond? Is there a loading indicator? Does the UI remain interactive?
- **Back button:** What if the user completes step 3 of a wizard and hits the browser back button? Does it go to step 2 or somewhere unexpected?
- **Screen sizes:** Does the layout work on mobile (375px), tablet (768px), and desktop (1440px)? Do elements overlap or overflow?
- **Keyboard navigation:** Can a user tab through the form, press Enter to submit, and use Escape to close modals? Is focus management correct?

Build tests for these scenarios, not just the feature's primary use case.

---

## Test Matrix Report Format

Use this format to report results, whether from automated or manual testing:

```markdown
| Scenario | Steps | Expected | Actual | Status |
|----------|-------|----------|--------|--------|
| Login with valid creds | Enter email, password, click Login | Redirect to dashboard | Redirected to /dashboard | PASS |
| Login with wrong password | Enter email, wrong password, click Login | Error message shown | "Invalid credentials" displayed | PASS |
| Login with empty fields | Click Login without entering anything | Validation errors on both fields | Email field highlighted, password field not highlighted | FAIL |
| Login on mobile viewport | Same as valid login at 375px width | Redirect to dashboard, no layout issues | Login button partially hidden by keyboard | FAIL |
```

Every FAIL row must include:
- What was expected
- What actually happened
- Screenshot evidence (if manual mode)
- Severity assessment (blocker, major, minor)

---

## Subagents

### QA Automation Subagent (sonnet)

Writes and runs Playwright tests with a QA mindset. This subagent:

- Reads the spec or acceptance criteria
- Writes Playwright test files covering user journeys
- Runs tests using `scripts/with_server.py`
- Reports results in test matrix format
- Follows the recon-then-action pattern strictly

Prompt template: `agents/qa-automation-agent.md`

### QA Manual Subagent (sonnet)

Executes a manual test plan via browser interaction and screenshots. This subagent:

- Takes the test plan (from spec or user)
- Opens the application in a browser
- Walks through each scenario step by step
- Captures before/after screenshots
- Compiles results into a test matrix report

Prompt template: `agents/qa-manual-agent.md`

---

## Workflow Position

### Entry

This skill is invoked after the feature has been implemented and dev-verified. The expected prior step is `enggenie:qa-verify` - the developer has confirmed that unit tests pass, linting is clean, and the build succeeds. Now it is time to verify the product works for users.

### Exit

After testing is complete:

- **All tests pass:** Proceed to `enggenie:deploy-ship`.
- **Any tests fail:** Route failures back to the developer with the test matrix report, screenshot evidence, and reproduction steps. Do not proceed to deploy-ship until failures are resolved and retested.

---

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Automation tool | Playwright (Python) |
| Server management | `scripts/with_server.py` |
| Test focus | User journeys, not implementation |
| Page interaction pattern | Recon-then-action |
| Automation subagent | `agents/qa-automation-agent.md` (sonnet) |
| Manual subagent | `agents/qa-manual-agent.md` (sonnet) |
| Predecessor | enggenie:qa-verify |
| Successor (pass) | enggenie:deploy-ship |
| Successor (fail) | Back to developer |
