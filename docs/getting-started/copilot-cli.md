# Getting Started with enggenie on GitHub Copilot CLI

## Prerequisites

- GitHub Copilot CLI installed ([docs.github.com](https://docs.github.com/en/copilot/using-github-copilot/using-github-copilot-in-the-command-line))
- A code project to work in
- Terminal access

## Step 1: Install enggenie

**Option A: Universal install (recommended)**

```bash
npx skills add badrusiddique/enggenie-skill
```

This auto-detects Copilot CLI and installs all 13 skills. Skip to Step 2.

**Option B: Manual install**

Clone the repo and add instructions:

```bash
git clone https://github.com/badrusiddique/enggenie-skill.git ~/.copilot/skills/enggenie
```

Then add this to your project's `AGENTS.md` or `.github/copilot-instructions.md`:

```markdown
## Skills
Use the skills in ~/.copilot/skills/enggenie/skills/ for development workflows.
When a skill applies, read the SKILL.md file and follow its instructions.
For tool name mappings, see ~/.copilot/skills/enggenie/references/copilot-tools.md
```

## Step 2: Verify Installation

Ask Copilot:

```
List all the enggenie skills in ~/.copilot/skills/enggenie/skills/
```

**What you should see:** 13 skill directories (enggenie, pm-refine, architect-design, architect-plan, dev-implement, dev-tdd, dev-debug, review-code, review-design, qa-verify, qa-test, deploy-ship, memory-recall).

## Step 3: Tool Name Differences

Copilot CLI uses different tool names than Claude Code. enggenie includes a mapping reference at `references/copilot-tools.md`:

| Claude Code | Copilot CLI |
|------------|-------------|
| `Read` | `readFile` |
| `Edit` | `editFile` |
| `Write` | `createFile` |
| `Bash` | `runInTerminal` |
| `Grep` | `getFileTextSearch` |
| `Glob` | `getWorkspaceFiles` |

## Step 4: Try Your First Skill

```
I want to add a function that validates email addresses using TDD.
Read the skill at ~/.copilot/skills/enggenie/skills/dev-tdd/SKILL.md and follow it.
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

**Copilot doesn't find the skills:**
- Verify: `ls ~/.copilot/skills/enggenie/skills/`
- Make sure `AGENTS.md` or `.github/copilot-instructions.md` references the correct path

**Tool name errors:**
- Reference `references/copilot-tools.md` explicitly in your prompt

## What's Next?

- [All Skills Usage Examples](../skills/usage-examples.md) - Quick examples for every skill
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) - End-to-end workflow
