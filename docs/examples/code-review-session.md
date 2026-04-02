# Code Review Session Walkthrough

Two scenarios using enggenie:review-code.
Stack: TypeScript/Node.js backend, React frontend.

---

## Scenario A: Requesting Review

After implementing a search filter feature, the user wants a code review before creating a PR.

**User:** Review the changes on this branch before I open a PR.

> I'm using enggenie:review-code to request a review.

### Get the diff scope

```
$ BASE_SHA=$(git merge-base HEAD main)
$ HEAD_SHA=$(git rev-parse HEAD)
$ git diff --stat $BASE_SHA $HEAD_SHA

 src/api/routes/search.ts              | 42 +++++++++
 src/api/routes/search.test.ts         | 67 ++++++++++++++
 src/services/search/filter-builder.ts | 85 ++++++++++++++++++
 src/services/search/filter-builder.test.ts | 91 +++++++++++++++++++
 src/services/search/index.ts          |  3 +
 src/types/search.ts                   | 18 ++++
 6 files changed, 306 insertions(+)
```

### Dispatch Code Reviewer subagent (sonnet)

The subagent receives the full diff, the task spec, and the review checklist. It returns:

**Review Results:**

**1. BLOCKING -- SQL injection in filter-builder.ts:34**

```typescript
// Current code
const query = `SELECT * FROM products WHERE category = '${filter.category}'`;
```

User input is interpolated directly into SQL. This is a SQL injection vulnerability. Use parameterized queries.

**2. IMPORTANT -- Missing validation on search route**

`src/api/routes/search.ts` accepts `req.query.filters` and passes it to `filterBuilder` without validation. If `filters` is not an array, `filterBuilder.map()` will throw. Add input validation with a schema (the codebase uses Zod -- see `src/api/validators/`).

**3. MINOR -- Inconsistent naming**

`filter-builder.ts` exports `buildFilter()` but the test file calls it `createFilter()`. Both compile because the test imports from a relative path that re-exports with an alias. Clean up the alias or rename for consistency.

**4. OBSERVATION -- filterBuilder could be generic**

The filter builder is specific to products. It could be generalized to work with any entity.

### Act on feedback

**Assistant:** Review returned 4 items. Acting on them in order.

**Blocking -- SQL injection.** Fixed. Switched to parameterized query:

```typescript
const query = 'SELECT * FROM products WHERE category = $1';
const result = await db.query(query, [filter.category]);
```

Added a test that passes `'; DROP TABLE products; --` as the category and verifies the query is parameterized.

**Important -- Missing validation.** Fixed. Added Zod schema matching the pattern in `src/api/validators/order.validator.ts`:

```typescript
const searchFiltersSchema = z.object({
  filters: z.array(filterSchema).min(1).max(20),
});
```

Added test for invalid input returning 400.

**Minor -- Inconsistent naming.** Fixed. Removed the alias in `index.ts`, both files now use `buildFilter`.

**Observation -- Make filterBuilder generic.** Not acting on this.

```
$ grep -r "buildFilter" --include="*.ts" src/
src/services/search/filter-builder.ts:export function buildFilter
src/services/search/filter-builder.test.ts:  buildFilter(
src/api/routes/search.ts:  buildFilter(
```

One caller. One entity type. Making this generic adds indirection without value. If a second entity needs filtering later, generalize then. (YAGNI)

```
$ npm test
Tests: 152 passed, 0 failed
```

All fixes verified. Ready for PR.

---

## Scenario B: Receiving Human Review Feedback

A teammate left 3 comments on PR #87 (the welcome email feature from the full-feature-walkthrough).

> I'm using enggenie:review-code to process review feedback.

### Step 1 -- Read everything first

```
$ gh api repos/acme/webapp/pulls/87/comments --jq '.[].body'
```

**Comment 1** (on `welcome-email.ts:12`):
> "Should we extract the email template into a separate file? Mixing template HTML with service logic feels wrong."

**Comment 2** (on `welcome-email-queue.ts:28`):
> "The retry delay calculation is unclear. Can you add a comment explaining the backoff formula?"

**Comment 3** (on `auth.controller.ts:65`):
> "This will break if the queue connection is down. We need a try/catch around the queue.add() call."

All three read. Now evaluate each one.

### Step 2 -- Evaluate

**Comment 1 -- Extract email template.**

Check the codebase:

```
$ find src/templates -name "*.ts" 2>/dev/null | head -5
(no results)

$ find src -name "*template*" | head -5
(no results)
```

No template directory or pattern exists in this codebase. There is one email template (this one). Extracting it into a new directory structure for a single template adds a directory, a loader utility, and a convention that nothing else follows.

This is a YAGNI situation. Push back.

**Comment 2 -- Add comment for backoff formula.**

The code:
```typescript
const delay = Math.pow(2, attemptNumber) * 1000; // 2s, 4s, 8s
```

The reviewer is right. The formula is `2^n * 1000ms` but that is not obvious at a glance, especially the relationship between attempt number and actual delay. A one-line comment costs nothing and helps the next reader. Fix it.

**Comment 3 -- Try/catch around queue.add().**

Check the current behavior:

```typescript
// auth.controller.ts:63-66
const user = await userService.create(userData);
await queue.add('welcome-email', { userId: user.id });
return res.status(201).json({ user });
```

If the queue connection is down, `queue.add()` throws and the entire signup fails with a 500. The user's account IS created (line 63 succeeded) but they get an error response and might try to sign up again, hitting a duplicate email error. The reviewer is correct. The email queue should not block signup.

Fix it.

### Step 3 -- Respond and implement

**Comment 1 response:**

```
$ gh api repos/acme/webapp/pulls/87/comments/401/replies \
  -f body="One template, one caller. No template directory exists in the codebase. Extracting now adds structure for a single file. If we add more email templates, I will extract them all at that point."
```

**Comment 2 fix:**

```typescript
// Exponential backoff: attempt 1 = 2s, attempt 2 = 4s, attempt 3 = 8s
const delay = Math.pow(2, attemptNumber) * 1000;
```

```
$ gh api repos/acme/webapp/pulls/87/comments/402/replies \
  -f body="Fixed. Added comment explaining the backoff progression."
```

**Comment 3 fix:**

```typescript
const user = await userService.create(userData);
try {
  await queue.add('welcome-email', { userId: user.id });
} catch (err) {
  logger.error('Failed to enqueue welcome email', { userId: user.id, error: err.message });
}
return res.status(201).json({ user });
```

Added a test that mocks `queue.add` throwing and verifies the signup still returns 201.

```
$ gh api repos/acme/webapp/pulls/87/comments/403/replies \
  -f body="Fixed. queue.add() failure is now caught and logged. Signup completes regardless. Added test."
```

### Step 4 -- Verify

```
$ npm test
Tests: 158 passed, 0 failed
```

All fixes tested. No regressions.

```
$ git commit -m "fix: handle queue failure during signup, clarify backoff comment"
$ git push
```

---

## What Good Review Looks Like

Notice what did NOT happen in either scenario:

- No "You're absolutely right!" -- just "Fixed." or "Not acting on this."
- No "Great catch!" -- the SQL injection was a real bug. It was fixed. The commit speaks for itself.
- No agreement without verification -- Comment 1 was checked against the codebase before responding. The push-back was specific: one template, one caller, no existing pattern.
- No implementing everything blindly -- Comment 1 was evaluated and declined with reasoning. Comments 2 and 3 were evaluated and accepted with code changes.

The YAGNI check on the filter builder (Scenario A) and the email template extraction (Scenario B) both followed the same pattern: grep for callers, count them, decide based on what exists today.
