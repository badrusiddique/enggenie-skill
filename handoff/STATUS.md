# STATUS - enggenie

Snapshot taken Oct 6 2026 from disk (/Users/badru.siddique/magento/learning/enggenie-skill) and the Claude Code session "ENGGENIE" (id e0ab1bf8-0fde-4f16-9e8a-f52a472e4124, 2026-06-01 07:02 to 2026-06-22 11:37, transcript timestamps are UTC, verified: the last commit 4435dc7 is dated 2026-06-22 17:07:44 +0530 on disk = 11:37:44 UTC, matching the transcript's last action at 11:37).

## At a glance

- Product: role-based SDLC skill suite (Markdown only). Released and public: up to v3.0.0 (tag + GitHub release).
- Since v3.0.0 there are 4 local commits (README overhaul, v3.1.0 project-first config, v3.1.1 docs set, SessionStart hook) that are NOT pushed and NOT tagged. plugin.json says 3.1.1; CHANGELOG has 3.1.1 and 3.1.0 entries; latest tag on remote is v3.0.0.
- Content/marketing: Medium follow-up draft (untracked) is not published; LinkedIn post drafted in chat only; two Medium thread replies drafted (first one posted by user per pasted thread).
- Session ended with everything committed locally and the user told to run `git push origin main` themselves.

## Per-feature table

| Feature / work item | Status | Evidence / gap |
|---|---|---|
| Rename architect-design/plan to dev-brainstorm/dev-plan (v2.7.0) | COMPLETE | commit f6d57b3, tag v2.7.0, GH release. Residual: stale "Architect" text in .claude-plugin/marketplace.json, .cursor-plugin/plugin.json, gemini-extension.json |
| T-shirt sizing in pm-refine (v2.7.0) | COMPLETE | skills/pm-refine/SKILL.md; Fibonacci/linear remain as CLAUDE.md overrides |
| pm-refine design-artifact check + review-design exit checkpoint (v2.7.0) | COMPLETE | Step 1 "Design artifact check", Exit Action step 1 |
| Multi-lens review-code (3 lenses + consolidation) (v3.0.0) | COMPLETE | commit 95f89fd, tag v3.0.0; 4 files in skills/review-code/agents/ |
| Review etiquette round 2+ | COMPLETE | section "Review Etiquette -- Rounds 2+" in review-code SKILL.md |
| Em-dash cleanup | PARTIAL | done in skills/, .agents/skills, docs/*.md, README; remains in CHANGELOG.md, CLAUDE.md, plans/enggenie-design-plan.md, docs/blog/assets/carbon/{02,04,06}*.txt |
| docs/guides/adopting.md + 2 ADR examples (v3.0.0) | COMPLETE | pushed |
| Post-release fix of Architect refs in README + claude-code.md | COMPLETE | 4aaf247 pushed |
| README overhaul (landing page, philosophy, personas) | PARTIAL | committed a85e036, NOT pushed |
| Other 4 getting-started guides updated for v3 | NOT STARTED | cursor, copilot-cli, gemini-cli, opencode (assistant flagged as lower priority) |
| review-code Step 0 complement/full detection (v3.1.0) | PARTIAL | committed 8f5de95; not pushed/tagged; not tested on a real repo with .github/agents |
| dev-commit Step 0 project convention detection (v3.1.0) | PARTIAL | same |
| qa-test platform detection + Mobile Mode (v3.1.0) | PARTIAL | same; Detox/Maestro flows not exercised on a real RN project |
| docs/guides/team-customization.md (`## enggenie` config keys) | PARTIAL | doc exists; skills do NOT read skip_skills / default_mode / platform keys (grep-verified: keys appear only in docs/faq.md and team-customization.md) - docs describe behavior that is not implemented |
| ARCHITECTURE.md, SECURITY.md, .github templates, docs/faq.md, jira-mcp.md, memory-recall.md (v3.1.1) | PARTIAL | committed 2a057d6, not pushed |
| SessionStart hook for priority over other suites | PARTIAL | committed 4435dc7; never run in a fresh session; not in CHANGELOG; .agents mirror lacks using-enggenie |
| User global ~/.claude/CLAUDE.md "AI Skills Priority" section | COMPLETE | present in the CLAUDE.md loaded by this machine (verified in current context) |
| GitHub repo description + topics (SEO) | COMPLETE | applied with gh repo edit; 19 topics (limit 20) |
| Tags/releases v3.1.0 / v3.1.1 | NOT STARTED | |
| Medium follow-up post | PARTIAL | docs/blog/enggenie-v3-medium-post.md untracked; placeholders unresolved; title not changed; unpublished |
| Blog assets | PARTIAL | 2 mermaid PNGs rendered; 6 Carbon PNGs + 3 GIFs not produced |
| LinkedIn post | PARTIAL | text drafted in chat (short version), not in a file; not posted [UNCERTAIN] |
| Replies to Medium comments | PARTIAL | reply 1 posted (user pasted it live); reply 2 (rule-based vs confidence-threshold) drafted, posting unknown |
| developer.ai gap analysis | COMPLETE | outcome folded into v3.0.0; deferred: challenger pass, DoR gate, project-context.md, qa-audit |
| gstack analysis | COMPLETE (analysis) | adopted: project-first config, platform-agnostic qa-test, detect tooling; deferred: confidence scores, adversarial review, template docs, fix-first |
| Final cross-check of docs for stale 3.0 vs 3.1 wording | NOT STARTED | |

## Repo / branch state (verified Oct 6 2026)

- Path: /Users/badru.siddique/magento/learning/enggenie-skill
- Remote: https://github.com/badrusiddique/enggenie-skill.git
- Branch: main only; no other branches; `git worktree list` shows only the main worktree; no stashes.
- `git status -sb`: `main...origin/main [ahead 4]`
- Unpushed commits (oldest first): a85e036 (2026-06-01), 8f5de95, 2a057d6, 4435dc7 (all 2026-06-22).
- Untracked: .DS_Store, docs/.DS_Store, docs/blog/.DS_Store, docs/blog/assets/ (carbon/, diagrams/, images/, render-diagrams.sh), docs/blog/enggenie-v3-medium-post.md, docs/verification/ (skill-verification-report.md, superpowers-vs-enggenie-comparison.md). No modified tracked files.
- Ignored by .gitignore: .agents/, .claude/, skills-lock.json (so the .agents mirror and skills-lock.json edits are not in git).
- Tags on remote: v1.0.0 ... v3.0.0 (latest). Local tags match; no v3.1.x.
- gh auth: logged in as badrusiddique (token value not recorded).

## Transcript vs disk disagreements

- Transcript summary (second compaction) says the blog title was updated to "A Security Bug Survived Three Human Code Reviews..."; disk file still has the original title. Disk wins.
- Transcript summary says user "decided to include link in body" for LinkedIn; the transcript shows only that it was offered. [UNCERTAIN]
- Transcript said `.agents/skills` has 13 dirs and skills/ has 14; disk now shows skills/ with 15 (adds using-enggenie) and .agents/skills with 13.
- Plan file ~/.claude/plans/one-of-my-collegues-magical-blum.md is cited throughout the transcript but is NOT on disk now.

- Transcript QA claims "skills/ vs .agents/ diff clean" (checked only for review-code and the files synced at that time). Disk today (`diff -rq skills .agents/skills`): skills/dev-tdd/SKILL.md differs (the .agents copy lacks the "Deep Rebuttals" section, about 52 lines), skills/qa-test/scripts/with_server.py differs, skills/pm-refine/references/ is an empty dir (not tracked by git), dev-commit and using-enggenie exist only in skills/. The mirror is gitignored so nothing in git is affected.
- Transcript says the zero-"Architect" sweep was clean for skills/. Disk: skills/review-code/SKILL.md line 31 still says "what was planned (Architect)" and skills/dev-implement/SKILL.md line 32 says "handoff context from PM and/or Architect". docs/qa/e2e-test-plan.md (lines 11, 93, 94) and the tracked original post docs/blog/enggenie-medium-post.md (lines 46, 305, 306, 319) also still use Architect. The v2.7.0/v3.0.0 greps only searched for the strings architect-design / architect-plan, not the bare word.
- The repo's own CLAUDE.md "Pre-Release Verification Gate" (8 steps: test branch on ~/magento/learning/claude-pocket-heist-app, per-skill scenario runs, 3 personas, a head-to-head comparison against the other skill suite, meta-verification, 4 gates) was NOT run as written in this session. The session used the user's standing 6-category subagent QA gate instead (functionality, zero-mentions scan, skills-expert handoff, persona walkthrough, marketplace/platform docs, security). No v3.1.x gate of either kind was run before the 8f5de95 / 2a057d6 / 4435dc7 commits (only grep checks).

## BLOCKED / NOT VERIFIED

- Plan file missing on disk (see above); recovered final text from raw jsonl.
- The SessionStart hook behavior (not run); Detox/Maestro/complement mode behavior (not run on a real project).
- Whether Medium reply 2, LinkedIn post, Medium post were ever published (no evidence in transcript or disk).
- Whether the Medium post's heist-app "security bug survived three reviews" story is real or illustrative [UNCERTAIN].
- Sibling repo ~/magento/learning/claude-pocket-heist-app (the test codebase named by CLAUDE.md and the demo app source): not part of this session's work, but on disk it is on branch test/skill-verification-v2 with modified .claude/settings.local.json and tool-use.json (read-only observation; remote git@github.com:badrusiddique/claude-pocket-heist-app.git).
- Marketplace id: README/docs install with `/plugin install enggenie@badrusiddique-enggenie-skill` but .claude-plugin/marketplace.json declares name "enggenie-marketplace" [UNCERTAIN whether the id after @ comes from that name or the repo slug; never tested in this session].
- GitHub remote state beyond tags was not re-queried (read-only; no network write). `git ls-remote --tags` confirmed remote tags up to v3.0.0.
