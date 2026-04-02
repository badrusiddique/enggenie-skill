# Getting Started with enggenie on Claude Code

This guide walks you through installing enggenie, verifying it works, and trying your first skills. Every step includes what you should see afterward so you can confirm things are working.

No prior experience with AI coding plugins is required.

---

## Prerequisites

Before you begin, make sure you have:

- **Claude Code installed.** If you do not have it yet, visit [https://claude.ai/claude-code](https://claude.ai/claude-code) and follow the installation instructions for your operating system.
- **A code project to work in.** Any project with source code files will do. If you have a project with tests already written, that is ideal for trying the QA skills.
- **Terminal access.** Claude Code runs in your terminal (macOS Terminal, iTerm2, Windows Terminal, or any Linux terminal).

To confirm Claude Code is installed, open your terminal and run:

```bash
claude --version
```

**What you should see:** A version number like `1.x.x`. If you see "command not found," Claude Code is not installed yet — go to the link above first.

---

## Step 1: Install enggenie

In your terminal, run this command:

```bash
claude plugin add --from github.com/badrusiddique/enggenie-skill
```

**What you should see:** A confirmation message indicating the plugin was added successfully, similar to:

```
Added plugin enggenie from github.com/badrusiddique/enggenie-skill
```

**If you see an error:**

- `"not authenticated"` — Run `claude login` first, then retry the install command.
- `"plugin not found"` — Double-check the URL. It must be exactly `github.com/badrusiddique/enggenie-skill` with no typos.
- `"network error"` — Check your internet connection and try again.
- `"permission denied"` — Try running with `sudo` or check your file permissions.

---

## Step 2: Verify Installation

Start Claude Code in any project directory:

```bash
cd your-project
claude
```

Then type this message to Claude:

```
What enggenie skills do I have?
```

**What you should see:** Claude should list all 13 skills organized by role:

| Role | Skills |
|------|--------|
| PM | `enggenie:pm-refine` |
| Architect | `enggenie:architect-design`, `enggenie:architect-plan` |
| Developer | `enggenie:dev-implement`, `enggenie:dev-tdd`, `enggenie:dev-debug` |
| Reviewer | `enggenie:review-code`, `enggenie:review-design` |
| QA | `enggenie:qa-verify`, `enggenie:qa-test` |
| Deploy | `enggenie:deploy-ship` |
| Memory | `enggenie:memory-recall` |
| Meta | `enggenie:enggenie` (the orchestrator) |

**If you see fewer than 13 skills:** Try removing and re-adding the plugin:

```bash
claude plugin remove enggenie
claude plugin add --from github.com/badrusiddique/enggenie-skill
```

---

## Step 3: Try Your First Skill (enggenie:qa-verify)

This skill makes Claude provide **evidence** instead of guessing whether things work.

In any project that has tests, tell Claude:

```
Run the tests and tell me if they pass
```

**What happens behind the scenes:**

1. The `enggenie:qa-verify` skill activates automatically.
2. Claude runs your actual test suite (it does not guess or assume).
3. Claude shows you the real test output — pass counts, fail counts, error messages.
4. If tests fail, Claude shows the specific failures with details.

**What you should see:** Real terminal output from your test runner, followed by a clear summary. For example:

```
Ran 42 tests: 40 passed, 2 failed.

Failed tests:
- test_user_login: Expected status 200, got 401
- test_email_validation: "not-an-email" was accepted as valid
```

**Why this matters:** Without enggenie, AI assistants often say "the tests should pass" without actually running them. The qa-verify skill requires evidence before making any claims about test status.

---

## Step 4: Try a Development Workflow (enggenie:dev-tdd)

This skill enforces Test-Driven Development: write the test first, watch it fail, then write the code to make it pass.

Tell Claude:

```
Add a utility function that validates email addresses. Use TDD.
```

**What happens behind the scenes:**

1. The `enggenie:dev-tdd` skill activates automatically.
2. **RED phase:** Claude writes a test for email validation first, then runs it. The test fails because the function does not exist yet. Claude shows you the failure.
3. **GREEN phase:** Claude writes the minimum code to make the test pass, then runs the test again. Claude shows you the passing result.
4. **REFACTOR phase:** Claude cleans up the code if needed, runs tests again to confirm nothing broke.

**What you should see:** Three distinct phases with test output at each stage:

```
RED: wrote test_validate_email.py — running tests...
  FAIL: test_valid_email (ModuleNotFoundError)

GREEN: wrote validate_email.py — running tests...
  PASS: test_valid_email
  PASS: test_invalid_email
  PASS: test_empty_string

REFACTOR: cleaned up edge case handling — running tests...
  PASS: all 3 tests
```

**Why this matters:** Without enggenie, AI assistants typically write the function first and the test second (or skip tests entirely). The dev-tdd skill enforces the correct RED-GREEN-REFACTOR cycle.

---

## Step 5: Explore More Skills

Here is a quick reference for what to say to trigger each skill:

| What you want to do | Say this to Claude | Skill that fires |
|---------------------|--------------------|------------------|
| Write a product spec | "Write a spec for user search" | `enggenie:pm-refine` |
| Brainstorm a technical approach | "Let's brainstorm the caching approach" | `enggenie:architect-design` |
| Create an implementation plan | "Create a plan from this spec" | `enggenie:architect-plan` |
| Execute a plan with subagents | "Execute the plan" | `enggenie:dev-implement` |
| Add a feature with TDD | "Add a validate email function using TDD" | `enggenie:dev-tdd` |
| Debug a failing test | "This test is failing, help me fix it" | `enggenie:dev-debug` |
| Review your code changes | "Review my changes" | `enggenie:review-code` |
| Check UI against a design | "Check the dashboard against the design" | `enggenie:review-design` |
| Verify tests pass with evidence | "Are the tests passing?" | `enggenie:qa-verify` |
| Run browser-level QA testing | "Test the login flow as a QA engineer" | `enggenie:qa-test` |
| Create a PR and commit | "Create a PR for this work" | `enggenie:deploy-ship` |
| Recall previous session context | "What did we do last session?" | `enggenie:memory-recall` |

You do not need to memorize these. Just describe what you want in natural language and the right skill will activate.

---

## Step 6: Customize for Your Team (Optional)

You can configure enggenie behavior in your project's `CLAUDE.md` file. This file lives at the root of your project and contains instructions Claude follows automatically.

Example `CLAUDE.md` with enggenie configuration:

```markdown
# Project: my-app

## Testing
- Use pytest for all tests
- Tests live in the `tests/` directory
- Run tests with: `pytest tests/ -v`

## Code Review Standards
- All functions must have docstrings
- No print statements in production code
- Maximum function length: 50 lines

## TDD Requirements
- Every new feature must start with a failing test
- Minimum 80% code coverage on new code
```

When enggenie skills activate, they will respect these project-level instructions. For example, `enggenie:dev-tdd` will use `pytest` as your test runner because you specified it in `CLAUDE.md`.

---

## What's Next?

Now that enggenie is installed and working, explore further:

- **[Examples](../examples/)** — See full walkthroughs of enggenie skills on real tasks.
- **[Guides](../guides/)** — Deep dives on specific workflows (TDD, debugging, planning).
- **[Skill reference](../../README.md)** — Full documentation for all 13 skills.
- **[Contributing](../../CONTRIBUTING.md)** — Want to add or improve a skill? Start here.

If you run into issues, open an issue at [github.com/badrusiddique/enggenie-skill/issues](https://github.com/badrusiddique/enggenie-skill/issues).
