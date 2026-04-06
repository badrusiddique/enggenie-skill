---
name: pm-refine
description: Use when refining user stories, writing feature specifications, estimating story points, creating subtasks, planning spikes, or generating QA test plans - covers the product management side of development before implementation begins
---

# enggenie:pm-refine

Turn vague feature requests into deployable specifications. This skill takes "I want to build X" and produces a complete spec with acceptance criteria, estimation, subtask breakdown, QA plan, and Jira tickets. It also refines existing stories, plans spikes, and re-estimates work with transparent reasoning.

No spec ships with TBD sections. No story gets estimated without showing the math. No feature starts implementation without edge cases documented.

---

## Announcement

When this skill is invoked, announce:

> I'm using enggenie:pm-refine to generate a feature specification.

---

## Modes

This skill operates in four modes. The user's intent determines which mode activates.

### Spec Mode

Trigger: "I want to build X", "Write a spec for X", "New feature: X"

Generates a complete feature specification from scratch. This is the primary mode and follows the full workflow described below.

### Refine Mode

Trigger: "Refine PROJ-1234", "Polish this story", "Tighten the AC on X"

Takes an existing story or set of acceptance criteria and improves them. Pulls the current state from Jira (if available), identifies gaps, strengthens acceptance criteria, adds missing edge cases, and updates the ticket. Does not generate a new spec from scratch -- works with what exists.

### Spike Mode

Trigger: "Spike: can we use X for Y?", "Research ticket for X", "Time-boxed investigation"

Generates a time-boxed research ticket. Every spike has:
- A clear question to answer (not "explore X" -- a specific yes/no or which-option question)
- A time box (default: 1 day, configurable)
- Success criteria: what artifact or decision comes out of the spike
- A decision template: "If yes, then [next ticket]. If no, then [alternative]."
- A follow-up ticket placeholder linked to the spike outcome

### Estimate Mode

Trigger: "Re-estimate PROJ-1234", "How big is this?", "Break down the estimate for X"

Re-estimates an existing story with full transparency. Pulls the story from Jira (if available), breaks the work into areas, estimates each area independently, applies the estimation method, and shows all work. Produces a revised point value with justification.

---

## Spec Generation Workflow

This is the full workflow for Spec Mode. Other modes use subsets of these steps.

### Step 1: Parse Intent

Extract from the user's request:
- Feature title (human-readable name)
- Slug (kebab-case identifier for file names and branch names)
- Branch name suggestion (e.g., `feature/<slug>`)
- Figma link (if the user provided one)
- Project board / Jira project key (if the user specified one)

If any critical piece is ambiguous, ask. Do not guess at scope.

### Step 2: Ask Clarifying Questions

Ask clarifying questions to fill gaps. One question at a time. Wait for the answer before asking the next.

Questions to consider (ask only what is missing, skip what is obvious):
- What is the scope boundary? What is explicitly NOT included?
- Which repos and services are affected?
- Are there database schema changes? New tables, columns, indexes?
- Are there API contract changes? New endpoints, modified payloads, versioning?
- Are there frontend requirements? New pages, components, state changes?
- What are the edge cases? What happens when the input is empty, duplicated, or malformed?
- Who are the consumers of this feature? Internal teams, external APIs, end users?
- Are there performance requirements? Expected load, latency targets?
- Are there security implications? Auth changes, new permissions, data sensitivity?

Do not ask all of these. Ask only the ones where the answer is not obvious from context. Three to five questions is typical. Stop when you have enough to write a complete spec.

### Step 3: Validate Workspace

Check the current state of affected repos:
- Run `git status` across relevant repos
- Verify proposed branch names do not already exist (`git branch -a | grep <slug>`)
- Flag any uncommitted work that might conflict

If workspace issues are found, report them and ask the user how to proceed. Do not silently ignore dirty state.

### Step 4: Pull Design Context

If a Figma link was provided and Figma MCP is available:
- Extract component dimensions, spacing, and layout structure
- Pull design tokens (colors, typography, border radius)
- Identify interactive states (hover, active, disabled, error)
- Note responsive breakpoints if visible in the design

