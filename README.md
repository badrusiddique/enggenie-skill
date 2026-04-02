# enggenie - The Right Expert for the Right Moment

> Role-based SDLC skills for AI coding assistants.
> **PM** · **Architect** · **Dev** · **Reviewer** · **QA** · **Deploy**

**enggenie** gives your AI coding assistant expertise across the entire software development lifecycle - not just coding. Each skill is a domain expert that activates when you need it.

## What is a "skill"?

A skill is a set of instructions that makes your AI assistant behave like an expert in a specific area. When you say "debug this test failure," enggenie automatically activates its debugging skill - which enforces systematic root cause investigation instead of random guessing.

**You don't invoke skills manually.** They activate based on what you're doing.

## Install

```bash
# Claude Code (recommended)
claude plugin add --from github.com/badrusiddique/enggenie-skill

# Cursor
# Copy this repo to your Cursor plugins directory

# Other platforms - see Getting Started guides below
```

## What's Inside

| Role | Skill | What It Does | Example Trigger |
|------|-------|-------------|-----------------|
| **PM** | `enggenie:pm-refine` | Spec generation, story refinement, estimation | "Write a spec for user search" |
| **Architect** | `enggenie:architect-design` | Brainstorming, ADRs, technical decisions | "Let's brainstorm the caching approach" |
| **Architect** | `enggenie:architect-plan` | Implementation plans with deployment phases | "Create a plan from this spec" |
| **Dev** | `enggenie:dev-implement` | Subagent-driven TDD execution | "Execute the plan" |
| **Dev** | `enggenie:dev-tdd` | TDD discipline (RED-GREEN-REFACTOR) | "Add a validate email function" |
| **Dev** | `enggenie:dev-debug` | Systematic root cause investigation | "This test is failing" |
| **Reviewer** | `enggenie:review-code` | Request + receive code reviews | "Review my changes" |
| **Reviewer** | `enggenie:review-design` | Frontend/UI quality enforcement | "Check the dashboard against the design" |
| **QA** | `enggenie:qa-verify` | Evidence before completion claims | "Are the tests passing?" |
| **QA** | `enggenie:qa-test` | Playwright + manual browser testing | "Test the login flow as a QA engineer" |
| **Deploy** | `enggenie:deploy-ship` | Commit, PR, branch completion, Jira | "Create a PR for this work" |
| **Memory** | `enggenie:memory-recall` | Cross-session context (requires claude-mem) | "What did we do last session?" |

## Why enggenie?

### vs. no skills

AI assistants without skills skip tests, guess at bugs, claim "done" without evidence, and write code before designing. enggenie enforces discipline at every stage.

### vs. superpowers

[superpowers](https://github.com/obra/superpowers) covers coding (TDD, debugging, planning, code review). enggenie covers the **entire SDLC**:

| Capability | superpowers | enggenie |
|-----------|-------------|----------|
| TDD discipline | Yes | Yes |
| Systematic debugging | Yes | Yes |
| Implementation planning | Flat task lists | Phased plans with deployment gates |
| Code review | 2 separate skills | 1 unified skill |
| Verification | Yes | Yes |
| **Spec generation** | No | Yes - full specs with estimation |
| **QA testing** | No | Yes - Playwright + manual |
| **Design review** | No | Yes - accessibility, responsive, states |
| **Deployment/PR** | Basic branch completion | Commits, PRs, Jira updates |
| **Cross-session memory** | No | Yes - via claude-mem |
| **Brainstorming modes** | 1 rigid flow | 3 modes (brainstorm/architecture/discussion) |

Everything superpowers does, enggenie does. enggenie just does more.

[Full migration guide →](docs/guides/switching-from-superpowers.md)

## Getting Started

Pick your platform:

- **[Claude Code](docs/getting-started/claude-code.md)** - Full guide with examples
- **[Cursor](docs/getting-started/cursor.md)** - Full guide with examples
- **[GitHub Copilot CLI](docs/getting-started/copilot-cli.md)** - Full guide with examples
- **[Google Gemini CLI](docs/getting-started/gemini-cli.md)** - Full guide with examples
- **[OpenCode.ai](docs/getting-started/opencode.md)** - Full guide with examples

### Quick Start (Claude Code)

```bash
# 1. Install
claude plugin add --from github.com/badrusiddique/enggenie-skill

# 2. Open any project
cd your-project

# 3. Start coding - skills activate automatically
# Try: "Add a function that validates email addresses"
# enggenie:dev-tdd will enforce RED-GREEN-REFACTOR

# Try: "This test is failing, help me fix it"
# enggenie:dev-debug will enforce systematic investigation
```

## Examples

- [Full Feature Walkthrough](docs/examples/full-feature-walkthrough.md) - Idea → spec → plan → code → test → ship
- [Debugging Session](docs/examples/debug-session.md) - Systematic root cause investigation
- [Code Review Session](docs/examples/code-review-session.md) - Requesting and receiving reviews
- [QA Testing Session](docs/examples/qa-testing-session.md) - Playwright + manual testing

## For Teams

enggenie is customizable per team:

- **Spec templates** - Override the default with your team's format
- **Commit format** - Conventional commits, emoji prefixes, Jira ticket references
- **Estimation method** - Fibonacci, T-shirt sizing, or linear
- **Architecture context** - Describe your system in CLAUDE.md

See [Team Setup Guide](docs/guides/team-setup.md).

## How It Works

enggenie uses a **role-based architecture**. Each skill is an expert in one part of the SDLC:

```
PM (enggenie:pm-refine)
  ↓ spec
Architect (enggenie:architect-design → enggenie:architect-plan)
  ↓ plan
Dev (enggenie:dev-implement + enggenie:dev-tdd)
  ↓ code
Reviewer (enggenie:review-code + enggenie:review-design)
  ↓ reviewed code
QA (enggenie:qa-verify + enggenie:qa-test)
  ↓ verified
Deploy (enggenie:deploy-ship)
  ↓ shipped

Debug (enggenie:dev-debug) - interrupts any stage when something breaks
Memory (enggenie:memory-recall) - available to all stages
```

Skills consume each other's outputs: the plan inherits phases from the spec, the implementation follows the plan, verification checks the acceptance criteria. Each handoff is explicit.

See [How It Works](docs/guides/how-it-works.md) for the full architecture.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome contributions - especially new reference docs, platform adapters, and bug reports.

## License

[MIT](LICENSE)

## Credits

Created by [Badru Siddique](https://github.com/badrusiddique). Inspired by the discipline of [superpowers](https://github.com/obra/superpowers) and the philosophy that engineers deserve expert assistance at every stage of their work, not just coding.
