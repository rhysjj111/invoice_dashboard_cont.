# Testing
This document is an extention of README.md and contains the tests carried out on invoice_dashboard app.

## URLs

### Navigation
Tests on link URLs.

**Start point** | **Button/link** | **Expected outcome** | **Result** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
login.html | 'Continue' | Validation warning message. Form not submitted. | 'Please enter date in format dd/mm/yyyy'. Form not submitted.| Pass
Start date | 30/12/2016 | Success message. Form submitted and data stored in database | 'Success'. Data in database.| Pass

### Forms
Tests on link URLs.

#### New entries

**Question** | **Answer given** | **Expected outcome** | **Result** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
Start date | 30 Decemeber 2016 | Validation warning message. Form not submitted. | 'Please enter date in format dd/mm/yyyy'. Form not submitted.| Pass
Start date | 30/12/2016 | Success message. Form submitted and data stored in database | 'Success'. Data in database.| Pass