If Figma MCP is not available, note that design details should be added manually and move on. Do not block the spec on tooling availability.

### Step 5: Generate the Spec

Generate the spec using the team's template if one exists at `docs/enggenie/templates/spec-template.md` or `templates/spec-template.md` in the target repo. If no team template is found, use the default template at `templates/spec-template.md`.

The spec must contain all of the following sections. No section may contain "TBD", "TODO", or empty content.

**Summary** -- What the feature does and why it matters. Two to three sentences. Written for someone who has not seen the Figma or heard the verbal discussion.

**Architecture Context** -- Where this feature fits in the system. If multiple services are involved, include a text-based system diagram showing the interaction flow. If it is a single-service change, describe which layer of the service is affected (API, service, data, UI).

**Repos and Services in Scope** -- List every repository and service that will be touched. For each, state what changes in that repo.

**Functional Requirements** -- Numbered list. Each requirement is a single, testable statement. Not "the system should handle errors" -- instead, "when the payment gateway returns a 502, the system retries once after 2 seconds and returns a user-facing error if the retry also fails."

**Figma Design Reference** -- If a Figma link was provided, include it here with extracted dimensions, tokens, and layout notes from Step 4. If no design was provided, state "No design provided -- implementation should follow existing UI patterns in the codebase."

**Implementation Order** -- Phased. Downstream services first, then middleware, then upstream consumers. Each phase is independently deployable. Deploying Phase 1 alone must not break the system.

**Per-Phase Deployment Readiness Checklists** -- For each phase, a checklist of conditions that must be true before that phase can ship. Include backward compatibility checks, migration safety, and rollback strategy.

**Acceptance Criteria** -- Two levels:
- User-level: what the end user observes ("user sees a confirmation toast after submitting the form")
- Technical per service: what each service does ("billing-service publishes an InvoiceCreated event to the billing.events topic")

Each acceptance criterion is a single, verifiable statement. If you cannot describe how to verify it, it is not an acceptance criterion.

**Edge Cases** -- Every edge case identified during clarifying questions, plus any discovered during spec writing. Each edge case has a stated behavior: "When X happens, the system does Y."

**Open Questions** -- Pre-seeded with at least three questions. These are genuine unknowns that need answers before or during implementation. Not padding -- real questions that affect implementation decisions.

**Manual QA Test Plan** -- A table with the following columns:

| Scenario | Steps | Expected | Dev Result | QA Result |
|----------|-------|----------|------------|-----------|

Minimum 8 scenarios covering the happy path, error cases, edge cases, and boundary conditions. "Dev Result" and "QA Result" columns are left blank for the team to fill during testing.

**Playwright Automation Scenarios** -- List of scenarios that should be automated with Playwright, plus the file locations where those test files should live. Follow existing test directory conventions in the repo.

**Documentation Checklist** -- What documentation needs to be created or updated: API docs, runbooks, architecture diagrams, onboarding guides, changelog entries.

**Jira Ticket Structure** -- If a project board was specified, include the ticket structure:

- **Story**: Title, description (from the spec summary), estimation (from the estimation method below)
- **Subtasks**: One per repo or functional area. Each subtask has a feature-specific title (not "Backend work" -- instead "Add invoice generation endpoint to billing-service"). Each subtask has its own estimate.
- **QA Subtask**: For the QA team to execute the manual test plan and verify automation coverage.
- **BA Subtask**: For business analysis review and stakeholder sign-off.

### Step 6: Create Jira Tickets

If Jira MCP is available and the user specified a project board, ask the user for confirmation before creating any tickets:
- Present the proposed ticket structure (story + subtasks) for user review
- Only create tickets after the user explicitly approves
- Create the story with the full spec as the description
- Create subtasks linked to the story
- Set estimates on each ticket
- Link related tickets if referenced

If Jira MCP is not available, output the ticket structure in the spec so the user can create them manually. Do not block the spec on Jira availability.

### Step 7: Write the Handoff Context to the Jira Ticket

The Jira ticket is the contract between PM, Dev, and QA. Different people will pick this up in different sessions with no shared conversation context. The ticket must carry everything they need.

