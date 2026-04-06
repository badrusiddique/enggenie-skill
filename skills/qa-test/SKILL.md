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

## Jira Ticket Entry

When the user references a Jira ticket (e.g., "Test PROJ-1234", "QA PROJ-1234"):

1. Read the Jira ticket using MCP tools
2. Find the "For QA" section in the ticket description — it contains the spec path, key edge cases, and Playwright scenarios written by the PM
3. Find the "Dev Handoff" comment — it contains the PR link, what was built, known limitations, and focus areas written by the Dev
4. Open the linked spec file. Extract the acceptance criteria, QA test plan table, and Playwright automation scenarios
5. Open the PR to understand what code changed

This gives you the full chain: what PM specified → what Dev built → what QA should verify. If any piece is missing, ask the user for clarification.

If Jira MCP is not available, ask: "I can't read PROJ-1234 directly. Can you share the spec path and PR link?"

---

## Automation Mode (Playwright)

### Reading Acceptance Criteria

Before writing any tests, check for context in this order:

1. **Jira ticket** (if referenced) — read the "For QA" section and "Dev Handoff" comment for spec path, focus areas, and known limitations
2. **Spec file** (if `pm-refine` produced one) — extract acceptance criteria, QA test plan table, and Playwright scenarios
3. **User description** — if neither Jira nor spec exists, ask the user for the expected behavior

Map each acceptance criterion to one or more test scenarios. Pay special attention to the "Focus areas" from the Dev Handoff — these are the areas the Dev flagged as needing QA attention.

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

If the project has a server lifecycle script (e.g., a wrapper that starts the server, waits for readiness, runs tests, and stops the server), use it. This pattern avoids orphaned server processes and ensures clean test runs.

Recommended lifecycle steps:
- Start the application server
- Wait for the server to be ready (health check)
- Run the test suite
- Stop the server after tests complete (regardless of pass/fail)

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
- Runs tests with proper server lifecycle management
- Reports results in test matrix format
- Follows the recon-then-action pattern strictly

### QA Manual Subagent (sonnet)

Executes a manual test plan via browser interaction and screenshots. This subagent:

- Takes the test plan (from spec or user)
- Opens the application in a browser
- Walks through each scenario step by step
- Captures before/after screenshots
- Compiles results into a test matrix report

---

## Workflow Position

### Entry

This skill is invoked after the feature has been implemented and dev-verified. The expected prior step is `enggenie:qa-verify` - the developer has confirmed that unit tests pass, linting is clean, and the build succeeds. Now it is time to verify the product works for users.

### Exit

After testing is complete:

- **All tests pass:** Proceed to `enggenie:deploy-ship`.
- **Any tests fail:** Route failures back to the developer with the test matrix report, screenshot evidence, and reproduction steps. Do not proceed to deploy-ship until failures are resolved and retested.

### Update Jira with QA Results

If a Jira ticket is associated with this work, add a comment with the QA results:

```markdown
## QA Results
- Status: [PASS / FAIL — X of Y scenarios passed]
- Test matrix: [summary or link to full report]
- Bugs found:
  - [Bug 1: description, severity, reproduction steps]
  - [Bug 2: description, severity, reproduction steps]
  - Or "None — all scenarios passed"
- Automation coverage: [X Playwright tests added at path/to/tests/]
- Areas not tested: [anything skipped with reason — or "Full coverage per spec"]
```

This closes the loop. The PM who wrote the spec can see what passed and what didn't. The Dev who built it can see exactly what failed and reproduce it. No Slack threads needed.

---

## Subagent Context Preservation

When subagents (QA Automation, QA Manual) complete their work, explicitly capture their key outputs back to the main conversation:

- **QA Automation subagent:** Test file paths created, pass/fail results, test matrix
- **QA Manual subagent:** Screenshot evidence paths, test scenario results, test matrix report

Do not assume the orchestrating agent retains subagent context automatically. Extract the full test results before reporting.

---

## Recommended Model

**Primary:** sonnet
**Why:** QA testing requires understanding user journeys, writing robust Playwright tests, and identifying edge cases. Sonnet balances quality with speed.

This is a recommendation. Ask the user: "Confirm model selection or override?" Do not proceed until the user responds.

---

## Quick Reference

| Aspect | Detail |
|--------|--------|
| Automation tool | Playwright (Python) |
| Server management | Project server lifecycle script |
| Test focus | User journeys, not implementation |
| Page interaction pattern | Recon-then-action |
| Automation subagent | QA Automation (sonnet) |
| Manual subagent | QA Manual (sonnet) |
| Predecessor | enggenie:qa-verify |
| Successor (pass) | enggenie:deploy-ship |
| Successor (fail) | Back to developer |
