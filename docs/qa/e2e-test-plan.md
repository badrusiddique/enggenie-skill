# enggenie Skill Suite - End-to-End QA Test Plan

**Version:** 1.0
**Date:** 2026-04-02
**Product:** enggenie-skill (SDLC skill suite plugin for AI coding assistants)

---

## 1. Summary

This document defines a comprehensive end-to-end QA test plan for the enggenie skill suite plugin. enggenie provides 14 skills across 7 roles (PM, Architect, Dev, Reviewer, QA, Deploy, Memory) and supports 5 AI coding assistant platforms. The plan covers installation, individual skill activation, cross-skill integration, platform-specific behavior, and negative/edge cases.

**Scope:**
- 51 total test cases: 26 P1 (critical path), 25 P2 (important but non-blocking)
- All 14 skills validated individually
- Cross-skill handoff chains verified
- All 5 supported platforms covered
- Negative and edge case scenarios included

**Out of Scope:**
- Performance/load testing
- Security penetration testing
- Upstream AI model behavior validation

---

## 2. Test Environment Requirements

| Requirement | Details |
|---|---|
| **Node.js** | v18+ with npx available |
| **Claude Code** | Latest stable release |
| **Cursor** | Latest stable release |
| **GitHub Copilot CLI** | Latest stable release |
| **Google Gemini CLI** | Latest stable release |
| **OpenCode.ai** | Latest stable release |
| **OS** | macOS (primary), Linux, Windows (secondary) |
| **Git** | v2.30+ with a test repository initialized |
| **Network** | Internet access for package installation |
| **Test Repository** | A sample project with source code, tests, and a README for skill exercises |

---

## 3. Execution Notes

- Execute all P1 tests before P2 tests. A P1 failure blocks release.
- Platform-specific tests (Category: Platform) require the corresponding tool installed and configured.
- For skill activation tests, type the prompt exactly as written in the Steps column and observe whether the correct skill engages.
- Cross-skill integration tests must be run sequentially within a single session to validate state handoff.
- Record pass/fail in the Status column. For failures, open an issue with the Test ID and reproduction steps.
- "Expected Result" describes observable behavior - exact wording from the assistant may vary, but the described behavior must occur.

---

## 4. Test Cases

### 4.1 Installation & Setup

| ID | Priority | Category | Test Name | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-001 | P1 | Install | Universal install via npx | 1. Run `npx skills add badrusiddique/enggenie-skill` in a terminal. 2. Verify command exits 0. 3. Check that skill files are present in the expected directory. | Installation completes without errors. Skill configuration files are created. | |
| TC-002 | P1 | Install | Claude Code native install - marketplace add | 1. In Claude Code, run `/plugin marketplace add badrusiddique/enggenie-skill`. 2. Observe output. | Plugin is added to the marketplace registry. Confirmation message displayed. | |
| TC-003 | P1 | Install | Claude Code native install - plugin install | 1. After TC-002, run `/plugin install enggenie@badrusiddique-enggenie-skill`. 2. Observe output. | Plugin installs successfully. All 14 skills are registered. | |
| TC-004 | P1 | Install | Claude Code native install - reload plugins | 1. After TC-003, run `/reload-plugins`. 2. Verify skills are available. | Plugins reload without error. enggenie skills are active and discoverable. | |
| TC-005 | P2 | Install | Cursor platform install | 1. Run `npx skills add badrusiddique/enggenie-skill` from a Cursor-integrated terminal. 2. Open Cursor and verify skill availability. | Skills are recognized by Cursor. No configuration errors. | |
| TC-006 | P2 | Install | GitHub Copilot CLI platform install | 1. Run `npx skills add badrusiddique/enggenie-skill`. 2. Verify skills are accessible from GitHub Copilot CLI. | Skills are registered and invocable within Copilot CLI. | |
| TC-007 | P2 | Install | Google Gemini CLI platform install | 1. Run `npx skills add badrusiddique/enggenie-skill`. 2. Verify skills are accessible from Gemini CLI. | Skills are registered and invocable within Gemini CLI. | |
| TC-008 | P2 | Install | OpenCode.ai platform install | 1. Run `npx skills add badrusiddique/enggenie-skill`. 2. Verify skills are accessible from OpenCode.ai. | Skills are registered and invocable within OpenCode.ai. | |
| TC-009 | P1 | Install | Reinstall / upgrade over existing install | 1. With enggenie already installed, run `npx skills add badrusiddique/enggenie-skill` again. 2. Verify no duplicates and latest version is present. | Existing installation is updated cleanly. No duplicate skill registrations. | |

