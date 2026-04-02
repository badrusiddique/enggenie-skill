# QA Testing Session Walkthrough

Testing a user registration flow using enggenie:qa-test.
Stack: React frontend, Node.js/Express backend, Playwright for automation.

---

## Context

The registration feature has passed enggenie:qa-verify -- unit tests pass, build is clean, lint has zero warnings. Now we test whether real users can actually register.

---

## Automation Mode: Playwright Tests

> I'm using enggenie:qa-test for automation QA testing.

### Read acceptance criteria from spec

The spec at `specs/user-registration-spec.md` lists these acceptance criteria:

1. User can register with email and password
2. Password must be at least 8 characters with one uppercase and one number
3. Duplicate email shows "Account already exists" error
4. After registration, user is redirected to `/dashboard`
5. Registration form is accessible via keyboard navigation

### Write tests for user journeys

The QA Automation subagent (sonnet) is dispatched. It writes tests focused on what users do, not what the code does.

```python
# tests/e2e/test_registration.py
from playwright.sync_api import expect

BASE_URL = "http://localhost:3000"


def test_user_can_register_with_valid_credentials(page):
    """Happy path: fill form, submit, land on dashboard."""
    page.goto(f"{BASE_URL}/register")
    page.wait_for_load_state("networkidle")

    page.fill('[data-testid="email-input"]', 'newuser@example.com')
    page.fill('[data-testid="password-input"]', 'SecurePass1')
    page.fill('[data-testid="confirm-password-input"]', 'SecurePass1')
    page.click('[data-testid="register-button"]')

    page.wait_for_url(f"{BASE_URL}/dashboard")
    expect(page).to_have_url(f"{BASE_URL}/dashboard")


def test_weak_password_shows_validation_error(page):
    """Password 'abc' should trigger validation before form submits."""
    page.goto(f"{BASE_URL}/register")
    page.wait_for_load_state("networkidle")

    page.fill('[data-testid="email-input"]', 'test@example.com')
    page.fill('[data-testid="password-input"]', 'abc')
    page.fill('[data-testid="confirm-password-input"]', 'abc')
    page.click('[data-testid="register-button"]')

    error = page.locator('[data-testid="password-error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("at least 8 characters")


def test_duplicate_email_shows_account_exists_error(page):
    """Registering with an email that already exists shows a specific error."""
    page.goto(f"{BASE_URL}/register")
    page.wait_for_load_state("networkidle")

    # This email was seeded in the test database
    page.fill('[data-testid="email-input"]', 'existing@example.com')
    page.fill('[data-testid="password-input"]', 'SecurePass1')
    page.fill('[data-testid="confirm-password-input"]', 'SecurePass1')
    page.click('[data-testid="register-button"]')

    error = page.locator('[data-testid="form-error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Account already exists")


def test_password_mismatch_shows_error(page):
    """Confirm password field does not match password field."""
    page.goto(f"{BASE_URL}/register")
    page.wait_for_load_state("networkidle")

    page.fill('[data-testid="email-input"]', 'mismatch@example.com')
    page.fill('[data-testid="password-input"]', 'SecurePass1')
    page.fill('[data-testid="confirm-password-input"]', 'DifferentPass2')
    page.click('[data-testid="register-button"]')

    error = page.locator('[data-testid="confirm-password-error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Passwords do not match")
```

Note: every test follows recon-then-action. `goto` then `wait_for_load_state("networkidle")` before any interaction. Selectors use `data-testid` attributes observed from the actual DOM, not guessed from source code.

### Run the tests

```
$ python scripts/with_server.py -- pytest tests/e2e/test_registration.py -v

Starting server on port 3000...
Waiting for health check... OK (1.2s)

tests/e2e/test_registration.py::test_user_can_register_with_valid_credentials PASSED
tests/e2e/test_registration.py::test_weak_password_shows_validation_error PASSED
tests/e2e/test_registration.py::test_duplicate_email_shows_account_exists_error PASSED
tests/e2e/test_registration.py::test_password_mismatch_shows_error PASSED

4 passed in 8.34s

Stopping server... done.
```

All four automated scenarios pass.

---

## Manual Mode: Browser-Assisted Testing

> I'm using enggenie:qa-test for manual QA testing.

The spec's QA test plan has 8 scenarios. The QA Manual subagent (sonnet) walks through each one using browser tools.

### Scenario 1: Happy path registration

**Navigate:** Open `http://localhost:3000/register`
**Wait:** networkidle
**Screenshot:** Initial state -- form with email, password, confirm password fields, and a "Create Account" button.

