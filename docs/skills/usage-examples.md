# enggenie Skill Usage Examples

> Real-world examples showing exactly what to say and what happens for each skill.

## How to Read These Examples

Each example shows:
- **What you say** - The exact prompt you type
- **What happens** - Step-by-step description of the skill's behavior
- **What you see** - Example output you should expect
- **Tips** - Pro tips for getting the most out of the skill

---

## PM Role

### enggenie:pm-refine - Write Specs and Refine Stories

**Example 1: Generate a feature spec**

What you say:
> "I want to build a user notification system that sends email alerts when tasks are overdue"

What happens:
1. The skill announces: "I'm using enggenie:pm-refine to generate a feature specification."
2. It asks clarifying questions one at a time:
   - "Which repos/services will this touch?"
   - "Should notifications be real-time or batched daily?"
   - "Do you have a Figma design for the notification preferences UI?"
3. After your answers, it generates a full spec with:
   - Summary and architecture context
   - Functional requirements
   - Acceptance criteria (user-level and technical)
   - Edge cases (what if email fails? what about timezone differences?)
   - QA test plan
   - Story point estimate with transparent math

What you see:
```
Spec saved to docs/specs/user-notifications.md
Estimated: 5 story points (Backend: 3h + Frontend: 2h + Testing: 1h = 3.6h raw, anchored at 5 on Fibonacci scale)
Next: invoke enggenie:architect-plan to create an implementation plan?
```

**Example 2: Estimate an existing story**

What you say:
> "Estimate the search feature story - it involves adding full-text search to our product catalog"

What happens:
1. The skill breaks the work into areas (backend API, search indexing, frontend UI, testing)
2. Estimates each area in hours
3. Applies the buffer and rounds to Fibonacci
4. Shows all math transparently

What you see:
```
Estimate breakdown:
  Backend API + search indexing: 4h
  Frontend search UI: 3h
  Integration testing: 2h
  Raw total: 9h
  With 1.2x buffer: 10.8h
  Fibonacci anchor: 8 story points
```

**Tips:**
- The more context you give up front, the fewer clarifying questions the skill needs to ask
- You can say "skip questions, just generate the spec" if you want a first draft fast
- Specs are saved as markdown files you can edit by hand afterward

---

## Architect Role

### enggenie:architect-design - Brainstorm and Make Technical Decisions

**Example 1: Brainstorm a technical approach**

What you say:
> "Let's brainstorm how to implement caching for our API responses"

What happens:
1. The skill enters Brainstorm mode
2. Explores your codebase to understand current patterns
3. Asks: "What are your main performance concerns - latency, throughput, or both?"
4. Proposes 2-3 approaches with concrete tradeoffs:
   - Option A: Redis cache with TTL (fast, requires Redis infrastructure)
   - Option B: In-memory cache with LRU eviction (simple, per-instance only)
   - Option C: CDN-level caching (zero code change, limited to GET requests)
5. Recommends one based on your constraints
6. Saves the decision

What you see:
```
Brainstorm complete. 3 options evaluated.
Recommendation: Option A (Redis with TTL)
  - Best fit for your multi-instance deployment
  - Aligns with existing Redis usage in your auth module
Decision saved to docs/decisions/api-caching-approach.md
```

**Example 2: Make an architecture decision (ADR)**

What you say:
> "We need to decide between REST and GraphQL for our new API"

What happens:
1. The skill enters Architecture mode
2. Presents both sides with concrete tradeoffs specific to YOUR codebase
3. Documents the decision as an ADR:
   - Context: Why this decision matters
   - Decision: What we chose
   - Consequences: What changes
4. Saves to docs/adrs/

What you see:
```
ADR-007: Use REST for the new API
Context: Team has 3 years REST experience, 0 GraphQL. Client needs are simple CRUD.
Decision: REST with OpenAPI spec
Consequences: Simpler onboarding, no GraphQL learning curve, may revisit if query flexibility becomes a bottleneck.
Saved to docs/adrs/007-rest-over-graphql.md
```

**Tips:**
- Brainstorm mode is open-ended. Architecture mode drives toward a recorded decision.
- You can reference previous ADRs: "Review ADR-003 before deciding"
- The skill always ties recommendations back to your specific codebase, not generic advice

