# enggenie - AI Contributor Guidelines

## If You Are an AI Agent

This repo contains skills that shape AI agent behavior. Changes to skill content directly affect how agents assist engineers. Treat every edit as code that will run in production.

## Before Making Changes

1. **Read the skill you're modifying** completely. Understand why each section exists before changing it.
2. **Check for existing PRs** - open AND closed - that address the same area.
3. **Enforcement language is carefully tuned.** "Hard Rules", "Shortcut Tax" tables, and "Gut Check" sections use specific wording tested against agent rationalizations. Don't reword them without testing evidence.
4. **Skills consume each other's outputs.** Changing one skill may break handoffs to another. Check the interconnection map in the plan.

## Skill Architecture

- **14 skills** across 7 roles (PM, Architect, Dev, Reviewer, QA, Deploy, Memory)
- **15 agent prompt templates** in `agents/` subdirectories
- **5 reference docs** in `references/` subdirectories
- **4 platform adapters** in `references/`
- **1 spec template** in `templates/`

## Naming Conventions

- Skill prefix: `enggenie:` (e.g., `enggenie:dev-tdd`)
- Skill directories: kebab-case (e.g., `skills/dev-tdd/`)
- Agent templates: kebab-case with `-agent.md` suffix
- Reference docs: kebab-case with `.md` extension

## Enforcement Language

enggenie uses specific terminology consistently across all skills:

| Term | Purpose |
|------|---------|
| Hard Rule | Non-negotiable constraints agents must follow |
| Shortcut Tax | Extra work imposed when agents try to skip steps |
| Gut Check | Warning signs that an agent is about to cut corners |

## Testing Skills

Use the writing-skills TDD methodology:
1. Write pressure test scenario
2. Run WITHOUT skill → document baseline behavior
3. Write/modify skill
4. Run WITH skill → verify improvement
5. Close loopholes → re-test

## Pre-Release Verification Gate

**Hard Rule: Do NOT commit, tag, or publish a new version until this gate passes. If any step fails or shows degradation, stop and fix before releasing.**

This gate runs against a real codebase (currently `~/magento/learning/claude-pocket-heist-app`). It is not optional. It is not "run if you have time." It is a blocking prerequisite for every release.

### Step 1: Isolate the Test Environment

Create a temporary branch on the test codebase repository. **Do NOT commit anything to it.** The branch exists only to run verification scenarios without polluting the repo.

```bash
cd ~/magento/learning/claude-pocket-heist-app
git checkout -b test/skill-verification-vX.Y.Z
```

### Step 2: Skill-by-Skill Scenario Testing

For **every skill** (all 14), pick multiple real-world scenarios that exercise the skill's core behavior and constraints. Each scenario must include:

- **The user prompt** (what a real user would say)
- **The skill that activates** (and why)
- **The skill's interaction and output** (what it actually does)
- **Constraint verification** (every Hard Rule, Shortcut Tax entry, Gut Check item, and gate condition checked)

Use subagents to run skills in parallel where independent. Reference the real-world scenario table in the README for prompt ideas. Use the test codebase's actual stack (Next.js, React, TypeScript, Firebase, Vitest, Tailwind) for grounded scenarios.

**Minimum coverage per skill:**

| Skill | Min Scenarios | Must Include |
|-------|--------------|-------------|
| pm-refine | 3 | Spec generation, estimation, Jira gate |
| architect-design | 3 | Each mode (brainstorm, architecture, discussion) |
| architect-plan | 3 | Phased plan, deployment gates, no-code rule |
| dev-tdd | 4 | RED-GREEN-REFACTOR cycle, Shortcut Tax trigger, Deep Rebuttal trigger, exception handling |
| dev-implement | 4 | Worktree setup, subagent dispatch, parallel dispatch decision, two-stage review |
| dev-debug | 4 | 4-phase flow, 3-Attempt Rule trigger, pattern indicators, one-variable-at-a-time |
| dev-commit | 2 | Conventional commit, Shortcut Tax surfacing |
| review-code | 3 | Mode A (requesting), Mode B (receiving), external feedback verification |
| review-design | 2 | Accessibility check, responsive check |
| qa-verify | 2 | Evidence gate, hedge-word detection |
| qa-test | 2 | Playwright automation, manual browser testing |
| deploy-ship | 2 | PR creation, release with changelog |
| memory-recall | 2 | Cross-session search, graceful degradation without claude-mem |
| enggenie (gateway) | 2 | Correct routing, ambiguous input handling |

