# Getting Started with enggenie on GitHub Copilot CLI

This guide walks you through setting up enggenie with GitHub Copilot CLI, verifying it works, and trying your first skills.

No prior experience with AI coding plugins is required.

> **Note:** GitHub Copilot's plugin and extension system is evolving. The steps below reflect general guidance. If they do not match your version, check [GitHub Copilot's documentation](https://docs.github.com/en/copilot) for the latest plugin installation method. Tool names differ from Claude Code - see [copilot-tools.md](../../references/copilot-tools.md) for the mapping.

---

## Prerequisites

- **GitHub Copilot CLI installed.** Follow GitHub's official setup instructions at [docs.github.com/en/copilot](https://docs.github.com/en/copilot).
- **An active GitHub Copilot subscription.** Free tier or paid - either works.
- **A code project to work in.** Any project with source code and tests is ideal.
- **Terminal access.** Copilot CLI runs in your terminal.

To confirm Copilot CLI is installed, run:

```bash
gh copilot --version
```

**What you should see:** A version number. If you see "command not found," install the GitHub CLI first (`gh`), then the Copilot extension.

---

## Step 1: Install enggenie

GitHub Copilot's plugin system may support loading skill definitions from a repository. The general approach:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git
```

Then configure Copilot to load the skill definitions from the cloned repository. Check GitHub Copilot's current documentation for the exact configuration method, as the plugin system is under active development.

> **Important:** The exact installation steps depend on your Copilot CLI version and GitHub's latest plugin specification. If the above does not work, check [docs.github.com/en/copilot](https://docs.github.com/en/copilot) for updated instructions on loading custom extensions.

**What you should see:** After configuration, the enggenie skills should be available when you interact with Copilot.

---

## Step 2: Verify Installation

Start a Copilot CLI session and ask:

```
What enggenie skills do I have?
```

**What you should see:** A list of 13 skills across 6 roles (PM, Architect, Developer, Reviewer, QA, Deploy) plus Memory and Meta. See [claude-code.md](claude-code.md) for the full list.

---

## Step 3: Try Your First Skill (enggenie:qa-verify)

In any project with tests, tell Copilot:

```
Run the tests and tell me if they pass
```

**What happens:**

1. The `enggenie:qa-verify` skill activates.
2. Copilot uses `runInTerminal` to execute your test suite.
3. You see real test output with pass/fail counts.

**What you should see:** Actual terminal output from your test runner, followed by a summary with evidence of what passed and what failed.

---

## Step 4: Try a Development Workflow (enggenie:dev-tdd)

Tell Copilot:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens:**

1. **RED:** Writes a failing test, runs it with `runInTerminal`, shows the failure.
2. **GREEN:** Writes the implementation, runs tests, shows them passing.
3. **REFACTOR:** Cleans up and confirms tests still pass.

**What you should see:** Three distinct phases, each with real test output.

---

## Step 5: Explore More Skills

| What you want to do | Say this | Skill that fires |
|---------------------|----------|------------------|
| Write a product spec | "Write a spec for user search" | `enggenie:pm-refine` |
| Create an implementation plan | "Create a plan from this spec" | `enggenie:architect-plan` |
| Add a feature with TDD | "Add a validate email function using TDD" | `enggenie:dev-tdd` |
| Debug a failing test | "This test is failing, help me fix it" | `enggenie:dev-debug` |
| Review code changes | "Review my changes" | `enggenie:review-code` |
| Verify tests with evidence | "Are the tests passing?" | `enggenie:qa-verify` |
| Create a PR | "Create a PR for this work" | `enggenie:deploy-ship` |

---

## Tool Name Differences

Copilot CLI uses different tool names than Claude Code. Key differences:

| Claude Code | Copilot CLI |
|-------------|-------------|
| `Read` | `readFile` |
| `Edit` | `editFile` |
| `Bash` | `runInTerminal` |
| `Grep` | `getFileTextSearch` |

See [copilot-tools.md](../../references/copilot-tools.md) for the complete mapping.

---

## What's Next?

- **[Examples](../examples/)** - Full walkthroughs of enggenie skills.
- **[Guides](../guides/)** - Deep dives on TDD, debugging, and planning workflows.
- **[copilot-tools.md](../../references/copilot-tools.md)** - Complete tool name mapping.
- **[Skill reference](../../README.md)** - Documentation for all 13 skills.
