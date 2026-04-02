# Full Feature Walkthrough: Idea to Ship

End-to-end session adding email notifications when users sign up.
Stack: Node.js/Express backend, React frontend, PostgreSQL, SendGrid for email.

---

## 1. The Request

**User:** I want to add email notifications when users sign up. Welcome email with their name and a link to complete their profile.

---

## 2. enggenie:pm-refine -- Specification

> I'm using enggenie:pm-refine to generate a feature specification.

**Assistant:** Before I write the spec, a few questions.

1. Which email provider are you using? SendGrid, SES, Postmark, or something else?

**User:** SendGrid. We already have an API key in our env vars as `SENDGRID_API_KEY`.

**Assistant:** Got it. Second question:

2. Should the email send synchronously during signup, or should it be queued? Synchronous means the user waits for the email to send before seeing the success page. Queued means signup completes immediately and the email sends in the background.

**User:** Queued. We have a Bull queue already set up for background jobs.

**Assistant:** Last question:

3. What happens if the email fails to send? Retry? Log and move on? Alert someone?

**User:** Retry 3 times with exponential backoff. If all retries fail, log the error and move on. Do not block the user's account creation.

**Assistant:** Clear. Let me validate the workspace.

```
$ git status
On branch main
nothing to commit, working tree clean

$ git branch -a | grep welcome-email
(no results)
```

Workspace is clean. Branch name `feature/welcome-email` is available.

The assistant dispatches three subagents:
- **Refinement subagent** (sonnet) -- explores the codebase, finds `src/queues/`, `src/services/email/`, existing Bull queue patterns
- **QA Planner subagent** (sonnet) -- generates 10 test scenarios from the acceptance criteria
- **Spec Reviewer subagent** (sonnet) -- validates the spec has no TBD sections

After all three return, the assistant presents the spec:

**Assistant:** Spec is ready. Key sections:

**Acceptance Criteria:**
- User receives a welcome email within 60 seconds of signup
- Email contains the user's first name and a profile completion link pointing to `/profile/setup?token=<jwt>`
- If SendGrid returns a non-2xx response, the job retries 3 times with exponential backoff (2s, 4s, 8s)
- If all retries fail, the error is logged to `application.log` with the user ID and SendGrid error code
- User account is fully active regardless of email delivery status

**QA Test Plan:** 10 scenarios covering happy path, SendGrid down, invalid email format, special characters in name, duplicate signup, and more.

**Estimation:**
```
Backend (queue + service):  3h raw -> +20% -> 3.6h -> 5 points
Email template:             1h raw -> +20% -> 1.2h -> 2 points
Testing:                    2h raw -> +20% -> 2.4h -> 3 points
Total: 10 points -> exceeds 8 cap -> split into 2 stories
```

Spec saved to `specs/welcome-email-spec.md`.

**User:** Approved. Let's plan the implementation.

**Assistant:**
> Spec approved. Next: invoke enggenie:architect-plan to create the implementation plan.

---

## 3. enggenie:architect-plan -- Planning

> I'm using enggenie:architect-plan to create an implementation plan.

The assistant reads `specs/welcome-email-spec.md`, then dispatches:
- **Explorer subagent** (sonnet) -- finds existing patterns in `src/queues/invoice-queue.ts`, `src/services/email/transactional.ts`
- **Doc Discovery subagent** (haiku) -- reads SendGrid v3 API docs, extracts `sgMail.send()` signature and error codes

**Assistant:** Plan ready. Two phases:

