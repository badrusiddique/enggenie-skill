---
name: architect-plan
description: Use when creating implementation plans from specs or requirements - phased task breakdown with deployment readiness gates before any coding begins
---

# enggenie:architect-plan

Create implementation plans that are phased, independently deployable, and contain complete code in every step. No placeholders. No hand-waving. Every phase can be deployed to production before the next phase begins. If a step says "write a test," the actual test code is right there. If a step says "add a route," the route definition is spelled out.

This is not a flat task list. This is a deployment-sequenced plan with gates between phases. Each phase ships alone or it does not ship at all.

---

## Announcement

When this skill is invoked, announce:

> I'm using enggenie:architect-plan to create an implementation plan.

---

## Entry Conditions

Activate this skill when ANY of the following are true:

- An approved design exists from enggenie:architect-design
- An approved spec exists from enggenie:pm-refine
- The user directly requests an implementation plan, task breakdown, or phased plan

---

## Planning Steps

### Step 1: Early Scope Check

Before starting the plan, verify scope is manageable:
- Count the repos/services involved. If more than 3, suggest decomposition into separate plans.
- Check if the feature spans frontend + backend + infrastructure. If yes, confirm with the user that a single plan is appropriate.
- If the spec (from pm-refine) already has phases, use those as your starting decomposition.

### Step 2: Check for Spec

If enggenie:pm-refine produced a spec, READ IT. Do not summarize from memory. Open the file.

Inherit from the spec:
- Phases and their ordering
- Target repos and services
- Acceptance criteria for each requirement
- Edge cases and error scenarios
- Non-functional requirements (performance, security, etc.)

If no spec exists, ask the user: "No spec found. Should I work from your description, or should we run enggenie:pm-refine first?"

### Step 3: Codebase Discovery

Use an Explorer subagent (model: sonnet, execution: background) to search the codebase.

The Explorer searches the codebase for:
- Existing patterns that the implementation should reuse (not reinvent)
- Utility functions, helpers, shared modules already available
- Naming conventions, file organization, import patterns
- Test patterns and test infrastructure already in place
- Configuration patterns (env vars, feature flags, dependency injection)

If memory-recall is available, search for prior art: "Last time we built something like X, we used pattern Y in repo Z." Pull that context forward.

Do not proceed to task breakdown until discovery is complete. The plan must build on what exists, not ignore it.

### Step 4: Doc Discovery

Use a Doc Discovery subagent (model: haiku, execution: standard) to read external documentation.

The Doc Discovery agent reads external API documentation and extracts:
- Specific method signatures and parameters needed
- Authentication patterns and token handling
- Rate limits, pagination, and error response formats
- SDK versions and breaking changes between versions

Capture exact method names and signatures. The plan will reference these directly -- no "consult the docs" deferrals.

### Step 5: File Map

Produce a complete file map. Every file that will be created, modified, or deleted, with a one-line responsibility statement.

```
Files to CREATE:
  src/services/billing/invoice-generator.ts    - generates invoice PDFs from order data
  src/services/billing/invoice-generator.test.ts - unit tests for invoice generation
  src/api/routes/invoices.ts                   - REST endpoints for invoice CRUD

Files to MODIFY:
  src/api/routes/index.ts                      - register new invoice routes
  src/services/billing/index.ts                - export invoice-generator module
  src/config/permissions.ts                    - add invoice-related permission scopes

Files to DELETE:
  (none)
```

Every file in the plan must appear in this map. Every file in this map must appear in the plan. No orphans.

### Step 6: Phased Task Breakdown

Build the plan using this structure. Phases are ordered by deployment dependency -- downstream services first, then middleware, then upstream consumers.

```markdown
## Phase 1 -- <service-name> (downstream)
Branch: <branch-name>

### Task 1.1: [component]
Files: create/modify/test exact paths
- [ ] Write failing test (actual test code included below)
- [ ] Run test, verify it fails (exact command + expected output)
- [ ] Write minimal implementation (actual code included below)
- [ ] Run test, verify it passes (exact command)
- [ ] Commit

### Task 1.2: [component]
Files: create/modify/test exact paths
- [ ] Write failing test (actual test code included below)
- [ ] Run test, verify it fails (exact command + expected output)
- [ ] Write minimal implementation (actual code included below)
- [ ] Run test, verify it passes (exact command)
- [ ] Commit

### Deployment Readiness -- Phase 1
- [ ] All tests pass (`npm test` or equivalent -- exact command)
- [ ] No breaking changes to existing contracts
- [ ] Backward compatibility verified (existing callers still work)
- [ ] User verifies: [specific manual check, not vague "looks good"]
- [ ] Phase can be deployed independently before Phase 2 begins

## Phase 2 -- <service-name> (middleware)
Depends on: Phase 1 deployed
Branch: <branch-name>

### Task 2.1: [component]
...

### Deployment Readiness -- Phase 2
- [ ] All tests pass
- [ ] Integration with Phase 1 verified
- [ ] User verifies: [specific manual check]
- [ ] Phase can be deployed independently before Phase 3 begins
```

