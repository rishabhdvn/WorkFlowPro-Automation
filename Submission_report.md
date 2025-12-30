# QA Automation Case Study - Submission Report

## Part 1: Debugging Flaky Test Code

### 1. Root Cause Analysis
The original `test_user_login` failed intermittently in CI/CD due to **race conditions**:
* **Issue:** `assert page.url == "..."` executes immediately after the click. In slower CI environments, the browser redirect hasn't completed yet, causing a failure.
* **Issue:** `assert page.locator(...).is_visible()` does not wait for the element to hydrate if the app uses dynamic loading (React/Vue).
* **Issue:** Hardcoded credentials (`admin@company1.com`) make the test brittle and insecure.

### 2. The Fix
I refactored the test (see `tests/test_login_fix.py`) to use Playwright's **Auto-waiting Assertions**.
* **Fix:** Replaced `assert page.url` with `expect(page).to_have_url(...)`. This retries automatically until the timeout.
* **Fix:** Replaced standard asserts with `expect(locator).to_be_visible()`.

---

## Part 2: Test Framework Design

### 1. Framework Architecture
I designed a scalable **Page Object Model (POM)** framework:
* **`config/`**: Handles environment variables (Staging vs. Prod).
* **`pages/`**: (Proposed) To store UI selectors, separating logic from tests.
* **`tests/`**: Split into `ui`, `api`, and `integration` for faster feedback loops.
* **`conftest.py`**: Uses `pytest` fixtures for setup/teardown, ensuring every test gets a clean browser state.

### 2. Missing Requirements & Clarifications
* **2FA Handling:** The case study mentions 2FA. *Assumption:* We have a bypass mechanism (e.g., a specific header or secret key) for test users to avoid SMS automation complexity.
* **Test Data Cleanup:** *Question:* Do we have a database "reset" API, or must we manually DELETE every object created?
* **Mobile Definition:** *Clarification:* Does "Mobile Testing" require real devices (BrowserStack Appium) or is responsive web (Viewport resizing) sufficient? I implemented Viewport resizing for speed but architected the `conftest` to support BrowserStack drivers if needed.

---

## Part 3: API + UI Integration Strategy

### 1. The Hybrid Approach
My integration test (`tests/test_integration.py`) verifies the "Project Creation" flow using the most efficient layer for each step:
1.  **API Layer:** Creates the data. *Why?* It is 50x faster than UI creation and less flaky.
2.  **UI Layer:** Verifies the data. *Why?* This confirms the user actually *sees* the result.
3.  **Security Layer:** Uses `browser.new_context()` to verify Tenant Isolation.

### 2. Tenant Isolation
I validate that `User B` cannot see `User A's` project by spinning up a completely separate browser context (Incognito mode) within the same test. This guarantees no cookies or session data leak between tenants.