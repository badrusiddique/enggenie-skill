# I Got Tired of My AI Coding Assistant Only Knowing How to Code

*An Engineering Manager's journey from plugin sprawl to a unified skill suite that covers the entire SDLC.*

---

Last month's sprint retro was rough.

Our PM was frustrated because a "small feature" ballooned into a three-sprint saga -- the original request was two sentences, the spec was nonexistent, and the edge cases kept surfacing mid-implementation. Our SSE was annoyed because a junior dev pushed code with zero tests ("I tested it manually"). QA was tired of hearing "it works on my machine." And our lead had spent two hours debugging a test failure by randomly changing things until something stuck.

I sat there thinking: we use Claude Code every day. It writes code fast. But it's not helping with any of the stuff that actually slows us down.

🔧

---

## AI Coding Assistants Have a Blind Spot

In my experience managing a squad, **the actual coding is a fraction of what we spend time on.** The rest is planning, designing, testing, reviewing, debugging, deploying. And most AI coding tools are really good at the coding part, and completely absent for the rest.

I watched these pain points repeat sprint after sprint:

**1. Vague requests → no spec → rework.** Someone says "add notifications" and the dev starts coding immediately. No acceptance criteria. No edge cases. Two sprints later, we're still reworking it because nobody asked "what happens when the email fails?"

**2. Inconsistent code reviews.** Some PRs get rubber-stamped. Others get 40 comments about variable naming. The AI "review" catches syntax issues but misses the SQL injection on line 42.

**3. Tests? What tests?** "I'll write tests after" is the most expensive sentence in software engineering. They never write them after.

**4. Debugging by guessing.** "Let me try adding a null check." "Let me try changing this import." Two hours of random changes. The root cause was on a completely different file.

**5. "Done" means "it compiles."** Not "it meets the acceptance criteria." Not "the tests pass." Just... it compiles.

I tried fixing this with individual plugins -- a TDD enforcer, a debugging guide, a spec generator. I ended up with six different skills installed and couldn't remember which one did what. My AI assistant had more identity crises than a college freshman. 🤷