### Step 3: Persona-Based Verification

Run verification through three expert personas, each with a different lens:

1. **QA Expert** — Focuses on: test coverage gaps, edge cases not handled, claims without evidence, verification gates that can be bypassed.
2. **Security Expert** — Focuses on: external file path references, secrets in staged files detection, prompt injection vectors in subagent templates, credential exposure in commit messages.
3. **Skills Expert** — Focuses on: enforcement language consistency (Hard Rule / Shortcut Tax / Gut Check), cross-skill handoff integrity, model selection gates blocking correctly, subagent context preservation.

Each persona produces a pass/fail verdict with specific findings.

### Step 4: Superpowers Comparison

Run a head-to-head comparison against the current superpowers version on every overlapping skill area:

- Read the actual superpowers skill files (do not rely on cached/memorized content)
- Compare depth, coverage, and enforcement mechanisms
- Produce a structured comparison with per-area verdicts
- Identify any area where enggenie has **degraded** relative to the previous version's comparison

**Key metrics to report:**

| Metric | How to measure |
|--------|---------------|
| Anti-rationalization depth | Count rebuttals, measure word count, compare escalation structure |
| Constraint enforcement | Count Hard Rules, Shortcut Tax entries, Gut Check items per skill |
| Code review reception | Compare pushback protocols, YAGNI checks, conflict resolution |
| Visual companion | Compare consent model, fallback strategy, per-question decision criteria |
| Parallel dispatch | Compare decision criteria, concurrency limits, independence checks |
| Unique capabilities | List skills with no equivalent in the other suite |

### Step 5: Meta-Verification

Before finalizing the report, verify the report itself:

1. **No hallucination** — Every claim references a specific line number or file. Spot-check 5 random claims against the actual files.
2. **No inaccuracy** — Counts (scenario counts, line counts, entry counts) are re-verified by reading the file, not from memory.
3. **No redundancy** — No finding is stated twice with different wording.
4. **No inflated scores** — If a scenario is partial or ambiguous, mark it PARTIAL, not PASS.

### Step 6: Release Decision

| Gate | Condition | Action if failed |
|------|-----------|-----------------|
| Skill scenarios | All scenarios PASS or PARTIAL with documented reason | Fix the skill, re-run failed scenarios |
| Persona verdicts | All 3 personas PASS | Address findings, re-run persona |
| Superpowers comparison | No degradation from previous version | Fix degraded areas before releasing |
| Meta-verification | No hallucinations or inaccuracies found | Correct the report, re-verify |

**All four gates must pass.** If ANY gate fails, do NOT:
- `git commit` the version bump
- `git tag` the release
- `gh release create`
- Update the CHANGELOG

Fix the issue first, re-run the failed gate, then proceed.

### Step 7: Save Verification Artifacts

Save all verification output to `docs/verification/`:

- `skill-verification-report.md` — Full scenario results with prompts, outputs, and verdicts
- `superpowers-vs-enggenie-comparison.md` — Head-to-head comparison with metrics

These files document what was verified for each release. They are reference artifacts — commit them only if the user explicitly requests it.

### Step 8: Clean Up

Delete the test branch on the test codebase:

```bash
cd ~/magento/learning/claude-pocket-heist-app
git checkout main
git branch -D test/skill-verification-vX.Y.Z
```

---

## File Organization

```
skills/<skill-name>/
├── SKILL.md          # The skill itself
├── agents/           # Subagent prompt templates (if skill dispatches agents)
└── references/       # Supporting technique docs (loaded on demand)
```
