# Switching from superpowers to enggenie

If you are using [superpowers](https://github.com/obra/superpowers), this guide maps every skill to its enggenie equivalent and covers what is new, what merged, and what changed.

## Feature Mapping

| superpowers skill | enggenie equivalent | Notes |
|-------------------|---------------------|-------|
| writing-plans | architect-plan | Phased plans with deployment gates instead of flat task lists |
| executing-plans | dev-implement | Subagent-driven with two-stage review gate |
| test-driven-development | dev-tdd | Same RED-GREEN-REFACTOR discipline, different enforcement language |
| systematic-debugging | dev-debug | Same 4-phase approach, adds parallel investigator dispatch |
| requesting-code-review | review-code (Mode A) | Merged into one skill |
| receiving-code-review | review-code (Mode B) | Merged into one skill |
| verification-before-completion | qa-verify | Same evidence-based verification, adds TodoWrite integration |
| brainstorming | architect-design | 3 modes (brainstorm, architecture, discussion) instead of 1 |
| subagent-driven-development | dev-implement | Merged into the implementation engine |
| using-git-worktrees | dev-implement (Phase 0) | Built into the implementation skill, not standalone |
| finishing-a-development-branch | deploy-ship | Expanded: commits, PRs, Jira updates, worktree cleanup |
| dispatching-parallel-agents | dev-implement | Parallel dispatch is built into the execution loop |
| using-superpowers | enggenie (gateway) | Routes to the right skill by intent |
| writing-skills | (removed) | Dev tool for authoring skills, not user-facing |

## What Is New in enggenie

These capabilities do not exist in superpowers:

- **pm-refine** -- Full spec generation with clarifying questions, estimation, subtask breakdown, QA test plan, and Jira ticket creation. Four modes: spec, refine, spike, estimate.
- **qa-test** -- QA-perspective testing with Playwright automation and manual browser testing. Tests user journeys, not implementation details. Recon-then-action pattern for reliable browser interaction.
- **review-design** -- Frontend/UI quality review: design system compliance, state coverage (loading, empty, error, hover, focus, disabled, active), responsive behavior, accessibility audit, AI code smell detection.
- **memory-recall** -- Cross-session context via claude-mem. 3-layer retrieval (search, timeline, fetch) for token-efficient memory access. AST-based code exploration.
- **Phased implementation plans** -- architect-plan produces deployment-sequenced plans with phase boundaries and readiness gates. Each phase is independently deployable. This replaces the flat task lists from writing-plans.

## What Merged

Several superpowers skills were consolidated:

**requesting-code-review + receiving-code-review = review-code.** One skill handles both sides. Mode A dispatches a reviewer subagent. Mode B processes human or external reviewer feedback. Same technical evaluation standard, fewer skills to maintain.

**executing-plans + subagent-driven-development = dev-implement.** The execution engine and the subagent dispatch pattern were always the same workflow. dev-implement handles plan execution, subagent dispatch, worktree management, and parallel agent coordination in one skill.

**using-git-worktrees = dev-implement Phase 0.** Worktree setup is built into the implementation flow. It detects or creates the worktree directory, ensures gitignore coverage, creates the feature branch worktree, runs project setup, and verifies baseline tests.

**dispatching-parallel-agents = dev-implement parallel dispatch.** The parallel coordination rules (max 3 concurrent, independence must be real, merge carefully) are embedded in the execution loop.

## What Was Removed

**writing-skills** -- This was a developer tool for authoring and testing skill files. It is not a user-facing capability. Teams that need to author custom skills can follow the [Writing Custom Skills](writing-custom-skills.md) guide.

## Enforcement Language Differences

enggenie uses its own terminology. If you are accustomed to superpowers language, here is the mapping:

| superpowers | enggenie | Purpose |
|-------------|----------|---------|
| Iron Law | Hard Rule | Non-negotiable constraint |
| Rationalization Prevention | Shortcut Tax | Table showing the cost of each shortcut |
| Red Flags | Gut Check | Pattern-matched warnings to stop and reassess |

The concepts are similar. The language is intentionally different to avoid confusion when both are installed and to reflect enggenie's softer enforcement philosophy (inform and guide, not refuse and block).

## Can I Use Both?

Yes. Both are standard skill plugins. They will coexist without errors.

However, there will be overlap. When you say "debug this test failure," both superpowers:systematic-debugging and enggenie:dev-debug will match. The orchestrator will pick one based on description matching. The result is unpredictable and depends on which description better matches your phrasing.

**Recommendation:** Switch fully. Install enggenie, remove superpowers. enggenie covers everything superpowers does, plus PM, QA testing, design review, deployment, and cross-session memory. Running both adds ambiguity without adding capability.

If you want to transition gradually, you can keep both installed and invoke enggenie skills by name (e.g., "use enggenie:dev-debug") until you are comfortable, then uninstall superpowers.
