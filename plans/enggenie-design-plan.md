# enggenie — Next-Gen SDLC Skill Suite

## Context

Engineers wear multiple hats throughout their day — PM, Architect, Dev, Reviewer, QA, Deploy. Existing skill suites (prior skill suites) focus on the coding phase with 14 skills but leave planning, QA, and deployment to ad-hoc behavior. enggenie covers the entire SDLC with role-based skills that match the hat you're wearing right now.

## Vision

**Philosophy: "The right expert for the right moment."**

**For:** Any engineer who thinks, designs, builds, reviews, tests, and ships software.
**Not just for:** Agile teams, though agile vocabulary is the default.

Each enggenie is a domain expert. Refining a story? `enggenie:pm-refine`. Debugging? `enggenie:dev-debug`. Shipping? `enggenie:deploy-ship`. Fixing a typo? No enggenie needed — the suite stays out of your way.

---

## Prior skill suites Feature Parity + Additions

Every prior skill suites capability is covered. Nothing is lost in switching.

| Prior skill suites Skill | Genie Equivalent | What Changes |
|---|---|---|
| using-prior skill suites (gateway) | **enggenie** (gateway) | Same routing + instruction priority hierarchy |
| brainstorming | **enggenie:architect-design** | 3 modes (brainstorm/architecture/discussion) + memory |
| writing-plans | **enggenie:architect-plan** | Phased plans with deployment readiness gates + spec inheritance |
| executing-plans | **enggenie:dev-implement** | Subagent-driven only (executing-plans was the weaker option) |
| subagent-driven-development | **enggenie:dev-implement** | Merged — one skill, not two |
| test-driven-development | **enggenie:dev-tdd** | Standalone discipline skill (fires during any coding) |
| systematic-debugging | **enggenie:dev-debug** | Matched + memory-aware |
| verification-before-completion | **enggenie:qa-verify** | Matched |
| requesting-code-review | **enggenie:review-code** | Merged request + receive into one skill |
| receiving-code-review | **enggenie:review-code** | Merged — eliminates redundancy |
| using-git-worktrees | Built into **enggenie:dev-implement** | Not a separate skill — setup is part of implementation |
| finishing-a-development-branch | **enggenie:deploy-ship** | Enhanced with PR creation + Jira updates |
| dispatching-parallel-agents | Built into **enggenie:dev-implement** | Pattern documented in dev-implement, not a separate skill |
| writing-skills | Not shipped | Used during development, not needed by end users |

**New in enggenie (no prior skill suites equivalent):**
- **enggenie:pm-refine** — Full spec generation, story refinement, estimation, Jira/Figma integration
- **enggenie:qa-test** — QA-perspective testing with Playwright automation + manual browser testing
- **enggenie:review-design** — Frontend/UI design quality enforcement
- **enggenie:memory-recall** — Cross-session context via claude-mem
- **Phased deployment model** — Each phase independently deployable with readiness gates
- **Spec → Plan → Code pipeline** — Skills consume outputs from prior skills

---

## 13 Skills Across 7 Roles

### Role: PM (Product Management)

#### enggenie:pm-refine
**Purpose:** Full spec generation + story refinement + estimation + spike management

**Triggers on:** Story refinement, spec writing, acceptance criteria, story pointing, subtasks, spikes, QA plan generation, Jira/Figma integration

**What it does:**
1. Parse intent — feature title, slug, branch name, Figma link, project board
2. Ask clarifying questions — scope, repos, DB changes, API impact, FE requirements, edge cases. One at a time. Wait for answers.
3. Validate workspace — git status across repos, branch uniqueness
4. Pull design context — if Figma MCP available, extract dimensions, tokens, colors, layout
5. Generate spec from template (team-overridable):
   - Summary (what + why)
   - Architecture context (system diagram)
   - Repos/services in scope
   - Functional requirements
   - Figma design reference (if provided)
   - Implementation order (phased, downstream-first, each phase independently deployable)
   - Per-phase deployment readiness checklists
   - Acceptance criteria (user-level + technical per service)
   - Edge cases
   - Open questions (pre-seeded with 3+)
   - Manual QA test plan table (Scenario | Steps | Expected | Dev Result | QA Result)
   - Playwright automation scenarios + file locations
   - Documentation checklist
   - Jira ticket structure (if project specified):
     - Story with transparent estimation (raw per area → buffer → Fibonacci)
     - Subtasks per repo/area (feature-specific titles)
     - QA + BA subtasks
6. Create Jira tickets if MCP available

**Modes:**
- **Spec mode** — Generate full spec from scratch ("I want to build X")
- **Refine mode** — Polish existing story/AC ("Refine GSL-1234")
- **Spike mode** — Time-boxed research ticket ("Spike: can OpenSearch handle X?")
- **Estimate mode** — Re-estimate existing story with breakdown

