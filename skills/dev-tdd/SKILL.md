---
name: dev-tdd
description: Use when writing any code - enforces test-driven development discipline with RED-GREEN-REFACTOR cycle, fires during any coding task
---

# dev-tdd

## Overview

No production code without a failing test first.

This is a discipline overlay, not a workflow step. It fires during ANY coding task - whether you're working from a plan, fixing a bug, adding a feature, or refactoring. There is no entry gate and no exit gate. If you're writing code, TDD rules are active.

The cycle is simple. The discipline is what matters.

## Announcement

When this skill is active, announce:

> "I'm using enggenie:dev-tdd to enforce test-driven development."

---

## Hard Rule: No Production Code Without a Failing Test First

If you catch yourself writing production code before a test: **stop**. Delete it. Write the test first.

No exceptions. No "just this once." No "I'll circle back." The test comes first or the code doesn't get written.

---

## Violating the Letter of TDD Is Violating the Spirit

There is no distinction between the letter and the spirit of TDD. The spirit IS the letter.

Writing a test that you know will pass is not TDD. Writing two tests before implementing is not TDD. Writing production code and then backfilling a test is not TDD. These aren't "close enough." They're a different practice entirely.

The value of TDD comes from the discipline of the cycle. Skip a step and you lose the feedback loop that makes it work.

---

## The Cycle: RED -> GREEN -> REFACTOR

Every piece of new behavior follows this cycle. Every time. No shortcuts.

### RED - Write a Failing Test

1. Write ONE minimal test that describes the next piece of behavior.
2. Run the test.
3. It **MUST fail** (not error - fail). A compilation error or import error is not RED. RED means the test ran and the assertion failed.
4. Read the failure message. It should describe the missing behavior clearly. If the failure message is confusing, fix the test before proceeding.

**Verification:** You saw a clear, expected failure message. The test ran. The assertion failed for the right reason.

### GREEN - Make It Pass

1. Write the **simplest** code that makes the failing test pass. Not the clever code. Not the complete code. The simplest.
2. Run the test. It **MUST pass**.
3. Run ALL tests. They **MUST all pass**. If something else broke, fix it before moving on.

**Verification:** The new test passes. All existing tests still pass. You wrote minimal code - nothing beyond what the test demanded.

### REFACTOR - Clean Up

1. Look at the code you just wrote. Look at the test you just wrote. Is there duplication? Poor naming? Unnecessary complexity?
2. Clean it up. Extract. Rename. Simplify.
3. Run ALL tests after every change. They **MUST stay green**.
4. No new behavior during refactor. If you want new behavior, start a new RED.

**Verification:** Tests are still green. Code is cleaner. No new behavior was added.

Then start the cycle again.

---

## Worked Example: Bug Fix with TDD

**Scenario:** Email validation accepts "user@" as valid.

**RED - Write the failing test:**
```python
def test_rejects_email_without_domain():
    assert validate_email("user@") == False
```

Run: `pytest tests/test_email.py::test_rejects_email_without_domain`
```
FAILED - assert True == False
```
Good. The test fails because the current code does not check for a domain.

**GREEN - Write the simplest fix:**
```python
def validate_email(email: str) -> bool:
    if "@" not in email:
        return False
    local, domain = email.rsplit("@", 1)
    return len(local) > 0 and len(domain) > 0
```

Run: `pytest tests/test_email.py`
```
4 passed
```
All tests pass. Do NOT add more validation yet.

**REFACTOR - Clean up while tests stay green:**
No refactoring needed - the code is already clean.

---

**Good test vs Bad test:**

| Aspect | Good | Bad |
|--------|------|-----|
| Name | `test_rejects_email_without_domain` | `test_email_validation` |
| Assertion | `assert validate_email("user@") == False` | `assert result is not None` |
| Scope | Tests ONE behavior | Tests multiple behaviors |
| Failure message | "assert True == False" tells you what broke | "AssertionError" tells you nothing |

---

## The Shortcut Tax

Every shortcut has a cost. Here's what you're actually paying.