```
## Phase 1 -- Backend (Email Service + Queue)
Branch: feature/welcome-email

### Task 1.1: Welcome email service
Files: create src/services/email/welcome-email.ts
       create src/services/email/welcome-email.test.ts

- [ ] Write failing test: sendWelcomeEmail() returns SendGrid message ID
- [ ] Run: npm test -- --grep "welcome-email" -> FAIL (module not found)
- [ ] Implement sendWelcomeEmail(user: User): Promise<string>
- [ ] Run: npm test -- --grep "welcome-email" -> PASS
- [ ] Commit: "feat: add welcome email service"

### Task 1.2: Queue job processor
Files: create src/queues/welcome-email-queue.ts
       create src/queues/welcome-email-queue.test.ts
       modify src/queues/index.ts

- [ ] Write failing test: job processor calls sendWelcomeEmail with user data
- [ ] Run test -> FAIL
- [ ] Implement WelcomeEmailProcessor with 3 retries, exponential backoff
- [ ] Run test -> PASS
- [ ] Commit: "feat: add welcome email queue processor"

### Task 1.3: Hook into signup flow
Files: modify src/controllers/auth.controller.ts
       modify src/controllers/auth.controller.test.ts

- [ ] Write failing test: POST /auth/signup enqueues a welcome-email job
- [ ] Run test -> FAIL
- [ ] Add queue.add('welcome-email', { userId }) after user creation
- [ ] Run test -> PASS
- [ ] Commit: "feat: enqueue welcome email on signup"

### Deployment Readiness -- Phase 1
- [ ] All tests pass: npm test -> 0 failures
- [ ] Existing signup flow still works (no breaking changes)
- [ ] Queue processes jobs when SENDGRID_API_KEY is set
- [ ] User verifies: sign up a test user, check Bull dashboard for queued job

## Phase 2 -- Email Template + Error Handling
Depends on: Phase 1 complete
Branch: same branch

### Task 2.1: HTML email template
### Task 2.2: Retry failure logging
### Deployment Readiness -- Phase 2
```

Plan saved to `plans/welcome-email-implementation-plan.md`.

**User:** Looks good. Execute it.

---

## 4. enggenie:dev-implement -- Coding

> I'm using enggenie:dev-implement to execute this plan.

### Phase 0: Worktree Setup

```
$ ls -d .worktrees 2>/dev/null || echo "not found"
not found

$ grep -q "worktrees" .gitignore && echo "found" || echo "not found"
not found
```

**Assistant:** No worktree directory exists. Which name do you prefer: `.worktrees/` or `worktrees/`?

**User:** `.worktrees/`

```
$ mkdir .worktrees
$ echo ".worktrees/" >> .gitignore
$ git add .gitignore && git commit -m "chore: add worktree directory to .gitignore"
$ git worktree add .worktrees/welcome-email -b feature/welcome-email
Preparing worktree (new branch 'feature/welcome-email')

$ cd .worktrees/welcome-email && npm install
added 847 packages in 12s

$ npm test
Tests: 142 passed, 0 failed
```

Baseline is green. Starting Task 1.1.

### Task 1.1: Welcome email service

**Assistant dispatches implementer subagent (sonnet).**

The subagent writes the failing test first:

```typescript
// src/services/email/welcome-email.test.ts
import { sendWelcomeEmail } from './welcome-email';
import sgMail from '@sendgrid/mail';

jest.mock('@sendgrid/mail');

describe('sendWelcomeEmail', () => {
  it('sends email with user name and profile link', async () => {
    (sgMail.send as jest.Mock).mockResolvedValue([{ statusCode: 202, headers: {}, body: '' }]);

    const result = await sendWelcomeEmail({
      id: 'user-123',
      email: 'jane@example.com',
      firstName: 'Jane',
    });

    expect(sgMail.send).toHaveBeenCalledWith(
      expect.objectContaining({
        to: 'jane@example.com',
        subject: 'Welcome to the platform, Jane',
      })
    );
    expect(result.success).toBe(true);
  });
});
```

```
$ npm test -- --grep "welcome-email"
FAIL  src/services/email/welcome-email.test.ts
  Cannot find module './welcome-email'
```

RED. Now the implementation:

```typescript
// src/services/email/welcome-email.ts
import sgMail from '@sendgrid/mail';
import { generateProfileToken } from '../auth/tokens';

interface WelcomeEmailUser {
  id: string;
  email: string;
  firstName: string;
}

export async function sendWelcomeEmail(user: WelcomeEmailUser) {
  const token = generateProfileToken(user.id);
  const profileLink = `${process.env.APP_URL}/profile/setup?token=${token}`;

  await sgMail.send({
    to: user.email,
    from: process.env.SENDGRID_FROM_EMAIL!,
    subject: `Welcome to the platform, ${user.firstName}`,
    html: `<p>Hi ${user.firstName},</p><p>Complete your profile: <a href="${profileLink}">here</a>.</p>`,
  });

  return { success: true };
}
```

```
$ npm test -- --grep "welcome-email"
PASS  src/services/email/welcome-email.test.ts
  1 test passed
```

GREEN. Commit: `feat: add welcome email service`

**Spec Reviewer subagent** checks the diff against the spec. Finding: "Missing edge case -- what if firstName contains HTML characters?" The implementer adds a sanitization step and a test for `<script>` in the name. Re-review passes.

**Quality Reviewer subagent** checks code quality. Clean pass.

Tasks 1.2 and 1.3 follow the same RED-GREEN-REFACTOR cycle.

### Phase Boundary

```
$ npm test
Tests: 149 passed, 0 failed (7 new tests added)
```

**Assistant:**
> Phase 1 is complete. All automated checks pass. Please verify manually before I proceed to Phase 2.

**User:** Signed up a test user. Bull dashboard shows the job processed. Email arrived in my inbox. Proceed.

Phase 2 executes the same way. After all tasks complete:

---

## 5. enggenie:qa-verify -- Verification

> I'm using enggenie:qa-verify to verify before claiming completion.

```
$ npm test
Tests: 156 passed, 0 failed, exit 0

$ npm run build
Build completed successfully, exit 0

$ npm run lint
0 errors, 0 warnings
```

**Assistant:** All 156 tests pass. Build succeeds. Lint is clean. Checking acceptance criteria against the spec:

- Welcome email received within 60 seconds: VERIFIED (manual test)
- Email contains first name and profile link: VERIFIED (email content checked)
- Retry on failure: VERIFIED (unit test mocks SendGrid 502, confirms 3 retries)
- Failure logging: VERIFIED (unit test confirms error log with user ID)
- Account active regardless of email: VERIFIED (integration test confirms user can log in even when SendGrid mock fails)

5/5 acceptance criteria verified.

---

## 6. enggenie:deploy-ship -- Shipping

> I'm using enggenie:deploy-ship to create PR.

```
$ git diff --staged
(shows all changes across 6 files)
```

**Assistant:** Proposed commit for final changes:

```
feat: add welcome email notification on user signup

Users receive a welcome email via SendGrid after signup.
Email is queued via Bull with 3 retries and exponential backoff.
Account creation is not blocked by email delivery failures.
```

Proceed? [y/edit/n]

**User:** y

```
$ git push -u origin feature/welcome-email
$ gh pr create --title "Add welcome email on signup" --body "..."
https://github.com/acme/webapp/pull/87
```

**Assistant:**

PR created: https://github.com/acme/webapp/pull/87

Summary:
- Welcome email service using SendGrid v3 API
- Bull queue processor with exponential backoff retry (3 attempts)
- 14 new tests, all passing

Branch is ready. Choose a completion path:
1. Merge locally to main
2. Push and create PR (already done)
3. Keep branch as-is
4. Discard work

**User:** 2 -- already done. We will merge after review.

**Assistant:** Branch and worktree preserved until PR merges. Jira MCP not available -- update PROJ-456 status to "In Review" manually. PR link: https://github.com/acme/webapp/pull/87

---

## Timeline

| Step | Skill | What Happened |
|------|-------|---------------|
| Request | -- | User described the feature |
| Spec | pm-refine | 3 clarifying questions, spec with 5 AC, 10 QA scenarios, estimation |
| Plan | architect-plan | 2-phase plan, 5 tasks, file map, deployment gates |
| Code | dev-implement | Worktree setup, TDD per task, spec + quality review gates |
| Verify | qa-verify | 156 tests pass, build clean, 5/5 AC verified |
| Ship | deploy-ship | Conventional commit, PR created, Jira note |
