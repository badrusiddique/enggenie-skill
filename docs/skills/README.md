# enggenie Skills Reference

All 13 skills organized by role. Each skill is a domain expert that activates based on user intent.

## PM

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:pm-refine` | Spec generation, story refinement, estimation | "Write a spec for X", "Estimate this story", "Spike: can we use X?" | Four modes (spec, refine, spike, estimate) with transparent estimation math and Jira ticket creation |

## Architect

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:architect-design` | Brainstorming, ADRs, technical decisions | "Let's brainstorm the caching approach", "Should we use Kafka or SQS?" | Three modes (brainstorm, architecture, discussion) with decisions grounded in codebase evidence |
| `enggenie:architect-plan` | Phased implementation plans with deployment gates | "Create a plan from this spec", "Break this into tasks" | Deployment-sequenced phases, no placeholders, every step contains real code |

## Dev

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:dev-implement` | Subagent-driven TDD execution | "Execute the plan", "Start implementing" | Two-stage review gate (spec compliance + code quality) on every task, parallel dispatch |
| `enggenie:dev-tdd` | TDD discipline (RED-GREEN-REFACTOR) | "Add a validate email function", "Write this code" | Discipline overlay that fires during any coding, not a workflow step |
| `enggenie:dev-debug` | Systematic root cause investigation | "This test is failing", "Bug in the auth flow" | Four phases (investigate, find pattern, test hypothesis, fix), 3-attempt rule |

## Reviewer

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:review-code` | Request and receive code reviews | "Review my changes", "Got review feedback on the PR" | Two modes (requesting/receiving) with technical evaluation, not emotional performance |
| `enggenie:review-design` | Frontend/UI quality enforcement | "Check the dashboard against the design", "Accessibility audit" | Design system compliance, state coverage, responsive behavior, AI code smell detection |

## QA

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:qa-verify` | Evidence before completion claims | "Are the tests passing?", "Is this done?" | Verification gate: run the command, read the output, state the evidence |
| `enggenie:qa-test` | Playwright automation and manual browser testing | "Test the login flow", "Run QA on this feature" | QA mindset (empty data, double-click, slow network, back button), recon-then-action pattern |

## Deploy

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:deploy-ship` | Commits, PRs, Jira updates, branch completion | "Commit this", "Create a PR", "Ship it" | Conventional commits, 4 branch completion options, worktree cleanup, Jira integration |

## Memory

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie:memory-recall` | Cross-session context via claude-mem | "What did we do last session?", "Have we solved this before?" | 3-layer retrieval (search, timeline, fetch) for token-efficient memory access |

## Gateway

| Skill | Purpose | Example Triggers | Key Feature |
|-------|---------|------------------|-------------|
| `enggenie` | Routes ambiguous intent to the right specialist | Any SDLC-related request that does not match a specific skill | Defines what is outside the suite (quick questions, simple edits, file exploration) |

## Skill Interconnection

Skills consume each other's outputs in a defined pipeline:

```
pm-refine (spec) --> architect-design (approved design) --> architect-plan (phased plan)
    --> dev-implement (code) --> review-code + review-design (reviewed code)
    --> qa-verify + qa-test (verified code) --> deploy-ship (shipped)
```

`dev-debug` interrupts any stage when something breaks.
`memory-recall` is available to all stages as a utility.
`dev-tdd` is a discipline overlay active during all coding.

## Subagent Summary

| Skill | Subagents | Models |
|-------|-----------|--------|
| pm-refine | refinement, qa-planner, spec-reviewer, memory | sonnet, sonnet, sonnet, haiku |
| architect-design | explorer, memory | sonnet, haiku |
| architect-plan | explorer, doc-discovery, plan-reviewer | sonnet, haiku, sonnet |
| dev-implement | implementer, spec-reviewer, quality-reviewer | haiku/sonnet, sonnet, sonnet |
| dev-debug | investigator, memory | sonnet, haiku |
| review-code | code-reviewer | sonnet |
| review-design | design-reviewer | sonnet |
| qa-test | qa-automation, qa-manual | sonnet, sonnet |
