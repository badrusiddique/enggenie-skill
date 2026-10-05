# OPEN_QUESTIONS - enggenie

Everything unresolved at the end of the session (2026-06-22 11:37 UTC) plus items found when checking disk on Oct 6 2026. "Owner" = who must answer. [UNCERTAIN] = could not be established from transcript or disk.

## A. Needs the user's decision

- Q-01 (user) Version/tag scheme for the 4 unpushed commits. CHANGELOG has 3.1.0 and 3.1.1; plugin.json 3.1.1; hook not in CHANGELOG. Tag v3.1.0 + v3.1.1, or v3.2.0, or something else? Earlier user rule: capability additions are major releases.
- Q-02 (user) The `## enggenie` project-config layer (skip_skills, review_code.default_mode, dev_commit.conventions, qa_test.platform, qa_test.mobile_runner, adopted_skills): implement in the skills, or edit docs to say it is planned? Today docs/guides/team-customization.md and docs/faq.md claim skills read it ("Skills read this section at startup") - not true.
- Q-03 (user) Skill count: 14 documented vs 15 dirs in skills/ (using-enggenie). Count or hide?
- Q-04 (user) Does the "zero superpowers / Hudl mentions" rule (user memory feedback_no_superpowers_refs.md) apply to the whole repo? Current violations: SECURITY.md (author's work email at the hudl.com domain as the security contact), docs/faq.md, docs/guides/team-customization.md (rn-hudl example, superpowers conflict section), CLAUDE.md, CHANGELOG.md, docs/verification/superpowers-vs-enggenie-comparison.md (untracked). Also a conflict: the user explicitly asked for the superpowers-conflict fix to be documented for installers.
- Q-05 (user) Is the SessionStart hook's forceful language acceptable? And should the hook ship at all given it overrides other suites?
- Q-06 (user) Blog: apply title Option 1? Is the "bug survived three reviews / two weeks" story real or illustrative? LinkedIn says "three weeks"; post body says "two weeks". Add an acknowledgment line for inspiration (offered, undecided)?
- Q-07 (user) LinkedIn: link in body (compaction summary claims the user chose this; transcript only shows it offered) vs first comment; swap link to the new post URL when published.
- Q-08 (user) Should docs/verification/ and docs/blog/ be committed? Repo CLAUDE.md says verification files are committed only on request. Blog drafts are currently untracked.
- Q-09 (user) Do the other four getting-started guides (cursor, copilot-cli, gemini-cli, opencode) get v3 updates now? Assistant marked them lower priority and never did them.
- Q-10 (user) Update or delete the stale memory file project_enggenie.md (13 skills, architect names, 7 roles)? Needs approval before editing user memory/config.
- Q-11 (user) Submit to awesome-claude-code and other directories (suggested only).
- Q-12 (user) Was Medium reply 2 posted? Was the LinkedIn post posted? Was the Medium v3 post published? No evidence either way.

## B. Needs verification (nobody ran it)

- Q-13 SessionStart hook: does it run, produce valid JSON, get injected, and win over the other suite? Path: `CLAUDE_PLUGIN_ROOT=<repo> bash hooks/session-start | python3 -m json.tool`; then fresh-session check after plugin install. Does `npx skills add badrusiddique/enggenie-skill` install hooks at all? Do Cursor / Copilot CLI / Gemini CLI honor the same hook JSON?
- Q-14 review-code Step 0 complement/full mode on a repo that has .github/agents (e.g. the beta tester's mobile monorepo, private repo hudl/rn-hudl, accessed in-session via `gh api`) - behaviour untested.
- Q-15 dev-commit Step 0 on a repo with .claude/skills/using-git/SKILL.md - untested.
- Q-16 qa-test Mobile Mode (Detox / Maestro) - untested on a real React Native project; commands in the skill are plausible but unverified.
- Q-17 Which manifest does each platform read, and do the stale ones (marketplace.json, .cursor-plugin/plugin.json, gemini-extension.json at 2.0.0 with Architect) break installs or just display wrong text? Is the Claude Code install id `enggenie@badrusiddique-enggenie-skill` consistent with marketplace.json name "enggenie-marketplace"?
- Q-18 The repo's own 8-step Pre-Release Verification Gate (CLAUDE.md) vs the 6-category gate: which is canonical going forward, and has either been run for 3.1.x? (Neither was.)
- Q-19 Machine state: user-level ~/.agents/skills contains enggenie skills (dev-brainstorm, dev-plan, using-enggenie, ... dated Jul 6 2026) while ~/.agents/.skill-lock.json still records April 3 installs of architect-design / architect-plan; ~/.claude/commands/architect-design.md and architect-plan.md are dangling symlinks to ~/.agents/skills/architect-*/SKILL.md (those dirs no longer exist). Who copied the Jul 6 files and from where (the remote has no using-enggenie)? [UNCERTAIN]. Also enggenie is not listed in ~/.claude/plugins/installed_plugins.json, so on this machine it is available only as user-level skills, not as an installed plugin.
- Q-20 Does docs/faq.md claim "Both superpowers and enggenie respect user instructions as the highest priority ... it overrides session-start hook behavior" hold true? Asserted by the assistant, not tested.
- Q-21 docs/faq.md facts asserted without measurement: "tested with Claude Sonnet and Claude Haiku", token estimates per skill. [UNCERTAIN] source.
- Q-22 jira-mcp.md / memory-recall.md: setup commands (`claude mcp add atlassian`, `/plugin install mem@thedotmack-claude-mem`) were written from assistant knowledge, not run. The installed plugin on disk is `claude-mem@thedotmack` v10.6.3, so the `mem@thedotmack-claude-mem` id looks wrong [UNCERTAIN]. Platform-support tables (Cursor/Gemini/OpenCode) are guesses.

## C. Known defects not yet decided as tasks

- Q-23 Stale word "Architect": skills/review-code/SKILL.md:31, skills/dev-implement/SKILL.md:32, docs/qa/e2e-test-plan.md, docs/blog/enggenie-medium-post.md, three manifests, GitHub (fixed), memory file. Is the old blog post an archive?
- Q-24 Em-dashes remain in CHANGELOG.md (20), CLAUDE.md (10), plans/enggenie-design-plan.md (141), carbon 02/04/06 txt. Change CHANGELOG history lines or leave?
- Q-25 .agents mirror drift (dev-tdd, qa-test/scripts/with_server.py; missing dev-commit and using-enggenie) and the empty skills/pm-refine/references dir.
- Q-26 README/docs/blog still say "v3.0.0"; plugin is 3.1.1; blog mentions the shipped version as v3.0.0 and "last week".
- Q-27 Demo numbers in blog/Carbon sources (e.g. "167 passed", two blocking items) are illustrative [UNCERTAIN]; not from a real run.
- Q-28 Detail loss: gstack and developer.ai analyses exist only as summaries inside plan text (condensed transcript truncates subagent reports; raw jsonl has them). Do they need to be re-derived from /Users/badru.siddique/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl before the next iteration?
- Q-29 The approved plan file ~/.claude/plans/one-of-my-collegues-magical-blum.md no longer exists (BLOCKED / NOT VERIFIED); final text of each plan version is reconstructed in CODE_REFERENCE.md section 14 from the transcript.
- Q-30 claude-mem search failed in-session (`Error calling Worker API: fetch is not defined`); the memory-recall skill and its docs depend on it.
- Q-31 Security posture: SECURITY.md promises 48-hour acknowledgement and uses a company email; confirm it is the address the author wants public, or replace (a personal address / GitHub private vulnerability reporting).
- Q-32 The harness raised a SECURITY WARNING when an Explore subagent executed another plugin's session-start script from the plugin cache (flagged as executing external code / persistence). Confirm nothing from that run persisted; the user was not asked.
- Q-33 Test codebase ~/magento/learning/claude-pocket-heist-app: left on branch test/skill-verification-v2 with modified tracked files .claude/settings.local.json and tool-use.json (and a worktree-marked branch feature/heist-countdown-timer). Not touched in the session; state may be from earlier work.
