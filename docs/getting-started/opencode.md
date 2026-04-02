# Getting Started with enggenie on OpenCode.ai

## Prerequisites

- OpenCode installed ([opencode.ai](https://opencode.ai))
- A code project to work in
- Terminal access

## Step 1: Install enggenie

**Option A: Universal install (recommended)**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects OpenCode and installs all 14 skills. Skip to Step 2.

**Option B: Manual install**

Clone the repo and add instructions:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git ~/.opencode/plugins/enggenie
```

Then add this to your project's `.opencode/instructions.md` (create it if it doesn't exist):

```markdown
## Skills
Use the skills in ~/.opencode/plugins/enggenie/skills/ for development workflows.
When a skill applies, read the SKILL.md file and follow its instructions.
For tool name mappings, see ~/.opencode/plugins/enggenie/references/opencode-tools.md
```

## Step 2: Verify Installation

Ask OpenCode:

```
List all the enggenie skills in ~/.opencode/plugins/enggenie/skills/
```

**What you should see:** 13 skill directories, each with a SKILL.md file.

## Step 3: Tool Name Differences

OpenCode uses similar but lowercase tool names. enggenie includes a mapping reference at `references/opencode-tools.md`:

| Claude Code | OpenCode |
|------------|----------|
| `Read` | `read` |
| `Edit` | `edit` |
| `Write` | `write` |
| `Bash` | `bash` |
| `Grep` | `grep` |
| `Glob` | `glob` |

OpenCode's tools closely mirror Claude Code, making enggenie skills work with minimal adaptation.

## Step 4: Try Your First Skill

```
I want to add a function that validates email addresses using TDD.
Read the skill at ~/.opencode/plugins/enggenie/skills/dev-tdd/SKILL.md and follow it.
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

**OpenCode doesn't find the skills:**
- Verify: `ls ~/.opencode/plugins/enggenie/skills/`
- Check that `.opencode/instructions.md` references the correct path

## What's Next?

- [All Skills Usage Examples](../skills/usage-examples.md) - Quick examples for every skill
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) - End-to-end workflow