### 4.2 Individual Skill Activation

| ID | Priority | Category | Test Name | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-010 | P1 | Skill | enggenie gateway activation | 1. Prompt: "What can enggenie do?" 2. Observe response. | The gateway skill activates. Response lists available roles and skills with usage guidance. | |
| TC-011 | P1 | Skill | pm-refine activation | 1. Prompt: "Refine this feature idea: users should be able to export reports as PDF." 2. Observe response. | pm-refine skill activates. Response includes clarifying questions, acceptance criteria, or a refined requirements statement. | |
| TC-012 | P1 | Skill | architect-design activation | 1. Prompt: "Design the architecture for a notification microservice." 2. Observe response. | architect-design skill activates. Response includes system components, data flow, and technology considerations. | |
| TC-013 | P1 | Skill | architect-plan activation | 1. Prompt: "Create an implementation plan for the notification service." 2. Observe response. | architect-plan skill activates. Response includes phased plan with milestones, dependencies, and task breakdown. | |
| TC-014 | P1 | Skill | dev-implement activation | 1. Prompt: "Implement a REST endpoint for creating a new user." 2. Observe response. | dev-implement skill activates. Response includes working code with proper structure and conventions. | |
| TC-015 | P1 | Skill | dev-tdd activation and RED-GREEN-REFACTOR | 1. Prompt: "Use TDD to build a string calculator function." 2. Observe response. | dev-tdd skill activates. Response follows RED-GREEN-REFACTOR discipline: writes a failing test first (RED), then minimal code to pass (GREEN), then refactors (REFACTOR). | |
| TC-016 | P1 | Skill | dev-debug activation and 4-phase methodology | 1. Prompt: "Debug this error: TypeError: Cannot read property 'map' of undefined." Provide a code snippet. 2. Observe response. | dev-debug skill activates. Response follows systematic 4-phase debugging: reproduce, isolate, identify root cause, fix with verification. | |
| TC-017 | P1 | Skill | review-code activation | 1. Prompt: "Review this pull request code" and provide a code diff or snippet. 2. Observe response. | review-code skill activates. Response provides structured code review with findings, severity, and suggestions. | |
| TC-018 | P1 | Skill | review-design activation | 1. Prompt: "Review this UI component against the design system." Provide component code. 2. Observe response. | review-design skill activates. Response evaluates design system compliance, responsive behavior, accessibility, and state coverage. | |
| TC-019 | P1 | Skill | qa-verify activation | 1. Prompt: "Verify that the user registration feature meets these acceptance criteria: [list criteria]." 2. Observe response. | qa-verify skill activates. Response systematically checks each criterion with evidence before making claims. | |
| TC-020 | P1 | Skill | qa-test activation | 1. Prompt: "Generate test cases for a shopping cart checkout flow." 2. Observe response. | qa-test skill activates. Response includes structured test cases covering happy path, edge cases, and error scenarios. | |
| TC-021 | P1 | Skill | deploy-ship activation | 1. Prompt: "Commit my changes and create a PR." 2. Observe response. | deploy-ship skill activates. Response includes conventional commit message proposal and PR creation workflow. | |
| TC-022 | P1 | Skill | memory-recall activation | 1. Prompt: "What do you remember about the previous architecture decisions?" 2. Observe response. | memory-recall skill activates. Response retrieves and presents relevant stored context from prior interactions (or gracefully reports none found). | |

### 4.3 Cross-Skill Integration