### enggenie:architect-plan - Create Implementation Plans

**Example: Plan a multi-service feature**

What you say:
> "Create an implementation plan for the notification system spec"

What happens:
1. Reads the spec from pm-refine
2. Explores your codebase for existing patterns
3. Generates a phased plan:
   - Phase 1 (Backend): notification service, email templates, queue setup
   - Phase 2 (Frontend): preferences UI, notification center
   - Each phase is independently deployable
   - Every task has exact file paths and test commands
4. Reviews the plan for completeness (no placeholder text allowed)

What you see:
```
Implementation plan generated: 2 phases, 7 tasks
  Phase 1 - Backend (3 tasks):
    1.1 Create NotificationService in src/services/notification.ts
    1.2 Add email templates in src/templates/email/
    1.3 Configure message queue in src/config/queue.ts
  Phase 2 - Frontend (4 tasks):
    2.1 Add preferences page at src/pages/settings/notifications.tsx
    2.2 Create NotificationCenter component
    2.3 Wire up WebSocket for real-time updates
    2.4 Integration tests
Plan saved to docs/plans/notification-system.md
Next: invoke enggenie:dev-implement to execute this plan?
```

**Tips:**
- Plans reference exact file paths in your project, not generic examples
- Each phase can be deployed and tested independently
- The skill rejects plans with vague steps like "implement the feature" - every task must be concrete

---

## Dev Role

### enggenie:dev-tdd - Test-Driven Development

**Example: Add a new function with TDD**

What you say:
> "Add a function that validates phone numbers"

What happens:
1. RED - Writes a failing test first:
   ```python
   def test_rejects_invalid_phone():
       assert validate_phone("abc") == False
   ```
