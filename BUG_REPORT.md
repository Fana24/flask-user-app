# Bug Report and Testing Documentation

## Student Name: Fana Nkosi
## Date: 6 February 2026
## Project: Flask User Registration Application

---

# Section 1: Test Cases Documentation

## Test Case Summary Table

| Test ID | Description | Input Type | Input Data | Expected Result | Actual Result | Status |
|---------|-------------|------------|------------|-----------------|---------------|--------|
| TC-01 | Valid Registration | Valid | username: newuser, email: newuser@example.com | User created, redirect to profile | ERROR - Syntax error | FAIL |
| TC-02 | Invalid Email | Invalid | email: invalid-email | Validation error shown | Cannot test - app crashes | FAIL |
| TC-03 | Empty Required Fields | Invalid | All fields empty | Validation errors | Cannot test - app crashes | FAIL |
| TC-04 | Minimum Age (1) | Edge | age: 1 | Registration succeeds | Cannot test - app crashes | FAIL |
| TC-05 | Maximum Age (150) | Edge | age: 150 | Registration succeeds | Cannot test - app crashes | FAIL |

---

## Detailed Test Cases

### TEST CASE 1: Valid User Registration
- **Test ID:** TC-01
- **Input Type:** Valid
- **Description:** Test that a user can register with all valid inputs
- **Pre-conditions:** Application is running, no user with same username/email exists
- **Test Data:**
  - Username: newuser
  - Email: newuser@example.com
  - First Name: New
  - Last Name: User
  - Age: 30
  - Bio: Hello world
- **Steps:**
  1. Navigate to /register
  2. Fill in all form fields with test data
  3. Click Register button
- **Expected Result:** User is created, redirected to profile page with success message
- **Actual Result (Before Fix):** Application crashes with SyntaxError
- **Actual Result (After Fix):** User created successfully, redirected to profile
- **Status:** PASS (after fix)

---

### TEST CASE 2: Invalid Email Format
- **Test ID:** TC-02
- **Input Type:** Invalid
- **Description:** Test that registration fails with invalid email format
- **Test Data:**
  - Username: testuser2
  - Email: invalid-email (no @ symbol)
  - First Name: Test
  - Last Name: User
- **Expected Result:** Form displays "Please enter a valid email address" error
- **Actual Result (After Fix):** Validation error displayed correctly
- **Status:** PASS (after fix)

---

### TEST CASE 3: Empty Required Fields
- **Test ID:** TC-03
- **Input Type:** Invalid
- **Description:** Test that registration fails when required fields are empty
- **Test Data:** All fields left empty
- **Expected Result:** Form displays "required" validation errors
- **Actual Result (After Fix):** Multiple validation errors displayed
- **Status:** PASS (after fix)

---

### TEST CASE 4: Edge Case - Minimum Age
- **Test ID:** TC-04
- **Input Type:** Edge Case
- **Description:** Test registration with minimum valid age boundary (1)
- **Test Data:**
  - Username: younguser
  - Email: young@example.com
  - Age: 1
- **Expected Result:** Registration succeeds
- **Actual Result (Before Fix):** Validation error due to reversed min/max
- **Actual Result (After Fix):** Registration succeeds
- **Status:** PASS (after fix)

---

### TEST CASE 5: Edge Case - Maximum Age
- **Test ID:** TC-05
- **Input Type:** Edge Case
- **Description:** Test registration with maximum valid age boundary (150)
- **Test Data:**
  - Username: olduser
  - Email: old@example.com
  - Age: 150
- **Expected Result:** Registration succeeds
- **Actual Result (Before Fix):** Validation error due to reversed min/max
- **Actual Result (After Fix):** Registration succeeds
- **Status:** PASS (after fix)

---

# Section 2: Bug Identification and Fixes

## Bug #1: Syntax Error - Missing Comma

### Location
- **File:** `app/routes.py`
- **Function:** `register()`
- **Line Number:** Approximately line 25-32

### Description
A comma is missing between the `last_name` and `age` parameters when creating a new User object. This causes a SyntaxError that prevents the application from starting.

### Error Message