After creating or updating the Jira ticket, ensure the ticket description includes these sections:

```markdown
## Spec
[Link to spec file in repo, e.g., enggenie/spec_heist-timer.md]

## Key Decisions
- [Decision 1 from clarifying questions — e.g., "Timer logic: client-side useEffect, not server-side"]
- [Decision 2 — e.g., "Warning threshold: 30 minutes (turns red)"]
- [Decision 3 — e.g., "Expired state: show 'Expired' badge, disable all actions"]

## Edge Cases
- [Edge case 1 and its expected behavior]
- [Edge case 2 and its expected behavior]

## For Dev
- Spec file: [path in repo]
- Start with: "Pick up PROJ-1234" or "Plan and build PROJ-1234 based on [spec path]"
- Key constraints: [anything Dev must know — performance targets, API contracts, backward compatibility]

## For QA
- Test against: [spec path]
- QA test plan: [section reference or file path]
- Key edge cases to verify: [top 3-5 edge cases that are easy to miss]
- Playwright scenarios: [list from spec or "see spec section X"]
```

**Why this matters:** A Dev picking up this ticket two weeks later — with no context from the PM conversation — reads the ticket and has everything needed to start. A QA engineer picking it up after the PR reads the ticket and knows exactly what to verify. No Slack messages needed. No "hey, what did we decide about X?"

If Jira MCP is not available, include these sections in the spec .md file under a "## Handoff Context" heading at the end.

---

## Estimation Method

All estimates follow this process. The method is transparent -- show every step of the math.

1. **Raw estimate per area** -- Break the work into areas (backend, frontend, database, infrastructure, testing). Estimate each area in hours or relative complexity.

2. **Add 20% buffer** -- Multiply the raw estimate by 1.2. This accounts for integration overhead, context switching, and minor unknowns.

3. **Round UP to nearest Fibonacci number** -- The buffered estimate maps to the Fibonacci scale: 1, 2, 3, 5, 8. Always round up, never down.

**Note:** In this method, raw hour estimates map directly to the Fibonacci scale - the Fibonacci number IS the estimate, not a separate "points" concept. 3.6 hours rounds up to 5 on the Fibonacci scale.

4. **Estimate the story AS A WHOLE** -- Use the largest sub-area as the anchor. Do not sum sub-estimates - summing Fibonacci numbers produces non-Fibonacci totals.

5. **Cap at 8** -- Any estimate above 8 points means the story is too large. Decompose it into smaller stories. No exceptions.

6. **Show the work** -- Every estimate includes the transparent calculation:

```
Backend API:     3h raw -> +20% -> 3.6h -> round up -> 5 points
Frontend UI:     2h raw -> +20% -> 2.4h -> round up -> 3 points
Database migration: 1h raw -> +20% -> 1.2h -> round up -> 2 points
Testing:         2h raw -> +20% -> 2.4h -> round up -> 3 points
Largest sub-area: 5 points (Backend API) -> story estimate: 5 points
```

The estimation method is configurable per team. Check the project's CLAUDE.md for overrides:
- **Fibonacci** (default): 1, 2, 3, 5, 8
- **T-shirt**: XS, S, M, L, XL (mapped to 1, 2, 3, 5, 8 internally)
- **Linear**: 1-10 scale without Fibonacci rounding

---

## Subagents

This skill dispatches the following subagents to produce a thorough spec.

### Refinement Subagent (model: sonnet)

Explores the codebase to identify affected files, existing patterns, and service boundaries. Proposes the subtask breakdown and per-area estimates. Runs before the spec is finalized so the spec reflects actual code structure, not assumptions.

### QA Planner Subagent (model: sonnet)

Generates the QA test plan from the acceptance criteria. Thinks with a QA mindset: what will the developer miss? What breaks under load? What happens with empty inputs, duplicate submissions, concurrent edits, expired sessions? Produces both the manual test plan table and the Playwright automation scenario list.

### Spec Reviewer Subagent (model: sonnet)

Reviews the complete spec before it is saved. Checks for:
- Sections with TBD, TODO, or empty content
- Acceptance criteria that cannot be verified
- Missing edge cases for identified requirements
- Inconsistencies between the functional requirements and the implementation order
- Open questions that should have been answered during clarifying questions