![This is fine](https://media.giphy.com/media/QMHoU66sBXqqLqYvGO/giphy.gif)

---

## What If Your AI Assistant Could Wear Every Hat? 💡

The realization hit me during a 1:1 with our lead: what if instead of separate plugins for each problem, there was **one skill suite** that covered the entire workflow -- from spec to ship?

Every role on the squad gets a matching AI skill:

- **PM** writes the spec with acceptance criteria and estimation
- **Architect** brainstorms approaches and creates phased plans
- **Dev** builds with TDD, debugs systematically, never guesses
- **QA** verifies with evidence, tests from the user's perspective

Architecture, deployment, code review, cross-session memory -- it covers those too.

That's how [enggenie](https://github.com/badrusiddique/enggenie-skill) was born. **14 skills, 7 expert roles, one install command.**

```bash
npx skills add badrusiddique/enggenie-skill
```

No config files. Skills activate automatically based on what you're doing. 🚀

---

## Demo: "Add Notifications" to Full Spec in 90 Seconds 📋

Our PM says:

> "I want to add email notifications when users sign up. Welcome email with their name and a profile completion link."

Two sentences. No acceptance criteria. No edge cases. Normally this turns into three Slack threads and a meeting.

With enggenie installed, here's what Claude Code does:

```
╭─────────────────────────────────────────────────────╮
│ I'm using enggenie:pm-refine to generate a feature  │
│ specification.                                       │
╰─────────────────────────────────────────────────────╯

Before I write the spec, a few questions.

1. Which email provider are you using?
   SendGrid, SES, Postmark, or something else?

> SendGrid. We have an API key in our env vars.

Got it. Second question:

2. Should the email send synchronously during signup,
   or should it be queued?

> Queued. We have Bull already set up.

Last question:

3. What happens if the email fails to send?
   Retry? Log and move on? Alert someone?

> Retry 3 times with exponential backoff.
  If all retries fail, log and move on.
```

Three questions. Then it dispatches subagents -- one explores the codebase for existing patterns, one generates a QA test plan, one reviews the spec for completeness.

The output:

```
Acceptance Criteria:
  ✅ User receives welcome email within 60 seconds of signup
  ✅ Email contains user's first name and profile link
  ✅ If SendGrid fails, retries 3x with exponential backoff (2s, 4s, 8s)
  ✅ Failed retries logged with user ID and error code
  ✅ Account active regardless of email delivery status

QA Test Plan: 10 scenarios
  (happy path, SendGrid down, invalid email, special chars in name,
   duplicate signup, rate limiting, template rendering, ...)

Estimation:
  Backend (queue + service):  5 pts
  Email template:             2 pts
  Testing:                    3 pts
  Total: 10 pts → exceeds 8-point cap → auto-split into 2 stories

Spec saved to specs/welcome-email-spec.md
```

Notice it asked about failure handling. Most devs would skip that. Most AI assistants would skip that too. The PM skill doesn't let you skip it because that's where bugs live.

---

## Demo: No Code Without a Failing Test First 🔴🟢✨

Quick TDD refresher for the non-devs reading this: **write the test first, watch it fail, then write just enough code to make it pass, then clean up.** That's RED-GREEN-REFACTOR. It sounds slow. It's actually faster than debugging untested code in production at 2am.

Here's what happens when you ask Claude Code to add a function:

```
> Add a function that validates email addresses

╭─────────────────────────────────────────────────────╮
│ I'm using enggenie:dev-tdd to enforce test-driven   │
│ development.                                         │
╰─────────────────────────────────────────────────────╯

🔴 RED: Writing failing test first.

  // email-validator.test.ts
  describe('validateEmail', () => {
    it('rejects invalid email without @', () => {
      expect(validateEmail('notanemail')).toBe(false);
    });
  });

  $ npm test -- --grep "validateEmail"
  FAIL ✗ Cannot find module './email-validator'
```

The test fails. Good. That's the point. Now:

```
🟢 GREEN: Writing minimal implementation.

  // email-validator.ts
  export function validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  $ npm test -- --grep "validateEmail"
  PASS ✓ 1 test passed

✨ REFACTOR: Adding edge cases.

  🔴 rejects empty string        → FAIL → implement → PASS
  🔴 rejects email with spaces   → FAIL → implement → PASS
  🔴 rejects double-dot domain    → FAIL → implement → PASS

  All 4 tests passing. Function ready.
```

The hard rule built into this skill: **"If you catch yourself writing production code before a test: stop. Delete it. Write the test first."**

My senior dev told me he actually started following TDD because the AI made him feel guilty for not doing it. I'll take that win.

---

## Demo: "This Test Was Passing Yesterday" -- Solved in 4 Phases 🔍

This one is my favorite. Here's a realistic scenario: a test fails with `TypeError: Cannot read property 'name' of undefined`. Nothing in that file changed. Classic "works on my machine, breaks in CI" situation.

Here's how enggenie:dev-debug handles it:

```
╭─────────────────────────────────────────────────────╮
│ I'm using enggenie:dev-debug for systematic root    │
│ cause investigation.                                 │
╰─────────────────────────────────────────────────────╯

PHASE 1 — INVESTIGATE

  Error: TypeError: Cannot read property 'name' of undefined
    at getProfile (user.controller.ts:47)

  The crash is at: team: user.team.name
  user.team is undefined.

  Checking recent commits...
  ⚠️  a3f1b2c: "refactor: update team service to use new API response format"

  git diff shows:
  -    return response.data;
  +    return response.data.team;
```

It found the suspicious commit in 30 seconds. Now it compares:

```
PHASE 2 — FIND THE PATTERN

  team.service.ts (UPDATED):
    return response.data.team;    // unwraps new format ✓

  user.service.ts (NOT UPDATED):
    team: teamData.data;          // still expects old format ✗

  Root cause: API response changed from { id, name }
  to { team: { id, name } }. Team service was updated.
  User service was missed.
```

Then the one-line hypothesis test:

```
PHASE 3 — TEST HYPOTHESIS

  Hypothesis: user.service.ts needs to unwrap response.data.team

  Change: teamData.data → teamData.data.team
  Result: test PASSES ✓

PHASE 4 — FIX

  Regression test written (RED → GREEN)
  Fix applied.

  $ npm test
  85/85 tests passed, exit 0
```

**Total time: 10 minutes.** Without systematic debugging, someone would have added `user.team?.name ?? 'Unknown'` -- which hides the bug instead of fixing it. The profile would silently show "Unknown" instead of the actual team name. Nobody would notice until a PM files a bug two sprints later.

The four-phase structure forced the investigation to trace backward from symptom to source, compare working vs broken code, and find the actual divergence point **before writing any fix.**

---

## Demo: "Tests Pass" -- Prove It 👀

This is the skill that makes managers and leads say "I need this."

Most AI assistants will cheerfully tell you "tests should pass" without actually running them. enggenie:qa-verify enforces a simple rule: **show your work.**

```
╭─────────────────────────────────────────────────────╮
│ I'm using enggenie:qa-verify to verify before       │
│ claiming completion.                                 │
╰─────────────────────────────────────────────────────╯

Running: npm test
...

Results:
  156/156 tests passed
  Exit code: 0
  Coverage: 89% lines, 82% branches

Running: npm run build
  Build completed, exit 0

Running: npm run lint
  0 errors, 0 warnings

Checking acceptance criteria:
  ✅ Welcome email received within 60s (manual verification)
  ✅ Email contains first name and profile link (content verified)
  ✅ Retry on SendGrid failure (unit test confirms 3 retries)
  ✅ Failure logging with user ID (unit test confirms)
  ✅ Account active regardless of email (integration test)

5/5 acceptance criteria verified with evidence.
```

No "should work." No "probably passes." Every claim backed by actual output. There's a line in the skill that hit different when I read it back:

> *"Claiming work is complete without verification is dishonesty, not efficiency."*

Harsh? Maybe. Accurate? Absolutely.

---

## The Whole Picture: Spec to Ship

Those four demos cover about half of what enggenie does. Here's the full roster:

| Role | Skill | What It Does |
|------|-------|-------------|
| **PM** | `pm-refine` | Specs, story refinement, estimation |
| **Architect** | `architect-design` | Brainstorming, ADRs, technical decisions |
| **Architect** | `architect-plan` | Phased implementation plans |
| **Dev** | `dev-implement` | Executes plans with TDD subagents |
| **Dev** | `dev-tdd` | RED-GREEN-REFACTOR on every change |
| **Dev** | `dev-debug` | 4-phase systematic debugging |
| **Dev** | `dev-commit` | Conventional commit messages |
| **Reviewer** | `review-code` | Code review with severity levels |
| **Reviewer** | `review-design` | UI/design system compliance |
| **QA** | `qa-verify` | Evidence before completion claims |
| **QA** | `qa-test` | Playwright + manual browser testing |
| **Deploy** | `deploy-ship` | Commits, PRs, branch completion |
| **Memory** | `memory-recall` | Cross-session context |
| **Gateway** | `enggenie` | Routes to the right skill |

Each skill knows what comes next. The PM hands off to the Architect. The Architect hands off to the Dev. The Dev hands off to QA. QA hands off to Deploy. It's a complete pipeline -- not 14 isolated tools, but one coherent workflow from idea to production.

---

## Get Started in One Command

**Claude Code (primary), with support for Cursor, Copilot CLI, Gemini CLI, and OpenCode:**

```bash
npx skills add badrusiddique/enggenie-skill
```

Auto-detects your platform. No config files needed.

Try one skill to start:
- Say *"Write a spec for user notifications"* → pm-refine activates
- Say *"This test is failing, help me fix it"* → dev-debug activates
- Say *"Add a validate email function"* → dev-tdd activates

**GitHub:** [github.com/badrusiddique/enggenie-skill](https://github.com/badrusiddique/enggenie-skill)

---

## The Retro Was Different Last Month

Remember that sprint retro I described at the top? We had a very different one last month.

Specs come with acceptance criteria and QA test plans before anyone writes a line of code. Tests are written first -- not because I mandated it, but because the AI enforces the discipline and nobody wants to be the one who turns it off. Debugging follows a systematic investigation instead of the "let me try this" lottery. And "done" means verified with evidence, not vibes.

enggenie is open source, MIT licensed, and I built it because I got tired of watching the same problems repeat every sprint. One of our devs told me the AI guilt-tripped him into writing tests first. Another said the debugging skill saved him from a two-hour rabbit hole. Small wins, but they compound.

If you manage a team, you'll recognize every pain point in this post. If you're an engineer, you'll recognize every shortcut -- each skill has a "Shortcut Tax" section that lists what it costs when you skip the discipline.

Try it on your next feature. [Let me know what breaks.](https://github.com/badrusiddique/enggenie-skill/issues)

---

*[Badru Siddique](https://github.com/badrusiddique) is an Engineering Manager who builds developer tools to make engineering teams move faster without cutting corners.*

**Tags:** `AI Coding` · `Software Engineering` · `TDD` · `Engineering Management` · `Developer Tools`