2. Runs the test - confirms it FAILS (function doesn't exist yet)
3. GREEN - Writes the simplest code to pass:
   ```python
   def validate_phone(phone):
       return phone.isdigit() and 7 <= len(phone) <= 15
   ```
4. Runs the test - confirms it PASSES
5. REFACTOR - Cleans up if needed
6. Repeats for more test cases (empty string, country codes, special characters)

What you see:
```
RED: test_rejects_invalid_phone FAILED (expected - function does not exist)
GREEN: test_rejects_invalid_phone PASSED
RED: test_accepts_valid_international FAILED
GREEN: test_accepts_valid_international PASSED
REFACTOR: extracted regex pattern to constant PHONE_PATTERN
All 4 tests passing. Function ready.
```

**Tips:**
- The skill enforces writing the test BEFORE the code. If you already wrote code, it will ask you to delete it and start with a test.
- Say "add edge case tests" to make the skill think about unusual inputs
- Works with any test framework your project already uses (pytest, jest, xunit, etc.)

### enggenie:dev-implement - Execute Plans with Subagents

**Example: Execute a multi-task plan**

What you say:
> "Execute the notification system plan"

What happens:
1. Sets up a git worktree for isolated development
2. Runs existing tests to confirm a clean baseline
3. For each task in the plan:
   - Dispatches a coding subagent to implement with TDD
   - Dispatches a spec reviewer to verify correctness
   - Dispatches a quality reviewer to check code quality
4. Between phases, asks for your confirmation before proceeding
5. After all tasks, runs the full test suite

What you see:
```
Worktree created: .worktrees/feat-notifications
Baseline: 142/142 tests passing

Phase 1 - Backend:
  Task 1.1 [coding agent]: NotificationService created, 3 tests added
  Task 1.1 [spec review]: matches spec requirements
  Task 1.1 [quality review]: clean, no issues
  Task 1.2 [coding agent]: 2 email templates created
  Task 1.3 [coding agent]: queue config added, 2 tests added
Phase 1 complete: 147/147 tests passing

Proceed to Phase 2? (y/n)
```

**Tips:**
- You can pause between phases to review the code yourself
- If a subagent finds a problem, it stops and asks you rather than guessing
- The worktree keeps your main branch clean until you are ready to merge

### enggenie:dev-debug - Systematic Debugging

**Example: Fix a failing test**

What you say:
> "This test is failing: test_user_login returns 401 instead of 200"

What happens:
1. Phase 1 (Investigate): Reads the full error, reproduces it, checks recent changes
2. Phase 2 (Find Pattern): Compares working login tests with the failing one
3. Phase 3 (Test Hypothesis): "I think the auth token is expired because the test setup doesn't refresh it"
4. Phase 4 (Fix): Writes a regression test, fixes the root cause, verifies all tests pass

What you see:
```
INVESTIGATE: Reproduced failure. test_user_login returns 401.
  Last passing commit: abc1234 (2 days ago)
  Changed files since: auth_middleware.py, token_service.py

FIND PATTERN: test_admin_login passes, test_user_login fails.
  Difference: admin test refreshes token in setUp(), user test does not.

HYPOTHESIS: Token expiry. The user test reuses a stale token from a previous test run.

FIX:
  Added regression test: test_user_login_with_expired_token
  Fixed: Added token refresh to test_user_login setUp()
  Result: 48/48 tests passing
```

**Tips:**
- The skill never guesses. It gathers evidence first. If it cannot find the cause after 3 attempts, it escalates as an architecture problem.
- Paste the full error message for best results
- You can say "don't fix it yet, just diagnose" if you want to understand before changing code

---

## Reviewer Role

### enggenie:review-code - Code Review

**Example 1: Request a review before PR**

What you say:
> "Review my changes before I create a PR"

What happens:
1. Gets the diff of your changes
2. Dispatches a code reviewer that checks: correctness, tests, security, performance
3. Reports findings by severity:
   - Critical: SQL injection in user input handling - FIX NOW
   - Important: Missing error handling on API call - fix before PR
   - Minor: Variable naming inconsistency - note for later

What you see:
```
Code review complete. 5 findings:

CRITICAL (1):
  src/api/users.ts:42 - User input passed directly to SQL query.
  Fix: Use parameterized query. Example provided below.

IMPORTANT (2):
  src/services/email.ts:18 - No error handling on sendEmail(). If SMTP fails, the request hangs.
  src/api/users.ts:55 - Missing rate limiting on login endpoint.

MINOR (2):
  src/utils/format.ts:7 - Variable 'x' should be 'formattedDate'.
  src/api/users.ts:30 - Unused import 'lodash'.
```

**Example 2: Process PR feedback**

What you say:
> "I got review feedback on my PR, help me address it"

What happens:
1. Reads ALL feedback comments first (does not react immediately)
2. Evaluates each technically - agrees only when correct
3. Pushes back when feedback is wrong (with evidence)
4. Implements fixes in order: blocking first, then simple, then complex

What you see:
```
PR #42 has 6 comments. Analysis:

Comment 1 (reviewer: alice): "This function is too long" - AGREE. Will extract helper.
Comment 2 (reviewer: bob): "Use Map instead of Object" - DISAGREE. Object is correct here
  because keys are static strings. Will reply with explanation.
Comment 3 (reviewer: alice): "Missing null check" - AGREE. Critical fix.

Addressing in order: #3 (critical), #1 (simple refactor), then replying to #2.
```

**Tips:**
- The skill does not rubber-stamp everything. It pushes back on incorrect feedback with evidence.
- Run this before every PR to catch issues early
- You can say "focus on security only" to narrow the review scope

### enggenie:review-design - Frontend Design Quality

**Example: Review a UI component**

What you say:
> "Check the dashboard component against our design system"

What happens:
1. Checks design system token usage (no hardcoded colors/spacing)
2. Verifies all 7 states: loading, empty, error, hover, focus, disabled, active
3. Tests responsive behavior at mobile/tablet/desktop breakpoints
4. Runs accessibility audit: ARIA labels, keyboard nav, color contrast
5. Reports issues with severity (Critical/Important/Minor)

What you see:
```
Design review for DashboardComponent:

CRITICAL (1):
  Missing loading state. Users see a blank screen for 2-3 seconds on slow connections.

IMPORTANT (3):
  Hardcoded color #333 at line 45 - should use var(--text-primary)
  No keyboard navigation for the filter dropdown
  Empty state shows raw "[]" instead of a friendly message

MINOR (2):
  Spacing between cards is 16px, design system specifies 20px (--spacing-md)
  Hover state on cards missing on touch devices

Accessibility: 4/7 checks pass. Failing: keyboard nav, color contrast on badges, missing ARIA labels on chart.
Responsive: Desktop OK, Tablet OK, Mobile FAIL (cards overflow on 320px width).
```

**Tips:**
- Works best when your project has a design system or token file it can reference
- Say "check accessibility only" or "check responsive only" to narrow the review
- The skill checks real component code, not screenshots

---

## QA Role

### enggenie:qa-verify - Evidence Before Claims

**Example: Verify work is complete**

What you say:
> "Are the tests passing?"

What happens:
1. Runs the FULL test command (not a partial run)
2. Reads the COMPLETE output
3. Reports with evidence: "47/47 tests pass, exit code 0"
4. NEVER says "should pass" or "probably works"

What you see:
```
Running: npm test
...
47/47 tests passed
Exit code: 0
Coverage: 89% (lines), 82% (branches)

Verdict: ALL TESTS PASSING. Evidence verified.
```

**Tips:**
- This skill fires automatically whenever the AI is about to claim work is done. It prevents "it should work" without proof.
- If tests fail, it shows the exact failures, not a summary
- You can say "run tests with coverage" to get coverage numbers too

### enggenie:qa-test - QA Testing (Playwright + Manual)

**Example 1: Automated testing**

What you say:
> "Test the login flow as a QA engineer"

What happens:
1. Writes Playwright tests from a user's perspective:
   - Navigate to login page
   - Enter credentials
   - Submit form
   - Verify redirect to dashboard
2. Tests edge cases a developer might miss:
   - Empty form submission
   - Wrong password
   - Double-click on submit button
   - Back button after login

What you see:
```
Playwright test suite created: tests/e2e/login.spec.ts

Test results:
  PASS: Login with valid credentials redirects to dashboard
  PASS: Empty email shows validation error
  PASS: Wrong password shows "Invalid credentials" message
  PASS: Double-click submit only sends one request
  FAIL: Back button after login returns to login page (should redirect to dashboard)

4/5 tests passing. 1 bug found.
Bug: After successful login, pressing browser back button shows the login form again instead of redirecting to dashboard.
```

**Example 2: Manual browser testing**

What you say:
> "Manually QA the search feature on all screen sizes"

What happens:
1. Opens the page in a browser
2. Takes screenshots at each step
3. Tests at mobile (320px), tablet (768px), and desktop (1024px)
4. Reports results in a test matrix with PASS/FAIL verdicts

What you see:
```
Manual QA Report: Search Feature

| Test Case                  | Mobile (320px) | Tablet (768px) | Desktop (1024px) |
|----------------------------|----------------|----------------|-------------------|
| Search input visible       | PASS           | PASS           | PASS              |
| Type and see suggestions   | FAIL           | PASS           | PASS              |
| Select a suggestion        | PASS           | PASS           | PASS              |
| Clear search               | PASS           | PASS           | PASS              |
| No results message         | PASS           | PASS           | PASS              |

Bug: On mobile (320px), search suggestions dropdown is cut off by the viewport edge.
Screenshots saved to qa-screenshots/search-feature/
```

**Tips:**
- Automated tests are saved to your project so they run in CI going forward
- Manual testing requires a running dev server
- You can specify exact screen sizes: "test at 375px and 1440px"

---

## Deploy Role

### enggenie:deploy-ship - Commit, PR, Ship

**Example 1: Commit your work**

What you say:
> "Commit these changes"

What happens:
1. Analyzes your staged changes
2. Proposes a commit message:
   > feat: add email notification service with queue processing
3. Waits for your approval (never auto-commits)
4. You can edit the message or approve as-is

What you see:
```
Proposed commit message:
  feat: add email notification service with queue processing

Staged files:
  src/services/notification.ts (new)
  src/config/queue.ts (modified)
  tests/services/notification.test.ts (new)

Approve this commit? (y/edit/n)
```

**Example 2: Create a PR**

What you say:
> "Create a PR for this work"

What happens:
1. Pushes your branch
2. Creates a PR with:
   - Summary from the spec/plan
   - Test plan from QA results
   - Links to spec and Jira ticket (if available)
3. Shows you the PR URL

What you see:
```
Branch pushed: feat/notification-system
PR created: #42 "feat: add email notification system"

PR includes:
  Summary: 3 bullet points from the spec
  Test plan: 5 test cases from QA
  Linked: JIRA-1234

URL: https://github.com/your-org/your-repo/pull/42
```

**Example 3: Full ship workflow**

What you say:
> "Ship it"

What happens:
1. Runs all tests one final time
2. Creates a clean commit
3. Pushes and opens a PR
4. Adds reviewers if configured

**Tips:**
- The skill never auto-commits or auto-pushes. It always asks first.
- Commit messages follow conventional commits format (feat:, fix:, docs:, etc.)
- If tests fail during the ship workflow, it stops and tells you what broke

---

## Memory Role

### enggenie:memory-recall - Cross-Session Context

**Example 1: Recall past work**

What you say:
> "What did we work on in the auth module last week?"

What happens:
1. Searches memory efficiently (index first, then details)
2. Returns: "Last Tuesday you refactored the auth middleware to use JWT refresh tokens. The ADR is in docs/adrs/jwt-refresh.md."
3. Uses ~2k tokens instead of ~20k (10x savings)

What you see:
```
Found 2 relevant memories:

1. [March 25] Refactored auth middleware to use JWT refresh tokens.
   ADR: docs/adrs/jwt-refresh.md
   Changed files: src/middleware/auth.ts, src/services/token.ts

2. [March 27] Fixed token expiry bug in auth flow.
   Related test: tests/auth/token-refresh.test.ts
```

**Example 2: Resume a previous session**

What you say:
> "Let's continue where we left off"

What happens:
1. Searches memory for the most recent work session
2. Loads the relevant context (what was being built, what was done, what is left)
3. Summarizes the current state so you can pick up immediately

What you see:
```
Last session (March 28):
  Working on: Notification system - Phase 2 (Frontend)
  Completed: Tasks 2.1 and 2.2 (preferences page, notification center)
  Remaining: Task 2.3 (WebSocket integration), Task 2.4 (integration tests)
  Branch: feat/notification-system
  Tests: 155/155 passing

Ready to continue with Task 2.3?
```

**Tips:**
- Requires the claude-mem plugin. If not installed, other skills simply skip memory lookups silently.
- Memory recall is automatic - you do not need to explicitly ask for it. Skills check memory before starting work.
- The more you use enggenie, the richer the memory context becomes across sessions.

---

## Quick Reference

| What you want to do | What to say | Skill that fires |
|---------------------|-------------|-----------------|
| Write a feature spec | "I want to build X" | pm-refine |
| Brainstorm approaches | "What's the best way to do X?" | architect-design |
| Create an implementation plan | "Plan how to build X" | architect-plan |
| Build a feature with TDD | "Execute the plan" | dev-implement |
| Add a function | "Add a function that does X" | dev-tdd |
| Fix a bug | "This test is failing" | dev-debug |
| Review code | "Review my changes" | review-code |
| Check UI quality | "Check the dashboard design" | review-design |
| Verify work is done | "Are tests passing?" | qa-verify |
| QA test a feature | "Test the login flow" | qa-test |
| Commit and ship | "Create a PR" | deploy-ship |
| Recall past work | "What did we do last time?" | memory-recall |

---

## Common Workflows

These skills work best when chained together. Here are the most common end-to-end workflows:

### New Feature (Full Lifecycle)
1. **pm-refine** - "I want to build a notification system" (generates spec)
2. **architect-design** - "Brainstorm the technical approach" (picks architecture)
3. **architect-plan** - "Create an implementation plan" (breaks into tasks)
4. **dev-implement** - "Execute the plan" (builds it with TDD)
5. **review-code** - "Review my changes" (catches issues)
6. **qa-test** - "Test the notification flow" (QA from user perspective)
7. **deploy-ship** - "Create a PR" (ships it)

### Bug Fix (Fast Track)
1. **dev-debug** - "This test is failing: ..." (diagnoses and fixes)
2. **qa-verify** - "Are tests passing?" (confirms the fix)
3. **deploy-ship** - "Commit and create a PR" (ships the fix)

### Code Review Response
1. **review-code** - "I got review feedback on PR #42" (analyzes feedback)
2. **qa-verify** - "Are tests still passing?" (confirms nothing broke)
3. **deploy-ship** - "Push the fixes" (updates the PR)
