# {FEATURE_TITLE}

## Summary

**What:** {ONE_SENTENCE_DESCRIPTION}
**Why:** {BUSINESS_VALUE_OR_USER_NEED}

## Architecture Context

{SYSTEM_DIAGRAM_IF_MULTI_SERVICE}

List of services involved:

- {SERVICE_1}
- {SERVICE_2}

## Repos/Services in Scope

| Repo/Service | Role | Changes |
|-------------|------|---------|
| {REPO_1} | {ROLE} | {CHANGES} |
| {REPO_2} | {ROLE} | {CHANGES} |

## Functional Requirements

1. {REQUIREMENT_1} — Acceptance: {TEST_CONDITION}
2. {REQUIREMENT_2} — Acceptance: {TEST_CONDITION}
3. {REQUIREMENT_3} — Acceptance: {TEST_CONDITION}

## Figma Design Reference

{FIGMA_LINK_OR_NA}

If provided, note: key dimensions, design tokens, colors, layout constraints.

## Implementation Order

Phased, downstream-first. Each phase is independently deployable.

### Phase 1 — {DOWNSTREAM_SERVICE}

- [ ] {WHAT_TO_BUILD}
- [ ] {WHAT_TO_BUILD}
- [ ] Deployment readiness: {CHECKLIST_ITEM}

### Phase 2 — {MIDDLEWARE_SERVICE}

Depends on: Phase 1 deployed

- [ ] {WHAT_TO_BUILD}
- [ ] {WHAT_TO_BUILD}
- [ ] Deployment readiness: {CHECKLIST_ITEM}

### Phase 3 — {UPSTREAM_SERVICE}

Depends on: Phase 2 deployed

- [ ] {WHAT_TO_BUILD}
- [ ] Deployment readiness: {CHECKLIST_ITEM}

## Acceptance Criteria

### User-Level

- [ ] As a user, I can {USER_ACTION_1}
- [ ] As a user, I can {USER_ACTION_2}
- [ ] As a user, I see {EXPECTED_BEHAVIOR}

### Technical (per service)

- [ ] {SERVICE_1}: {TECHNICAL_CRITERION}
- [ ] {SERVICE_2}: {TECHNICAL_CRITERION}
- [ ] {SERVICE_3}: {TECHNICAL_CRITERION}

## Edge Cases

1. What if {EDGE_CASE_1}?
2. What if {EDGE_CASE_2}?
3. What if {EDGE_CASE_3}?

## Open Questions

1. {SCOPE_QUESTION}
2. {INTEGRATION_QUESTION}
3. {EDGE_CASE_QUESTION}

## Manual QA Test Plan

| Scenario | Steps | Expected | Dev Result | QA Result |
|----------|-------|----------|------------|-----------|
| {SCENARIO_1} | {STEPS} | {EXPECTED} | | |
| {SCENARIO_2} | {STEPS} | {EXPECTED} | | |
| {SCENARIO_3} | {STEPS} | {EXPECTED} | | |

## Playwright Automation Scenarios

| Test | File Location | Covers |
|------|--------------|--------|
| {TEST_NAME_1} | {FILE_PATH} | {ACCEPTANCE_CRITERIA_COVERED} |
| {TEST_NAME_2} | {FILE_PATH} | {ACCEPTANCE_CRITERIA_COVERED} |

## Documentation Checklist

- [ ] API docs updated
- [ ] README updated
- [ ] Architecture diagram updated (if applicable)
- [ ] Runbook updated (if applicable)

## Jira Ticket Structure

**Story:** {FEATURE_TITLE}
**Points:** {RAW_ESTIMATE} -> +20% buffer -> Fibonacci -> Cap at 8

| Subtask | Area | Estimate |
|---------|------|----------|
| {SUBTASK_1} | {AREA} | {ESTIMATE} |
| {SUBTASK_2} | {AREA} | {ESTIMATE} |
| QA Testing | QA | {ESTIMATE} |
| BA Review | BA | {ESTIMATE} |