**Subagents:**
- **Refinement subagent** (sonnet) — Explores codebase, identifies affected files/services, proposes subtask breakdown and estimates
- **QA Planner subagent** (sonnet) — Generates QA test plan from acceptance criteria with QA mindset (edge cases, error scenarios, what the dev won't think of)
- **Memory subagent** (haiku, if recall available) — "Have we built something similar? What did the spec look like?"

**Subagent prompt templates required:**
- `agents/refinement-agent.md`
- `agents/qa-planner-agent.md`

**Entry condition:** None — this is often the first skill in a workflow
**Exit action:** Spec saved. Next step: invoke `enggenie:architect-design` (if design discussion needed) or `enggenie:architect-plan` (if design is clear)

**Team extensibility:**
- Teams provide their own template in `docs/engenggenie/templates/spec-template.md`
- Architecture context configured in CLAUDE.md
- Estimation method configurable (Fibonacci, T-shirt, linear)

---

### Role: Architect

#### enggenie:architect-design
**Purpose:** Brainstorming + architectural decisions + technical discussions

**Triggers on:** Brainstorming, architecture review, technical discussion, design session, ADR, tradeoff analysis, system design

**What it does:**

**Brainstorm mode** — Exploring an idea:
1. Explore project context (dispatch Explorer subagent in background)
2. If memory available: search past decisions in same domain
3. Ask clarifying questions one at a time, multiple choice when possible
4. Propose 2-3 approaches with concrete tradeoffs and recommendation
5. Present design section by section, get approval after each
6. Save to `docs/engenggenie/specs/` (or team preference)

**Architecture mode** — System design:
1. Map existing system (smart_search/outline if memory available)
2. Draw component boundaries, data flow, integration points
3. Document as ADR: Context → Decision → Consequences → Status
4. Save to `docs/engenggenie/adrs/`

**Discussion mode** — Evaluating options:
1. Present both sides with concrete tradeoffs (not abstract pros/cons)
2. Test against codebase reality ("Does pattern X work here? Let me check...")
3. Reach a decision, document it
4. Save to `docs/engenggenie/decisions/`

**Hard Rule: No code until design is approved.** Short designs are fine (3 sentences for simple features). But the user says "go" before anyone builds.

**Subagents:**
- **Explorer subagent** (sonnet, background) — Reads codebase, finds existing patterns, understands current architecture
- **Memory subagent** (haiku, if available) — "Have we designed something similar? What decisions did we make?"

**Entry condition:** None — can be invoked directly
**Exit action:** Design approved → invoke `enggenie:architect-plan`

**What makes it different from prior skill suites:brainstorming:**
- Three modes instead of one rigid 9-step flow
- No mandatory visual companion offer (saves tokens and a message round-trip)
- No forced "spec self-review" step (done inline)
- No forced "user reviews written spec" gate (user already approved during design)
- Architecture and technical discussion are first-class (prior skill suites has no equivalent)
- Memory-informed: checks past decisions before proposing new ones

---

#### enggenie:architect-plan
**Purpose:** Implementation planning from specs — phased, independently deployable

**Triggers on:** Implementation plan, plan from spec, task breakdown, before writing code

**What it does:**
1. **Check for spec** — If pm-refine produced a spec, READ IT. Inherit phases, repos, AC.
2. **Discovery** — Search codebase for existing patterns to reuse. If memory available, search for prior art ("last time we built similar X, we used pattern Y").
3. **Doc discovery** — Dispatch subagent to read external API docs and extract specific methods/signatures needed.
4. **File map** — Every file that will be created or modified, with responsibility.
5. **Phased task breakdown:**

```markdown
## Phase 1 — <service-name> (downstream)
Branch: <branch-name>

### Task 1.1: [component]
Files: create/modify/test exact paths
- [ ] Write failing test (actual test code)
- [ ] Run test, verify it fails (exact command + expected output)
- [ ] Write minimal implementation (actual code)
- [ ] Run test, verify it passes (exact command)
- [ ] Commit

### Deployment Readiness — Phase 1
- [ ] All tests pass
- [ ] No breaking changes to existing contracts
- [ ] User verifies: [specific manual check]
- [ ] Phase can be deployed independently before Phase 2

## Phase 2 — <service-name> (middleware)
Depends on: Phase 1 deployed
...
```

6. **No placeholders** — Every step has real content. No "add error handling" or "similar to Task N" or "TBD."
7. **Self-review** — Check spec coverage, placeholder scan, type consistency across tasks.

**Plan header:**
```markdown
# [Feature] Implementation Plan

> Execute with: enggenie:dev-implement

**Goal:** [one sentence]
**Approach:** [2-3 sentences]
**Spec:** [link to spec if exists]
**Prior Art:** [from memory, if available]
```

**Subagents:**
- **Explorer subagent** (sonnet) — Finds existing patterns, utilities, and conventions
- **Doc discovery subagent** (haiku) — Reads external API docs, extracts signatures

**Subagent prompt templates required:**
- `agents/explorer-agent.md`
- `agents/doc-discovery-agent.md`

**Entry condition:** Approved design (from architect-design) OR approved spec (from pm-refine) OR direct user request
**Exit action:** Plan saved. Next step: invoke `enggenie:dev-implement`

**What makes it different from prior skill suites:writing-plans:**
- Consumes spec from pm-refine (inherits phases, AC, repos)
- Doc discovery phase (from claude-mem's make-plan, adapted)
- Prior art from memory
- Phased execution with deployment readiness gates (prior skill suites plans are flat task lists)

---

### Role: Dev (Developer)

#### enggenie:dev-implement
**Purpose:** Execute implementation plans using TDD with subagent-driven development

**Triggers on:** Execute plan, implement feature, start coding, TDD, build this

**What it does:**

**Setup (built-in, not a separate skill):**
1. Check for worktree directory (.worktrees/ or worktrees/)
2. Verify it's gitignored (fix if not)
3. Create worktree with feature branch
4. Run project setup (auto-detect: npm install, dotnet restore, pip install, etc.)
5. Verify baseline tests pass

**Per task:**
1. Dispatch **Implementer subagent** with:
   - Full task text (NOT a reference to the plan file)
   - Context from prior tasks (what was built, what to import)
   - Project conventions

2. Implementer follows RED-GREEN-REFACTOR:
   - Write failing test → verify it fails → write minimal code → verify it passes → refactor → commit

3. Dispatch **Spec Reviewer subagent** with:
   - Git diff (BASE_SHA..HEAD_SHA)
   - The spec/requirements for this task
   - Checklist: Does it match spec? Anything missing? Anything extra?

4. If spec issues → Implementer fixes → Spec reviewer re-reviews

5. Dispatch **Code Quality Reviewer subagent** with:
   - Same git diff
   - Quality checklist: clean code, no bugs, good tests, YAGNI

6. If quality issues → Implementer fixes → Quality reviewer re-reviews

7. Mark task complete, move to next

**After each phase (if multi-phase plan):**
- Check deployment readiness
- Ask user to verify manually
- Only proceed to next phase after confirmation

**Hard Rule: No production code without a failing test first.**

If you catch yourself writing code before a test: stop. Delete it. Write the test first.

**The Shortcut Tax** — what it costs when you skip:

| Shortcut | What it costs you |
|----------|------------------|
| "I'll write tests after" | Tests pass immediately — you've proved nothing. Bugs ship. You'll debug in prod. |
| "Too simple to test" | Simple code breaks. 30 seconds to test. 30 minutes to debug in prod. |
| "Already manually tested" | No record. Can't re-run. You'll re-test every change by hand forever. |
| "TDD slows me down" | TDD is faster than debugging. Systematic beats ad-hoc. Every study confirms this. |
| "Just this once" | That's what you said last time. And the time before. Discipline compounds. |
| "Keep the code as reference" | You'll adapt it instead of writing tests first. That's testing-after. Delete means delete. |
| "Need to explore first" | Fine. Explore. Then throw away the exploration code. Start fresh with TDD. |
| "The test is hard to write" | Listen to the test. Hard to test = hard to use = bad design. Simplify the interface. |

**Violating the letter of TDD is violating the spirit.** "I'm following the spirit by testing after" is a rationalization. The spirit IS the letter.

**Model selection for subagents:**
- Implementer on simple tasks (1-2 files, clear spec) → haiku
- Implementer on complex tasks (multi-file, integration) → sonnet
- Spec reviewer → sonnet
- Code quality reviewer → sonnet
- Final reviewer (after all tasks) → opus

**Handling subagent status:**
- **DONE** → Proceed to spec review
- **DONE_WITH_CONCERNS** → Read concerns. Correctness/scope → address before review. Observations → note and proceed.
- **NEEDS_CONTEXT** → Provide missing context, re-dispatch
- **BLOCKED** → Assess: context problem → provide context. Task too large → break it up. Plan wrong → escalate to user. NEVER retry same model with same context.

**Subagent prompt templates required:**
- `agents/implementer-agent.md` — What to build, TDD cycle, self-review, status reporting
- `agents/spec-reviewer-agent.md` — Check spec compliance, nothing missing, nothing extra
- `agents/quality-reviewer-agent.md` — Code quality, bugs, test quality, YAGNI

**Entry condition:** Approved plan (from architect-plan) OR direct user request
**Exit action:** All tasks complete, verified → invoke `enggenie:deploy-ship`

---

#### enggenie:dev-debug
**Purpose:** Systematic root cause investigation — 4 phases, no guessing

**Triggers on:** Bug, test failure, unexpected behavior, error, something broken, not working

**What it does:**

**Hard Rule: No fixes without understanding the cause first.**

**Phase 1 — Investigate:**
- Read error messages completely (stack traces, line numbers, error codes)
- Reproduce consistently (exact steps, every time?)
- Check recent changes (git diff, new deps, config changes)
- In multi-component systems: add diagnostic logging at each boundary, run once, see WHERE it breaks
- Trace data flow backward from symptom to source

**Phase 2 — Find the pattern:**
- Find similar working code in same codebase
- Compare working vs broken — list every difference
- Understand dependencies and assumptions

**Phase 3 — Test one hypothesis:**
- State it: "I think X causes this because Y"
- Make the SMALLEST change to test it
- One variable at a time
- Worked? → Phase 4. Didn't? → New hypothesis. Don't stack fixes.

**Phase 4 — Fix it:**
- Write failing test that reproduces the bug
- Fix the root cause (not the symptom)
- Verify: test passes, no other tests break
- If 3+ fix attempts fail → STOP. This is an architecture problem. Discuss with the team.

**The Shortcut Tax:**

| Shortcut | What it costs you |
|----------|------------------|
| "Quick fix for now, investigate later" | Later never comes. You'll hit the same bug again. |
| "Just try changing X" | Random changes create new bugs. You'll thrash for hours. |
| "It's probably X, let me fix that" | "Probably" means you haven't investigated. Probably wrong. |
| "Add multiple changes, run tests" | Can't isolate what worked. New bugs from untested changes. |
| "One more fix attempt" (after 2+) | 3 failures = architecture problem, not a code bug. Stop fixing, start questioning. |

**Subagents:**
- **Investigator subagent** (sonnet) — Gathers evidence: reads logs, traces data flow, checks recent changes. Returns structured findings.
- **Memory subagent** (haiku, if available) — "Have we seen this bug pattern before? What was the root cause?"

**Subagent prompt templates required:**
- `agents/investigator-agent.md`

**Supporting references:**
- `references/root-cause-tracing.md` — Backward tracing technique for deep call stacks
- `references/multi-component-debugging.md` — Diagnostic instrumentation at component boundaries

**Entry condition:** None — bugs happen anytime
**Exit action:** Bug fixed, test written → resume previous workflow (dev-implement, or standalone)

---

#### enggenie:dev-tdd
**Purpose:** TDD discipline enforcement — standalone, fires during any coding

**Why standalone:** In prior skill suites, TDD is the most-used discipline skill. It fires whenever anyone writes code — with or without a plan. Embedding it only in dev-implement means ad-hoc coding gets no TDD guidance. This skill is the discipline layer; dev-implement is the orchestration layer.

**Triggers on:** Writing code, implementing a function, adding a feature, fixing a bug (when not using dev-implement), any coding task

**Hard Rule: No production code without a failing test first.**

If you catch yourself writing code before a test: stop. Delete it. Write the test first.

**The Cycle — RED → GREEN → REFACTOR:**

**RED:** Write one minimal test showing what should happen.
- Clear name, tests real behavior, one assertion.
- Run test → it MUST fail. Not error — fail.
- Failure message matches expected behavior.

**GREEN:** Write the simplest code to pass the test.
- Don't add features. Don't refactor. Don't "improve."
- Run test → it MUST pass. All other tests still pass.

**REFACTOR:** Clean up while tests stay green.
- Remove duplication, improve names, extract helpers.
- Don't add behavior. Keep tests green.

**The Shortcut Tax:**

| Shortcut | What it costs you |
|----------|------------------|
| "I'll write tests after" | Tests pass immediately — you've proved nothing. Bugs ship. |
| "Too simple to test" | Simple code breaks. 30 seconds to test. 30 minutes to debug in prod. |
| "Already manually tested" | No record. Can't re-run. You'll re-test every change by hand forever. |
| "TDD slows me down" | TDD is faster than debugging. Systematic beats ad-hoc. |
| "Just this once" | That's what you said last time. Discipline compounds. |
| "Keep the code as reference" | You'll adapt it instead of writing tests first. Delete means delete. |
| "Need to explore first" | Fine. Explore. Then throw it away. Start fresh with TDD. |
| "The test is hard to write" | Hard to test = hard to use = bad design. Simplify the interface. |
| "Tests after achieve same goals" | After answers "what does this do?" First answers "what should it do?" |
| "Existing code has no tests" | You're improving it. Add tests for what you touch. |
| "I already see the problem" | Seeing symptoms ≠ understanding root cause. Write the test. |

**Violating the letter of TDD is violating the spirit.** The spirit IS the letter.

**Gut Check — STOP and start over if:**
- You wrote code before a test
- Your test passed immediately (didn't see RED)
- You're writing multiple tests at once
- You're "just going to quickly add" something
- You're thinking "this case is different because..."
- You're keeping deleted code "as reference"

**When stuck:**

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write assertion first. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup huge | Extract helpers. Simplify design. |

**Supporting references:**
- `references/testing-anti-patterns.md` — Never test mock behavior, never add test-only methods to production, mock COMPLETE data structures
- `references/defense-in-depth.md` — Validate at every layer, make bugs structurally impossible

**Relationship to dev-implement:** dev-implement orchestrates subagents and manages the plan. dev-tdd fires as a discipline overlay on ANY coding — with or without dev-implement. When dev-implement is active, dev-tdd's rules are automatically enforced through the implementer subagent prompt.

**Entry condition:** None — fires during any coding task
**Exit action:** None — this is a discipline overlay, not a workflow step

---

### Role: Reviewer

#### enggenie:review-code
**Purpose:** Code review — both requesting and receiving

**Triggers on:** Code review, review PR, review feedback, before merging

**Requesting review:**
1. Get git SHAs (base and head)
2. Dispatch **Code Reviewer subagent** with: diff, spec/requirements, review checklist
3. Act on feedback:
   - Critical/blocking → fix immediately
   - Important → fix before proceeding
   - Minor → note for later
   - Wrong → push back with reasoning

**Receiving review (from human or external reviewer):**
1. Read ALL feedback without reacting
2. For each item: understand → verify against codebase → evaluate
3. If ANY item is unclear: STOP. Ask for clarification on ALL unclear items BEFORE implementing any.
4. Implement in order: blocking → simple → complex
5. Test each fix individually
6. Verify no regressions

**YAGNI check:** When reviewer suggests "implementing properly" — grep codebase for actual usage. If unused: "This isn't called anywhere. Remove it (YAGNI)?" If used: implement properly.

**GitHub thread handling:** When replying to inline PR comments, use `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies` — reply in the thread, not as top-level comment.

**Gut Check — Are you doing review right?**
- Saying "You're absolutely right!" → Stop. Just fix it. Actions speak louder.
- Implementing without understanding → Stop. Ask what they mean.
- Agreeing with everything → Stop. Check if it's technically correct for THIS codebase.
- Afraid to push back → If it breaks something, say so. Technical correctness over social comfort.
- Partially implementing → Stop. Clarify ALL unclear items first. Items may be related.

**Subagent prompt templates required:**
- `agents/code-reviewer-agent.md`

**Entry condition:** Code written (from dev-implement) OR PR received
**Exit action:** Review complete → resume workflow

---

#### enggenie:review-design
**Purpose:** Frontend/UI design quality enforcement

**Triggers on:** Frontend implementation, UI component, design system, making it look professional, responsive design, accessibility

**What it does:**
- Verify design system components are used (not custom CSS for things the system handles)
- Check against Figma design (if spec has Figma reference)
- Review for "AI code smell": generic layouts, Bootstrap defaults, inconsistent spacing, missing states
- Check: loading states, error states, empty states, hover states, focus states
- Verify responsive behavior (mobile, tablet, desktop)
- Accessibility audit: ARIA labels, keyboard navigation, color contrast, screen reader support
- Animation/transition review: smooth, purposeful, not janky

**Subagents:**
- **Design Reviewer subagent** (sonnet) — Reads Figma context from spec, reviews component code, checks design system usage, identifies quality gaps

**Subagent prompt templates required:**
- `agents/design-reviewer-agent.md`

**Entry condition:** Frontend code written (from dev-implement FE phase)
**Exit action:** Design review passed → proceed to qa-verify/qa-test

---

### Role: QA

#### enggenie:qa-verify
**Purpose:** Developer verification — evidence before claims

**Triggers on:** About to say "done", claiming work is complete, before committing, before PR, verifying fix

**Hard Rule: Don't say "done" until you've seen the proof.**

**The Check:**
```
Before claiming ANYTHING is complete:
1. IDENTIFY — What command proves this claim?
2. RUN — Execute the FULL command. Fresh. Complete. Not partial.
3. READ — Full output. Exit code. Failure count. Warnings.
4. VERIFY — Does output actually confirm your claim?
   YES → State claim WITH evidence ("47/47 tests pass, exit 0")
   NO  → State actual status ("3 failures in auth module")
5. ONLY THEN — Make the claim.
```

| Claim | You need | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | "Should pass", previous run, partial run |
| Build works | Build command: exit 0 | "Linter passed" (linter ≠ compiler) |
| Bug fixed | Original symptom gone + regression test passes | "Code changed, should be fixed" |
| Feature complete | Every AC verified with evidence | "Tests pass" (tests ≠ requirements) |
| Subagent succeeded | Check VCS diff, verify changes exist | Trust subagent's "success" report |

**Gut Check — About to claim success?**
- Using "should", "probably", "seems to" → Run the command first.
- Expressing satisfaction ("Done!", "Perfect!") before verification → Stop. Verify. Then celebrate.
- Trusting a subagent's success report → Check the diff yourself.
- Thinking "just this once" → No exceptions. The one you skip is the one that breaks.

**Subagents:**
- **Verification subagent** (haiku) — Runs test suite, build, linter. Reports raw output, not interpretation.

**Entry condition:** Code written, ready to claim completion
**Exit action:** Verified → proceed to qa-test (if QA needed) or deploy-ship

---

#### enggenie:qa-test
**Purpose:** QA-perspective testing — user journeys, not implementation details

**Triggers on:** QA testing, acceptance testing, test the feature, manual QA, automation testing, Playwright, user journey

**The difference:** `qa-verify` asks "does my code work?" `qa-test` asks "does the product work for users?"

**Automation mode (Playwright):**
1. Read acceptance criteria from spec (if pm-refine produced one)
2. Write Playwright tests for USER JOURNEYS:
   ```python
   # QA tests what the user does, not what the code does
   def test_user_can_filter_by_team():
       page.goto('http://localhost:3000/dashboard')
       page.wait_for_load_state('networkidle')
       page.click('text=Filter')
       page.click('text=Team A')
       items = page.locator('.item-row').all()
       assert all('Team A' in item.text_content() for item in items)
   ```
3. Use `scripts/with_server.py` for server lifecycle management
4. Follow recon-then-action: navigate → wait for networkidle → screenshot/inspect → identify selectors → execute

**Manual mode (Browser-assisted):**
1. Take QA test plan from spec (or from user)
2. For each test scenario:
   - Navigate to the page
   - Screenshot initial state
   - Execute the steps (click, fill, submit)
   - Screenshot the result
   - Compare against expected result
   - Report: PASS/FAIL with screenshot evidence
3. Generate test matrix report

**Subagents:**
- **QA Automation subagent** (sonnet) — Writes and runs Playwright tests with QA mindset
- **QA Manual subagent** (sonnet) — Executes manual test plan via browser, takes screenshots

**Subagent prompt templates required:**
- `agents/qa-automation-agent.md`
- `agents/qa-manual-agent.md`

**Entry condition:** Feature implemented and dev-verified
**Exit action:** QA results reported → proceed to deploy-ship (if passing) or back to dev (if failing)

---

### Role: Deploy

#### enggenie:deploy-ship
**Purpose:** Commit + push + PR + branch completion + Jira update

**Triggers on:** Commit, push, create PR, ship it, merge, done with this branch

**Commit:**
1. Analyze staged changes
2. Propose conventional commit message:
   ```
   <type>: <description>

   Types: feat | fix | refactor | docs | test | perf | chore
   ```
3. Present tense ("add", not "added"). Explain WHY, not just what.
4. Subject line under 72 chars.
5. Wait for user confirmation — NEVER auto-commit.

**Push + PR:**
1. Push branch with `-u` flag
2. Create PR with:
   ```markdown
   ## Summary
   [2-3 bullets from spec/plan]

   ## Test Plan
   [From qa-verify/qa-test results]

   ## Spec
   [Link to spec if exists]

   ## Jira
   [Link to story if available]
   ```

**Jira update (if MCP available):**
- Transition ticket status (e.g., In Progress → In Review)
- Add comment with PR link

**Branch completion:**
1. Verify tests pass (stop if they don't)
2. Present exactly 4 options:
   - Merge locally to base branch
   - Push and create PR
   - Keep branch as-is
   - Discard work (requires typed "discard" confirmation)
3. Execute choice
4. Cleanup worktree (for merge, PR, and discard — NOT for keep)

**Team extensibility:** Commit format configurable via CLAUDE.md:
- Emoji prefix: `✨ feat:` (optional, off by default)
- Jira ticket in subject: `[GSL-1234] feat:` (optional)
- Conventional Commits strict mode (optional)
- Co-authored-by tag (optional)

**Entry condition:** Code verified (from qa-verify)
**Exit action:** Shipped. Next story begins.

---

### Role: Memory

#### enggenie:memory-recall
**Purpose:** Cross-session context search and token-efficient code exploration

**Triggers on:** "What were we doing?", "Did we solve this before?", "How did we do X last time?", previous session context

**Requires:** claude-mem plugin installed. If not installed, this skill silently does nothing when invoked by other skills. Only shows an error when directly invoked by the user.

**3-layer memory search (token-efficient):**
1. **Search** → Get index with IDs (~50-100 tokens/result)
   ```
   search(query="authentication", limit=20, project="my-project")
   ```
2. **Timeline** → Get context around interesting results
   ```
   timeline(anchor=11131, depth_before=3, depth_after=3)
   ```
3. **Fetch** → Get full details ONLY for filtered IDs (~500-1000 tokens each)
   ```
   get_observations(ids=[11131, 10942])
   ```

**Never fetch full details without filtering first. 10x token savings.**

**Code exploration (AST-based, token-efficient):**
1. **smart_search** → Find symbols across codebase (~2-6k tokens vs ~39-59k for Explore agent)
2. **smart_outline** → Get file structure (~1-2k tokens vs ~12k+ for full Read)
3. **smart_unfold** → See specific function implementation (~400-2k tokens)

**How other skills use memory (graceful degradation):**
```
Every skill that references memory does this:

IF memory-recall available:
  [Search for relevant context]
  [Present findings to user or use in skill logic]
ELSE:
  [Skip silently — proceed without memory]
  [No error message, no mention of missing feature]
```

**Entry condition:** None — available anytime
**Exit action:** Context provided → resume whatever workflow triggered the recall

---

## Cross-Cutting Patterns (Applied Across All Skills)

These patterns from prior skill suites are preserved and adapted with original voice:

**1. TodoWrite Tracking:** Every skill with a checklist creates TodoWrite items. Mark in_progress before starting, completed after finishing. Prevents skipped steps.

**2. Announcement Pattern:** Each skill begins with "I'm using enggenie:[skill-name] to [purpose]." Makes behavior explicit and trackable.

**3. Instruction Priority Hierarchy (in gateway):**
1. User's explicit instructions (CLAUDE.md, project config) — highest
2. Genie skills — override default system behavior
3. Default system prompt — lowest

**4. Subagent Gate (in gateway):** If dispatched as a subagent to execute a task, skip the gateway skill.

**5. Parallel Agent Dispatch:** When multiple independent investigation threads exist (e.g., debugging two unrelated failures), dispatch one agent per independent problem domain. Documented as a pattern in dev-implement and dev-debug, not a separate skill (prior skill suites' dispatching-parallel-agents was rarely triggered standalone).

---

## Skill Interconnection & Handoff Enforcement

```
enggenie:pm-refine
  EXIT → "Spec saved. Invoke enggenie:architect-design or enggenie:architect-plan"
  GATE → Other skills check: does a spec exist? If yes, consume it.

enggenie:architect-design
  EXIT → "Design approved. Invoke enggenie:architect-plan"
  GATE → Must have user approval before proceeding to plan

enggenie:architect-plan
  ENTRY → Checks for spec (from pm-refine). If exists, inherits phases/AC.
  EXIT → "Plan saved. Invoke enggenie:dev-implement"
  GATE → Must have user approval before proceeding to implement
  REVIEW → Dispatch plan-reviewer subagent before presenting to user

enggenie:dev-implement
  ENTRY → Checks for plan (from architect-plan).
  EXIT → "All tasks complete. Invoke enggenie:qa-verify"
  GATE → No code without failing test (enforced by enggenie:dev-tdd)

enggenie:dev-tdd
  OVERLAY → Active during ANY coding (with or without dev-implement)
  GATE → No production code without failing test first

enggenie:review-code
  ENTRY → After dev-implement tasks (automatic in subagent flow)
  ALSO → When human PR review is received

enggenie:review-design
  ENTRY → After FE phase of dev-implement

enggenie:qa-verify
  ENTRY → Before any completion claim
  EXIT → "Verified. Invoke enggenie:qa-test or enggenie:deploy-ship"

enggenie:qa-test
  ENTRY → After qa-verify, when user-perspective testing is needed
  EXIT → Results reported. If passing → deploy-ship. If failing → back to dev.

enggenie:deploy-ship
  ENTRY → After verification/QA
  EXIT → Shipped. Next story.

enggenie:dev-debug
  ENTRY → Anytime something breaks. Interrupts any workflow.
  EXIT → Bug fixed → resume previous workflow

enggenie:memory-recall
  ENTRY → Anytime. Available to all other skills as a utility.
```

**Enforcement style:** Each skill declares what MUST come next. If a user says "just build it" without a plan, `enggenie:dev-implement` says: "No plan found. Should I create one with enggenie:architect-plan first, or proceed without a plan?"

This is SOFTER than prior skill suites (which blocks entirely) but PRESENT (not silent). The user can override, but they're informed.

---

## Skill Discovery (How Skills Self-Trigger)

Each skill has a CSO-optimized description (says WHEN to use, never HOW):

```yaml
enggenie:pm-refine: "Use when refining user stories, writing feature specifications,
  estimating story points, creating subtasks, planning spikes, or generating QA plans"

enggenie:architect-design: "Use when brainstorming features, making architectural decisions,
  evaluating technical tradeoffs, or documenting decisions as ADRs"

enggenie:architect-plan: "Use when creating implementation plans from specs or requirements —
  phased task breakdown with deployment readiness gates"

enggenie:dev-implement: "Use when executing an implementation plan task-by-task —
  dispatches subagents, manages worktrees, handles phased deployment"

enggenie:dev-tdd: "Use when writing any code — enforces test-driven development discipline
  with RED-GREEN-REFACTOR cycle, fires during any coding task"

enggenie:dev-debug: "Use when encountering any bug, test failure, or unexpected behavior —
  systematic root cause investigation before proposing any fixes"

enggenie:review-code: "Use when requesting or receiving code review — dispatches reviewer
  subagent or processes human PR feedback with technical evaluation"

enggenie:review-design: "Use when reviewing frontend implementation against design specs —
  design system compliance, responsive behavior, accessibility audit"

enggenie:qa-verify: "Use before claiming any work is complete — evidence-based verification
  that tests pass, builds succeed, and requirements are met"

enggenie:qa-test: "Use for QA-perspective testing — Playwright automation or manual browser
  testing focused on user journeys, not implementation details"

enggenie:deploy-ship: "Use when committing, pushing, creating PRs, or completing branches —
  conventional commits, PR creation, Jira updates, worktree cleanup"

enggenie:memory-recall: "Use when asking about previous sessions — cross-session context
  search via claude-mem with token-efficient 3-layer retrieval"

enggenie (gateway): "Use when starting a development conversation and intent isn't clearly
  matched by a specific enggenie skill — routes to the right role-based expert"
```

Gateway fires ONLY when intent is ambiguous. "Debug this test failure" → dev-debug fires directly.

---

## File Structure

```
enggenie/
├── README.md                              # Installation, philosophy, skill overview
├── LICENSE (MIT)
├── .claude-plugin/
│   └── plugin.json                        # Plugin metadata for marketplace
├── skills/
│   ├── enggenie/
│   │   └── SKILL.md                       # Gateway/router (includes instruction priority, subagent gate)
│   ├── pm-refine/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   │   ├── refinement-agent.md
│   │   │   ├── qa-planner-agent.md
│   │   │   └── spec-reviewer-agent.md     # Reviews spec completeness before saving
│   │   └── references/
│   │       └── default-spec-template.md   # Overridable by team
│   ├── architect-design/
│   │   └── SKILL.md
│   ├── architect-plan/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       ├── explorer-agent.md
│   │       ├── doc-discovery-agent.md
│   │       └── plan-reviewer-agent.md     # Reviews plan completeness before saving
│   ├── dev-implement/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       ├── implementer-agent.md
│   │       ├── spec-reviewer-agent.md     # Checks code matches spec
│   │       └── quality-reviewer-agent.md
│   ├── dev-tdd/
│   │   ├── SKILL.md                       # Standalone TDD discipline
│   │   └── references/
│   │       ├── testing-anti-patterns.md   # Mock pitfalls, test-only code smell
│   │       └── defense-in-depth.md        # Validate at every layer
│   ├── dev-debug/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   │   └── investigator-agent.md
│   │   └── references/
│   │       ├── root-cause-tracing.md
│   │       ├── multi-component-debugging.md
│   │       └── condition-based-waiting.md # Replace timeouts with condition polling
│   ├── review-code/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── code-reviewer-agent.md
│   ├── review-design/
│   │   ├── SKILL.md
│   │   └── agents/
│   │       └── design-reviewer-agent.md
│   ├── qa-verify/
│   │   └── SKILL.md
│   ├── qa-test/
│   │   ├── SKILL.md
│   │   ├── agents/
│   │   │   ├── qa-automation-agent.md
│   │   │   └── qa-manual-agent.md
│   │   └── scripts/
│   │       └── with_server.py
│   ├── deploy-ship/
│   │   └── SKILL.md
│   └── memory-recall/
│       └── SKILL.md
├── references/
│   ├── cursor-tools.md                    # Tool name mappings for Cursor
│   ├── copilot-tools.md                   # Tool name mappings for Copilot CLI
│   ├── gemini-tools.md                    # Tool name mappings for Gemini CLI
│   └── opencode-tools.md                  # Tool name mappings for OpenCode
├── templates/
│   └── spec-template.md                   # Default, teams override in their repo
├── .claude-plugin/
│   ├── plugin.json                        # Claude Code plugin manifest
│   └── marketplace.json                   # Marketplace listing metadata
├── .cursor-plugin/
│   └── plugin.json                        # Cursor plugin manifest
├── gemini-extension.json                  # Gemini CLI extension manifest
├── README.md
├── CONTRIBUTING.md
├── CLAUDE.md                              # AI contributor guidelines
├── LICENSE (MIT)
└── docs/
    ├── getting-started/
    │   ├── README.md                      # Quick start guide
    │   ├── claude-code.md
    │   ├── cursor.md
    │   ├── copilot-cli.md
    │   ├── gemini-cli.md
    │   └── opencode.md
    ├── guides/
    │   ├── philosophy.md
    │   ├── how-it-works.md
    │   ├── team-setup.md
    │   ├── switching-from-prior skill suites.md
    │   └── writing-custom-skills.md
    ├── skills/
    │   └── README.md                      # All 13 skills overview
    ├── examples/
    │   ├── full-feature-walkthrough.md    # End-to-end: idea → spec → plan → code → test → ship
    │   ├── debug-session.md               # Real debugging session
    │   ├── code-review-session.md         # Review workflow example
    │   └── qa-testing-session.md          # QA workflow example
    └── changelog/
        └── CHANGELOG.md
```

**Total: 13 skills, 14 agent prompt templates, 9 reference files (5 technique + 4 platform), 1 script, 1 spec template, 6 getting-started docs**

---

## Implementation Order

| Order | Skill | Why first | Effort |
|-------|-------|-----------|--------|
| 1 | **enggenie:dev-tdd** | Foundation discipline. Every other coding skill references it. | Medium |
| 2 | **enggenie:dev-implement** | Core engine. Proves the subagent architecture. | High |
| 3 | **enggenie:architect-plan** | Feeds dev-implement. Together they cover plan→execute. | Medium |
| 4 | **enggenie:qa-verify** | Quick win. Lightweight. High daily impact. | Low |
| 5 | **enggenie:dev-debug** | Every dev hits bugs. Daily use. | Medium |
| 6 | **enggenie:pm-refine** | Biggest differentiator. No other suite has this. | High |
| 7 | **enggenie:architect-design** | Brainstorming entry point. | Medium |
| 8 | **enggenie:review-code** | Every PR cycle. Must match prior skill suites' depth. | Medium |
| 9 | **enggenie:qa-test** | QA gap-filler. Playwright + manual with evidence. | Medium |
| 10 | **enggenie:deploy-ship** | Last mile. Important but well-understood. | Low |
| 11 | **enggenie:review-design** | Frontend quality. | Medium |
| 12 | **enggenie** | Gateway — build last, once routing needs are clear. | Low |
| 13 | **enggenie:memory-recall** | Memory layer — add when core is solid. | Low |

**For each skill, follow writing-skills methodology:**
1. Write 2-3 pressure test scenarios
2. Run WITHOUT skill → document baseline (what went wrong, what rationalizations)
3. Write skill addressing those specific failures
4. Run WITH skill → verify improvement
5. Find new loopholes → close → re-test
6. Repeat until bulletproof

---

## Verification Plan

**Per skill:**
1. Write SKILL.md + agent prompt templates
2. Create 2-3 realistic test scenarios
3. Baseline test (WITHOUT skill) → record behavior, rationalizations
4. Skill test (WITH skill) → record behavior
5. Compare: skill must demonstrably improve quality/consistency
6. Loophole test: try to make Claude bypass the skill's rules
7. Close loopholes, re-test

**Integration tests:**
- pm-refine → architect-plan → dev-implement → qa-verify → deploy-ship (happy path)
- dev-implement → dev-debug → dev-implement (bug during implementation)
- qa-test → pm-refine (QA found missing AC, refine story)
- Full SDLC: pm-refine → architect-design → architect-plan → dev-implement → review-code → qa-verify → qa-test → deploy-ship

**Switching test:** Give enggenie to a prior skill suites user. Can they do everything they did before? Do the new skills (pm-refine, qa-test, memory-recall) add value they notice?

**Collect impact data during testing:**
- Time-to-completion with/without each skill
- Error rate and rework rate
- Include concrete numbers in shipped skill content (like prior skill suites' "15-30 min systematic vs 2-3 hours thrashing")

---

## Publishing Plan

### Phase 1: Core (skills 1-5)
Build dev-tdd, dev-implement, architect-plan, qa-verify, dev-debug. Test each with writing-skills methodology.
- Repo: `github.com/badrusiddique/enggenie`
- Local testing in `~/.claude/skills/enggenie/`

### Phase 2: Differentiators (skills 6-9)
Add pm-refine, architect-design, review-code, qa-test. Integration test: full SDLC flow.

### Phase 3: Polish (skills 10-13)
Add deploy-ship, review-design, gateway, memory-recall. End-to-end test.

### Phase 4: Publish

**Step 1: GitHub Repository**
- Create `github.com/badrusiddique/enggenie` (public)
- MIT license
- README with: philosophy, installation, skill overview, migration guide from prior skill suites

**Step 2: Plugin Manifest** (`.claude-plugin/plugin.json`)
```json
{
  "name": "enggenie",
  "description": "Role-based SDLC skill suite: PM, Architect, Dev, Reviewer, QA, Deploy — the right expert for the right moment",
  "version": "1.0.0",
  "author": {
    "name": "Badru Siddique",
    "email": "<your-email>"
  },
  "homepage": "https://github.com/badrusiddique/enggenie",
  "repository": "https://github.com/badrusiddique/enggenie",
  "license": "MIT",
  "keywords": [
    "skills", "sdlc", "tdd", "debugging", "planning",
    "code-review", "qa", "deployment", "agile", "pm",
    "architecture", "subagents", "workflows"
  ]
}
```

**Step 3: Marketplace File** (`.claude-plugin/marketplace.json`)
```json
{
  "name": "enggenie-marketplace",
  "description": "Genie — Role-based SDLC skill suite for Claude Code",
  "owner": {
    "name": "Badru Siddique"
  },
  "plugins": [
    {
      "name": "enggenie",
      "description": "Role-based SDLC skill suite: PM, Architect, Dev, Reviewer, QA, Deploy",
      "version": "1.0.0",
      "source": "./"
    }
  ]
}
```

**Step 4: Installation Methods**
Users can install via:
```bash
# Direct from GitHub (works immediately)
claude plugin add --from github.com/badrusiddique/enggenie

# Or add marketplace, then install
claude plugin add-marketplace github.com/badrusiddique/enggenie
claude plugin add enggenie
```

**Step 5: Discovery Platforms**
- Submit to [claudepluginhub.com](https://www.claudepluginhub.com) — central plugin registry
- Submit to [skills.sh](https://skills.sh) — skill discovery platform
- Both index from GitHub automatically once the repo has `.claude-plugin/plugin.json`

**Step 6: Community Marketplace (Optional)**
- Submit PR to `anthropics/claude-plugins-official` or `muratcankoylan/Agent-Skills-for-Context-Engineering` to be listed in a known marketplace
- This enables `claude plugin add enggenie` without specifying the GitHub URL

### Phase 5: Multi-Platform Support

Prior skill suites already supports Cursor, Copilot CLI, Codex, and Gemini via platform adapter references. Genie should ship with first-class support for all major AI coding tools.

**Supported platforms:**

| Platform | Config File | How Skills Load |
|----------|------------|-----------------|
| Claude Code | `.claude-plugin/plugin.json` | Native skill system via `Skill` tool |
| Cursor | `.cursor-plugin/plugin.json` | Skills auto-discovered, invoked via `skill` tool |
| GitHub Copilot CLI | `.copilot-plugin/plugin.json` | Skills loaded via `skill` tool |
| Google Gemini CLI | `gemini-extension.json` | Skills activated via `activate_skill` tool |
| OpenCode.ai | `.opencode/plugin.json` | Skills loaded from plugin directory |

**Platform adapter references** (in `references/`):
- `references/cursor-tools.md` — Tool name mappings (Cursor equivalents for Read, Edit, Bash, etc.)
- `references/copilot-tools.md` — Tool name mappings for Copilot CLI
- `references/gemini-tools.md` — Tool name mappings for Gemini CLI
- `references/opencode-tools.md` — Tool name mappings for OpenCode

**Gateway skill platform adaptation:** The `enggenie` gateway includes a section:
```
## Platform Adaptation
Skills use Claude Code tool names by default. For other platforms:
- Cursor: See references/cursor-tools.md
- Copilot CLI: See references/copilot-tools.md
- Gemini CLI: See references/gemini-tools.md
- OpenCode: See references/opencode-tools.md
```

### Phase 6: Documentation

**Principle: Write for a beginner who has never used an AI coding plugin before.** Every doc should assume zero prior knowledge. Include exact commands, expected outputs, screenshots descriptions, and "what you should see" after every step. No jargon without explanation. No steps without verification.

**Repository docs structure:**
```
docs/
├── getting-started/
│   ├── README.md                    # Quick start (install → first skill → see value in 5 min)
│   ├── claude-code.md               # Getting started with Claude Code
│   ├── cursor.md                    # Getting started with Cursor
│   ├── copilot-cli.md               # Getting started with GitHub Copilot CLI
│   ├── gemini-cli.md                # Getting started with Google Gemini CLI
│   └── opencode.md                  # Getting started with OpenCode.ai
├── guides/
│   ├── philosophy.md                # "The right expert for the right moment"
│   ├── how-it-works.md              # Architecture, subagent flow, skill map with diagrams
│   ├── team-setup.md                # How teams customize enggenie
│   ├── switching-from-prior skill suites.md # Migration guide with feature mapping table
│   └── writing-custom-skills.md     # How to extend enggenie with team-specific skills
├── skills/
│   └── README.md                    # All 13 skills: name, purpose, when it fires, example trigger
├── examples/
│   ├── full-feature-walkthrough.md  # End-to-end: idea → spec → plan → code → test → ship
│   ├── debug-session.md             # Real debugging session using enggenie:dev-debug
│   ├── code-review-session.md       # Requesting + receiving review workflow
│   └── qa-testing-session.md        # Playwright + manual QA workflow
└── changelog/
    └── CHANGELOG.md                 # Semantic versioning changelog
```

**Root-level docs:**
- `README.md` — Hero section, install command, skill overview table, philosophy, links to getting-started
- `CONTRIBUTING.md` — How to contribute (clear guidelines, welcoming tone)
- `LICENSE` — MIT
- `CLAUDE.md` — Contributor guidelines for AI agents working on enggenie itself

---

**Getting-started doc template (each platform follows this exact structure):**

```markdown
# Getting Started with enggenie on [Platform]

## Prerequisites
- [Platform] installed ([link to install guide])
- A code project to work in (any language)
- Terminal access

## Step 1: Install enggenie

Run this command in your terminal:
\`\`\`bash
[exact install command for this platform]
\`\`\`

**What you should see:**
\`\`\`
✓ Plugin "enggenie" installed successfully
  13 skills available
\`\`\`

**If you see an error:** [Common errors and fixes for this platform]

## Step 2: Verify Installation

Open your project in [Platform] and type:
\`\`\`
"What skills do I have from enggenie?"
\`\`\`

**What you should see:** A list of 13 skills grouped by role (PM, Architect, Dev, Reviewer, QA, Deploy, Memory).

## Step 3: Try Your First Skill

Let's try `enggenie:qa-verify` — the simplest skill that shows immediate value.

In any project with tests, type:
\`\`\`
"Run the tests and tell me if they pass"
\`\`\`

**What happens:**
1. enggenie:qa-verify activates automatically (you'll see "I'm using enggenie:qa-verify...")
2. It runs your test command
3. Instead of saying "tests should pass," it shows you EVIDENCE:
   \`\`\`
   47/47 tests pass, exit code 0. All tests passing.
   \`\`\`

**Why this matters:** Without enggenie, AI assistants often say "the tests should pass" without actually running them. enggenie:qa-verify enforces evidence before claims.

## Step 4: Try a Development Workflow

Now let's try something more powerful. Tell your assistant:
\`\`\`
"I want to add a utility function that validates email addresses. Let's use TDD."
\`\`\`

**What happens:**
1. `enggenie:dev-tdd` activates
2. It writes a failing test FIRST (RED)
3. Shows you the test failure
4. Writes minimal code to pass (GREEN)
5. Refactors if needed
6. Shows evidence that tests pass

## Step 5: Explore More Skills

| What you want to do | Say this | Skill that fires |
|---------------------|---------|-----------------|
| Plan a new feature | "I want to build a user dashboard" | enggenie:architect-design |
| Create an implementation plan | "Create a plan for the dashboard" | enggenie:architect-plan |
| Debug a failing test | "This test is failing, help me fix it" | enggenie:dev-debug |
| Review code before PR | "Review my changes before I push" | enggenie:review-code |
| Write a spec with estimation | "Write a spec for the search feature" | enggenie:pm-refine |
| Ship your code | "Commit and create a PR" | enggenie:deploy-ship |

## Step 6: Customize for Your Team (Optional)

Add to your project's CLAUDE.md (or equivalent config):
\`\`\`markdown
## enggenie Configuration
- Spec template: docs/templates/our-spec-template.md
- Commit format: [JIRA-123] type: description
- Estimation method: T-shirt (S/M/L/XL)
\`\`\`

See [Team Setup Guide](../guides/team-setup.md) for all configuration options.

## What's Next?
- [Full Feature Walkthrough](../examples/full-feature-walkthrough.md) — See enggenie handle an entire feature from idea to deployment
- [All 13 Skills Explained](../skills/README.md) — What each skill does and when it fires
- [How It Works](../guides/how-it-works.md) — Architecture, subagent model, skill interconnection
```

---

**README.md structure (beginner-friendly):**
```markdown
# enggenie — The Right Expert for the Right Moment

> Role-based SDLC skills for AI coding assistants.
> PM · Architect · Dev · Reviewer · QA · Deploy

**enggenie** gives your AI coding assistant expertise across the entire software development lifecycle — not just coding. Each skill is a domain expert that activates when you need it.

## What is a "skill"?

A skill is a set of instructions that makes your AI assistant behave like an expert in a specific area. When you say "debug this test failure," enggenie automatically activates its debugging skill — which enforces systematic root cause investigation instead of random guessing.

**You don't invoke skills manually.** They activate based on what you're doing.

## Install

\`\`\`bash
# Claude Code (recommended)
claude plugin add --from github.com/badrusiddique/enggenie

# Cursor
[cursor install command]

# Other platforms — see Getting Started guides below
\`\`\`

## What's Inside

| Role | Skill | What It Does | Example Trigger |
|------|-------|-------------|-----------------|
| PM | enggenie:pm-refine | Spec generation, story refinement, estimation | "Write a spec for user search" |
| Architect | enggenie:architect-design | Brainstorming, ADRs, technical decisions | "Let's brainstorm the caching approach" |
| Architect | enggenie:architect-plan | Implementation plans with deployment phases | "Create a plan from this spec" |
| Dev | enggenie:dev-implement | Subagent-driven TDD execution | "Execute the plan" |
| Dev | enggenie:dev-tdd | TDD discipline (RED-GREEN-REFACTOR) | "Add a validate email function" |
| Dev | enggenie:dev-debug | Systematic root cause investigation | "This test is failing" |
| Reviewer | enggenie:review-code | Request + receive code reviews | "Review my changes" |
| Reviewer | enggenie:review-design | Frontend/UI quality enforcement | "Check the dashboard against the design" |
| QA | enggenie:qa-verify | Evidence before completion claims | "Are the tests passing?" |
| QA | enggenie:qa-test | Playwright + manual browser testing | "Test the login flow as a QA engineer" |
| Deploy | enggenie:deploy-ship | Commit, PR, branch completion, Jira | "Create a PR for this work" |
| Memory | enggenie:memory-recall | Cross-session context (requires claude-mem) | "What did we do last session?" |

## Why enggenie?

**vs. no skills:** AI assistants without skills skip tests, guess at bugs, claim "done" without evidence, and write code before designing. enggenie enforces discipline.

**vs. prior skill suites:** Prior skill suites covers coding (TDD, debugging, planning). enggenie covers the entire SDLC — adds PM, QA, deployment, design review, and memory. Everything prior skill suites does, enggenie does too. [Migration guide →](docs/guides/switching-from-prior skill suites.md)

## Getting Started

Pick your platform:
- **[Claude Code](docs/getting-started/claude-code.md)** — Full guide with examples
- **[Cursor](docs/getting-started/cursor.md)** — Full guide with examples
- **[GitHub Copilot CLI](docs/getting-started/copilot-cli.md)** — Full guide with examples
- **[Google Gemini CLI](docs/getting-started/gemini-cli.md)** — Full guide with examples
- **[OpenCode.ai](docs/getting-started/opencode.md)** — Full guide with examples

## Examples

- [Full Feature Walkthrough](docs/examples/full-feature-walkthrough.md) — Idea → spec → plan → code → test → ship
- [Debugging Session](docs/examples/debug-session.md) — Systematic root cause investigation
- [Code Review Session](docs/examples/code-review-session.md) — Requesting and receiving reviews
- [QA Testing Session](docs/examples/qa-testing-session.md) — Playwright + manual testing

## For Teams

enggenie is customizable per team — spec templates, commit format, estimation method, architecture context. See [Team Setup Guide](docs/guides/team-setup.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). We welcome contributions — especially new reference docs, platform adapters, and bug reports.

## License

MIT
```

---

**Publishing Step-by-Step Guide (for the author):**

### How to Publish enggenie

**Step 1: Create GitHub Repository**
```bash
# Create repo on GitHub
gh repo create badrusiddique/enggenie --public --description "Role-based SDLC skill suite for AI coding assistants" --license MIT

# Clone locally
git clone https://github.com/badrusiddique/enggenie.git
cd enggenie
```

**Step 2: Add GitHub Topics** (for SEO/discoverability)
```bash
gh repo edit --add-topic claude-code,ai-skills,sdlc,tdd,agile,developer-tools,code-review,qa-testing,project-management,cursor,copilot,gemini
```

**Step 3: Create Directory Structure**
```bash
mkdir -p .claude-plugin .cursor-plugin skills/{enggenie,pm-refine,architect-design,architect-plan,dev-implement,dev-tdd,dev-debug,review-code,review-design,qa-verify,qa-test,deploy-ship,memory-recall} references templates docs/{getting-started,guides,skills,examples,changelog}
# Create agent subdirectories for skills that need them
mkdir -p skills/pm-refine/{agents,references} skills/architect-plan/agents skills/dev-implement/agents skills/dev-tdd/references skills/dev-debug/{agents,references} skills/review-code/agents skills/review-design/agents skills/qa-test/{agents,scripts}
```

**Step 4: Write All Files**
Write each SKILL.md, agent template, reference doc, and config file per the plan.

**Step 5: Test Locally**
```bash
# Install as local plugin (Claude Code)
claude plugin add --from ./

# Verify skills load
# Open a project and ask: "What enggenie skills do I have?"

# Pressure test each skill using writing-skills methodology
# (baseline without → with skill → close loopholes)
```

**Step 6: Commit and Push**
```bash
git add -A
git commit -m "feat: initial release of enggenie SDLC skill suite (13 skills, 7 roles)"
git push origin main
```

**Step 7: Create GitHub Release**
```bash
gh release create v1.0.0 --title "enggenie v1.0.0" --notes "Initial release: 13 skills across 7 roles covering the entire SDLC."
```

**Step 8: Register as Self-Hosted Marketplace**
The `.claude-plugin/marketplace.json` file makes the repo itself a marketplace. Users can:
```bash
# Option A: Direct install from GitHub
claude plugin add --from github.com/badrusiddique/enggenie

# Option B: Add as marketplace, then install
claude plugin add-marketplace github.com/badrusiddique/enggenie
claude plugin add enggenie
```

**Step 9: Submit to Discovery Platforms**
- **claudepluginhub.com** — Submit repo URL. The hub reads `.claude-plugin/plugin.json` and indexes automatically.
- **skills.sh** — Submit repo URL. Indexes individual skills from `skills/` directory.
- Both platforms crawl GitHub repos with `.claude-plugin/` directories.

**Step 10: Submit to Community Marketplaces (Optional)**
- Open PR to `anthropics/claude-plugins-official` to be listed in the official marketplace
- Open PR to `muratcankoylan/Agent-Skills-for-Context-Engineering` for community marketplace

**Step 11: Cross-Platform Plugin Configs**
- `.cursor-plugin/plugin.json` — same format as `.claude-plugin/plugin.json`
- `gemini-extension.json` — Gemini CLI extension manifest
- Skills work across platforms; only the manifest format differs.

**Step 12: Announce**
- GitHub README serves as landing page
- Share on relevant communities (Twitter/X, Reddit r/ClaudeAI, Discord servers)
- Collect feedback, iterate, release v1.1.0

### Phase 7: Community & Growth
- Gather feedback from engineers using it
- Collect impact data (time-to-completion, error rates)
- Iterate based on real usage
- Semantic versioning with changelog
- Submit to community marketplaces for broader discovery
- Blog post / announcement for visibility
