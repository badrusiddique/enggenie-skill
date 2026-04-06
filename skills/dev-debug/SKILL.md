---
name: dev-debug
description: Use when encountering any bug, test failure, or unexpected behavior - systematic root cause investigation before proposing any fixes
---

# dev-debug

## Overview

Systematic debugging. Four phases. No guessing.

Bugs tempt you to guess. "Probably this." "Let me just try." "One more thing." Every guess costs time, introduces noise, and drifts you further from the root cause. This skill enforces a discipline: understand first, fix second.

## Announcement

When this skill is active, announce:

> "I'm using enggenie:dev-debug for systematic root cause investigation."

---

## Hard Rule: No Fixes Without Understanding the Cause First

Do NOT propose a fix until you can state: "The bug is caused by X, because I observed Y."

No "try this." No "maybe it's." No "let's see if." You state the cause, you show the evidence, then you fix. If you cannot state the cause, you are still in Phase 1.

---

## Phase 1 -- Investigate

Gather evidence. Do not interpret yet. Do not fix anything.

### Read Error Messages Completely

Read the FULL error output. Not the first line. Not the summary. The whole thing.

- Stack trace: every frame. The cause is often 3-4 frames deep, not at the top.
- Line numbers: go to the exact line. Read 10 lines above and below.
- Error codes: look them up. Error codes exist because the message alone is ambiguous.
- Stderr vs stdout: check both. Some failures are silent on stdout.

### Reproduce Consistently

Before investigating further, confirm you can reproduce the bug:

1. Write down the exact steps.
2. Run them. Does the bug appear?
3. Run them again. Does it appear every time?
4. If intermittent: note the frequency. Note what varies between runs.

If you cannot reproduce it, you cannot verify a fix. Do not proceed to Phase 3 without reproduction.

### Check Recent Changes

```
git log --oneline -20
git diff HEAD~5
```

What changed recently? New dependencies? Config changes? Environment variables? Version bumps? The bug exists now and didn't before. Something changed. Find what.

### Multi-Component Systems: Trace the Boundary

When the system has multiple components (services, layers, modules):

1. Identify every boundary the failing request crosses.
2. Add diagnostic logging at EACH boundary -- input and output.
3. Run the reproduction steps ONCE.
4. Read the logs. Find WHERE the data goes wrong.

Do not guess which component is broken. Instrument and observe. The logs will tell you.

### Trace Data Flow Backward

Start at the symptom. Work backward:

- Where does this value come from?
- What function produced it?
- What were the inputs to that function?
- Where did THOSE inputs come from?

Keep going until you find the point where expected behavior diverges from actual behavior. That is your investigation target.

**Phase 1 exit criteria:** You can describe WHERE the bug manifests and WHAT the incorrect behavior is, with evidence from logs, traces, or reproduction.

---

## Phase 2 -- Find the Pattern

Now interpret. Compare. Understand.

### Find Similar Working Code

Search the codebase for similar functionality that works correctly:

- Same API, different endpoint
- Same pattern, different module
- Same operation, different data type

If something similar works, the difference between working and broken is your investigation target.

### Compare Working vs Broken

List EVERY difference between working and broken code:

- Different function calls
- Different argument order
- Different config values
- Different error handling
- Different timing or ordering
- Different dependencies or versions

Write the list down. Do not hold it in your head. One of these differences is the cause.

### Understand Dependencies and Assumptions

Every piece of code makes assumptions:

- Input format and range
- Availability of services
- Order of operations
- State of shared resources
- Environment variables and config

Which assumptions does the broken code make? Which of those assumptions are violated? Check each one.

**Phase 2 exit criteria:** You have a ranked list of likely causes, based on evidence from Phase 1 and comparison with working code.

---

## Phase 3 -- Test One Hypothesis

Pick the most likely cause from your Phase 2 list. Test it. One at a time.

### State the Hypothesis

Before making any change, write it down:

> "I think [X] causes this because [Y]."

If you cannot fill in both X and Y with specifics, you are guessing. Go back to Phase 2.

### Make the Smallest Change

The change should test ONE thing:

- Change one variable
- Comment out one call
- Add one assertion
- Swap one value

If your "test change" touches more than one thing, you are testing multiple hypotheses simultaneously. You will not know which one mattered.

### Evaluate

- **Worked?** -- Bug is gone. Move to Phase 4.
- **Didn't work?** -- Revert. Completely. Formulate a new hypothesis. Do not stack a second change on top of a failed first change.
- **Partially worked?** -- You are close but your hypothesis is incomplete. Refine it. Do not ship a partial fix.

### One Variable at a Time

This is not a suggestion. This is the rule. If you change two things and the bug disappears, you do not know which change fixed it. You do not know if both changes are needed. You have introduced uncertainty into your fix.

Change one thing. Test. Revert if it fails. Change the next thing. Test.

**Phase 3 exit criteria:** You have identified the root cause through a single, minimal change that eliminates the bug.

---

## Phase 4 -- Fix It

Now -- and only now -- write the fix.