**Execute:**
- Fill email: `manual-test-1@example.com`
- Fill password: `ValidPass9`
- Fill confirm password: `ValidPass9`
- Click "Create Account"

**Wait:** URL changes to `/dashboard`
**Screenshot:** Dashboard page with welcome message "Hi, manual-test-1@example.com"

**Expected:** Redirect to dashboard after registration.
**Actual:** Redirected to `/dashboard`. Welcome message displayed.
**Status:** PASS

### Scenario 2: Empty form submission

**Navigate:** `http://localhost:3000/register`
**Wait:** networkidle
**Screenshot:** Empty form.

**Execute:** Click "Create Account" without filling any fields.

**Screenshot:** Form with validation errors.

**Expected:** Validation errors on email and password fields.
**Actual:** Email field shows "Email is required." Password field shows "Password is required." Confirm password shows no error (it waits for password to be filled first).
**Status:** PASS

### Scenario 3: Mobile viewport (375px)

**Execute:** Resize viewport to 375x812 (iPhone dimensions).
**Navigate:** `http://localhost:3000/register`
**Wait:** networkidle
**Screenshot:** Registration form on mobile.

**Execute:** Fill all fields, click "Create Account."
**Screenshot:** Result page.

**Expected:** Form is usable on mobile, no elements overflow or overlap.
**Actual:** The "Create Account" button is partially obscured by the soft keyboard when the confirm password field has focus. User must scroll down to tap the button.
**Status:** FAIL -- Severity: major. The button should remain visible above the keyboard, or the form should auto-scroll to keep the active element and submit button in view.

### Scenario 4: Double-click submit

**Navigate:** `http://localhost:3000/register`
**Wait:** networkidle

**Execute:** Fill valid credentials. Double-click "Create Account" rapidly.

**Expected:** Only one account is created. Button disables after first click.
**Actual:** Two requests sent to `/api/auth/register`. First succeeds (201), second fails (409 "Account already exists"). User sees a flash of the error message before redirecting to dashboard.
**Status:** FAIL -- Severity: major. The submit button should disable after the first click to prevent duplicate submissions. The 409 flash is a poor user experience.

### Remaining scenarios

Scenarios 5-8 (keyboard navigation, special characters in email, password exactly 8 characters, back button after registration) all pass.

---

## Test Matrix Report

| Scenario | Steps | Expected | Actual | Status |
|----------|-------|----------|--------|--------|
| Happy path registration | Fill valid data, submit | Redirect to dashboard | Redirected to /dashboard, welcome shown | PASS |
| Empty form submission | Click submit with no data | Validation errors on required fields | Email and password errors shown | PASS |
| Weak password | Enter "abc", submit | Validation error about requirements | "at least 8 characters" error shown | PASS |
| Duplicate email | Use existing email, submit | "Account already exists" error | Error message displayed | PASS |
| Password mismatch | Different password/confirm | "Passwords do not match" error | Error shown on confirm field | PASS |
| Mobile viewport (375px) | Register on iPhone width | Form usable, no overflow | Submit button obscured by keyboard | FAIL (major) |
| Double-click submit | Rapid double-click register | One account created, button disables | Two requests sent, 409 error flash | FAIL (major) |
| Keyboard navigation | Tab through form, Enter to submit | All fields reachable, Enter submits | Full keyboard access works | PASS |

**Result: 6 PASS, 2 FAIL**

Both failures are severity "major" -- the feature works but has usability issues that affect real users.

---

## Exit

Two failures found. Routing back to the developer with this report.

**FAIL 1 -- Mobile keyboard overlap:** The submit button is hidden behind the mobile keyboard when the last input field has focus. Fix: add scroll-into-view behavior on focus, or use a sticky submit button above the keyboard.

**FAIL 2 -- Double-click duplicate submission:** The register button accepts multiple clicks, sending duplicate API requests. Fix: disable the button after the first click and re-enable only if the request fails.

Both issues need to be fixed and retested before proceeding to enggenie:deploy-ship.

---

## What This Session Demonstrated

**Automation mode** tested the core user journeys -- the paths a developer would think to check. All four passed.

**Manual mode** found two bugs that automation missed: the mobile keyboard overlap and the double-click race condition. These are the kinds of bugs that only surface when you interact with the actual product the way a real user would -- on a small screen, clicking impatiently.

The recon-then-action pattern (navigate, wait, screenshot, then act) prevented flaky results. Every interaction started from a known page state, not an assumed one. The screenshots at each step provide evidence for every PASS and FAIL verdict.
