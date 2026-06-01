# Adopting enggenie as a Team

Installing everything at once and using deploy-ship on day one is a reliable way to have a bad first week with enggenie.

Not because the skills don't work - they do. But because each skill builds on behaviors the previous one established. If your team hasn't developed the habit of writing tests before code, dev-implement won't help - it will just produce well-structured code without tests. If dev has never seen a pm-refine spec, the handoff to Jira context won't land the way it's supposed to.

The teams that stick with enggenie adopt it in stages. Here is the order that works.

---

## Stage 1: Observe (Days 1-3)

**Skills:** `dev-brainstorm`, `review-code` (advisory mode only)

**What to do:**
Use dev-brainstorm on a real design question you're actually facing. Not a toy example - something with genuine tradeoffs. Ask it to write an ADR. Read the ADR. Notice what it got right, what it missed, what context it needed that you had to supply.

Run review-code on a PR that already passed human review. Compare what the three lenses flag against what your reviewer caught.

**What not to do yet:** Do not let any enggenie output go directly into a commit or PR. This stage is about calibration, not productivity.

**What success looks like:** Someone on the team says "the security lens caught something we would have missed." That's the signal to move to Stage 2.

---

## Stage 2: Spec and plan (Week 1)

**Skills:** `pm-refine`, `dev-plan`

**What to do:**
Pick one upcoming story that has vague acceptance criteria - there is always one. Run pm-refine on it. Have the PM and the lead dev read the output together. Annotate what's wrong, what's missing, what surprised them. Run it again with that feedback in the prompt.

Then run dev-plan on the refined spec. Have the dev who will actually build it read the plan. Do the phases make sense? Are the dependencies right? Are the task sizes reasonable?

The goal here is not perfect output on the first run. The goal is understanding where your context needs to be more explicit.

**What not to do yet:** Don't execute the plan yet. Don't commit to the spec as-is without human review. AI writes, humans validate.

**What success looks like:** The dev picks up the story and says "this spec actually tells me what to build." That is a meaningfully different statement than usual.

---

## Stage 3: TDD-guided build (Weeks 2-3)

**Skills:** `dev-tdd`, `dev-implement`

**What to do:**
Start with dev-tdd on isolated features only - utility functions, service layer methods, API route handlers. Not UI components and not anything that touches multiple services at once. The scope matters here: TDD is easiest to enforce on units with clear inputs and outputs.

When a task from the dev-plan is ready to execute, use dev-implement on a single task at a time. Review each failing test before letting it proceed to implementation. This is not slowness - this is the point. If the test doesn't describe the right behavior, catch it before the implementation exists.

**What not to do yet:** Don't let dev-implement run a full phase unsupervised. Keep a human in the loop between tasks until the team has seen enough cycles to trust the output.

**What success looks like:** A developer says "the failing test showed me I'd misread the spec" before writing a single line of implementation code.

---

## Stage 4: Full pipeline (Month 1+)

**Skills:** `qa-verify`, `qa-test`, `deploy-ship`

**What to do:**
Add qa-verify as a gate before any PR is opened. Not after - before. qa-verify running and showing green with actual exit codes and test counts becomes the definition of "done" locally.

Add qa-test for features with user-facing flows. Start with one critical path per sprint - session join, checkout, login - rather than trying to cover everything.

Use deploy-ship to create PRs. The PR body it produces is better than most developers write by hand - it includes the spec context, what was built, what the reviewer should focus on.

**Human gates to keep:** Even with the full pipeline, a human should review the qa-verify output before merging. And someone should read the PR body before approving to confirm the spec context is accurate.

**What not to do yet:** Don't remove human review from the critical path. enggenie makes review better - it doesn't replace it.

**What success looks like:** A PR comes in and the reviewer says "I can actually tell what this is supposed to do from the PR description."

---

## Stage 5: Optional integrations

**Skills:** `memory-recall`, `enggenie` gateway + Jira MCP

**memory-recall** becomes valuable around the six-week mark, when decisions from previous sessions start to matter. Before that, teams usually have enough context in active files. Enable it when someone asks "how did we handle X last time?" more than twice in a sprint.

**Jira MCP handoffs** are worth setting up when:
- PM and dev are different people
- QA runs in a separate phase from dev
- Any role needs to pick up work cold without a verbal briefing

The Jira integration does not require code changes - it requires Atlassian MCP to be configured in your AI coding tool's settings. See [docs/guides/team-setup.md](team-setup.md) for the setup steps.

**What not to do yet:** Don't require Jira integration for teams where one person handles PM-Dev-QA in a single session. The overhead of writing handoff context to Jira is only worth it when someone else is reading it.

---

## What to expect

The first week will feel slower. That is not a sign something is wrong. It means the constraints are working - TDD enforced, specs written before coding, tests running before "done" is claimed. Speed comes back in week three when the review cycles shorten and bugs stop coming back from QA.

Most teams that tried to skip stages came back and did it in order anyway. Stage 1 (observe) is the one most skips happen on - it feels unproductive to just watch the tool. But the calibration it produces makes every subsequent stage go faster. Skip it if you want, but plan to spend extra time in Stage 2 doing the calibration work that Stage 1 would have handled.

---

## FAQ

**"Our devs don't have time to read ADRs."**
Then dev-brainstorm output goes into a decision log and devs reference it when they hit a question the code doesn't answer. The ADR is not required reading - it's a record. The decision is required reading.

**"We already have code review in our process."**
Good. review-code makes it better, not different. The three lenses catch things human reviewers miss under deadline pressure - not because humans are bad at reviewing, but because a human reviewer under time pressure naturally deprioritizes the security lens when the feature looks correct.

**"Can we just use the deploy-ship skill without the rest?"**
Yes. But you will get a well-formatted PR for code that may not have tests, may have security issues, and may not match the spec. The pipeline is valuable because of what it catches before deploy-ship runs.
