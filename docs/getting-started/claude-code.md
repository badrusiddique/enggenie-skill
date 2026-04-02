# Getting Started with enggenie on Claude Code

## Prerequisites

- Claude Code installed ([install guide](https://docs.anthropic.com/en/docs/claude-code))
- [Node.js](https://nodejs.org) installed (for the `npx` installer in Option A)
- A code project to work in (any language)
- Terminal access

## Step 1: Install enggenie

**Option A: Universal install (recommended)**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects Claude Code and installs all 14 skills.

**Option B: Native plugin system**

Run these commands inside Claude Code:

```
/plugin marketplace add badrusiddique/enggenie-skill
/plugin install enggenie@badrusiddique-enggenie-skill
/reload-plugins
```

**What you should see:**

```
Installed 14 skills
```

**If you see an error:**
- "Marketplace not found" - check the repo name is exactly `badrusiddique/enggenie-skill`
- "Plugin not found" - make sure you added the marketplace first
- "Already installed" - you're good, just run `/reload-plugins`

## Step 2: Verify Installation

In Claude Code, type:

```
What enggenie skills do I have?
```

**What you should see:** A list of 14 skills grouped by role:
- PM: `enggenie:pm-refine`
- Architect: `enggenie:architect-design`, `enggenie:architect-plan`
- Dev: `enggenie:dev-implement`, `enggenie:dev-tdd`, `enggenie:dev-debug`, `enggenie:dev-commit`
- Reviewer: `enggenie:review-code`, `enggenie:review-design`
- QA: `enggenie:qa-verify`, `enggenie:qa-test`
- Deploy: `enggenie:deploy-ship`
- Memory: `enggenie:memory-recall`

## Step 3: Try Your First Skill

Open any project with tests and type:

```
Run the tests and tell me if they pass
```

**What happens:**
1. `enggenie:qa-verify` activates automatically (you'll see "I'm using enggenie:qa-verify...")
2. It runs your test command
3. Instead of saying "tests should pass," it shows you evidence:

```
47/47 tests pass, exit code 0. All tests passing.
```

**Why this matters:** Without enggenie, AI assistants often say "the tests should pass" without running them. `enggenie:qa-verify` enforces evidence before claims.

## Step 4: Try TDD

Tell Claude Code:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens:**
1. `enggenie:dev-tdd` activates
2. Writes a failing test FIRST (RED phase)
3. Shows you the test failure output
4. Writes minimal code to make the test pass (GREEN phase)
5. Refactors if needed (REFACTOR phase)
6. Shows evidence that all tests pass

## Step 5: Try Debugging

If you have a failing test, try:

```
This test is failing, help me fix it
```

**What happens:**
1. `enggenie:dev-debug` activates
2. Phase 1: Investigates - reads errors, checks recent changes
3. Phase 2: Finds the pattern - compares working vs broken code
4. Phase 3: Tests one hypothesis at a time
5. Phase 4: Fixes with a regression test

It will NEVER guess. It investigates systematically.

## Step 6: Explore More Skills

| What you want to do | Say this | Skill that fires |
|---------------------|---------|-----------------|
| Plan a new feature | "I want to build a user dashboard" | `enggenie:architect-design` |
| Create an implementation plan | "Create a plan for the dashboard" | `enggenie:architect-plan` |
| Write a full spec | "Write a spec for the search feature" | `enggenie:pm-refine` |
| Execute a plan | "Execute the plan" | `enggenie:dev-implement` |
| Review code before PR | "Review my changes before I push" | `enggenie:review-code` |
| Ship your code | "Commit and create a PR" | `enggenie:deploy-ship` |
| Test like QA | "Test the login flow as a QA engineer" | `enggenie:qa-test` |

## Step 7: Customize for Your Team (Optional)

Add to your project's `CLAUDE.md`:

```markdown
## enggenie Configuration
- Spec template: docs/templates/our-spec-template.md
- Commit format: [JIRA-123] type: description
- Estimation method: T-shirt (S/M/L/XL)
```

See [Team Setup Guide](../guides/team-setup.md) for all configuration options.

## Troubleshooting

**Skills not activating:**
- Run `/reload-plugins` to refresh
- Check that the plugin is listed with `/plugin list`

**Wrong skill fires:**
- You can invoke a specific skill: "Use enggenie:dev-debug to investigate this"

**Want to see all available skills:**
- Type: "List all enggenie skills"

## What's Next?

- [All Skills Usage Examples](../skills/usage-examples.md) - Quick examples for every skill
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) - Idea to spec to plan to code to ship
- [How It Works](../guides/how-it-works.md) - Architecture and skill interconnection
