---
name: deploy-ship
description: Use when committing, pushing, creating PRs, or completing branches - conventional commits, PR creation, Jira updates, worktree cleanup
---

# Deploy and Ship

**Announce:** "I'm using enggenie:deploy-ship to [commit/create PR/complete branch]."

## The Last Mile

Code is verified. Tests pass. Now ship it cleanly. This skill handles commits, PRs, Jira updates, and branch completion - the final steps before the next story begins.

---

## 1. Commit

### Analyze Staged Changes

Run `git diff --staged` and read the full output. Understand what changed and why before proposing a message.

### Propose a Conventional Commit Message

Format:
```
<type>: <description>

[optional body - explain WHY, not what]
```

**Types:**
| Type | When |
|------|------|
| feat | New capability for the user |
| fix | Bug fix |
| refactor | Code restructure, no behavior change |
| docs | Documentation only |
| test | Adding or updating tests only |
| perf | Performance improvement |
| style | Formatting, whitespace, linting (no logic change) |
| chore | Build, config, tooling, dependencies |

**Rules:**
- Present tense: "add search endpoint", not "added search endpoint"
- Subject line under 72 characters
- Body explains WHY, not just what changed
- One logical change per commit - if the diff spans unrelated concerns, suggest splitting

### Wait for Confirmation

Present the proposed message to the user. NEVER auto-commit. The user confirms, edits, or rejects.

```
Proposed commit:
  feat: add pagination to search results

  Unbounded result sets cause timeouts on datasets over 10k rows.
  Default page size of 50 with cursor-based navigation.

Proceed? [y/edit/n]
```

---

## 2. Push and Create PR

### Push

Push the branch with tracking:
```
git push -u origin <branch-name>
```

### Create PR

Use `gh pr create` with this structure:

```markdown
## Summary
- [2-3 bullets describing what shipped, drawn from spec/plan]

## Test Plan
- [From qa-verify/qa-test results - actual evidence, not aspirations]

## Spec
- [Link to spec if one exists, omit section if none]

## Jira
- [Link to Jira ticket if available, omit section if none]
```

Keep the PR title short (under 70 characters), present tense, and descriptive. The title is not a commit message - it should communicate the change to reviewers scanning a list.

---

## 3. Jira Update and Dev Handoff to QA

If Jira MCP tools are available:
- Transition the ticket status (e.g., In Progress → In Review)
- Add a structured comment with the Dev handoff context for QA:

```markdown
## Dev Handoff
- PR: [GitHub PR link]
- What was built: [2-3 bullet summary of what shipped vs what was planned]
- Spec deviations: [anything that changed from the original spec, or "None — built as specified"]
- Known limitations: [anything not covered, deferred, or working differently than spec — or "None"]
- Test coverage:
  - Unit tests: [count] tests added/modified
  - Integration tests: [count if applicable]
  - Manual testing done: [brief summary of what Dev verified]
- For QA:
  - Test against: [spec file path]
  - Focus areas: [top 3 areas that need QA attention — e.g., "timer behavior at exactly 0, expired heist state, page refresh during countdown"]
  - Environment notes: [anything QA needs to know — env vars, feature flags, test data setup]
```

This comment is the handoff to QA. A QA engineer picking up this ticket — with no knowledge of what the Dev did — reads this comment and knows exactly what to test, where to focus, and what the Dev already verified.

If Jira MCP tools are NOT available:
- Skip gracefully. Output the handoff context so the user can paste it into Jira manually.
- Do not error. Do not block the flow.

```
Jira MCP not available - update PROJ-1234 status to "In Review" manually.
PR link: https://github.com/org/repo/pull/42
[paste the Dev Handoff block above into the ticket as a comment]
```

---

## 4. Branch Completion

### Pre-check: Tests Must Pass

Run the test suite. If tests fail, STOP. Do not offer completion options until tests are green. Direct the user back to enggenie:qa-verify.

### Present Exactly 4 Options

```
Branch is ready. Choose a completion path:

  1. Merge locally to base branch
  2. Push and create PR
  3. Keep branch as-is
  4. Discard work (requires typing "discard" to confirm)
```

No other options. No hybrid paths. One choice, one outcome.

