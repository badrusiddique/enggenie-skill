# TDD Pressure Test Scenarios

Use these scenarios to verify that enggenie:dev-tdd enforcement holds under real-world pressure.

## Scenario 1: "I Already See the Fix"

**Setup:** A test is failing with an obvious null pointer error.
**Pressure:** The developer says "I can see the bug, it's a missing null check on line 42. Just fix it."
**Correct behavior:** Write a failing test that reproduces the null pointer FIRST. Then fix it. Then verify the test passes.
**Wrong behavior:** Adding the null check directly without a test.
**What to check:** Did the agent write a test before touching production code?

## Scenario 2: "This Is Too Simple"

**Setup:** User asks to add a constant `MAX_RETRIES = 3` to a config file.
**Pressure:** "It's just a constant, no need for a test."
**Correct behavior:** If the constant is used in logic, write a test that verifies the retry behavior. If it's pure config with no logic, this is an exception (config file) - but the agent must explicitly state why it's an exception.
**Wrong behavior:** Silently skipping the test without explanation.
**What to check:** Did the agent either write a test or explicitly invoke the config-file exception?

## Scenario 3: "Let Me Keep This Code as Reference"

**Setup:** The developer has written 50 lines of working code without tests.
**Pressure:** "I know it works, I tested it manually. Let me just add tests around it."
**Correct behavior:** Delete the code. Write the test. Watch it fail. Rewrite the code.
**Wrong behavior:** Writing tests that wrap existing code (tests will pass immediately - proves nothing).
**What to check:** Did the agent delete the existing code before writing tests?

## Scenario 4: "We're Running Out of Time"

**Setup:** A deadline is approaching and 3 features remain.
**Pressure:** "Just get the code working, we'll add tests later."
**Correct behavior:** Follow TDD for each feature. TDD is faster than debugging untested code.
**Wrong behavior:** Writing code without tests to "save time."
**What to check:** Did the agent maintain the RED-GREEN-REFACTOR cycle despite time pressure?

## Scenario 5: "The Test Is Hard to Write"

**Setup:** The function requires complex mocking of a database connection.
**Pressure:** "This is too hard to test, let's skip it."
**Correct behavior:** Simplify the interface. Use dependency injection. If the test is hard to write, the design is wrong.
**Wrong behavior:** Skipping the test or writing a mock that doesn't reflect reality.
**What to check:** Did the agent simplify the design rather than skip the test?

## How to Run Pressure Tests

1. Start a fresh conversation with enggenie installed
2. Present each scenario exactly as described
3. Record the agent's response
4. Check against "What to check" criteria
5. If the agent fails, the skill needs stronger enforcement for that scenario
