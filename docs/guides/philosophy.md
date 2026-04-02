# The Right Expert for the Right Moment

enggenie's design philosophy in one sentence: **every skill is a domain expert that activates when you need it and stays silent when you don't.**

## Role-Based Architecture

Traditional AI coding tools give you one generalist. enggenie gives you a team of specialists.

Each skill maps to a role in the software development lifecycle:

| Role | Skills | Domain |
|------|--------|--------|
| PM | pm-refine | Specs, stories, estimation |
| Architect | architect-design, architect-plan | Design decisions, phased plans |
| Dev | dev-implement, dev-tdd, dev-debug | Execution, TDD discipline, debugging |
| Reviewer | review-code, review-design | Code quality, UI/UX compliance |
| QA | qa-verify, qa-test | Verification, Playwright and manual testing |
| Deploy | deploy-ship | Commits, PRs, Jira, branch completion |
| Memory | memory-recall | Cross-session context |

When you say "write a spec," you get the PM. When you say "this test is failing," you get the debugger. When you say "create a PR," you get the deploy engineer. Each one brings domain-specific discipline, enforcement, and output formats.

## Skills Stay Out of Your Way

Not everything needs a skill. Quick questions, simple edits, file exploration, and git queries bypass the suite entirely. The gateway skill explicitly defines what is not its business.

There is no overhead when you do not need it. The suite is activated by intent, not by presence. Installing enggenie does not change how your assistant handles "what does this function do?" -- it changes how it handles "debug this test failure."

## Softer Enforcement: Inform, Don't Block

enggenie informs and guides. It does not refuse to work.

If a user's CLAUDE.md says "don't use TDD," enggenie follows the user's instructions. The instruction priority is explicit:

1. User's instructions (CLAUDE.md, project config, direct requests) -- highest
2. enggenie skills -- override default system behavior where they conflict
3. Default system prompt -- lowest

This is intentional. A skill suite that overrides the engineer is a liability. A skill suite that makes the engineer better is an asset.

## Original Enforcement Language

enggenie uses its own terminology, distinct from other skill frameworks:

- **Hard Rules** -- Non-negotiable constraints. "No production code without a failing test first." These exist because specific agent failure modes are well-documented and repeatable. A Hard Rule closes a known loophole.

- **Shortcut Tax** -- A table showing what each common shortcut actually costs. Not "don't do this" -- instead, "here is the concrete price you pay." Examples: "I'll write tests after" costs you tests that prove nothing because they pass immediately. "Too simple to test" costs you 30 minutes debugging in production to save 30 seconds writing a test.

- **Gut Check** -- A list of red flags that signal you are about to make a mistake. "STOP and reassess if you notice yourself changing code without a hypothesis." These are not rules -- they are pattern-matched warnings.

## Skills Consume Each Other's Outputs

The suite is not 14 isolated tools. It is a pipeline:

```
pm-refine produces a spec
  architect-design produces an approved design
    architect-plan produces a phased implementation plan
      dev-implement executes the plan task by task
        review-code and review-design validate quality
          qa-verify and qa-test confirm correctness
            deploy-ship commits, creates PRs, updates Jira
```

Each handoff is explicit. The plan inherits phases from the spec. The implementation follows the plan. The QA test plan maps to acceptance criteria from the spec. Verification checks the acceptance criteria before claiming completion. Nothing is implicit or assumed.

Memory (memory-recall) is available to all stages -- "have we built something similar?" -- and degrades gracefully when not installed.

## Team Extensibility

enggenie is configurable, not opinionated about team process:

- **Spec templates** -- Teams override the default by placing their own at `docs/enggenie/templates/spec-template.md` in their repo.
- **Commit format** -- Conventional commits by default. Teams configure emoji prefixes, Jira ticket references, strict mode, and co-authored-by tags in CLAUDE.md.
- **Estimation method** -- Fibonacci (default), T-shirt sizing, or linear scale. Configured per project.
- **Architecture context** -- Described in CLAUDE.md so skills understand the service topology without re-discovering it every session.
- **Jira project key** -- Configured once, used by pm-refine and deploy-ship.

The goal: a team installs enggenie, adds a few lines to CLAUDE.md, and the suite adapts to their workflow. No forking. No custom builds.
