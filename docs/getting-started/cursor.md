# Getting Started with enggenie on Cursor IDE

This guide walks you through setting up enggenie in Cursor, verifying it works, and trying your first skills. Every step includes what you should see afterward.

No prior experience with AI coding plugins is required.

> **Note:** Cursor's plugin system is evolving. If the steps below do not match your version of Cursor, check [Cursor's documentation](https://docs.cursor.com) for the latest plugin installation method. Tool names in Cursor differ from Claude Code - see [cursor-tools.md](../../references/cursor-tools.md) for the mapping.

---

## Prerequisites

- **Cursor IDE installed.** Download from [cursor.com](https://cursor.com) if you do not have it.
- **A code project open in Cursor.** Any project with source code will work.
- **Cursor's AI features enabled.** You should be able to open the AI chat panel (Cmd+L on macOS, Ctrl+L on Windows/Linux).

To confirm Cursor is working with AI, open a project and press Cmd+L (or Ctrl+L). You should see an AI chat panel appear on the right side.

---

## Step 1: Install enggenie

Cursor supports loading plugin configurations from a `.cursor-plugin` directory in a repository. There are two ways to install:

**Option A: Clone the repo and reference it**

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git
```

Then in your Cursor settings, add the path to the cloned repo as a plugin source. Check Cursor's current documentation for the exact setting location, as this may vary by version.

**Option B: Copy the plugin directory into your project**

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git /tmp/enggenie
cp -r /tmp/enggenie/.cursor-plugin your-project/.cursor-plugin
cp -r /tmp/enggenie/skills your-project/.cursor-plugin/skills
```

> **Important:** The exact installation method depends on your Cursor version. Cursor's plugin system is under active development. If neither option above works, check [docs.cursor.com](https://docs.cursor.com) for the latest instructions on loading custom plugins.

**What you should see:** After restarting Cursor or reloading the window, the enggenie skills should be available in the AI chat panel.

**If you see nothing new:** Make sure you restarted Cursor after adding the plugin files. Some versions require a full restart.

---

## Step 2: Verify Installation

Open the AI chat panel in Cursor (Cmd+L or Ctrl+L) and type:

```
What enggenie skills do I have?
```

**What you should see:** A list of 13 skills organized by role (PM, Architect, Developer, Reviewer, QA, Deploy, Memory, Meta). See the [claude-code.md](claude-code.md) guide for the full list.

**If skills are missing:** Ensure the `.cursor-plugin` directory is in your project root and contains the plugin.json file and skills directory.

---

## Step 3: Try Your First Skill (enggenie:qa-verify)

In any project that has tests, type in the AI chat panel:

```
Run the tests and tell me if they pass
```

**What happens:**

1. The `enggenie:qa-verify` skill activates.
2. Cursor's AI runs your test suite using `run_command` (Cursor's equivalent of a shell command).
3. You see real test output - not guesses.

**What you should see:** Actual test runner output with pass/fail counts and specific failure details if any tests fail.

**Why this matters:** Without enggenie, AI assistants often claim tests pass without running them. This skill requires evidence.

---

## Step 4: Try a Development Workflow (enggenie:dev-tdd)

Type in the AI chat panel:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens:**

1. The `enggenie:dev-tdd` skill activates.
2. **RED:** Writes a failing test first, runs it, shows the failure.
3. **GREEN:** Writes code to pass the test, runs it, shows success.
4. **REFACTOR:** Cleans up if needed, confirms tests still pass.

**What you should see:** Three phases with test output at each stage, using Cursor's `run_command` tool to execute tests.

---

## Step 5: Explore More Skills

| What you want to do | Say this | Skill that fires |
|---------------------|----------|------------------|
| Write a product spec | "Write a spec for user search" | `enggenie:pm-refine` |
| Brainstorm a technical approach | "Let's brainstorm the caching approach" | `enggenie:architect-design` |
| Create an implementation plan | "Create a plan from this spec" | `enggenie:architect-plan` |
| Execute a plan | "Execute the plan" | `enggenie:dev-implement` |
| Add a feature with TDD | "Add a validate email function using TDD" | `enggenie:dev-tdd` |
| Debug a failing test | "This test is failing, help me fix it" | `enggenie:dev-debug` |
| Review code changes | "Review my changes" | `enggenie:review-code` |
| Verify tests with evidence | "Are the tests passing?" | `enggenie:qa-verify` |
| Create a PR | "Create a PR for this work" | `enggenie:deploy-ship` |

---

## Step 6: Customize for Your Team (Optional)

Add project-specific instructions to a configuration file at your project root. Cursor respects `.cursorrules` or similar configuration files. Add your testing commands, code standards, and project conventions there so enggenie skills follow your team's practices.

---

## Tool Name Differences

Cursor uses different tool names than Claude Code. If you are reading skill documentation that references Claude Code tools, see [cursor-tools.md](../../references/cursor-tools.md) for the mapping. Key differences:

| Claude Code | Cursor |
|-------------|--------|
| `Read` | `read_file` |
| `Edit` | `edit_file` |
| `Bash` | `run_command` |
| `Grep` | `search` |

---

## What's Next?

- **[Examples](../examples/)** - Full walkthroughs of enggenie skills.
- **[Guides](../guides/)** - Deep dives on TDD, debugging, and planning workflows.
- **[cursor-tools.md](../../references/cursor-tools.md)** - Complete tool name mapping for Cursor.
- **[Skill reference](../../README.md)** - Documentation for all 13 skills.
