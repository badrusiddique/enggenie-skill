# Getting Started with enggenie on Cursor

## Prerequisites

- Cursor IDE installed ([cursor.com](https://cursor.com))
- [Node.js](https://nodejs.org) 18+ installed (for Option A)
- A code project open in Cursor
- Terminal access

## Step 1: Install enggenie

**Option A: Universal install (recommended)**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects Cursor and installs all 14 skills. Skip to Step 2. (`npx` comes with Node.js. The `skills` CLI is from [skillkit.sh](https://www.skillkit.sh/).)

**Option B: Manual install**

Clone the repo and add a rules reference:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git ~/.cursor/skills/enggenie
```

Then add this to your project's `.cursor/rules/enggenie.mdc` file (or `.cursorrules` if using an older Cursor version):

```
Use the skills in ~/.cursor/skills/enggenie/skills/ for development workflows.
When a skill applies, read the SKILL.md file and follow its instructions.
For tool name mappings, see ~/.cursor/skills/enggenie/references/cursor-tools.md
```

## Step 2: Verify Installation

In Cursor's chat, type:

```
What enggenie skills do I have? Check ~/.cursor/skills/enggenie/skills/
```

**What you should see:** A list of 14 skill directories, each containing a SKILL.md file.

## Step 3: Tool Name Differences

Cursor uses different tool names than Claude Code. enggenie includes a mapping reference at `references/cursor-tools.md`:

| Claude Code | Cursor |
|------------|--------|
| `Read` | `read_file` |
| `Edit` | `edit_file` |
| `Write` | `write_file` |
| `Bash` | `run_command` |
| `Grep` | `search` |
| `Glob` | `find_files` |

The skills reference Claude Code tools by default. Cursor's agent will automatically translate these when it reads the mapping reference.

## Step 4: Try Your First Skill

In Cursor's chat, type:

```
I want to add a function that validates email addresses. Use TDD.
Read ~/.cursor/skills/enggenie/skills/dev-tdd/SKILL.md and follow it.
```

**What happens:**
1. Cursor reads the TDD skill
2. Writes a failing test FIRST
3. Shows the failure
4. Writes minimal code to pass
5. Refactors if needed

## Step 5: Try More Skills

| What you want to do | Say this |
|---------------------|---------|
| Debug a test failure | "This test fails. Read the dev-debug skill and follow it." |
| Plan a feature | "I want to build X. Read the architect-design skill and follow it." |
| Review code | "Review my changes. Read the review-code skill and follow it." |

**Tip:** After a few uses, Cursor learns to check for applicable skills automatically via your rules file.

## Step 6: Customize for Your Team (Optional)

Add to your project's `.cursor/rules/enggenie.mdc` (or `.cursorrules`):

```
## enggenie Configuration
- Spec template: docs/templates/our-spec-template.md
- Commit format: [JIRA-123] type: description
- Estimation method: T-shirt (S/M/L/XL)
```

## Troubleshooting

**Cursor doesn't find the skills:**
- Verify the clone path: `ls ~/.cursor/skills/enggenie/skills/`
- Make sure `.cursor/rules/enggenie.mdc` (or `.cursorrules`) points to the correct path

**Skills reference wrong tool names:**
- Cursor auto-translates most tool names. If not, reference `references/cursor-tools.md` explicitly.

## What's Next?

- [All Skills Usage Examples](../skills/usage-examples.md) - Quick examples for every skill
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) - End-to-end workflow
