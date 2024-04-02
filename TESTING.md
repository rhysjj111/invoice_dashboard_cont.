# Testing
This document is an extention of README.md and contains the tests carried out on invoice_dashboard app.

## URLs

### Navigation
Tests on link URLs. All tests are carried out at mobile and desktop screen sizes.

**Start point** | **Button/link** | **Conditions** | **Expected outcome** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
login.html | 'Continue' | None | Navigate to allauth login page | Pass
allauth login.html | 'Back' | None | Navigate to index.html | Pass
" " | 'Login' | Valid credentials used | Navigate to invoice_list with success message | Pass
" " | 'Login' | Invalid credentials used | Warning expressing issue displayed to user | Pass
" " | 'Forgot your password?' | None | Navigate to invoice_list.html | Pass
allauth logout.html | 'Logout' | User logged in | User logged out successfully and returned to index.html with a success message | Pass
allauth logout.html | 'Logout' | User logged in | User logged out successfully and returned to index.html with a success message | Pass
invoice_list.html | Add invoice, edit invoice | None | Relevant modal pops up, feedback provided to user | Pass
" " | Go to customers | None | Redirects to customer_list.html | Pass
" " | Change status of invoice | Logged in as 'Mechanic', 'Foreman' and 'Accounts' at seperate times. | Status of invoice successfuly changes to intended status, feedback provided to user | Pass
" " | Change filter view of invoices | Logged in as 'Mechanic', 'Foreman' and 'Accounts' at seperate times. | Each filter should display only the relevant invoices | Pass
invoice_summary.html | Toggle invoice headings (Details, Parts, Labour) | None | Each heading should reveal correct information or message conveying no information added to database | Pass
" " | Add part, add labour, edit part/labour/details | None | Relevant modal pops up, feedback provided to user | Pass
" " | Delete part, labour entry | None | Confirmation modal pops up, entry is successfuly deleted from the database, feedback provided to user | Pass
" " | Add invoice, edit invoice | None | Relevant modal pops up | Pass
" " | Delete invoice entry | None | Confirmation modal pops up, entry is successfuly deleted from the database, feedback provided to user | Pass

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
Mechanic, Foreman | Visit invoice_list.html | Only see filter views for valid and invalid invoice views. | Pass
Accounts | " " | See filters for valid, pending and inactive. | Pass
Mechanic | Search for invoices that are restricted  | Only show invoices that are appropriate | #####################
Mechanic | Change status of invoice from 'open' to 'ready for processing'  | Invoice status changes successfully, user feedback to say so, invoice disapears from view and into Foreman view | #####################

### Invoice app
#### Invoice summary
**Section** | **Action** | **Expected view** | **Pass/Fail**
:-----:|:-----:|:-----:|:-----:|:-----:
Invoice details form, parts form, labour form | Edit any of the fields and submit. | Success message, redirect to page, entry successfully edited. | Pass
Invoice details form, parts form, labour form | Submit with no changes to field. | Success message, redirect to page, no changes made. | Pass
Invoice details form, parts form, labour form | Enter invalid information and submit form. | Error message, redirect to page, no changes made. | Pass
Parts form, labour form | Check delete and submit. | Success message, redirect to page, entry deleted. | Pass
Invoice form | Change 'customer' select input to another customer when both 'customer' and 'vehicle' are prepopulated. | Vehicle choice is reset to default '-----' answer and vehicle list is filtered to new customer. | Pass
Totals | Parts and Labour rows added, fully populated | Subtotal calculated for field(s), total calculated. | Pass
Totals | Parts or Labour rows added, fully populated (not both) | Subtotal calculated for field, total calculated. | Pass
Totals | Parts or Labour rows added, partially populated | Error message displayed at subtotal and total. | Pass
Invoice | Delete button pressed #######