### Write a Failing Test That Reproduces the Bug

Before writing the fix:

1. Write a test that exercises the exact bug condition.
2. Run it. It MUST fail (confirming the test captures the bug).
3. If the test passes, your test is wrong. It does not reproduce the bug.

This test is your regression guard. It ensures the bug stays dead.

### Fix the Root Cause, Not the Symptom

- Symptom: "Response returns null" -- Fix: add null check. (WRONG)
- Root cause: "Query filter excludes valid records because date comparison uses wrong timezone" -- Fix: correct the timezone handling. (RIGHT)

If your fix is a null check, a try/catch, a retry, or a default value, you are probably treating the symptom. Ask: "Why is this value wrong in the first place?"

### Verify

1. Run the regression test. It MUST pass.
2. Run the FULL test suite. ALL tests MUST pass.
3. If other tests break, your fix has side effects. Investigate those before proceeding.

### The 3-Attempt Rule

If you have attempted 3 fixes and none of them resolved the bug:

**STOP.**

This is not a bug. This is an architecture problem. The system's design makes this failure mode possible or even likely. Patching it will not hold.

**Patterns indicating an architectural problem:**
- Each fix reveals new issues in a different place (shared state, hidden coupling)
- Fixes require "massive refactoring" to implement correctly
- Each fix creates new symptoms elsewhere in the system
- You are "sticking with it through sheer inertia" rather than questioning fundamentals

**STOP and question fundamentals:**
- Is this pattern fundamentally sound for what we need?
- Should we refactor the architecture rather than continue patching symptoms?
- Are we persisting because of sunk cost, not because the approach is correct?

This is NOT a failed hypothesis -- this is a wrong architecture. Discuss with the team. Describe what you found in Phases 1-3. Propose a design change, not another patch.

**Phase 4 exit criteria:** Regression test passes. Full suite passes. Root cause is addressed, not papered over.

---

## The Shortcut Tax

Every debugging shortcut has a cost. Here is what you are actually paying.

| Shortcut | What it costs you |
|----------|------------------|
| "Quick fix -- just add a null check" | You hid the bug. It will resurface in a different form, harder to trace. |
| "Just try this and see" | You changed two things. One worked, one didn't. Now you don't know which. |
| "It's probably the database" | You spent 2 hours on the database. It was a config file. Investigate, don't guess. |
| "Let me change a few things at once" | Multiple simultaneous changes make root cause identification impossible. |
| "One more attempt, I'm close" | You said that two attempts ago. Three failed fixes means stop and rethink. |
| "Works on my machine" | Environment difference IS the bug. Reproduce in the failing environment. |
| "The error message is misleading" | Maybe. But you haven't read it completely yet. Read every line first. |
| "I've seen this before" | Past experience is a hypothesis, not a diagnosis. Still verify in this context. |

---

## Gut Check

STOP and reassess if you notice yourself:

- **Changing code without a hypothesis** -- You are guessing. Go back to Phase 1.
- **Stacking changes** -- You added fix B on top of fix A. Revert both. Test one at a time.
- **Skipping reproduction** -- You cannot verify a fix for a bug you cannot reproduce.
- **Blaming the framework/library/OS** -- Possible, but verify YOUR code first. It is almost always your code.
- **Spending more than 30 minutes without new evidence** -- You are stuck in a loop. Change your investigation approach. Add more instrumentation. Read the source code of the dependency.
- **Feeling frustrated** -- Frustration leads to guessing. Step back. Re-read Phase 1. Start fresh with evidence.
- **Fixing the symptom** -- Null checks, retries, and default values are not fixes. They are band-aids. Find the root cause.
- **Not reverting failed attempts** -- Every failed fix that stays in the code is noise. Revert completely before trying the next hypothesis.

---

## User Signals - Change Approach If You See These

Your user's behavior tells you if your debugging approach is working:

| User says/does | What it means | Your action |
|----------------|---------------|-------------|
| "Is that not happening?" | You're not making visible progress | Share what you've found so far, even if incomplete |
| "Stop guessing" | You're proposing fixes without evidence | Go back to Phase 1. Gather evidence first. |
| "Just try X" | They have domain knowledge you lack | Try their suggestion. If it works, investigate WHY it works. |
| "We've been going in circles" | You're re-treading old ground | Summarize all hypotheses tested. Identify what's NOT been checked. |
| Long silence after your update | Your update was confusing or unhelpful | Ask: "Should I try a different approach?" |

---

## When Investigation Finds Nothing

If all 4 phases complete and the root cause remains unknown:

1. **Environmental:** Is the issue specific to one machine/environment? Try reproducing elsewhere.
2. **Timing/Race condition:** Is the issue intermittent? Add timestamps to logs. Look for ordering assumptions.
3. **External dependency:** Is a third-party service behaving differently? Check their status page, recent changes.
4. **Escalate:** Present your findings (what you checked, what you ruled out) and ask the user or team for domain expertise.

Never say "I can't find the cause" without listing what you investigated and ruled out.