| ID | Priority | Category | Test Name | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-023 | P1 | Integration | PM to Architect handoff (pm-refine -> architect-design) | 1. Use pm-refine to refine a feature. 2. Then prompt: "Now design the architecture for this feature." 3. Observe whether architect-design picks up the refined requirements. | architect-design activates with context from pm-refine output. The design references the refined requirements without re-prompting. | |
| TC-024 | P1 | Integration | Architect to Dev handoff (architect-plan -> dev-implement) | 1. Use architect-plan to create an implementation plan. 2. Then prompt: "Implement phase 1 of the plan." 3. Observe context continuity. | dev-implement activates and references the plan's phase 1 tasks. Code aligns with the architectural decisions. | |
| TC-025 | P1 | Integration | Full SDLC chain: refine -> design -> plan -> implement | 1. pm-refine a feature. 2. architect-design the solution. 3. architect-plan the implementation. 4. dev-implement the first component. | Each skill activates in sequence. Context carries forward through all stages. Final implementation traces back to original requirements. | |
| TC-026 | P1 | Integration | Dev to Review handoff (dev-implement -> review-code) | 1. Use dev-implement to generate code. 2. Prompt: "Now review the code you just wrote." | review-code activates and reviews the previously generated code. Findings reference specific lines from the implementation. | |
| TC-027 | P1 | Integration | TDD to QA handoff (dev-tdd -> qa-verify) | 1. Use dev-tdd to build a feature with tests. 2. Prompt: "Verify this implementation meets the acceptance criteria." | qa-verify activates. Verification references both the code and the tests produced by dev-tdd. | |
| TC-028 | P2 | Integration | Review to Debug handoff (review-code -> dev-debug) | 1. Use review-code and surface a bug. 2. Prompt: "Debug the issue found in the review." | dev-debug activates and targets the specific issue identified during code review. | |
| TC-029 | P2 | Integration | QA to Deploy handoff (qa-test -> deploy-ship) | 1. Use qa-test to generate and run test cases. 2. Prompt: "Ship this feature to production." | deploy-ship activates. Deployment plan acknowledges QA coverage and includes test validation as a gate. | |
| TC-030 | P2 | Integration | Full cycle with memory (memory-recall at start) | 1. In a new session, prompt: "Recall what we decided about the notification service." 2. Then continue with architect-plan. | memory-recall retrieves prior context. Subsequent architect-plan skill uses recalled context as input. | |
| TC-031 | P1 | Integration | Design review integration (architect-design -> review-design) | 1. Use architect-design to produce a system design. 2. Prompt: "Review this design for issues." | review-design activates and evaluates the architecture just produced, providing evidence-based critique. | |

### 4.4 Platform-Specific Behavior

| ID | Priority | Category | Test Name | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-032 | P1 | Platform | Claude Code - all 14 skills discoverable | 1. Install on Claude Code. 2. Activate each of the 14 skills by name or intent. | All 14 skills respond correctly on Claude Code. No missing or broken skill registrations. | |
| TC-033 | P2 | Platform | Cursor - skill activation via intent | 1. Install on Cursor. 2. Prompt with intent for pm-refine, dev-implement, and qa-test. | Skills activate automatically based on user intent in Cursor. | |
| TC-034 | P2 | Platform | GitHub Copilot CLI - skill activation via intent | 1. Install on Copilot CLI. 2. Prompt with intent for architect-design and deploy-ship. | Skills activate correctly within the Copilot CLI environment. | |
| TC-035 | P2 | Platform | Google Gemini CLI - skill activation via intent | 1. Install on Gemini CLI. 2. Prompt with intent for dev-tdd and review-code. | Skills activate correctly within the Gemini CLI environment. | |
| TC-036 | P2 | Platform | OpenCode.ai - skill activation via intent | 1. Install on OpenCode.ai. 2. Prompt with intent for dev-debug and memory-recall. | Skills activate correctly within the OpenCode.ai environment. | |
| TC-037 | P2 | Platform | Cross-platform consistency - same prompt, same skill | 1. Use the same prompt ("Refine this feature: user login with MFA") on Claude Code, Cursor, and one other platform. 2. Compare which skill activates. | pm-refine activates on all tested platforms. Output structure is consistent across platforms. | |
| TC-038 | P1 | Platform | Claude Code - /reload-plugins refreshes skills | 1. Modify a skill config locally. 2. Run `/reload-plugins`. 3. Verify the updated behavior takes effect. | Skills reload with updated configuration. No stale state persists. | |

### 4.5 Negative & Edge Cases

