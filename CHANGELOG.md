# Changelog

All notable changes to enggenie are documented here.

Format: [Semantic Versioning](https://semver.org/). Each version lists what was added, changed, or fixed.

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