### Execute the Choice

**Option 1 - Merge locally:**
```
git checkout <base-branch>
git merge <feature-branch>
```
After merging, run the full test suite on the merged result. If tests fail, abort and report the merge conflict.

Then cleanup worktree (see section 5).

**Option 2 - Push and create PR:**
Follow section 2 (Push and Create PR) above.
Worktree is preserved until PR is merged.

**Option 3 - Keep as-is:**
Do nothing. Branch and worktree remain untouched.

**Option 4 - Discard:**
Require the user to type "discard" - not "y", not "yes", not enter.
```
This will delete the branch and all uncommitted work. Type "discard" to confirm:
```
Then remove the branch and cleanup worktree (see section 5).

---

## 5. Worktree Cleanup

### Check if Working in a Worktree

```
git worktree list
```

If the current directory is a worktree (not the main working tree), cleanup applies.

### Cleanup Rules

| Completion Option | Remove Worktree? |
|-------------------|-----------------|
| 1. Merge locally | Yes |
| 2. Create PR | No - keep until PR merges |
| 3. Keep as-is | No |
| 4. Discard | Yes |

### Cleanup Steps (when applicable)

```
# Navigate out of the worktree first
cd <main-working-tree>

# Remove the worktree
git worktree remove <worktree-path>

# Optionally delete the branch (for discard only)
git branch -D <feature-branch>
```

Never remove a worktree while standing inside it.

---

## 6. Team Extensibility

These behaviors are OFF by default. Teams enable them via CLAUDE.md project configuration.

| Setting | Example | Default |
|---------|---------|---------|
| Emoji prefix | `✨ feat: add search` | Off |
| Jira ticket in subject | `[PROJ-1234] feat: add search` | Off |
| Conventional Commits strict mode | Reject non-conforming messages | Off |
| Co-authored-by tag | `Co-authored-by: AI Assistant <team@example.com>` | Off |

To enable, add to your project's CLAUDE.md:
```markdown
## Commit Conventions
- emoji_prefix: true
- jira_in_subject: true
- conventional_commits_strict: true
- co_authored_by: true
```

The skill reads these settings and applies them to the commit message proposal. The user still confirms before anything is committed.

---

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup |
|--------|-------|------|---------------|---------|
| 1. Merge locally | Yes | No | No | Yes |
| 2. Create PR | No | Yes | Yes | No |
| 3. Keep as-is | No | No | Yes | No |
| 4. Discard | No | No | No | Yes |

---

## Recommended Model

**Primary:** haiku
**Why:** Commits, PRs, and branch operations are straightforward. Haiku handles conventional commit formatting and PR descriptions efficiently.

Override: Use sonnet for complex multi-service deployments with phased rollout.

This is a recommendation. Ask the user: "Confirm model selection or override?" Do not proceed until the user responds.

---

## Jira Fallback

If no Jira ticket is referenced in the current conversation when creating a PR, ask:

> "Is there a Jira ticket for this work? I can read it to write a better PR summary and update the ticket status."

If the user provides one:
1. Read the ticket using MCP tools — get the spec summary for the PR description
2. Use the acceptance criteria to write a more specific test plan section in the PR
3. Transition the ticket status and add the Dev Handoff comment (Section 3)

If Jira MCP is not available, just use the ticket ID for the PR Jira section. This is a soft fallback — if the user says no, proceed with the PR using git context alone.

---

## Entry Condition

After verification (enggenie:qa-verify) or QA (enggenie:qa-test). Code is proven correct before this skill activates.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Auto-committing without user confirmation | ALWAYS present the commit message and wait for approval |
| Pushing to wrong remote branch | Verify remote and branch name before pushing |
| Creating PR against wrong base branch | Detect base branch from git config or ask explicitly |
| Skipping test verification before PR | Run full test suite. No exceptions. |
| Force-pushing without warning | NEVER force-push. If needed, explain why and get explicit permission |
| Committing .env or credential files | Check staged files for secrets before committing |
| Generic commit messages ("fix stuff") | Follow conventional commit format with WHY, not just what |

---

## Exit Action

Shipped. Worktree cleaned. Jira updated. The story is done. Next story begins.
