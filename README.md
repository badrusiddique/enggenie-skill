# enggenie - The Right Expert for the Right Moment

> Role-based skills for AI coding assistants across the entire software development lifecycle (SDLC). Your AI assistant becomes a PM, Architect, Developer, Code Reviewer, QA Engineer, and DevOps specialist - all in one plugin.

**What's a "skill"?** A skill is a set of instructions that teaches your AI coding assistant to behave like an expert in a specific area. Skills activate automatically based on what you're doing - you don't need to invoke them manually.

## Why enggenie?

Most AI coding tools only help with one thing: writing code. But software engineering is more than coding. You also need to:

- **Plan features** before building them
- **Design architecture** before coding
- **Write tests first** (not after)
- **Debug systematically** (not by guessing)
- **Review code** with technical rigor
- **Test like QA** (not like a developer)
- **Ship with confidence** (commits, PRs, deployment)

**enggenie makes your AI assistant an expert at ALL of these.** Each skill is a domain expert that activates automatically based on what you're doing.

## Highlights

- **14 skills** covering the entire software development lifecycle
- **7 expert roles** - PM, Architect, Dev, Reviewer, QA, Deploy, Memory
- **Model recommendations** - each skill suggests the optimal model (opus/sonnet/haiku) for best results
- **Zero configuration** - skills activate automatically based on your intent
- **Multi-platform** - works with Claude Code, Cursor, GitHub Copilot CLI, Google Gemini CLI, and OpenCode
- **Team customizable** - spec templates, commit format, estimation method, all configurable
- **TDD enforced** - never lets your AI skip writing tests first (TDD = Test-Driven Development: write the test before the code)
- **Evidence-based** - never claims "done" without running the tests and showing proof
- **Subagent-powered** - dispatches specialized AI sub-agents (smaller focused assistants) for implementation, review, and QA

## Install

