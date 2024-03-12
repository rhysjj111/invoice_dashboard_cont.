# Testing
This document is an extention of README.md and contains the tests carried out on invoice_dashboard app.

## URLs

### Navigation
Tests on link URLs.

**Start point** | **Button/link** | **Conditions** | **Expected outcome** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
login.html | 'Continue' | None | Navigate to allauth login page | Pass
allauth>..>login.html | 'Back' | None | Navigate to index.html | Pass
allauth>..>login.html | 'Login' | Valid credentials used | Navigate to invoice_list | Pass
allauth>..>login.html | 'Login' | Invalid credentials used | Warning expressing issue displayed to user | Pass
allauth>..>login.html | 'Forgot your password?' | None | Navigate to forf | Pass

### Forms
Tests on link URLs.

#### New entries

**Question** | **Answer given** | **Expected outcome** | **Result** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
Start date | 30 Decemeber 2016 | Validation warning message. Form not submitted. | 'Please enter date in format dd/mm/yyyy'. Form not submitted.| Pass
Start date | 30/12/2016 | Success message. Form submitted and data stored in database | 'Success'. Data in database.| Pass