---

## Subagents

### Investigator Subagent (sonnet)

Dispatched to gather evidence. Does NOT fix anything.

**Role:** Read logs, trace data flow, check recent changes, reproduce the bug. Return structured findings.

**Prompt template:** `agents/investigator-agent.md`

**Returns:**
- Error messages (full text, not summaries)
- Reproduction steps and results
- Recent changes in relevant files
- Data flow trace from symptom to source
- List of boundaries crossed and their status

### Memory Subagent (haiku, if available)

Checks project memory for previously encountered patterns.

**Role:** "Have we seen this bug pattern before?" Search memory for similar errors, similar symptoms, past root causes.

**Returns:**
- Similar past bugs and their root causes (if found)
- Relevant debugging notes from previous sessions
- "No matches found" (if nothing relevant)

**Graceful degradation:** If haiku is not available, skip this subagent. Memory search is helpful but not required. The investigator subagent provides sufficient evidence to proceed.

---

## Parallel Agent Dispatch

When multiple independent failures exist (e.g., 3 different test suites failing, 2 services returning errors), do NOT investigate them sequentially.

Dispatch one investigator subagent per failure domain:

1. Identify independent failure domains (failures that do not share code paths or data).
2. Dispatch one investigator per domain, each with its own scope.
3. Collect results from all investigators.
4. Look for shared root causes across domains -- multiple symptoms can have one cause.
5. If domains are NOT independent (shared state, shared services), investigate sequentially. Parallel investigation of coupled systems produces misleading results.

---

## Subagent Context Preservation

When subagents (Investigator, Memory) complete their work, explicitly capture their key findings back to the main conversation:

- **Investigator subagent:** Full error messages, reproduction results, recent changes, data flow trace, boundary status
- **Memory subagent:** Similar past bugs, previous root causes, relevant debugging notes

Do not assume the orchestrating agent retains subagent context automatically. Extract and summarize findings before forming hypotheses.

---

## Recommended Model

**Primary:** sonnet
**Why:** Debugging requires methodical reasoning and code comprehension. Sonnet balances analytical depth with speed for iterative hypothesis testing.

This is a recommendation. Ask the user: "Confirm model selection or override?" Do not proceed until the user responds.

---

## Supporting References

- `references/root-cause-tracing.md` -- Backward tracing technique: start at the symptom, trace data flow backward through each transformation until you find the divergence point.
- `references/multi-component-debugging.md` -- Diagnostic instrumentation for multi-service systems: where to add logging, what to capture at each boundary, how to correlate across services.
- `references/condition-based-waiting.md` -- Replace arbitrary timeouts with condition polling. When debugging timing issues, never use `sleep`. Poll for the expected condition with a timeout ceiling.
- `../dev-tdd/references/defense-in-depth.md` - Validate at every layer, make bugs structurally impossible

Read these references when you need detailed technique guidance. The phases above tell you WHAT to do. The references tell you HOW.

---

## Subagent Prompt Template

`agents/investigator-agent.md`

This template defines the investigator subagent's instructions:

- Scope: what to investigate (specific error, specific component, specific test)
- Evidence format: structured output with sections for errors, reproduction, changes, data flow
- Constraints: gather evidence only, do not propose fixes, do not modify code
- Exit: return findings when evidence is sufficient to form a hypothesis

---

## Entry / Exit

**Entry:** None -- bugs happen anytime. This skill interrupts any workflow. When a bug, test failure, or unexpected behavior is encountered, this skill activates immediately regardless of what other skill is running.

### Jira Bug Entry

When the user references a Jira ticket with QA findings (e.g., "Fix bugs from PROJ-1234", "QA found issues on PROJ-1234"):

1. Read the Jira ticket using MCP tools
2. Find the "QA Results" comment — it contains bug descriptions, severity, and reproduction steps
3. Find the "Dev Handoff" comment — it contains the PR link and what was built
4. Use the reproduction steps from QA as your Phase 1 starting point — QA already documented how to trigger the bug

This skips the "gather evidence" portion of Phase 1 and lets you jump to reproduction verification. Verify QA's reproduction steps work, then proceed to Phase 2.

**Exit:** Bug fixed, regression test written, full suite passes. Update the Jira ticket with a comment:

```markdown
## Bug Fix
- Root cause: [what caused the bug]
- Fix: [what was changed]
- PR: [link to fix PR]
- Regression test: [test name and file path]
```

Resume the previous workflow from where it was interrupted.

---

## Quick Reference

| Phase | Goal | Key Action | Move On When |
|-------|------|------------|-------------|
| 1. Investigate | Understand the symptom | Read errors, reproduce, trace data flow | You can reproduce consistently |
| 2. Find Pattern | Compare working vs broken | Find similar working code, list differences | You have a specific hypothesis |
| 3. Test Hypothesis | Validate one theory | Smallest possible change, one variable | Hypothesis confirmed or rejected |
| 4. Fix | Permanent solution | Failing test first, then fix root cause | Test passes, no regressions |