**Prerequisites:** [Node.js](https://nodejs.org) (for the `npx` installer)

**Any platform (Claude Code, Cursor, Gemini CLI, Copilot, OpenCode, and more):**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects your installed AI coding tools and installs all 14 skills. The `skills` CLI is from [skillkit.sh](https://www.skillkit.sh/) (by Vercel).

**Claude Code only (native plugin system):**

```
/plugin marketplace add badrusiddique/enggenie-skill
/plugin install enggenie@badrusiddique-enggenie-skill
/reload-plugins
```

For platform-specific setup, see [Getting Started guides](#getting-started) below.

## What's Inside

| Role | Skill | What It Does | Try Saying... |
|------|-------|-------------|---------------|
| **PM** | `enggenie:pm-refine` | Generates specs, refines stories, estimates points | "Write a spec for user notifications" |
| **Architect** | `enggenie:architect-design` | Brainstorms approaches, writes architecture decision records | "What's the best caching strategy?" |
| **Architect** | `enggenie:architect-plan` | Creates phased implementation plans | "Create a plan from this spec" |
| **Dev** | `enggenie:dev-implement` | Executes plans with TDD subagents | "Execute the plan" |
| **Dev** | `enggenie:dev-tdd` | Enforces RED-GREEN-REFACTOR on every code change | "Add a validate email function" |
| **Dev** | `enggenie:dev-debug` | 4-phase systematic root cause investigation | "This test is failing, help me fix it" |
| **Reviewer** | `enggenie:review-code` | Dispatches code reviewer, handles PR feedback | "Review my changes before I push" |
| **Reviewer** | `enggenie:review-design` | Checks UI against design system, states, a11y | "Check the dashboard against our design" |
| **QA** | `enggenie:qa-verify` | Requires evidence before any completion claim | "Are the tests passing?" |
| **QA** | `enggenie:qa-test` | Playwright automation + manual browser testing | "Test the login flow as a QA engineer" |
| **Dev** | `enggenie:dev-commit` | Analyzes diffs, proposes conventional commit messages | "Create a commit message" |
| **Deploy** | `enggenie:deploy-ship` | Conventional commits, PR creation, Jira updates | "Create a PR for this work" |
| **Memory** | `enggenie:memory-recall` | Cross-session context with 10x token savings | "What did we work on last session?" |
| **Gateway** | `enggenie` | Routes to the right skill when intent is ambiguous | "Help me with this feature" |

## How It Works

Skills activate automatically. You don't invoke them manually.

```
You say: "I want to build a user dashboard"
enggenie:architect-design activates -> brainstorms approaches

You say: "Create a plan for the dashboard"
enggenie:architect-plan activates -> generates phased implementation plan

You say: "Execute the plan"
enggenie:dev-implement activates -> TDD with subagent review per task

You say: "Are tests passing?"
enggenie:qa-verify activates -> runs tests, shows evidence

You say: "Create a PR"
enggenie:deploy-ship activates -> commits, pushes, creates PR
```

Each skill knows what comes next. The PM hands off to the Architect. The Architect hands off to the Dev. The Dev hands off to QA. QA hands off to Deploy. It's a complete pipeline.

## What Makes enggenie Different

### Test-Driven Development (TDD) - Enforced, Not Optional
TDD means writing a test first, then writing the code to make it pass, then cleaning up. enggenie:dev-tdd ensures your AI follows this cycle (called RED-GREEN-REFACTOR) every time. No exceptions. If it catches itself writing code first, it deletes it and starts over.

### Evidence Before Claims
enggenie:qa-verify prevents your AI from saying "tests pass" without actually running them. Every claim requires proof: command output, exit codes, failure counts.

### Systematic Debugging - No Guessing
enggenie:dev-debug follows a 4-phase investigation: Investigate, Find Pattern, Test Hypothesis, Fix. After 3 failed fix attempts, it escalates as an architecture problem instead of thrashing.

### Full Spec-to-Ship Pipeline
Other tools help with coding. enggenie helps with the ENTIRE workflow:
1. **PM** writes the spec with estimation
2. **Architect** designs the approach and plans implementation
3. **Dev** builds it with TDD and subagent review
4. **Reviewer** checks code quality and design compliance
5. **QA** tests from the user's perspective
6. **Deploy** commits, creates PRs, updates Jira

### Phased Deployment
Multi-service features are broken into independently deployable phases. Each phase has a readiness checklist. No big-bang releases.

## Getting Started

Pick your platform:

- **[Claude Code](docs/getting-started/claude-code.md)** - Full setup guide with examples
- **[Cursor](docs/getting-started/cursor.md)** - Full setup guide
- **[GitHub Copilot CLI](docs/getting-started/copilot-cli.md)** - Full setup guide
- **[Google Gemini CLI](docs/getting-started/gemini-cli.md)** - Full setup guide
- **[OpenCode.ai](docs/getting-started/opencode.md)** - Full setup guide

### Quick Start

```bash
# 1. Install (works with any AI coding tool)
npx skills add badrusiddique/enggenie-skill

# 2. Open any project
cd your-project

# 3. Start working - skills activate automatically
# Try: "Add a function that validates email addresses"
# enggenie:dev-tdd will enforce RED-GREEN-REFACTOR

# Try: "This test is failing, help me fix it"
# enggenie:dev-debug will enforce systematic investigation
```

## Examples

See real-world walkthroughs of each skill in action:

- [Full Feature Walkthrough](docs/examples/full-feature-walkthrough.md) - Idea to spec to plan to code to test to ship
- [Debugging Session](docs/examples/debug-session.md) - Systematic root cause investigation
- [Code Review Session](docs/examples/code-review-session.md) - Requesting and receiving reviews
- [QA Testing Session](docs/examples/qa-testing-session.md) - Playwright + manual browser testing
- [All Skills Usage Examples](docs/skills/usage-examples.md) - Quick examples for every skill

## For Teams

enggenie adapts to your team's conventions:

- **Spec templates** - Use your team's format instead of the default
- **Commit format** - Conventional commits, emoji prefixes, Jira ticket references
- **Estimation method** - Fibonacci, T-shirt sizing, or linear
- **Architecture context** - Describe your system in CLAUDE.md

See [Team Setup Guide](docs/guides/team-setup.md).

**Want your team to use enggenie?** Share this one-liner:
```bash
npx skills add badrusiddique/enggenie-skill
```
It works with whatever AI coding tool they use. No configuration needed.

## Architecture

```
PM (enggenie:pm-refine)
  -> spec
Architect (enggenie:architect-design -> enggenie:architect-plan)
  -> plan
Dev (enggenie:dev-implement + enggenie:dev-tdd)
  -> code
Reviewer (enggenie:review-code + enggenie:review-design)
  -> reviewed code
QA (enggenie:qa-verify + enggenie:qa-test)
  -> verified
Deploy (enggenie:deploy-ship)
  -> shipped

Debug (enggenie:dev-debug) - interrupts any stage when something breaks
Memory (enggenie:memory-recall) - available at all stages
```

## Plugin Discovery

enggenie is listed on multiple plugin directories across platforms:

| Directory | Platforms | URL |
|-----------|----------|-----|
| skills.sh | All (18+ tools) | [skills.sh](https://skills.sh) |
| ClaudePluginHub | Claude Code | [claudepluginhub.com](https://www.claudepluginhub.com) |
| Gemini Extensions Gallery | Gemini CLI | [geminicli.com/extensions](https://geminicli.com/extensions/) |
| Cursor Marketplace | Cursor | [cursor.com/marketplace](https://cursor.com/marketplace) |
| SkillsMP | All | [skillsmp.com](https://skillsmp.com) |

See the [full plugin discovery guide](docs/guides/plugin-discovery.md) for all directories and submission details.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome contributions - especially new reference docs, platform adapters, and bug reports.

## License

[MIT](LICENSE)

---

Built by [Badru Siddique](https://github.com/badrusiddique).
