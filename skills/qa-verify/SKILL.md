---
name: qa-verify
description: Use before claiming any work is complete - evidence-based verification that tests pass, builds succeed, and requirements are met
---

# Verification Before Completion

**Announce:** "I'm using enggenie:qa-verify to verify before claiming completion."

## Hard Rule: Don't say "done" until you've seen the proof.

No "should work." No "probably passes." No "looks good." Run the command. Read the output. State the evidence.

**Current-turn binding:** If you haven't run the verification command in THIS response, you cannot claim it passes. Previous turns don't count - state may have changed.

## The Verification Gate

Before claiming ANYTHING is complete, follow this exact sequence:

```
1. IDENTIFY - What command proves this claim?
2. RUN     - Execute the FULL command. Fresh. Complete. Not partial.
3. READ    - Full output. Exit code. Failure count. Warnings.
4. VERIFY  - Does output actually confirm your claim?
   YES → State claim WITH evidence ("47/47 tests pass, exit 0")
   NO  → State actual status ("3 failures in auth module")
5. ONLY THEN - Make the claim.
```

Claiming work is complete without verification is dishonesty, not efficiency. Skip any step and you're lying, not verifying.

## What Counts as Evidence

| Claim | You need | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures, exit 0 | "Should pass", previous run, partial run |
| Build works | Build command: exit 0, no errors | "Linter passed" (linter is not compiler) |
| Bug fixed | Original symptom gone + regression test passes | "Code changed, should be fixed" |
| Feature complete | Every acceptance criterion verified with evidence | "Tests pass" (tests are not requirements) |
| Subagent succeeded | Check VCS diff, verify changes actually exist | Trust subagent's "success" report |
| No regressions | Full test suite passes after change | "Only touched one file" |
| Linter clean | Linter output: 0 errors, 0 warnings | "Fixed the ones I saw" |

## Gut Check - About to Claim Success?

Stop if you notice yourself:

- **Using hedge words** - "should", "probably", "seems to", "I think" → Run the command first.
- **Celebrating early** - "Done!", "Perfect!", "All good!" before verification → Stop. Verify. Then state facts.
- **Trusting a subagent** - Agent reports "DONE" or "success" → Check the diff yourself. Agents can hallucinate completion.
- **Skipping "just this once"** - No exceptions. The one you skip is the one that breaks.
- **Extrapolating** - "Linter passed, so build will too" → Linter is not compiler. Run the build.
- **Relying on memory** - "Tests passed earlier" → Run them again. State may have changed.
- **Feeling confident** - Confidence is not evidence. Evidence is evidence.
- You're using ANY wording that implies success without evidence → This rule applies to:
  - Exact phrases ("tests pass", "build works")
  - Paraphrases ("I've confirmed the changes", "everything looks good")
  - Implications of success ("the fix addresses the issue")
  - ANY communication suggesting completion or correctness
  Violating the letter of this rule is violating the spirit of this rule.

## The Shortcut Tax

| Shortcut | What it costs you |
|----------|------------------|
| "Should work now" | You don't know until you run it. Run it. |
| "I'm confident it passes" | Confidence is not evidence. Evidence is evidence. |
| "Just this once" | No exceptions. The one you skip is the one that breaks. |
| "Linter passed, so build will too" | Linter is not compiler. Different tools, different checks. |
| "Agent said it's done" | Agents hallucinate completion. Verify the diff independently. |
| "Partial check is enough" | Partial check proves partial correctness. Run the full suite. |
| "I already ran this earlier" | State changes. Run it fresh. Read the current output. |
| "The change is too small to break anything" | Small changes cause big breaks. Verify anyway. |

## Verification Patterns

**Tests:**
```
Run: npm test (or equivalent)
See: "47/47 tests pass, exit 0"
Claim: "All 47 tests pass."
```

**Build:**
```
Run: npm run build (or equivalent)
See: "Build completed, exit 0"
Claim: "Build succeeds."
```

**Bug Fix (TDD Red-Green):**
```
1. Write regression test
2. Run → test FAILS (confirms bug is captured)
3. Apply fix
4. Run → test PASSES (confirms fix works)
5. Revert the fix temporarily → run the regression test → confirm it FAILS (proves the test catches the bug)
6. Restore the fix → run all tests → confirm everything passes
7. Run full suite → all pass (no regressions)
Claim: "Bug fixed. Regression test passes. No regressions (47/47 pass)."
```

**Requirements Completion:**
```
1. Re-read the spec/plan acceptance criteria
2. Create checklist from each criterion
3. Verify each one with evidence (run command, check output)
4. Report: all verified, or list gaps
Claim: "5/5 acceptance criteria verified." or "4/5 verified. Missing: [specific gap]."
```

**Subagent Output:**
```
1. Subagent reports "DONE"
2. Check VCS diff: git diff BASE_SHA..HEAD_SHA
3. Verify: files changed, tests added, implementation exists
4. Run tests yourself
Claim: "Subagent changes verified. 3 files modified, 2 tests added, all passing."
```

## When Verification Fails

If the output does NOT confirm your claim:

1. **State the actual status** - "3 tests failing in auth module" (not "almost done")
2. **Diagnose** - Read the failure output. What specifically failed?
3. **Fix** - Address the specific failure
4. **Re-verify** - Run the full gate again from step 1
5. **Never claim partial success as success** - "47/50 tests pass" is not "tests pass"

## TodoWrite Integration

When this skill activates, create a TodoWrite item:
```
"Verify: [specific claim] with evidence"
```
Mark it completed only AFTER evidence is gathered and stated.

## Entry Condition

None - fires before any completion claim:
- Before saying "done" or "complete"
- Before committing code
- Before creating a PR
- Before claiming a bug is fixed
- Before reporting subagent success

## Exit Action

Verified → proceed to enggenie:qa-test (if QA needed) or enggenie:deploy-ship (if shipping).
