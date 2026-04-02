# Getting Started with enggenie on Google Gemini CLI

This guide walks you through setting up enggenie with the Gemini CLI, verifying it works, and trying your first skills.

No prior experience with AI coding plugins is required.

> **Note:** Gemini CLI's extension system is evolving. The steps below reflect general guidance. If they do not match your version, check [Gemini CLI's documentation](https://github.com/google-gemini/gemini-cli) for the latest extension installation method. Tool names differ from Claude Code - see [gemini-tools.md](../../references/gemini-tools.md) for the mapping.

---

## Prerequisites

- **Gemini CLI installed.** Follow Google's setup instructions at the [Gemini CLI repository](https://github.com/google-gemini/gemini-cli).
- **A Google account with Gemini API access.**
- **A code project to work in.** Any project with tests is ideal.
- **Terminal access.**

To confirm Gemini CLI is installed, run:

```bash
gemini --version
```

**What you should see:** A version number. If you see "command not found," follow the installation instructions at the link above.

---

## Step 1: Install enggenie

Gemini CLI supports extensions configured via a JSON file. The enggenie repo includes a `gemini-extension.json` at its root.

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git
```

Then reference the extension configuration in your Gemini CLI setup. You may need to copy or symlink the `gemini-extension.json` file to your Gemini CLI extensions directory, or point your Gemini configuration to the cloned repo.

> **Important:** The exact installation steps depend on your Gemini CLI version. The extension system is under active development. Check [the Gemini CLI repo](https://github.com/google-gemini/gemini-cli) for the latest instructions on loading custom extensions.

**What you should see:** After configuration, the enggenie skills should be available in your Gemini CLI sessions.

---

## Step 2: Verify Installation

Start a Gemini CLI session and ask:

```
What enggenie skills do I have?
```

**What you should see:** A list of 13 skills across 6 roles (PM, Architect, Developer, Reviewer, QA, Deploy) plus Memory and Meta. See [claude-code.md](claude-code.md) for the full list.

---

## Step 3: Try Your First Skill (enggenie:qa-verify)

In any project with tests, tell Gemini:

```
Run the tests and tell me if they pass
```

**What happens:**

1. The `enggenie:qa-verify` skill activates.
2. Gemini uses `shell` to execute your test suite.
3. You see real test output with pass/fail counts.

**What you should see:** Actual terminal output from your test runner, not guesses. Evidence of what passed and what failed.

---

## Step 4: Try a Development Workflow (enggenie:dev-tdd)

Tell Gemini:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens:**

1. **RED:** Writes a failing test, runs it with `shell`, shows the failure.
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

Gemini CLI uses different tool names than Claude Code. Key differences:

| Claude Code | Gemini CLI |
|-------------|------------|
| `Read` | `read_file` |
| `Edit` | `edit_file` |
| `Bash` | `shell` |
| `Grep` | `grep` |

See [gemini-tools.md](../../references/gemini-tools.md) for the complete mapping and parameter differences.

---

## What's Next?

- **[Examples](../examples/)** - Full walkthroughs of enggenie skills.
- **[Guides](../guides/)** - Deep dives on TDD, debugging, and planning workflows.
- **[gemini-tools.md](../../references/gemini-tools.md)** - Complete tool name mapping.
- **[Skill reference](../../README.md)** - Documentation for all 13 skills.
