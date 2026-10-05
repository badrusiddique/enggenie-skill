# ITERATIONS - enggenie

One Claude Code session (title "ENGGENIE", id e0ab1bf8-0fde-4f16-9e8a-f52a472e4124, cwd /Users/badru.siddique/.claude, raw jsonl in /Users/badru.siddique/.cursor/projects/_raw/enggenie/e0ab1bf8-0fde-4f16-9e8a-f52a472e4124.jsonl, condensed in /Users/badru.siddique/.cursor/projects/_work/cond/enggenie_e0ab1bf8.md, 8811 lines). The session was compacted 3 times (about 2026-06-01 08:13, 2026-06-01 10:28, 2026-06-22 05:20) and resumed on 2026-06-22. It is a single linear session (no forks). All times are transcript timestamps (UTC, verified against git commit dates in +0530). Repo for all code work: /Users/badru.siddique/magento/learning/enggenie-skill.

Prior history (not in this session): memory notes say the project existed since early April 2026 (git history: initial commit through v2.6.0 on 2026-04-06, 54 commits total today). Memory project_enggenie.md is stale (13 skills, architect names, 7 roles).

---

## Iteration 1 - Feedback fix, release v2.7.0 (2026-06-01 07:02 - 07:38)

Status: COMPLETE (released).
Original intent: user pasted colleague feedback: (a) dislikes the "architect" role (do not push that pattern on teams); (b) pm-refine estimation seems to equate story points with hours; (c) "Where does initial UX/UI design come in? ... UX DNA and UX Prototypes?" Also asked "do you know the verification step from the last conversation thread?" (answer: standing 6-category QA gate) and "first initialize the entire conversation which contains the DOs and DONTs" (assistant invoked the `enggenie` gateway skill).
User answers to AskUserQuestion: architect is just a naming issue, rename; team sizes by T-shirt.
Implemented (file by file):
- Renamed directories skills/architect-design -> skills/dev-brainstorm, skills/architect-plan -> skills/dev-plan, and the same in .agents/skills/; re-pointed .claude/skills symlinks (`ln -sfn ../../.agents/skills/dev-brainstorm`, `dev-plan`; removed the old links).
- sed across skills/dev-brainstorm/SKILL.md and skills/dev-plan/SKILL.md (names, "Architect" -> "Dev"); across skills/enggenie, pm-refine, dev-implement, memory-recall SKILL.md.
- skills/enggenie/SKILL.md: overview sentence now "PM, Dev, Reviewer, QA, Deploy"; routing-table role column and All Skills table changed Architect -> Dev.
- skills/pm-refine/SKILL.md: Estimation Method section replaced by T-shirt sizing (XS/S/M/L/XL table, "relative complexity - not hours", per-area ratings, story rated as a whole, decompose if M or larger, XL must be decomposed; configurable T-shirt default / Fibonacci / Linear); Step 1 got a "Design artifact check" (confirm approved design, or note "No design artifact provided -- spec will describe expected behavior ...; UX review recommended", or flag provisional if in progress; "Design happens upstream of pm-refine"); Exit Action got step 1 "Design review checkpoint" invoking enggenie:review-design when a design artifact exists; frontmatter description "estimating story points" -> "sizing work (T-shirt)"; Team Configuration "Fibonacci (default)" -> "T-shirt (default)" (caught by QA).
- skills-lock.json keys renamed (gitignored; hashes blank). CLAUDE.md: "14 skills across 6 roles"; table rows renamed. sed over README, docs/getting-started/*, docs/guides/*, docs/skills/*, docs/examples/*, docs/blog/enggenie-medium-post.md, docs/verification/*, docs/qa/e2e-test-plan.md, plans/enggenie-design-plan.md. CHANGELOG: new top entry [2.7.0] - 2026-06-01 (history entries untouched).
- cp skills/{dev-brainstorm,dev-plan,enggenie,pm-refine}/SKILL.md into .agents/skills/ (the .agents copies had been stale/older, e.g. missing the "Jira Ticket Entry" section).
- Memory: wrote /Users/badru.siddique/.claude/projects/-Users-badru-siddique--claude/memory/feedback_enggenie_design_principles.md and indexed it in MEMORY.md.
- QA gate: 6 parallel subagents (functionality 10/10; zero superpowers/Hudl scan found only pre-existing mentions in CLAUDE.md lines 103,105,107,138,154 and docs/verification/superpowers-vs-enggenie-comparison.md; handoff chain 6/7 then fixed; persona 3/3; marketplace/platform docs 9/9; security 5/5 with one low note).
- Commit f6d57b3 "rename architect-design/plan to dev-brainstorm/dev-plan, update estimation to t-shirt sizing" (27 files). User asked "did you release it under a new version?" - assistant tagged v2.7.0, pushed main and tag, `gh release create v2.7.0 --title "v2.7.0 - dev-brainstorm, dev-plan, T-shirt sizing"`.
Missing: marketplace.json, .cursor-plugin/plugin.json, gemini-extension.json still carried "Architect" and 2.0.0 (not noticed; still stale today).
Decisions: see DECISIONS.md D-01 to D-04.

## Iteration 2 - developer.ai gap analysis and plan (2026-06-01 07:39 - 07:57)

Status: COMPLETE (plan approved; analysis only).
Intent: colleague's similar repo https://github.com/Ethanon/developer.ai - "assess what he has and I don't ... anything I can include (readme, doc, approach) making sure we are away from plagiarism ... include all the precheck for verification, caution before making a push".
Done: two Explore subagents (one fetched developer.ai, one inventoried enggenie). Plan file ~/.claude/plans/one-of-my-collegues-magical-blum.md written 3 times:
 1. v2.8.0 plan (4 agent files + challenger pass etc.) - REJECTED by user: "be your own critic and reviewer".
 2. Self-critique found 7 problems (challenger pass breaks code-reviewer-agent reference and is vague; DoR point 7 breaks Jira-optional users; ADOPTING.md and 2 ADRs belong later; README improvements thin; context templates dismissed too quickly; scope too big). Rewritten as v2.8.0 focused + v2.9.0 roadmap - REJECTED: "if we need to make a change it would be a major version release ... snapshots of the working ... sell this piece with proper documentation ... images, diagrams, relatable quotes, examples".
 3. Doc-quality audit by Explore subagent (README opens with jargon "Role-based skills for AI coding assistants ..."; best content, RED->GREEN output in docs/examples/full-feature-walkthrough.md, buried; philosophy.md first sentence is strong) -> v3.0.0 plan, APPROVED at 07:57.
Findings recorded: developer.ai has 7 named review personas in 2 layers, review etiquette (round 2+ only new/worse), 7-point Definition of Ready, CALIBRATE.md staged adoption, project-context templates, worked decision docs, GitHub Actions + scheduled audit scanners. enggenie strengths: full SDLC, 5 platforms, Jira-native handoff, TDD enforcement, evidence gate, systematic debug, graceful degradation, zero deps, claude-mem memory.
Plagiarism guardrails fixed here (see D-08).

## Iteration 3 - v3.0.0 implementation and release (2026-06-01 08:08 - 08:20)

Status: COMPLETE (released tag v3.0.0, GitHub release "v3.0.0 - Multi-lens review + documentation overhaul").
Intent: execute the approved plan: multi-lens review, README landing page, adopting guide, two ADR examples, CHANGELOG, full verification, release.
Implemented:
- Background agent (id a7a484d61c43f3cec) wrote README.md rewrite, docs/guides/adopting.md (5 stages: Observe; Spec and Plan; TDD-Guided Build; Full Pipeline; Optional Integrations), docs/examples/adr-timer-approach.md (ADR-001 heist session timer: client-side countdown from stored timestamp), docs/examples/adr-storage-strategy.md (localStorage vs Firestore hybrid).
- skills/review-code/SKILL.md: Step 2 "Dispatch Three Lens Subagents in Parallel" (model sonnet; same diff, spec, round number), Step 3 Consolidation (agents/code-reviewer-agent.md), Step 4 Act on Consolidated Findings; severity table Blocking / Advisory / Observation / Wrong; new section "Review Etiquette -- Rounds 2+" (ask user for previous findings, else treat as round 1); "Subagent Prompt Templates" lists 4 files; Subagent Context Preservation updated; Exit Condition "All Blocking and Advisory items are resolved".
- New: skills/review-code/agents/security-lens-agent.md, engineering-lens-agent.md (includes YAGNI caller-count grep guidance), test-lens-agent.md. Rewritten: skills/review-code/agents/code-reviewer-agent.md as consolidation agent (dedupe, keep higher severity, single report, no new findings). All synced to .agents/skills/review-code/.
- CHANGELOG: top entry [3.0.0] - 2026-06-01 (Added/Changed/Upgrading from v2.7.0).
- Push-caution checklist run as a bash block (git diff --stat, agent count = 4, skills vs .agents diff, stale architect refs, em-dash scan, superpowers/Hudl scan, CHANGELOG head). Two code-reviewer QA subagents found: em-dashes in review-code SKILL lines 27-28 and many pre-existing em-dashes; stale architect refs in .agents/skills/memory-recall and dev-implement (fixed by cp from skills/). Batch python replacement of em-dash with hyphen across skills/, .agents/skills, docs/ (14+ files).
- Commit 95f89fd "v3.0.0: multi-lens code review, docs overhaul, em-dash cleanup" (20 files, +1042/-392); tag v3.0.0; pushed; gh release created.
Missing at the time: README skills table and prose still said "Architect"; getting-started claude-code.md too (found in Iteration 4).

## Iteration 4 - Post-release honesty check and fix (2026-06-01 08:22 - 08:31)

Status: COMPLETE.
Intent: user asked "did you verify everything, did you update the getting started, readme doc with all possible options?" Assistant admitted "not fully".
Done: README lines 155/164/165 Architect -> Dev; docs/getting-started/claude-code.md "Architect:" line merged into Dev, review-code row notes 3-lens, What's Next links adopting.md and ADR examples. Commit 4aaf247 "fix: remove stale Architect role from README and getting-started". First `git push origin main` DENIED by the Claude Code auto-mode classifier (a question is not authorization); after the user said "yes please" the push succeeded (95f89fd..4aaf247).
Missing: cursor.md, copilot-cli.md, gemini-cli.md, opencode.md not updated for multi-lens (assistant called them lower priority).

## Iteration 5 - Public Medium comment replies (2026-06-01 08:31 - 08:32, and 10:39 - 10:40)

Status: PARTIAL (drafts delivered; posting not under assistant control).
Comment 1 (Mykola Kondratiuk, on the original Medium post): "14-role skill suite ... when the PM role and the Architect role disagree on scope, who wins?" Assistant drafted a reply: correct to 14 skills / 6 roles, Architect retired in v2.7.0, user is tiebreaker (skills surface the conflict and stop), Jira handoff makes conflicts visible. User wanted a warmer public version; the second draft was posted (user pasted the live thread at 10:39 showing the author reply).
Comment 2 (Mykola): "is the stop rule-based or confidence-threshold triggered?" Assistant draft (short, conversational): rule-based; honest gap - stop fires on detected conflict, not detected uncertainty; suggested making interpretations explicit before execution; ends with a question. Posting status: unknown.

## Iteration 6 - Medium follow-up post, assets, LinkedIn (2026-06-01 08:35 - 10:18)

Status: PARTIAL (draft + partial assets; unpublished).
Intent: user gave original post URL https://medium.com/@badru-siddique/my-ai-writes-code-fast-it-was-terrible-at-everything-else-c705997c4147 (title "My AI Writes Code Fast. It Was Terrible at Everything Else."; sections with emoji headings, demo-heavy, first person, closes "The Retro Was Different Last Month") and asked for a follow-up covering what changed since, why, what is new; tone with GIFs and emojis; later "make sure we are aware of plagiarism correctness, look at a post writing skills i might have".
Done:
- Plan file rewritten as "Medium Post: enggenie v3.0.0 Follow-Up" (rejected once for missing plagiarism + writing-skills check, then approved 09:18). No dedicated blog-writing skill found (superpowers 5.1.0 writing-skills is for SKILL.md authoring).
- docs/blog/enggenie-v3-medium-post.md written 4 times: v1 (1859 words) -> v2 after user "didn't like the formatting" (1547 words, hook moved to top, Architect section shrunk) -> v3 after user asked whether all 3.0.0 changes were covered (assistant admitted ADR examples + pm-refine design check were missing) -> final comprehensive version (2384 words per script, later file is 17690 bytes): sections "The Problem With Asking One Reviewer to Do Three Jobs", "Demo: Same PR, Three Specialists in Parallel", "Round 2: The Lens That Knows When to Stay Quiet", "Architecture Decisions That Don't Live in Slack", "Where's the Figma? - pm-refine Now Asks Before Anyone Writes Code", "Two Other Changes Worth Knowing" (Architect rename + T-shirt), "Rolling This Out Without D..." (adoption table), qa-verify deferred items, team quotes, closing. ASCII 3-lens diagram included. Placeholders left: 3 [GIF:], 3 [SCREENSHOT:], 2 [IMAGE:].
- Asset generation help: tools check (mmdc, convert, asciinema NOT installed). Created docs/blog/assets/diagrams/three-lens-flow.mmd, adr-flow.mmd; docs/blog/assets/render-diagrams.sh (npx @mermaid-js/mermaid-cli); docs/blog/assets/carbon/01-single-reviewer.txt .. 06-pr-deferred-items.txt (text to paste into carbon.now.sh: One Dark, JetBrains Mono 14px, mac window, export 2x PNG). On disk now: images/three-lens-flow.png and images/adr-flow.png exist (script was run by the user at some point); Carbon PNGs do not.
- Title options offered; recommended Option 1 "A Security Bug Survived Three Human Code Reviews. Three AI Lenses Caught It in Seconds." (others: "Your AI Reviewer Is Doing Three Jobs at Once. That's Why It Keeps Missing Things.", "I Upgraded My AI From One Reviewer to Three. Here's the Diff.", a "Security Expert, Engineering Expert, Test Expert - Simultaneously" variant). User only asked "what is the title btw for option 1"; never explicitly said apply it. File title unchanged.
- LinkedIn post drafted (hook "A security bug survived three human code reviews."), shortened on request, dangling "session join endpoint above" removed; link-placement discussion (LinkedIn reach vs link in body; link given points to the ORIGINAL post URL, to be swapped). Not saved in any file.
- User asked "will it get caught by the github which we took inspiration from?" - assistant: concept-only, no named personas, offered an optional acknowledgment line (not decided).
Missing: apply title, resolve placeholders, render Carbon PNGs, record GIFs, fix two-weeks vs three-weeks inconsistency, verify whether the demo incident is real, bump "v3.0.0" wording to current version, publish.

## Iteration 7 - README overhaul (2026-06-01 10:23 - 10:38)

Status: PARTIAL (committed, not pushed).
Intent: README "like developer.ai's: super detailed, elegant, diagrams, easy getting started ... explain why each component is made ... examples and use cases ... verify everything, do not miss anything from 3.0.0".
Done: two Explore agents (developer.ai README structure; enggenie accuracy audit). Plan rewritten as "README Overhaul: enggenie v3.0.0" with hard accuracy constraints (14 skills, 6 roles, install commands, severity words, T-shirt sizes, artifact names, 5 adoption stages, Jira and memory-recall optional). README.md rewritten (3292 words / 505 lines): hero before/after, What this is (and isn't), Who it is for (EM, Dev, PM), Design philosophy (Evidence over assertion, Constraint over reminder, Domain separation, Discipline that travels), heist inventory TDD RED/GREEN session, security-lens Blocking example, skills table with WHY column, before/after for multi-lens, "Your first three sessions", adoption path Mermaid diagram, optional integrations, documentation map by role. Self-review added the pm-refine PROVISIONAL note to the skills table. Commit a85e036 "docs: overhaul README with scope, philosophy, WHY explanations, and team adoption guide" (1 file, +221/-76). Not pushed.
Missing: README still documents v3.0.0-level features; broken links to docs/guides/jira-mcp.md and memory-recall.md found later (fixed in Iteration 9).

## Iteration 8 - Beta-tester feedback, gstack analysis, v3.1.0 (2026-06-22 03:53 - 04:39)

Status: PARTIAL (implemented and committed locally; not pushed, not tagged).
Intent: beta tester Brent Kelly (Hudl mobile) said: review-code lenses may conflict with the AI Reviewer / CI agents in the Mobile Monorepo (.github/agents, .claude/agents/local-code-reviewer.md); dev-commit may conflict with Hudl eng-standards and repo skill .claude/skills/using-git/SKILL.md; wishes for a workflow of skills where a project picks a subset; qa-test looks web-only. User also asked to analyze https://github.com/garrytan/gstack ("can you analyze it and see if we can improve on or take inspiration?") with the same parameters (verify, no plagiarism, well documented, elegant).
Done: three Explore agents (gstack analysis; hudl/rn-hudl files via `gh api`; enggenie skill files). Plan (v3.1.0, 4 streams) approved after a 40-minute pause. Implemented:
- skills/review-code/SKILL.md: "Step 0 -- Detect Existing Review Infrastructure" (`ls .github/agents/`, `ls .claude/agents/ | grep -i review`; Complement mode (recommended) vs Full mode; tell user which lenses are skipped and why; if local-code-reviewer.md exists suggest running it first).
- skills/dev-commit/SKILL.md: "Step 0: Detect Project Commit Conventions" (order: .claude/skills/using-git/SKILL.md; CLAUDE.md "## Commit|## Git|commit convention|commit message"; .commitlintrc*; CONTRIBUTING.md; follow exclusively, announce source, ask on ambiguity, never blend).
- skills/qa-test/SKILL.md: "Platform Detection" (package.json grep react-native|detox|maestro|appium; metro.config.js android/ ios/; app.json expo) -> "Mobile Mode" (Detox, Maestro `.maestro/`, manual mobile checklist: deep links, push, offline, background/foreground, orientation, OS versions, keyboard); Quick Reference table updated; web path unchanged.
- docs/guides/team-customization.md (new): detection order tables, `## enggenie` CLAUDE.md config examples, rn-hudl worked example.
- cp review-code and qa-test to .agents/skills (dev-commit has no .agents counterpart).
- Commit 8f5de95 "feat: project-first configuration for review-code, dev-commit, and qa-test" (4 files, +293/-3). `git add .agents` failed because .agents/ is gitignored.
gstack: deferred ideas (confidence 1-10 scores v4.0, adversarial review, template docs, fix-first AUTO-FIX/ASK v3.2). Detailed gstack findings were only summarized in the plan (condensed transcript truncates the agent report) [UNCERTAIN on depth].
Missing: no CHANGELOG entry at that point (added in Iteration 9); `## enggenie` config keys not wired into any skill; nothing tested on a real RN repo.

## Iteration 9 - Documentation audit and v3.1.1 docs set (2026-06-22 05:12 - 05:25)

Status: PARTIAL (committed locally, not pushed).
Intent: "review it as an expert and see if documentations, getting started docs, readme files needs to be added or updated; did you include stuff from gstack ... leverage some third party ... cautious of plagiarism ... SEO". Interrupted once by accident (Esc) and re-sent combined with the routing question (Iteration 10).
Done: Explore audit found 97 md files; broken links to docs/guides/jira-mcp.md and docs/guides/memory-recall.md (README ~lines 413,419,470,471 and CHANGELOG), missing ARCHITECTURE.md, issue/PR templates. Created: docs/guides/jira-mcp.md, docs/guides/memory-recall.md, ARCHITECTURE.md, SECURITY.md, .github/ISSUE_TEMPLATE/bug_report.md, .github/ISSUE_TEMPLATE/feature_request.md, .github/pull_request_template.md, docs/faq.md; team-customization.md gained "Working alongside other plugin suites" (superpowers conflict + CLAUDE.md fix); CHANGELOG got [3.1.1] and [3.1.0] entries. Commit 2a057d6 "docs: add missing guides, GitHub templates, architecture overview, FAQ" (10 files, +760). Push DENIED by classifier (no explicit authorization); user given the command.
Third-party doc tools: asked whether to leverage one; no tool was installed or used.

## Iteration 10 - Skill routing conflict and SEO metadata (2026-06-22 05:16 - 05:47, 11:11 - 11:37)

Status: PARTIAL.
Intent: "I have superpowers installed and enggenie but why is enggenie not picked ... how can folks land on this repo organically".
Diagnosis (Explore agent): superpowers 5.1.0 SessionStart hook (hooks.json -> session-start script) injects its using-superpowers skill in an EXTREMELY_IMPORTANT wrapper before any message; enggenie has no hook and loads on demand.
Done:
- 05:46 `gh repo edit --description "Role-based SDLC skill suite for AI coding assistants. 14 skills across PM, Dev, Reviewer, QA, and Deploy roles. Works with Claude Code, Cursor, Copilot CLI, Gemini CLI, and OpenCode."`; topics: tried to add 4 (failed: max 20), then removed skill-md-skillsmp and skills, added llm and opencode (19 topics now). Old description still said Architect.
- 11:11-11:24 user complained again; edit of ~/.claude/CLAUDE.md denied by classifier (question is not authorization); user said "yes add it and for others who would install enggenie ... make sure enggenie is always given the preference" -> `# AI Skills Priority` section added to /Users/badru.siddique/.claude/CLAUDE.md (names the 13 skills; "Do not route to superpowers:brainstorming ...").
- An Explore subagent ran the superpowers session-start script from the plugin cache; the harness flagged a SECURITY WARNING (executing external plugin code / persistence).
- 11:30-11:37 built the hook: skills/using-enggenie/SKILL.md, hooks/hooks.json, hooks/run-hook.cmd, hooks/session-start, .claude-plugin/plugin.json (version 2.6.0 -> 3.1.1, description without Architect, "hooks": "./hooks/hooks.json"); chmod +x on the two scripts. Commit 4435dc7 "feat: add SessionStart hook so enggenie takes priority over other skill suites" (5 files, +137/-2). Not pushed. Assistant's own note earlier (05:46): without a hook, precedence is not automatic; docs tell users to add the CLAUDE.md section.
Missing: hook never tested; not in CHANGELOG; not mirrored to .agents; skill count now 15 dirs; marketplace/cursor/gemini manifests untouched; suggested awesome-claude-code submission not done.

## Final state (last message of the session, 2026-06-22 11:37)

Assistant: "Committed. Push when ready: cd ~/magento/learning/enggenie-skill && git push origin main" plus a summary table of hook files. Last user message: 11:23 "yes add it and for others who would install enggenie for the first time on existing superpower or the other way round make sure enggenie is always given the preference". Nothing was mid-edit; work stopped after the hook commit.

## Cross-check addendum (Oct 6 2026, transcript fully re-read against disk)

- Verified against the whole 8811-line condensed transcript: iteration boundaries, commit hashes (f6d57b3, 95f89fd, 4aaf247, a85e036, 8f5de95, 2a057d6, 4435dc7), tags (v2.7.0, v3.0.0), the 3 compactions (08:13, 10:28 on 2026-06-01; 05:20 on 2026-06-22) and the two "Continue from where you left off." turns (06-22 03:53, 05:10 / 11:11) are accurate. Two user turns on 06-22 were interrupted/duplicated (05:16 Esc, re-sent combined).
- Iteration 1 detail: the QA gate also found the 5 pre-existing superpowers mentions in CLAUDE.md lines 103,105,107,138,154; the assistant treated them as "pre-existing/internal". The memory rule feedback_no_superpowers_refs says zero mentions repo-wide.
- Iteration 3 detail: the em-dash batch replacement (python, replaces " - ", "- ", " -", "-") covered skills/, .agents/skills, docs/ (including docs/blog/enggenie-medium-post.md) but NOT CHANGELOG.md, CLAUDE.md or plans/ (README.md was only scanned; it was already clean). Files fixed in that pass: skills/{deploy-ship,dev-brainstorm,dev-debug,pm-refine,review-design,qa-test,qa-verify,dev-implement,dev-plan}/SKILL.md plus their .agents copies and docs files.
- Iteration 6 detail: demo story inside the Medium draft says the bug lived "two weeks" with "three manual reviews"; LinkedIn draft says "Three weeks in our codebase". No evidence in the transcript that the bug is a real incident (the example is the heist demo app) [UNCERTAIN].
- Iteration 10 detail: the hook script chooses output by env var: CLAUDE_PLUGIN_ROOT set and COPILOT_CLI_PLUGIN_ROOT unset gives Claude Code JSON `hookSpecificOutput.additionalContext`; CURSOR_PLUGIN_ROOT gives `{"additional_context":...}`; else `{"additionalContext":...}`. Only the Claude Code path is plausible to have been exercised and it was not run at all.
- Not done in the session and easy to miss: nothing was ever run to test any skill in a live session after changes; every "verification" was grep/diff/subagent reading.