| ID | Priority | Category | Test Name | Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-039 | P1 | Negative | Ambiguous prompt - no clear skill match | 1. Prompt: "Help me with my project." 2. Observe response. | The enggenie gateway skill activates or the assistant asks clarifying questions. No incorrect skill fires silently. | |
| TC-040 | P2 | Negative | Empty prompt | 1. Send an empty or whitespace-only prompt. 2. Observe behavior. | No skill crashes. The assistant handles gracefully, requesting input. | |
| TC-041 | P2 | Negative | Conflicting intent - multiple skills match | 1. Prompt: "Write tests for this code and also review it." 2. Observe which skill(s) activate. | The assistant either sequences the skills logically (dev-tdd then review-code) or asks the user to clarify priority. No conflict or crash. | |
| TC-042 | P1 | Negative | Invoke skill before installation | 1. On a clean environment (no enggenie installed), prompt with skill intent. 2. Observe behavior. | The assistant does not crash. Skills are simply not available. Standard assistant behavior occurs. | |
| TC-043 | P2 | Negative | Very large input to a skill | 1. Provide a 500+ line code file to review-code. 2. Observe handling. | review-code handles the large input without truncation errors or crashes. Review covers key sections. | |
| TC-044 | P2 | Negative | Unsupported language/framework in dev-implement | 1. Prompt: "Implement a COBOL batch processing routine." 2. Observe response. | dev-implement activates and either provides best-effort implementation or clearly states limitation. No crash. | |
| TC-045 | P1 | Negative | Uninstall and verify clean removal | 1. Uninstall enggenie. 2. Verify no residual skill registrations remain. 3. Verify assistant returns to default behavior. | Clean removal with no orphaned files or registrations. Skills no longer activate. | |
| TC-046 | P2 | Negative | Network interruption during install | 1. Start `npx skills add badrusiddique/enggenie-skill`. 2. Disconnect network mid-install. 3. Observe error handling. | Installation fails gracefully with a clear error message. No partial/corrupt state left behind. | |
| TC-047 | P2 | Negative | dev-tdd with code that has no testable units | 1. Prompt: "Use TDD for this CSS stylesheet." Provide a CSS file. 2. Observe response. | dev-tdd activates and either adapts approach or explains why TDD is not applicable for the input. No crash. | |
| TC-048 | P2 | Negative | deploy-ship with no code context | 1. In a fresh session with no prior code, prompt: "Ship to production." 2. Observe response. | deploy-ship activates and asks for necessary context (what to deploy, where, configs) rather than producing an empty plan. | |
| TC-049 | P2 | Negative | memory-recall with no prior memory | 1. In a completely fresh environment, prompt: "Recall our previous decisions." 2. Observe response. | memory-recall activates and gracefully reports no prior context found. No error or hallucinated history. | |
| TC-050 | P2 | Negative | Rapid skill switching | 1. In quick succession: prompt for pm-refine, then immediately dev-debug, then qa-test. 2. Observe each activation. | Each skill activates correctly in sequence. No state bleed between skills. No crashes from rapid transitions. | |
| TC-051 | P1 | Negative | dev-debug without error context | 1. Prompt: "Debug this." with no code or error provided. 2. Observe response. | dev-debug activates and requests necessary context (error message, code, reproduction steps) rather than guessing. | |

---

## 5. Priority Summary

| Priority | Count | Description |
|---|---|---|
| **P1** | **26** | Critical path - must pass for release. Covers installation, all 13 skill activations, key integration chains, and critical negative cases. |
| **P2** | **25** | Important validation - should pass for release. Covers secondary platforms, edge cases, and extended integration scenarios. |
| **Total** | **51** | |

### P1 Test IDs
TC-001, TC-002, TC-003, TC-004, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015, TC-016, TC-017, TC-018, TC-019, TC-020, TC-021, TC-022, TC-023, TC-024, TC-025, TC-026, TC-027, TC-031, TC-032, TC-038, TC-039, TC-042, TC-045, TC-051

### P2 Test IDs
TC-005, TC-006, TC-007, TC-008, TC-028, TC-029, TC-030, TC-033, TC-034, TC-035, TC-036, TC-037, TC-040, TC-041, TC-043, TC-044, TC-046, TC-047, TC-048, TC-049, TC-050

---

## 6. Exit Criteria

- **Pass for release:** All 26 P1 tests pass. No more than 3 P2 tests fail, and none of those failures indicate data loss or corruption.
- **Conditional release:** All P1 tests pass. 4-6 P2 failures are accepted with filed issues and a follow-up fix timeline.
- **Block release:** Any P1 test fails.

---

## 7. Risks & Assumptions

| Risk | Mitigation |
|---|---|
| Platform CLI updates may change plugin interfaces | Pin tested CLI versions in environment requirements; re-test on upgrade |
| Intent-based activation may vary with underlying model changes | Test on the specific model versions used in production; document model versions in results |
| Memory-recall depends on session persistence mechanisms | Validate memory storage format before testing recall; test both same-session and cross-session recall |
| Network-dependent install steps are flaky in CI | Run install tests with retry logic; separate network tests from functional tests |
