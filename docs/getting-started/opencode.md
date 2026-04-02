# Getting Started with enggenie on OpenCode.ai

This guide walks you through setting up enggenie with OpenCode.ai, verifying it works, and trying your first skills.

No prior experience with AI coding plugins is required.

> **Note:** OpenCode's plugin system is evolving. The steps below reflect general guidance. If they do not match your version, check [OpenCode's documentation](https://opencode.ai) for the latest plugin installation method. Tool names differ slightly from Claude Code - see [opencode-tools.md](../../references/opencode-tools.md) for the mapping.

---

## Prerequisites

- **OpenCode installed.** Follow the setup instructions at [opencode.ai](https://opencode.ai).
- **A code project to work in.** Any project with tests is ideal.
- **Terminal access.**

To confirm OpenCode is installed, run:

```bash
opencode --version
```

**What you should see:** A version number. If you see "command not found," follow the installation instructions at the link above.

---

## Step 1: Install enggenie

Clone the enggenie repository:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git
```

Then configure OpenCode to load the skill definitions from the cloned repository. This typically involves adding the plugin path to your OpenCode configuration file.

> **Important:** The exact installation steps depend on your OpenCode version. The plugin system is under active development. Check [opencode.ai](https://opencode.ai) for the latest instructions on loading custom plugins.

**What you should see:** After configuration, the enggenie skills should be available in your OpenCode sessions.

---

## Step 2: Verify Installation

Start an OpenCode session and ask:

```
What enggenie skills do I have?
```

**What you should see:** A list of 13 skills across 6 roles (PM, Architect, Developer, Reviewer, QA, Deploy) plus Memory and Meta. See [claude-code.md](claude-code.md) for the full list.

---

## Step 3: Try Your First Skill (enggenie:qa-verify)

In any project with tests, tell OpenCode:

```
Run the tests and tell me if they pass
```

**What happens:**

1. The `enggenie:qa-verify` skill activates.
2. OpenCode uses `bash` to execute your test suite.
3. You see real test output with pass/fail counts.

**What you should see:** Actual terminal output from your test runner, not guesses. Evidence of what passed and what failed.

---

## Step 4: Try a Development Workflow (enggenie:dev-tdd)

Tell OpenCode:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens:**

1. **RED:** Writes a failing test, runs it with `bash`, shows the failure.
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

OpenCode tool names closely mirror Claude Code but use lowercase. Key differences:

| Claude Code | OpenCode |
|-------------|----------|
| `Read` | `read` |
| `Edit` | `edit` |
| `Bash` | `bash` |
| `Grep` | `grep` |

See [opencode-tools.md](../../references/opencode-tools.md) for the complete mapping.

---

## What's Next?

- **[Examples](../examples/)** - Full walkthroughs of enggenie skills.
- **[Guides](../guides/)** - Deep dives on TDD, debugging, and planning workflows.
- **[opencode-tools.md](../../references/opencode-tools.md)** - Complete tool name mapping.
- **[Skill reference](../../README.md)** - Documentation for all 13 skills.