| Shortcut | What it costs you |
|----------|------------------|
| "I'll write tests after" | Tests pass immediately - you've proved nothing. Bugs ship. |
| "Too simple to test" | Simple code breaks. 30 seconds to test. 30 minutes to debug in prod. |
| "Already manually tested" | No record. Can't re-run. You'll re-test every change by hand forever. |
| "TDD slows me down" | TDD is faster than debugging. Systematic beats ad-hoc. |
| "Just this once" | That's what you said last time. Discipline compounds. |
| "Keep the code as reference" | You'll adapt it instead of writing tests first. Delete means delete. |
| "Need to explore first" | Fine. Explore. Then throw it away. Start fresh with TDD. |
| "The test is hard to write" | Hard to test = hard to use = bad design. Simplify the interface. |
| "Tests after achieve same goals" | After answers "what does this do?" First answers "what should it do?" |
| "Existing code has no tests" | You're improving it. Add tests for what you touch. |
| "I already see the problem" | Seeing symptoms does not equal understanding root cause. Write the test. |

---

## Gut Check

STOP and start over if any of these are true:

- You wrote production code before writing a test
- Your test passed immediately (you never saw RED)
- You're writing multiple tests at once before implementing
- You're "just going to quickly add" something without a test
- You're thinking "this case is different because..."
- You're keeping deleted code "as reference"
- You wrote tests after implementation → Delete the code. Write the test. Watch it fail. Rewrite.
- You can't explain why a test failed → You don't understand the code. Investigate before proceeding.
- You're thinking "I already spent X hours on this code, deleting is wasteful" → Sunk cost fallacy. Delete it. TDD code is faster to rewrite than debug.
- You're thinking "TDD is dogmatic, I'm being pragmatic" → Pragmatic means following processes that work. TDD works. Skipping it is not pragmatic, it's reckless.

If you hit any of these: stop. Delete the production code. Go back to RED.

---

## Exceptions (Require Explicit User Permission)

These are the ONLY acceptable reasons to skip TDD. Each requires the user to explicitly say "skip TDD for this":

- **Throwaway prototypes** - Code that will be deleted before merge. Not "might be deleted" - WILL be deleted.
- **Generated code** - Auto-generated files (migrations, scaffolds, codegen output). Not hand-written code that "feels generated."
- **Configuration files** - Pure config with no logic (JSON, YAML, env files). Not config that contains conditional logic.

If you catch yourself thinking "this is basically an exception" - it's not. Ask the user.

---

## When Stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. Work backwards. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. Reduce dependencies. |
| Test setup huge | Extract helpers. Simplify the design. If setup is painful, the API is painful. |

---

## Good Tests

A good test has three qualities:

**Minimal** - Tests one thing. One behavior. One assertion where possible. When it fails, you know exactly what broke.

**Clear** - The test name describes the behavior, not the implementation. `test_returns_empty_list_when_no_items` tells you more than `test_get_items`.

**Shows intent** - The test demonstrates the desired API. Reading the test tells you how the code should be used. It's the first consumer of your design.

---

## Verification Checklist

Before marking ANY coding task complete, verify:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing (saw RED)
- [ ] Each test failed for the expected reason (correct failure message)
- [ ] Wrote minimal code to pass (no speculative generality)
- [ ] All tests pass (full suite, not just the new test)
- [ ] Tests use real code (mocks only when unavoidable - external services, file systems, network)
- [ ] Edge cases and error paths are covered

If any box is unchecked, you're not done.

---

## Supporting References

- `references/testing-anti-patterns.md` - Never test mock behavior, never add test-only methods to production code, mock COMPLETE data structures not partial ones
- `references/defense-in-depth.md` - Validate at every layer, make bugs structurally impossible through types and constraints

These references contain detailed patterns. Read them when you need specifics on test structure or validation strategy.

---

## Relationship to enggenie:dev-implement

`enggenie:dev-implement` orchestrates implementation work - it manages plans, dispatches subagents, and coordinates multi-step tasks.

`enggenie:dev-tdd` is a discipline overlay that fires during ANY coding, whether or not `dev-implement` is active. It is not a step in a workflow. It is the way code gets written.

When `dev-implement` is active, `dev-tdd`'s rules are enforced through the implementer subagent prompt. The subagent follows the RED-GREEN-REFACTOR cycle for every piece of code it writes.

When `dev-implement` is NOT active (ad-hoc coding, quick fixes, explorations that turn into real code), `dev-tdd` still fires. The discipline does not depend on having a plan.

---

## Recommended Model

**Primary:** sonnet
**Why:** TDD requires balanced speed and code quality. Sonnet writes good tests and clean implementations without the latency of opus. For complex domain logic, override to opus.

This is a recommendation. Ask the user: "Confirm model selection or override?"

---

## Entry / Exit

**Entry:** None. This skill fires during any coding task. No trigger required.

**Exit:** None. This is a discipline overlay, not a workflow step. It remains active as long as code is being written.