Rules for task breakdown:
- Each task step is 2-5 minutes of work. If you cannot finish a step in 5 minutes, it is too big. Break it down further.
- TDD sequence: failing test first, then implementation, then green. Always.
- Every task has exact file paths. Not "the config file" -- the actual path.
- Every task has a commit checkpoint. Small commits. One logical change per commit.
- Phases are deployment boundaries. The system must be stable and shippable at every phase boundary.

### Step 7: No Placeholders -- Enforced

Every step in the plan contains real, complete content. The following are violations:

- "Add appropriate error handling" -- specify WHICH errors and HOW they are handled
- "Similar to Task N" -- write it out again, fully
- "TBD" or "TODO" or "implement later" -- if it is not ready to specify, it is not ready to plan
- "See docs for details" -- the details are IN the plan or they do not exist
- "Add tests as needed" -- specify WHICH tests with WHAT assertions
- "Configure as appropriate" -- specify the exact configuration values
- "Handle edge cases" -- name each edge case and its handling

If you cannot be specific about a step, that step is not ready for the plan. Remove it or research it until you can be specific.

### Step 8: Self-Review

Use a Plan Reviewer subagent to validate the plan before presenting it.

The reviewer checks four things:

**Spec Coverage** -- Every requirement in the spec has at least one task that implements it. Every acceptance criterion has at least one test that validates it. Missing coverage is a blocking defect.

**Placeholder Scan** -- Search the entire plan for: TBD, TODO, "implement later", "as needed", "as appropriate", "similar to", "see above", "etc.", "and so on". Any match is a blocking defect.

**Type Consistency** -- Method names, function signatures, type definitions, and interface shapes must match across all tasks that reference them. If Task 1.2 defines `generateInvoice(order: Order): Invoice` then Task 2.1 must call it with that exact signature, not `createInvoice(data: any)`.

**Scope Check** -- The plan covers a single subsystem or feature. If the plan touches multiple independent systems with no shared dependency, it should be split into separate plans. One plan, one deployable unit of change.

Fix all defects found by the reviewer before presenting the plan.

---

## Plan Header Format

Every plan starts with this header:

```markdown
# [Feature Name] Implementation Plan

> Execute with: enggenie:dev-implement

**Goal:** [one sentence -- what the user gets when this is done]
**Approach:** [2-3 sentences -- how the implementation is structured]
**Spec:** [path to spec file if one exists, or "None -- built from user description"]
**Prior Art:** [patterns found by memory-recall, or "None found"]
```

---

## Subagent Context Preservation

When subagents (Explorer, Doc Discovery, Plan Reviewer) complete their work, explicitly capture their key findings back to the main conversation before proceeding:

- Existing patterns and utilities discovered by the Explorer
- API signatures and methods extracted by Doc Discovery
- Review defects and suggestions from the Plan Reviewer
- File paths that will be created or modified

Do not assume the orchestrating agent retains subagent context automatically. Extract and summarize findings before incorporating them into the plan.

---

## Recommended Model

**Primary:** opus
**Why:** Multi-phase planning with deployment gates requires understanding complex dependencies, service boundaries, and sequencing. Opus produces more thorough plans with fewer missed edge cases.

This is a recommendation. Ask the user: "This skill works best with opus for thorough implementation planning. Confirm or override?" Do not proceed until the user responds.

---

## Plans Directory

Save plans to the `/plans` directory at the project root by default. This makes plans easy to revisit and reference later.

```
plans/
  [feature-slug]-implementation-plan.md
  [feature-slug]-implementation-plan.md
```

If the project has an existing convention for plan storage (e.g., `docs/plans/`), follow that instead.

---

## Exit Action

When the plan is complete and passes self-review:

1. Save the plan to a file (e.g., `plans/[feature]-implementation-plan.md`)
2. Present the full plan to the user for review
3. Wait for explicit approval -- do not proceed without it

After the user approves, offer the execution choice:

> Plan ready. Execute with enggenie:dev-implement?

Do not auto-execute. The user decides when to start building.

---

## What This Skill Is Not

- This is not a flat task list. Flat lists have no deployment boundaries and no dependency ordering. This skill produces phased, deployment-sequenced plans.
- This is not a design document. Design decisions should already be made (by enggenie:architect-design) before this skill runs.
- This is not a spec. Requirements should already be refined (by enggenie:pm-refine) before this skill runs.
- This is not implementation. No code is written by this skill. Code happens in enggenie:dev-implement.

This skill produces one thing: a phased, deployment-sequenced, placeholder-free implementation plan that a developer (human or agent) can execute step by step without ambiguity.
