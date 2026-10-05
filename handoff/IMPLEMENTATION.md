# IMPLEMENTATION - enggenie

Repo: /Users/badru.siddique/magento/learning/enggenie-skill (remote https://github.com/badrusiddique/enggenie-skill.git). Branch main, HEAD 4435dc7, 4 commits ahead of origin/main (remote head 4aaf247, latest tag v3.0.0). 91 tracked files. Verified Oct 6 2026 from disk.

Product shape: pure Markdown skill suite. No runtime, no build, no tests, no npm. The only executable code is the SessionStart hook (bash) and skills/qa-test/scripts/with_server.py (Playwright server helper, pre-existing, not touched in the session).

Where each change lives in git:
- Released and pushed: f6d57b3 (v2.7.0), 95f89fd (v3.0.0), 4aaf247 (post-release fix).
- Committed locally only: a85e036, 8f5de95, 2a057d6, 4435dc7.
- Untracked (must be recorded, not committed): docs/blog/enggenie-v3-medium-post.md, docs/blog/assets/ (carbon/, diagrams/, images/, render-diagrams.sh), docs/verification/ (skill-verification-report.md, superpowers-vs-enggenie-comparison.md), several .DS_Store.

## Repo layout (disk)

```
skills/<name>/SKILL.md          canonical, tracked (15 dirs)
skills/review-code/agents/      4 files
.agents/skills/<name>/          real-dir mirror, gitignored (13 dirs)
.claude/skills/<name>           symlinks -> ../../.agents/skills/<name>, gitignored (13 links)
.claude-plugin/plugin.json      v3.1.1 + hooks
.claude-plugin/marketplace.json STALE 2.0.0, Architect
.cursor-plugin/plugin.json      STALE 2.0.0, Architect
gemini-extension.json           STALE 2.0.0, Architect
hooks/                          hooks.json, run-hook.cmd (755), session-start (755)
docs/getting-started/ (6)  docs/guides/ (9)  docs/examples/ (6)  docs/qa/ (1: e2e-test-plan.md)  docs/skills/ (2: README.md, usage-examples.md)  docs/changelog/ (CHANGELOG.md, 96 B)  docs/faq.md
docs/blog/ docs/verification/   UNTRACKED
.github/ISSUE_TEMPLATE/{bug_report,feature_request}.md  .github/pull_request_template.md
ARCHITECTURE.md SECURITY.md CHANGELOG.md CLAUDE.md CONTRIBUTING.md README.md LICENSE
plans/enggenie-design-plan.md  references/{copilot,cursor,gemini,opencode}-tools.md  templates/spec-template.md
skills-lock.json                gitignored
```

## File-by-file: skills

### skills/dev-brainstorm/SKILL.md and skills/dev-plan/SKILL.md (+ agents/)
- What: renamed from architect-design / architect-plan (git detects as renames: 94% / 98%). Frontmatter `name`, announcements ("I'm using enggenie:dev-brainstorm ..."), exit handoffs and the word "Architect" changed by sed (`s/architect-design/dev-brainstorm/g; s/architect-plan/dev-plan/g; s/Architect/Dev/g`). dev-brainstorm/agents/explorer-agent.md; dev-plan/agents/{doc-discovery,explorer,plan-reviewer}-agent.md moved with them.
- Commit f6d57b3, then em-dash cleanup in 95f89fd.
- State: complete. Remaining: none known. Mirror copies exist in .agents/skills/.
- Dependencies: gateway skill routing table, pm-refine exit action, dev-implement entry text, memory-recall text.

### skills/enggenie/SKILL.md (gateway)
- What: overview sentence "PM, Dev, Reviewer, QA, Deploy"; routing table and All Skills table role column Architect -> Dev. Model recommendations table left as-is.
- State: complete for the rename. NOT updated for using-enggenie or for the hook (it does not mention it). Says nothing about 15 dirs.
- Remaining: decide whether the gateway and using-enggenie overlap (both are routing tables).

### skills/pm-refine/SKILL.md
- Estimation Method section replaced: T-shirt sizing XS/S/M/L/XL, "relative complexity - not hours", per-area rating, story rated as a whole, "If M or larger -> check decomposition", XL must be decomposed; team override via CLAUDE.md (T-shirt default, Fibonacci 1,2,3,5,8, Linear 1-10).
- Step 1 "Design artifact check" added (provided -> confirm approved; none -> note "No design artifact provided ... UX review recommended before implementation"; in progress -> flag provisional). "Design happens upstream of pm-refine."
- Exit Action: new step 1 "Design review checkpoint" invoking enggenie:review-design when a design artifact exists; steps renumbered (save spec to enggenie/spec_[slug].md, write Jira handoff, present, wait for approval).
- Frontmatter description now "sizing work (T-shirt)"; Team Configuration line 321 now "T-shirt (default), Fibonacci, linear".
- State: complete. Note: references/ dir under skills/pm-refine is empty on disk (untracked by git).
- Open [UNCERTAIN]: the word PROVISIONAL is a convention in docs/README/blog; the SKILL text says "flag the spec as provisional".

### skills/review-code/SKILL.md + agents/
- v3.0.0: Step 2 "Dispatch Three Lens Subagents in Parallel" (model sonnet, same diff/spec/round number), Step 3 Consolidation via agents/code-reviewer-agent.md, Step 4 "Act on Consolidated Findings"; severity table Blocking / Advisory / Observation / Wrong; section "Review Etiquette -- Rounds 2+" (ask the user for previous findings; if unavailable run as round 1); "Subagent Prompt Templates" (4 files); Subagent Context Preservation updated; Exit Condition "All Blocking and Advisory items are resolved".
- agents/security-lens-agent.md, engineering-lens-agent.md, test-lens-agent.md (new): domain list, What to Report (what/where/why/suggestion), severity classification, What Not to Report, Round Context, Output Format. engineering-lens includes a YAGNI grep guard (`grep -r "FunctionOrClassName" --include="*.{ts,js,py}" .`, one caller or unused = flag, multiple callers = do not).
- agents/code-reviewer-agent.md (rewritten, name kept): consolidation only (dedupe, keep higher severity, cite lens(es), single report, must not invent findings or re-review).
- v3.1.0 (8f5de95): "Step 0 -- Detect Existing Review Infrastructure" (see CODE_REFERENCE.md).
- State: v3.0.0 part COMPLETE and released; Step 0 PARTIAL (committed, unpushed, never run on a real repo with .github/agents).
- Remaining: line 31 still says "(Architect)" (stale); `## enggenie` config key `review_code.default_mode` is documented but not read.
- Mirror: .agents/skills/review-code in sync with skills/ as of 8f5de95.

### skills/dev-commit/SKILL.md
- v3.1.0: "Step 0: Detect Project Commit Conventions" before "Step 1: Analyze Staged Changes". Order: .claude/skills/using-git/SKILL.md, CLAUDE.md (`## Commit|## Git|commit convention|commit message`), .commitlintrc*, CONTRIBUTING.md / .github/CONTRIBUTING.md. First match wins, follow exclusively, announce "Using commit conventions from [source file]. enggenie defaults are overridden.", ask when ambiguous, never blend.
- State: PARTIAL (committed, unpushed). Not mirrored to .agents/skills (no dir). `dev_commit.conventions` key documented, not read.

### skills/qa-test/SKILL.md
- v3.1.0: "Platform Detection" section (package.json grep for react-native|detox|maestro|appium; ls metro.config.js android/ ios/; app.json grep expo) -> "Mobile Mode" (Detox, Maestro `.maestro/`, manual mobile checklist: deep links, push notifications, offline, background/foreground, orientation, OS versions, keyboard). Quick Reference table has "Platform detection" and "Mobile automation tools" rows. Web path (Playwright via scripts/with_server.py) unchanged.
- State: PARTIAL. `qa_test.platform` and `qa_test.mobile_runner` keys documented, not read. Mirror in .agents in sync for SKILL.md; scripts/with_server.py in the mirror differs from skills/ (pre-existing drift).

### skills/using-enggenie/SKILL.md (new, 46 lines)
- Content injected by the SessionStart hook. Wrapped in `<SUBAGENT-STOP>` and `<EXTREMELY_IMPORTANT>`; says "For ALL software development work, you MUST use enggenie skills"; routing table of 13 skills + gateway; instruction priority (user > enggenie > other suites for non-SDLC > default); "Skip enggenie for" quick questions etc. States "14 skills" although skills/ has 15 dirs (using-enggenie is a context skill).
- State: committed 4435dc7, unpushed, never verified in a fresh session. Not in CHANGELOG. Not in .agents mirror.

### Other skills (unchanged in the session except sed/em-dash edits)
dev-implement (+3 agents), dev-tdd (+3 references), dev-debug (+1 agent, 3 references), qa-verify, review-design (+1 agent), deploy-ship, memory-recall. Edits: architect names -> dev names (dev-implement, memory-recall), em-dashes -> hyphens. dev-implement line 32 still says "PM and/or Architect". dev-tdd canonical has a "Deep Rebuttals" section (about 52 lines) absent from the .agents mirror.

## File-by-file: hook and manifests

- hooks/hooks.json: SessionStart, matcher `startup|clear|compact`, command `"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd" session-start`, async false.
- hooks/run-hook.cmd: polyglot (batch + bash). Windows branch tries Git for Windows bash, then bash on PATH, else exits 0 silently; Unix branch `exec bash "${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"`.
- hooks/session-start: reads skills/using-enggenie/SKILL.md, JSON-escapes via bash parameter expansion, prints platform-specific JSON (Claude Code / Cursor / generic). Exits 0 if the skill file is missing. Modeled on the structure of another installed plugin's hook (inspected by a subagent; harness raised a SECURITY WARNING about executing it).
- .claude-plugin/plugin.json: version 2.6.0 -> 3.1.1; description without Architect; `"hooks": "./hooks/hooks.json"`; keywords unchanged.
- STALE (never touched): .claude-plugin/marketplace.json (2.0.0, description has Architect, marketplace name "enggenie-marketplace"), .cursor-plugin/plugin.json (2.0.0, Architect), gemini-extension.json (2.0.0, Architect).
- skills-lock.json (gitignored): keys renamed to dev-brainstorm / dev-plan with empty computedHash; local only.

## File-by-file: docs

- README.md: v3.0.0 agent rewrite, post-release Architect fix (4aaf247), then full overhaul in a85e036 (505 lines, 3292 words): hero before/after, "What this is" (and isn't), "Who it is for" (EM, Dev, PM), "Design philosophy" (4 principles), heist TDD RED/GREEN session, security-lens Blocking example, skills table with WHY column (14 rows), before/after multi-lens, "Your first three sessions", Mermaid adoption diagram, optional integrations, documentation map by role. Still states v3.0.0-level features; says 14 skills.
- CHANGELOG.md: top entries [3.1.1] and [3.1.0] (2026-06-22), [3.0.0] and [2.7.0] (2026-06-01). 3.1.1 lists the docs set but NOT the SessionStart hook / using-enggenie / plugin.json bump. Contains 20 em-dashes (history entries).
- CLAUDE.md (repo): "14 skills across 6 roles"; Pre-Release Verification Gate (8 steps, see TRANSFER.md and STATUS.md); 10 em-dashes; mentions superpowers (lines around 103-154).
- docs/guides/adopting.md (new, v3.0.0): 5 stages - Observe; Spec and Plan; TDD-Guided Build; Full Pipeline; Optional Integrations.
- docs/examples/adr-timer-approach.md (ADR-001 heist session timer: client-side countdown from stored timestamp) and adr-storage-strategy.md (localStorage vs Firestore hybrid, TypeScript hooks).
- docs/getting-started/claude-code.md: Architect line merged into Dev; review-code row notes 3-lens; What's Next links adopting.md and ADR examples. cursor.md, copilot-cli.md, gemini-cli.md, opencode.md: NOT updated for v3.
- docs/guides/team-customization.md (new, 8f5de95 + section in 2a057d6): detection tables, `## enggenie` config examples, rn-hudl example, "Working alongside other plugin suites" (superpowers conflict, `## AI Skills Priority` CLAUDE.md snippet), explicit invocation tips.
- docs/guides/jira-mcp.md, docs/guides/memory-recall.md (new, 2a057d6): fill broken README links. jira-mcp.md describes `claude mcp add atlassian` and prompts for domain/email/API token (names only).
- ARCHITECTURE.md, SECURITY.md (contact email at the hudl.com domain), docs/faq.md, .github templates (2a057d6).
- plans/enggenie-design-plan.md: 141 em-dashes left; architect names sed-replaced.
- docs/verification/: skill-verification-report.md (17768 B), superpowers-vs-enggenie-comparison.md (9877 B) - untracked, pre-existing artifacts from the repo's own release gate (CLAUDE.md says commit only if the user asks).
- docs/blog/enggenie-medium-post.md (tracked, original launch post, 15205 B, still uses Architect in lines 46, 305, 306, 319).
- docs/blog/enggenie-v3-medium-post.md (UNTRACKED, 17690 B, 362 lines): final comprehensive draft; title on disk "I Gave My AI a Whole Team of Reviewers. Here's What It Found That One Reviewer Missed."; subtitle "Enggenie v3.0.0: three-lens code review, architecture decisions that survive the sprint, and specs that ask where the design is before anyone writes a line."; placeholders 3 [GIF:], 3 [SCREENSHOT:], 2 [IMAGE:].
- docs/blog/assets/ (UNTRACKED): diagrams/{three-lens-flow,adr-flow}.mmd, images/{three-lens-flow,adr-flow}.png (rendered Jun 1 15:21 local), carbon/01..06 .txt (text for carbon.now.sh; 02, 04, 06 contain em-dashes), render-diagrams.sh (755). The 6 Carbon PNGs do not exist.

## Dependencies and external state

- ~/.claude/CLAUDE.md "AI Skills Priority" section (outside the repo; present and verified in this machine's loaded context).
- Memory files in ~/.claude/projects/-Users-badru-siddique--claude/memory/: feedback_enggenie_design_principles.md (created in session), plus pre-existing project_enggenie.md (STALE: 13 skills, architect names, 7 roles), feedback_commit_style.md, feedback_no_superpowers_refs.md, feedback_qa_verification.md, feedback_no_emdash.md.
- GitHub (changed directly with gh, public): description "Role-based SDLC skill suite for AI coding assistants. 14 skills across PM, Dev, Reviewer, QA, and Deploy roles. Works with Claude Code, Cursor, Copilot CLI, Gemini CLI, and OpenCode."; 19 topics: agile, ai-skills, claude-code, code-review, copilot, cursor, developer-tools, gemini, qa-testing, sdlc, tdd, claude-code-plugin, claude-plugin, gemini-cli-extension, agent-skills, claude-skill, skill-md, llm, opencode (removed skill-md-skillsmp and skills). Releases created: v2.7.0, v3.0.0.
- Optional runtime integrations referenced by skills: Atlassian MCP (Jira handoff), claude-mem plugin (memory-recall).

## What remains (summary; ordered list in NEXT_STEPS.md)

Push 4 commits and tag; fix stale manifests and "Architect" leftovers; wire or de-document the `## enggenie` config keys; update CHANGELOG for the hook; resolve skill-count and superpowers-mention rulings; mirror/sync .agents; finish and publish blog assets; update 4 getting-started guides; run an actual verification gate.
