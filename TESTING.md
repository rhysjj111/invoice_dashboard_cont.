# Testing
This document is an extention of README.md and contains the tests carried out on invoice_dashboard app.

## URLs

### Navigation
Tests on link URLs.

**Start point** | **Button/link** | **Conditions** | **Expected outcome** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
login.html | 'Continue' | None | Navigate to allauth login page | Pass
allauth login.html | 'Back' | None | Navigate to index.html | Pass
" " | 'Login' | Valid credentials used | Navigate to invoice_list with success message | Pass
" " | 'Login' | Invalid credentials used | Warning expressing issue displayed to user | Pass
" " | 'Forgot your password?' | None | Navigate to invoice_list.html | Pass
allauth logout.html | 'Logout' | User logged in | User logged out successfully and returned to index.html with a success message | Pass
allauth logout.html | 'Logout' | User logged in | User logged out successfully and returned to index.html with a success message | Pass

### Forms
Tests on link URLs.

**Question** | **Answer given** | **Expected outcome** | **Result** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
Start date | 30 Decemeber 2016 | Validation warning message. Form not submitted. | 'Please enter date in format dd/mm/yyyy'. Form not submitted.| Pass
Start date | 30/12/2016 | Success message. Form submitted and data stored in database | 'Success'. Data in database.| Pass

### Account access
Test whether users with different accounts have appropriate access to information.

**User account** | **Action** | **Expected view** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
Mechanic | Visit invoice_list.html | Only see valid/invalid invoice views. | Pass
Mechanic | Search for invoices that are restricted  | Only show invoices that are appropriate | #####################
Mechanic | Search for invoices that are restricted  | Only show invoices that are appropriate | #####################