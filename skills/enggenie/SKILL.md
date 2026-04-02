---
name: enggenie
description: Use when starting a software development conversation and the user's intent is not clearly matched by a specific enggenie skill — routes to the right role-based expert
---

# enggenie — The Right Expert for the Right Moment

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, skip this skill entirely.
</SUBAGENT-STOP>

## Overview

enggenie is a role-based SDLC skill suite. Each skill is a domain expert — PM, Architect, Dev, Reviewer, QA, Deploy. This gateway skill routes you to the right one.

**If a specific enggenie skill already matched your task, you should be there instead of here.** This gateway fires only when intent is ambiguous.

## Instruction Priority

1. **User's explicit instructions** (CLAUDE.md, project config, direct requests) — highest priority
2. **enggenie skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If a user's CLAUDE.md says "don't use TDD" and enggenie:dev-tdd says "always use TDD," follow the user's instructions.

## Skill Routing

Match the user's intent to the right skill:

| User says something like... | Skill | Role |
|-----------------------------|-------|------|
| "I want to build X", "Write a spec", "Refine this story", "Estimate this" | enggenie:pm-refine | PM |
| "Let's brainstorm", "What's the best approach?", "Architecture review" | enggenie:architect-design | Architect |
| "Create a plan", "Break this into tasks", "How should we implement this?" | enggenie:architect-plan | Architect |
| "Execute the plan", "Build this", "Start implementing" | enggenie:dev-implement | Dev |
| "Add a function", "Write this code", "Implement X" (no plan context) | enggenie:dev-tdd | Dev |
| "This is broken", "Test failing", "Bug", "Not working" | enggenie:dev-debug | Dev |
| "Review my code", "Check this PR", "Got review feedback" | enggenie:review-code | Reviewer |
| "Check the design", "Does this match the mockup?", "Accessibility?" | enggenie:review-design | Reviewer |
| "Are tests passing?", "Is this done?", "Verify this works" | enggenie:qa-verify | QA |
| "Test this feature", "QA the login flow", "Run Playwright tests" | enggenie:qa-test | QA |
| "Commit this", "Create a PR", "Ship it", "Done with this branch" | enggenie:deploy-ship | Deploy |
| "What did we do last time?", "Did we solve this before?" | enggenie:memory-recall | Memory |

## When No Skill Matches

If the user's request doesn't clearly match any skill:

1. Ask: "What are you trying to accomplish?" with options:
   - Plan a feature (→ enggenie:pm-refine or enggenie:architect-design)
   - Build something (→ enggenie:architect-plan or enggenie:dev-implement)
   - Fix something (→ enggenie:dev-debug)
   - Review something (→ enggenie:review-code)
   - Test something (→ enggenie:qa-test)
   - Ship something (→ enggenie:deploy-ship)

2. Route to the appropriate skill.

## When NOT to Use Any Skill

Not everything needs a skill. Skip enggenie entirely for:
- Quick questions ("What does this function do?")
- Simple edits ("Change this variable name")
- File exploration ("Show me the directory structure")
- Git operations ("What changed in the last commit?")

The suite stays out of your way when you don't need it.

## Skill Priority

When multiple skills could apply, use this order:

1. **Process skills first** (architect-design, dev-debug) — these determine HOW to approach the task
2. **Implementation skills second** (dev-tdd, dev-implement) — these guide execution
3. **Verification skills third** (qa-verify, review-code) — these check the work

"Let's build X" → architect-design first, then dev-implement.
"Fix this bug" → dev-debug first, then dev-tdd for the fix.

## Rigid vs Flexible Skills

**Rigid** (follow exactly — don't adapt away discipline):
- enggenie:dev-tdd — RED-GREEN-REFACTOR cycle is non-negotiable
- enggenie:qa-verify — Evidence before claims is non-negotiable
- enggenie:dev-debug — 4-phase investigation is non-negotiable

**Flexible** (adapt principles to context):
- enggenie:architect-design — Modes and depth scale to project size
- enggenie:pm-refine — Spec detail scales to feature complexity
- enggenie:deploy-ship — Commit format adapts to team conventions

## Red Flags — STOP If You Think This

These thoughts mean you're rationalizing skipping a skill:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions lead to tasks. Check for skills first. |
| "I need more context first" | Skills tell you HOW to gather context. Check first. |
| "Let me explore the codebase first" | Skills define HOW to explore. Check first. |
| "I can handle this without a skill" | If a skill exists for this task, use it. |
| "The skill is overkill for this" | Simple things become complex. Use the skill. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This doesn't need a formal process" | If a skill exists, it exists for a reason. Use it. |
| "I remember what the skill says" | Skills evolve. Load the current version. |
| "I know the concept already" | Knowing the concept ≠ following the discipline. |
| "Let me just write the code quickly" | Quick code without TDD = slow debugging later. |

**If a skill applies to your task, using it is not optional.** You cannot rationalize your way out of this.

## Platform Adaptation

Skills use Claude Code tool names by default. For other platforms:
- **Cursor:** See `references/cursor-tools.md`
- **Copilot CLI:** See `references/copilot-tools.md`
- **Gemini CLI:** See `references/gemini-tools.md`
- **OpenCode:** See `references/opencode-tools.md`

## All Skills

| Role | Skill | Purpose |
|------|-------|---------|
| PM | enggenie:pm-refine | Spec generation, story refinement, estimation |
| Architect | enggenie:architect-design | Brainstorming, ADRs, technical decisions |
| Architect | enggenie:architect-plan | Phased implementation plans |
| Dev | enggenie:dev-implement | Subagent-driven TDD execution |
| Dev | enggenie:dev-tdd | TDD discipline (RED-GREEN-REFACTOR) |
| Dev | enggenie:dev-debug | Systematic root cause investigation |
| Reviewer | enggenie:review-code | Request + receive code reviews |
| Reviewer | enggenie:review-design | Frontend/UI quality enforcement |
| QA | enggenie:qa-verify | Evidence before completion claims |
| QA | enggenie:qa-test | Playwright + manual browser testing |
| Deploy | enggenie:deploy-ship | Commit, PR, branch completion, Jira |
| Memory | enggenie:memory-recall | Cross-session context (requires claude-mem) |
