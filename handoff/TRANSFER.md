# TRANSFER - enggenie

Machine: macOS (Darwin 25.6.0), user badru.siddique. Facts below verified with real commands on Oct 6 2026 unless marked [UNCERTAIN]. No secret values are recorded; only names.

## REPOS

| Repo | URL | Local path | Branch | State |
|---|---|---|---|---|
| enggenie-skill (the project) | https://github.com/badrusiddique/enggenie-skill.git (https) | /Users/badru.siddique/magento/learning/enggenie-skill | main (only branch; no other worktrees; no stashes) | HEAD 4435dc7, 4 commits ahead of origin/main (4aaf247); untracked files |
| claude-pocket-heist-app (demo / test codebase named in the repo CLAUDE.md gate; Next.js + TypeScript + Firebase) | git@github.com:badrusiddique/claude-pocket-heist-app.git (ssh) | /Users/badru.siddique/magento/learning/claude-pocket-heist-app | currently test/skill-verification-v2 | modified tracked files .claude/settings.local.json and tool-use.json; many local claude/feature/* branches; feature/heist-countdown-timer checked out in another worktree. Not changed in the session. |

Unpushed work that exists ONLY on this machine (handle before transfer):
- Commits (oldest first): a85e036 "docs: overhaul README with scope, philosophy, WHY explanations, and team adoption guide" (2026-06-01), 8f5de95 "feat: project-first configuration for review-code, dev-commit, and qa-test", 2a057d6 "docs: add missing guides, GitHub templates, architecture overview, FAQ", 4435dc7 "feat: add SessionStart hook so enggenie takes priority over other skill suites" (all 2026-06-22).
- Untracked: docs/blog/enggenie-v3-medium-post.md, docs/blog/assets/ (carbon/, diagrams/, images/, render-diagrams.sh), docs/verification/ (2 files), .DS_Store files.
- Gitignored but locally useful: .agents/, .claude/, skills-lock.json (regenerable; see NEXT_STEPS section 2e).
- No tag for 3.1.x exists locally or remotely (latest v3.0.0).

Options (pick one; do NOT push without the user's explicit yes):
```bash
# A. publish (after user approval and NEXT_STEPS cleanup)
cd /Users/badru.siddique/magento/learning/enggenie-skill && git push origin main
# B. carry over without publishing - portable bundle + tarball of untracked files
cd /Users/badru.siddique/magento/learning/enggenie-skill
git bundle create ~/enggenie-unpushed.bundle origin/main..main
tar czf ~/enggenie-untracked.tgz docs/blog docs/verification
# C. simplest: copy the whole directory (includes .git, ignored mirrors, untracked docs)
rsync -a /Users/badru.siddique/magento/learning/enggenie-skill/ <new-machine>:/path/enggenie-skill/
```
Ready-to-run clone (new machine) for option A or after pushing:
```bash
mkdir -p ~/magento/learning && cd ~/magento/learning
git clone https://github.com/badrusiddique/enggenie-skill.git
git clone git@github.com:badrusiddique/claude-pocket-heist-app.git   # optional, needed only for the repo's release gate / demo
```
Restore from option B:
```bash
cd ~/magento/learning && git clone https://github.com/badrusiddique/enggenie-skill.git && cd enggenie-skill
git fetch ~/enggenie-unpushed.bundle main:refs/heads/from-bundle && git merge --ff-only from-bundle
tar xzf ~/enggenie-untracked.tgz
```

## ENVIRONMENT SETUP

| Tool | Version used (verified) | Install | Post-install |
|---|---|---|---|
| macOS shell | zsh | - | note: `grep -P "\xe2\x80\x94"` gave false negatives; use the python scan in CODE_REFERENCE.md section 15; zsh errors on unquoted globs after `--include=*.md`, use `bash -c` |
| git | 2.46.0 | `brew install git` | `git config user.name` = Badru, user.email set to a personal address (not recorded here) in this repo |
| GitHub CLI gh | 2.58.0 | `brew install gh` | `gh auth login` (HTTPS, keyring). Verified logged in as badrusiddique; token scopes: gist, read:org, repo, workflow. Needed for `gh release create`, `gh repo edit`, `gh api` |
| Node / npm / npx | v25.6.1 / 11.9.0 / 11.9.0 | `brew install node` | needed for `npx skills add badrusiddique/enggenie-skill` and `npx @mermaid-js/mermaid-cli` (render diagrams) |
| Python | 3.14.6 | `brew install python` | used only for ad-hoc scans |
| Claude Code | 2.1.286 | https://docs.anthropic.com/en/docs/claude-code | sign in; see CLAUDE CODE SPECIFIC |
| mmdc (mermaid-cli) | NOT installed | not needed; script uses `npx --yes @mermaid-js/mermaid-cli` | - |
| imagemagick (convert), asciinema, ffmpeg, agg | NOT installed | optional for GIFs: `brew install asciinema agg ffmpeg` | Carbon images are made in the browser (carbon.now.sh), no install |
| Browser | any | - | carbon.now.sh for the 6 terminal images; Medium and LinkedIn for publishing (user's own accounts) |

The repo itself has no build step, no package.json, no tests; nothing to install for the content.

## ENVIRONMENT VARIABLES AND CONFIG

Names only, no values.
- CLAUDE_PLUGIN_ROOT - set by Claude Code when it runs a plugin hook; read by hooks/session-start to choose the Claude Code JSON format. Source: Claude Code at runtime. Manual setup: none (for a manual test, set it to the repo path).
- COPILOT_CLI_PLUGIN_ROOT - read by hooks/session-start (if set, Claude Code format is not used). Source: GitHub Copilot CLI at runtime [UNCERTAIN whether it exists].
- CURSOR_PLUGIN_ROOT - read by hooks/session-start for the Cursor JSON format. Source: Cursor at runtime [UNCERTAIN whether it exists].
- GitHub credentials: stored by gh in the macOS keyring (no env var). Git over SSH for the heist repo uses the user's SSH key (verified `ssh -T git@github.com` authenticates as badrusiddique).
- Jira (optional): Atlassian MCP asks for an Atlassian domain, email and API token; not set up for this project (claude.ai Atlassian MCP connector currently reports "Needs authentication").
- No .env files are used by the enggenie repo.
- Config files that matter: ~/.claude/CLAUDE.md (AI Skills Priority block), ~/.claude/settings.json (keys present: permissions, hooks, enabledPlugins, extraKnownMarketplaces, alwaysThinkingEnabled, tui, skipWorkflowUsageWarning, verbose, skipAutoPermissionPrompt), repo .claude-plugin/plugin.json, hooks/hooks.json.

## LOCAL FILES TO TRANSFER

| Full path | Purpose | How |
|---|---|---|
| /Users/badru.siddique/magento/learning/enggenie-skill/ | the project incl. unpushed commits, untracked blog + verification docs, gitignored mirrors | git bundle + tarball, or rsync (see REPOS) |
| /Users/badru.siddique/.cursor/projects/enggenie/ | these handoff docs (.cursorrules, STATUS, ITERATIONS, IMPLEMENTATION, NEXT_STEPS, DECISIONS, CODE_REFERENCE, OPEN_QUESTIONS, TRANSFER) | copy folder to the same relative path; open project in Cursor so .cursorrules loads |
| /Users/badru.siddique/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl (5262475 bytes) | raw copy of the full Claude Code session | copy file (keep permissions 600; it contains full tool output) |
| /Users/badru.siddique/.cursor/projects/_work/cond/enggenie_e0ab1bf8.md (456182 bytes, 8811 lines) | condensed readable transcript used for these docs | copy file |
| /Users/badru.siddique/.claude/projects/-Users-badru-siddique--claude/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl | original Claude Code session store (source of the _raw copy) [UNCERTAIN: path inferred from tool-result paths in the transcript; not re-verified] | copy if resuming the session on the same account layout is wanted |
| /Users/badru.siddique/.claude/CLAUDE.md | holds the "AI Skills Priority" block (enggenie over other suites), plus graphify, RTK rules | merge the block; do not overwrite blindly |
| /Users/badru.siddique/.claude/projects/-Users-badru-siddique--claude/memory/ (MEMORY.md, feedback_enggenie_design_principles.md, feedback_commit_style.md, feedback_no_superpowers_refs.md, feedback_qa_verification.md, feedback_no_emdash.md, project_enggenie.md [stale]) | user preference memory that governs enggenie work | copy the folder |
| /Users/badru.siddique/.claude/plans/one-of-my-collegues-magical-blum.md | plan file | DOES NOT EXIST any more (BLOCKED); text reconstructed in CODE_REFERENCE.md section 14 |
| /Users/badru.siddique/.agents/skills/ (enggenie skills dated Jul 6 2026, others) and /Users/badru.siddique/.agents/.skill-lock.json | user-level installed skills (via `npx skills add`) | not required; re-install with npx on the new machine. Contains stale April entries (architect-design/plan) |
| /Users/badru.siddique/.claude/commands/architect-design.md, architect-plan.md | dangling symlinks to removed dirs | do not transfer; delete on the new machine |
| /Users/badru.siddique/magento/learning/claude-pocket-heist-app/ | demo/test codebase | git clone (see REPOS); uncommitted local edits are not part of this project |

## CURSOR SPECIFIC

- Project rules: /Users/badru.siddique/.cursor/projects/enggenie/.cursorrules (106 lines, Cursor auto-loads). The repo itself has .cursor-plugin/plugin.json (STALE: version 2.0.0, Architect in description).
- The session itself was Claude Code, not Cursor; no Cursor settings, MCP configs or extensions were involved. No .cursor/ folder was created in the repo.
- Cursor install of the skills (documented in docs/getting-started/cursor.md): `npx skills add badrusiddique/enggenie-skill` auto-detects; the hook's Cursor branch (CURSOR_PLUGIN_ROOT, `additional_context`) is untested [UNCERTAIN].
- Open the folder /Users/badru.siddique/magento/learning/enggenie-skill in Cursor and keep this folder's STATUS.md / NEXT_STEPS.md handy; .cursorrules lives outside the repo, so copy it into the repo root only if the user wants it versioned (it contains workspace paths).

## CLAUDE CODE SPECIFIC

- Session: title "ENGGENIE", id e0ab1bf8-0fde-4f16-9e8a-f52a472e4124, 2026-06-01T07:02 to 2026-06-22T11:37 UTC, cwd /Users/badru.siddique/.claude, 3 compactions. Raw: /Users/badru.siddique/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl.
- Plugins on this machine now (enabledPlugins): claude-mem@thedotmack 10.6.3 (needed by memory-recall; its search tool failed during the session), superpowers@claude-plugins-official (session had 5.1.0, machine now 6.4.1; it is the competing suite that wins routing without the enggenie hook), slack@claude-plugins-official 1.3.0, hudl-incident@hudl 1.3.1, performance@performance-tools 1.0.0, and the dotnet-* plugins (unrelated). enggenie itself is NOT in installed_plugins.json; it is available only as user-level skills in ~/.agents/skills.
- To install enggenie as a plugin on a new machine: `/plugin marketplace add badrusiddique/enggenie-skill`, `/plugin install enggenie@badrusiddique-enggenie-skill`, `/reload-plugins` (command text from README/docs; not run in the session; id after @ [UNCERTAIN]). Or `npx skills add badrusiddique/enggenie-skill`.
- Skills invoked in the session: enggenie (gateway), claude-mem:mem-search. Subagent types used: Explore (many), code-reviewer (QA), general background agent (README/docs writer). Tools used: AskUserQuestion, ExitPlanMode (plan mode with user approvals), WebFetch (Medium post), mark_chapter, gh CLI via Bash.
- MCP servers: none were required. Optional: Atlassian MCP (Jira handoff docs), claude-mem MCP search tools. Currently `claude mcp list` shows claude.ai connectors (Google Docs/Sheets/Slides connected; Atlassian and others need authentication).
- Auto-mode classifier behaviour to expect: pushes to main and edits to ~/.claude/CLAUDE.md are blocked until the user says an explicit "yes" in chat.
- ~/.claude/CLAUDE.md global rules relevant here: prefer enggenie skills for SDLC (the block added in this session); user memory forbids AI co-author tags in commits.
- Plugin hook in the repo (hooks/hooks.json) is only active when enggenie is installed as a plugin; it is not active when the repo is merely opened.

## ACCOUNTS AND ACCESS

| Service | Account / auth type | Needed for | Regenerate / re-auth (names only) |
|---|---|---|---|
| GitHub | personal account badrusiddique (not SSO; org "hudl" is separate and only used read-only via `gh api` to view a private mobile-monorepo for the beta feedback) | push, tags, releases, `gh repo edit` | `gh auth login` (token scopes gist, read:org, repo, workflow); SSH key for the heist repo |
| Medium | personal @badru-siddique | publish follow-up post, reply to comment thread (Mykola Kondratiuk) | web login by the user; nothing automated |
| LinkedIn | personal | post | web login by the user |
| Anthropic / Claude Code | user's account | run sessions | `claude` login |
| npm | not used (no package published for enggenie; npx pulls from GitHub via skills CLI) | - | - |
| Atlassian (Jira) | optional, work SSO if used | Jira handoff features | API token via id.atlassian.com (do not store here) |
| carbon.now.sh, Mermaid CLI | no account | blog images | - |

## FIRST THING TO DO ON NEW MACHINE

1. Install tools: `brew install git gh node python` and Claude Code; `gh auth login`; check `ssh -T git@github.com`.
2. `mkdir -p ~/magento/learning ~/.cursor/projects` and copy this folder to `~/.cursor/projects/enggenie/` (plus `_raw/enggenie/` and `_work/cond/enggenie_e0ab1bf8.md`).
3. Restore the repo: clone, then apply the bundle and tarball from REPOS option B (or rsync the folder). Confirm: `git -C ~/magento/learning/enggenie-skill log origin/main..HEAD --oneline` shows 4 commits; `ls docs/blog docs/verification` shows the untracked files.
4. Merge the "AI Skills Priority" block from CODE_REFERENCE.md section 10 into `~/.claude/CLAUDE.md`; copy the memory folder to `~/.claude/projects/<new-project-dir>/memory/`.
5. Install claude-mem if memory-recall is needed: `/plugin marketplace add thedotmack/claude-mem` then install per its docs (id used in docs/guides/memory-recall.md may be wrong, see OPEN_QUESTIONS Q-22).
6. Open the repo in Cursor (or Claude Code) so `.cursorrules` / this handoff set is read; read STATUS.md then NEXT_STEPS.md.
7. Start with NEXT_STEPS.md section 0 and section 1 (user rulings), do not push without an explicit yes.

## VERIFY TRANSFER COMPLETE

```bash
cd ~/magento/learning/enggenie-skill
git log -1 --format=%h              # 4435dc7
git log origin/main..HEAD --oneline | wc -l     # 4 (or 0 if pushed)
git status -sb | head               # untracked: docs/blog, docs/verification
ls skills | wc -l                   # 15
ls skills/review-code/agents | wc -l            # 4
ls hooks                            # hooks.json run-hook.cmd session-start
ls docs/blog/assets/images          # three-lens-flow.png adr-flow.png
wc -c docs/blog/enggenie-v3-medium-post.md      # 17690
grep -c '"version": "3.1.1"' .claude-plugin/plugin.json   # 1
git ls-remote --tags origin | tail -1           # refs/tags/v3.0.0 (until a new tag is pushed)
ls ~/.cursor/projects/enggenie/ -A  # .cursorrules + 8 md files
wc -c ~/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl   # 5262475
gh auth status | head -3 ; node -v ; claude --version
head -8 ~/.claude/CLAUDE.md         # shows "AI Skills Priority"
```
