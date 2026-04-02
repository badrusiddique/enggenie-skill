# Getting Started with enggenie on Google Gemini CLI

## Prerequisites

- Gemini CLI installed ([github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli))
- A code project to work in
- Terminal access

## Step 1: Install enggenie

**Option A: Universal install (recommended)**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects Gemini CLI and installs all 13 skills. Skip to Step 2.

**Option B: Manual install**

Clone the repo and add a GEMINI.md reference:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git ~/.gemini/extensions/enggenie
```

Then add this to your project's `GEMINI.md`:

```markdown
## Skills
Use the skills in ~/.gemini/extensions/enggenie/skills/ for development workflows.
When a skill applies, read the SKILL.md file and follow its instructions.
For tool name mappings, see ~/.gemini/extensions/enggenie/references/gemini-tools.md
```

enggenie also ships a `gemini-extension.json` in the repo root for Gemini's extension discovery.

## Step 2: Verify Installation

Ask Gemini:

```
List all the enggenie skills in ~/.gemini/extensions/enggenie/skills/
```

**What you should see:** 13 skill directories, each with a SKILL.md file.

## Step 3: Tool Name Differences

Gemini CLI uses different tool names than Claude Code. enggenie includes a mapping reference at `references/gemini-tools.md`:

| Claude Code | Gemini CLI |
|------------|------------|
| `Read` | `read_file` |
| `Edit` | `edit_file` |
| `Write` | `write_file` |
| `Bash` | `shell` |
| `Grep` | `grep` |
| `Glob` | `glob` |

## Step 4: Try Your First Skill

```
I want to add a function that validates email addresses using TDD.
Read the skill at ~/.gemini/extensions/enggenie/skills/dev-tdd/SKILL.md and follow it.
```

## Step 5: Try More Skills

| What you want to do | Say this |
|---------------------|---------|
| Debug a test failure | "This test fails. Use the dev-debug skill." |
| Plan a feature | "I want to build X. Use the architect-design skill." |
| Create an implementation plan | "Create a plan. Use the architect-plan skill." |
| Review code | "Review my changes. Use the review-code skill." |
| Ship code | "Commit and create a PR. Use the deploy-ship skill." |

## Troubleshooting

**Gemini doesn't find the skills:**
- Verify: `ls ~/.gemini/extensions/enggenie/skills/`
- Check that `GEMINI.md` references the correct path

**Tool name errors:**
- Reference `references/gemini-tools.md` explicitly in your prompt

## What's Next?

- [All Skills Usage Examples](../skills/usage-examples.md) - Quick examples for every skill
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) - End-to-end workflow