The spec does not ship until the reviewer passes it. Fix all findings before presenting the spec to the user.

### Memory Subagent (model: haiku, optional)

Searches for prior art: "Have we built something similar before? What patterns did we use? What pitfalls did we hit?" Pulls forward any relevant context from previous specs, implementations, or retro notes.

Graceful skip if memory tooling is not installed. The spec is still complete without it -- this subagent adds context, not structure.

---

## Subagent Context Preservation

When subagents (Refinement, QA Planner, Spec Reviewer, Memory) complete their work, explicitly capture their key findings back to the main conversation:

- **Refinement subagent:** Affected files, service boundaries, subtask breakdown, per-area estimates
- **QA Planner subagent:** Manual test plan table, Playwright scenarios, edge cases identified
- **Spec Reviewer subagent:** Review findings, sections that need fixes, completeness assessment
- **Memory subagent:** Prior art found, relevant patterns, past pitfalls

Do not assume the orchestrating agent retains subagent context automatically. Extract and summarize findings before incorporating them into the spec.

---

## Recommended Model

**Primary:** opus
**Why:** Spec generation requires deep understanding of requirements, edge cases, estimation math, and cross-service dependencies. Opus produces more thorough specs with fewer gaps.

This is a recommendation. Ask the user: "This skill works best with opus for thorough spec generation. Confirm or override?" Do not proceed until the user responds.

---

## Default Spec Template

The default spec template is located at `templates/spec-template.md`. Teams can override this by placing their own template at `docs/enggenie/templates/spec-template.md` or `templates/spec-template.md` in their repo.

The default template contains all section headers, formatting conventions, and placeholder guidance. The skill fills in the content; the template provides the structure.

---

## Team Extensibility

Teams customize this skill through their repo configuration:

**Spec Template** -- Place a custom template at `docs/enggenie/templates/spec-template.md` in any repo. The skill uses the team template when working in that repo and falls back to the default when no team template exists.

**Architecture Context** -- Defined in the project's CLAUDE.md. Describes the service topology, shared libraries, and integration patterns. The skill reads this context when generating the Architecture Context section of the spec.

**Estimation Method** -- Configured in CLAUDE.md. Options: Fibonacci (default), T-shirt, linear. The skill uses the configured method for all estimates in that project.

**Jira Project Key** -- Configured in CLAUDE.md. The skill uses this key when creating tickets. If not configured, the skill asks during Step 1.

---

## Entry Conditions

None. This is often the first skill invoked in a workflow. It does not require output from any prior skill.

Common entry points:
- User describes a feature they want to build
- User pastes a Jira ticket and asks for refinement
- User asks for an estimate or story point breakdown
- User needs a spike ticket for technical research

---

## Exit Action

When the spec is complete and passes the Spec Reviewer:

1. Save the spec to `enggenie/spec_[slug].md` (e.g., `enggenie/spec_heist-timer.md`). If the team has a configured spec directory in CLAUDE.md, use that instead.
2. Write the handoff context to the Jira ticket (Step 7) — this ensures whoever picks up the ticket next has full context
3. Present the full spec to the user for review
4. Wait for explicit approval -- do not proceed without it

After the user approves, offer the next step:

> Spec approved. Jira ticket PROJ-1234 updated with handoff context for Dev and QA. Next: invoke enggenie:architect-design (if design decisions need discussion) or enggenie:architect-plan (if the design is clear and you are ready to plan implementation).

Do not auto-invoke the next skill. The user decides the next step.

---

## What This Skill Is Not

- This is not implementation planning. Phased task breakdowns with code-level detail happen in enggenie:architect-plan.
- This is not design discussion. Architecture tradeoffs and pattern selection happen in enggenie:architect-design.
- This is not coding. No code is written by this skill. Code happens in enggenie:dev-implement.
- This is not QA execution. Test execution and verification happen in enggenie:qa-verify.

This skill produces one thing: a complete, reviewable, actionable feature specification that the team can build from without ambiguity.
