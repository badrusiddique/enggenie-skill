---
name: dev-commit
description: Use when creating commit messages - analyzes git diffs, proposes conventional commit messages with appropriate type and emoji, and waits for user approval before committing
---

# enggenie:dev-commit

**Announce:** "I'm using enggenie:dev-commit to create a commit message."

## Overview

Analyze staged changes and propose a well-crafted commit message. The message explains WHY something changed, not just what changed. Every commit gets user approval before it lands.

---

## Step 1: Analyze Staged Changes

Run these commands to understand what is being committed:

```bash
git status
git diff --staged
```

Read the full diff output. Understand:
- Which files changed and why
- Whether the changes are a new feature, bug fix, refactoring, documentation, test, or performance improvement
- The relationship between changed files (are they part of one logical change?)

If nothing is staged, tell the user: "No changes are staged. Stage your changes with `git add` first."

---

## Step 2: Propose Commit Message

### Commit Types with Emojis

Only use the following types:

| Emoji | Type | When to use |
|-------|------|------------|
| ✨ | `feat:` | New feature or capability |
| 🐛 | `fix:` | Bug fix |
| 🔨 | `refactor:` | Code restructuring without behavior change |
| 📝 | `docs:` | Documentation only |
| 🎨 | `style:` | Formatting, whitespace, linting (no logic change) |
| ✅ | `test:` | Adding or updating tests |
| ⚡ | `perf:` | Performance improvement |

### Format

```
<emoji> <type>: <concise_description>

<optional_body_explaining_why>
```

### Rules

- **Present tense.** "add feature" not "added feature"
- **Explain why, not what.** The diff shows what changed. The message explains the motivation.
- **Subject line under 72 characters.**
- **One logical change per commit.** If staged changes cover multiple unrelated things, suggest splitting them.
- **No co-authored-by tags.** The commit should look human.
- **No AI attribution.** Do not add any mention of AI assistance.

---

## Step 3: Present and Confirm

Show the user:

1. **Summary of staged changes** - brief overview of what is staged
2. **Proposed commit message** - the full message with emoji, type, and body
3. **Ask for confirmation** - "Commit with this message? (yes/edit/cancel)"

**NEVER auto-commit.** Wait for explicit user approval.

If the user wants to edit, incorporate their changes and re-present. If they cancel, do nothing.

---

## Step 4: Commit

Only after user confirms:

```bash
git commit -m "<approved message>"
```

Report the result: commit hash, branch, and files committed.

---

## Hard Rules

1. **Never commit without user approval.** Present the message, wait for "yes."
2. **Never add co-authored-by or AI attribution.** Commits must look human-written.
3. **Never commit unstaged changes.** Only commit what is in the staging area.
4. **Never commit secrets.** Check staged files for .env, credentials, API keys, tokens. Warn the user if detected.

---

## Gut Check

- Are you about to auto-commit? Stop. Show the message first.
- Does the subject line exceed 72 characters? Shorten it.
- Does the message say "what" but not "why"? Add the motivation.
- Are there .env files or credentials staged? Warn immediately.
- Are the staged changes one logical unit? If not, suggest splitting.

---

## Recommended Model

**Primary:** haiku
**Why:** Commit message generation is a lightweight task. Haiku is fast and sufficient.

Override: Use sonnet for complex commits spanning many files where understanding relationships matters.

---

## Entry Condition

None - can be invoked anytime there are staged changes.

## Exit Action

Commit created (or cancelled). Resume previous workflow.
