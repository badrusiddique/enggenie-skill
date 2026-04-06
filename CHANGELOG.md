# Changelog

All notable changes to enggenie are documented here.

Format: [Semantic Versioning](https://semver.org/). Each version lists what was added, changed, or fixed.

---

## [2.6.0] - 2026-04-06

### Added
- **Jira ticket entry for cold-start skills** — architect-design, review-code, review-design, and qa-verify can now be picked up by someone with no prior context by reading the Jira ticket
- **Jira soft fallback for dev-commit** — prompts for ticket ID when no ticket is in context, for better commit messages and traceability
- **Jira soft fallback for deploy-ship** — prompts for ticket ID when creating a PR, for richer PR summaries and ticket status updates
- **Unified artifact directory** — all skill-generated files now save to `enggenie/` with role prefixes (`spec_`, `design_`, `adr_`, `decision_`, `plan_`) so all feature artifacts are co-located

### Changed
- 8 skill files enhanced (architect-design, architect-plan, pm-refine, review-code, review-design, qa-verify, dev-commit, deploy-ship)
- Artifact paths consolidated: `specs/`, `plans/`, `docs/enggenie/specs/`, `docs/enggenie/adrs/`, `docs/enggenie/decisions/` all replaced with unified `enggenie/` directory
- Every skill that can be picked up cold now has Jira context reading or a soft fallback prompt

---

## [2.5.0] - 2026-04-06

### Added
- **Jira-based handoff protocol across SDLC roles** — the Jira ticket becomes the living contract between PM, Dev, and QA. Each role reads context from the ticket and writes back for the next role.
- **pm-refine: Handoff Context (Step 7)** — writes structured "For Dev" and "For QA" sections into the Jira ticket with spec links, key decisions, edge cases, and constraints
- **architect-plan: Jira ticket entry** — reads PM's handoff context from the Jira ticket, extracts spec path and decisions, writes back plan file link and design decisions as a comment
- **dev-implement: Jira ticket entry** — reads ticket for spec path, plan link, and PM/Architect context before starting implementation
- **deploy-ship: Dev Handoff to QA** — writes structured comment to Jira with PR link, what was built vs planned, spec deviations, known limitations, test coverage, and QA focus areas
- **qa-test: Jira ticket entry** — reads PM's "For QA" section and Dev's "Dev Handoff" comment to get full chain context (spec → implementation → what to test)
- **qa-test: QA Results writeback** — writes test results, bugs found, automation coverage back to Jira ticket
- **dev-debug: Jira bug entry** — reads QA Results comment for bug reproduction steps, writes back root cause and fix PR
- **Gateway: Jira ticket routing** — "Pick up PROJ-1234" auto-detects the ticket's phase (fresh → plan, has PR → QA, has bugs → debug) and routes to the right skill

### Changed
- 7 skill files enhanced (pm-refine, architect-plan, dev-implement, deploy-ship, qa-test, dev-debug, enggenie gateway)
- All enhancements are additive — zero original content removed or modified
- The handoff protocol works with or without Jira MCP — when MCP is unavailable, handoff sections are written to spec files and output for manual Jira updates

---

## [2.4.0] - 2026-04-03

### Added
- **Deep anti-rationalization rebuttals in dev-tdd** - 5 multi-paragraph arguments dismantling the most dangerous TDD shortcuts (tests-after, sunk cost, dogmatism, pragmatism, spirit-vs-letter)
- **Architectural problem pattern indicators in dev-debug** - 3-Attempt Rule now includes specific patterns to recognize (hidden coupling, cascading symptoms, inertia) and explicit "question fundamentals" self-check
- **External feedback verification checklist in review-code** - 5-point checklist for evaluating suggestions from team and external reviewers before implementing, plus "I cannot verify this" admission pattern
- **Private pushback escape in review-code** - guidance for flagging concerns to user privately when public pushback would create friction
- **YAGNI power-dynamics framing in review-code** - escalation path for YAGNI disagreements (user decides, not reviewer)
- **Parallel dispatch decision criteria in dev-implement** - decision tree for evaluating task independence, agent prompt quality guidelines (Focused, Self-contained, Specific), and common dispatch mistakes table
- **Visual companion decision framework in architect-design** - per-question visual-vs-terminal decision test, 5 visual cases, 5 text cases, consent-first browser offering, Mermaid/ASCII fallback
- **Active Shortcut Tax surfacing in dev-commit** - directive to show relevant Shortcut Tax row to users when they attempt a commit shortcut

### Changed
- 6 skill files enhanced (dev-tdd, dev-debug, review-code, dev-commit, dev-implement, architect-design)
- All enhancements are additive — zero original content removed or modified

---

## [2.3.0] - 2026-04-03

### Added
- **Real-world SDLC scenario table** - 35+ scenarios mapping everyday developer activities to skills in the README (refinement, brainstorming, TDD, debugging, code review, QA, deployment, and more)
- **Mermaid flow diagram** - color-coded pipeline visualization replacing ASCII art in both README and how-it-works guide

---

## [2.2.0] - 2026-04-03

### Fixed
- **Model selection wait gate** - all 13 domain skills now explicitly stop and wait for user confirmation on model selection before proceeding (previously asked but did not wait for response)

---

## [2.1.0] - 2026-04-03

### Fixed
- **Security audit remediation** - removed external file path references (`agents/*.md`, `scripts/*.py`) flagged by skills.sh Gen, Snyk, and Socket scanners in architect-plan, pm-refine, and qa-test
- **Jira ticket creation gate** - pm-refine now requires explicit user approval before creating Jira tickets
- **Generic server lifecycle guidance** - qa-test replaced hardcoded script reference with pattern-based guidance

### Changed
- Subagent descriptions inlined directly in skill files instead of referencing external prompt template paths

---

## [2.0.0] - 2026-04-02

### Added
- **Model recommendations per skill** - each skill now suggests the optimal model (opus/sonnet/haiku) with reasoning, and asks for user confirmation
- **enggenie:dev-commit** - new skill for crafting conventional commit messages with emoji types, diff analysis, and mandatory user approval (14th skill)
- **Subagent context preservation** - all skills that dispatch subagents now include explicit instructions to capture key findings back to the main conversation
- **Plans directory convention** - architect-plan now saves plans to `/plans` by default for easy revisiting

### Changed
- Skill count: 13 -> 14 (added dev-commit)
- Plugin version bumped to 2.0.0

---

## [1.3.0] - 2026-04-02

### Added
- E2E QA test plan with 51 test cases across all 5 platforms
- Glossary of key terms (skill, plugin, TDD, subagent, SDLC, worktree) in getting-started docs
- Prerequisites section with Node.js requirement
- Platform recommendation for beginners (start with Claude Code)

### Changed
- Getting-started README restructured with quick glossary table

---

## [1.2.0] - 2026-04-02

### Added
- Plugin discovery guide covering 6 directories (skills.sh, ClaudePluginHub, SkillsMP, Gemini Extensions Gallery, Cursor Marketplace, Awesome OpenCode)
- README plugin discovery section with marketplace table
- GitHub topics for discoverability: `gemini-cli-extension`, `cursor-plugin`, `copilot-extension`, `opencode-plugin`

### Changed
- README improved for accessibility across all skill levels (beginner, PM, junior, senior, expert)
- Expanded TDD, SDLC, and subagent definitions inline

---

## [1.1.0] - 2026-04-02

### Added
- Getting-started guides for all 5 platforms: Claude Code, Cursor, GitHub Copilot CLI, Google Gemini CLI, OpenCode.ai
- Universal install via `npx skills add badrusiddique/enggenie-skill` (skillkit.sh)
- Platform-specific tool name mapping references
- `.gitignore` for skills.sh generated files
- Strict mode in plugin manifest for discovery indexing

### Changed
- README install instructions corrected for Claude Code marketplace workflow
- Gateway skill platform reference paths fixed (relative to skill location)

---

## [1.0.0] - 2026-04-02

### Added
- **13 skills across 7 roles** covering the entire SDLC
  - PM: `enggenie:pm-refine` - spec generation, story refinement, estimation
  - Architect: `enggenie:architect-design` - brainstorming, ADRs, technical decisions
  - Architect: `enggenie:architect-plan` - phased implementation plans
  - Dev: `enggenie:dev-implement` - subagent-driven TDD execution
  - Dev: `enggenie:dev-tdd` - TDD discipline (RED-GREEN-REFACTOR)
  - Dev: `enggenie:dev-debug` - systematic 4-phase root cause investigation
  - Reviewer: `enggenie:review-code` - request and receive code reviews
  - Reviewer: `enggenie:review-design` - frontend/UI design quality
  - QA: `enggenie:qa-verify` - evidence before completion claims
  - QA: `enggenie:qa-test` - Playwright automation and manual browser testing
  - Deploy: `enggenie:deploy-ship` - commits, PRs, Jira updates
  - Memory: `enggenie:memory-recall` - cross-session context
  - Gateway: `enggenie` - routes to the right skill
- 15 agent prompt templates for subagent dispatch
- 10 reference docs (5 technique, 4 platform tool mappings, 1 spec template)
- `with_server.py` for Playwright server lifecycle management
- Plugin manifests for Claude Code, Cursor, and Gemini CLI
- Comprehensive usage examples for all 13 skills
- Full feature walkthrough, debug session, code review, and QA testing examples
- MIT license
