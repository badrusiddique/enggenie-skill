# Changelog

All notable changes to enggenie are documented in this file.

## [1.0.0] - 2026-04-02

### Added

- Initial release: 13 skills across 7 roles (PM, Architect, Dev, Reviewer, QA, Deploy, Memory)
- **enggenie** -- Gateway skill that routes ambiguous intent to the right specialist
- **enggenie:pm-refine** -- Spec generation, story refinement, spike planning, estimation with transparent math
- **enggenie:architect-design** -- Brainstorming, ADRs, technical discussions in 3 modes
- **enggenie:architect-plan** -- Phased implementation plans with deployment readiness gates
- **enggenie:dev-implement** -- Subagent-driven TDD execution with two-stage review gate
- **enggenie:dev-tdd** -- RED-GREEN-REFACTOR discipline overlay active during all coding
- **enggenie:dev-debug** -- Systematic 4-phase root cause investigation with 3-attempt rule
- **enggenie:review-code** -- Request and receive code reviews with technical evaluation
- **enggenie:review-design** -- Frontend/UI quality review: design system, states, responsive, accessibility
- **enggenie:qa-verify** -- Evidence-based verification before any completion claim
- **enggenie:qa-test** -- Playwright automation and manual browser testing with QA mindset
- **enggenie:deploy-ship** -- Conventional commits, PR creation, Jira updates, branch completion
- **enggenie:memory-recall** -- Cross-session context via claude-mem with 3-layer retrieval
- 14 agent prompt templates across 8 skills
- 5 reference docs (testing-anti-patterns, defense-in-depth, root-cause-tracing, multi-component-debugging, condition-based-waiting)
- 4 platform adapters (Cursor, GitHub Copilot CLI, Google Gemini CLI, OpenCode)
- Default spec template
- Getting-started guide for Claude Code
- Team customization support (spec templates, commit format, estimation method, architecture context, Jira project key)
