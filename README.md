# An invoice dashboard for a vehicle repair workshop.

Live site: <br>
Github repository: https://github.com/rhysjj111/project_4_invoice_dashboard

### Overview

This project is MS4 for The Code Academy. It is an MVP for an invoice dashboard which will be tried and tested in a vehicle repair workshop once finished. It comprises of two main sections for configuration; 'invoices' and 'customers', three user types, who can use the software; 'mechanic', 'foreman' and 'accounts'. A finished invoice will be sent the the customer who will have the opportunity to view the invoice, save it to keep and pay securely via 'Stripe'.

## UX

### Site owner/developer goals
To construct a working MVP that can provide the most basic level of functionality for an invoice dashboard, for a workshop, which can either be iterated upon, changed or scrapped depending on results. 

### External users goals
* Eliminate the need for paper invoices which will save time when; constructing and editing and finding invoices, and save money on paper. 
* Provide a constant record of which invoices are at which stage, making sure invoices are double checked before they go out.
* Provide a record of who has paid, who's invoices are due, which means customers can be reminded before payments are overdue. 
* Automate sending reminder emails so they can be constructed with the click of a button to save time and keep emails consistent.
* Provide customers with an easy and safe way of paying an invoice.

### Proposed features
- Users can input customer and vehicle data which can be used to construct invoices.
- Users can add parts and labour entries to an invoice which will total costs and add VAT for the final bill to be presented to the customer.
- Automated reminder emails for payments nearly due.
- Send customers the invoice via email which they can follow a link to secure payment.

The features listed are the core functionality required to move from paper invoicing to online. I believe these are achievable with the technology and timeframe available.

### User stories
(user stories image)

## Design

### Design choices
- I've designed the wireframes 'mobile-first' to minimise unnecessary features or content. Another reason this design choice is it's anticipated the invoices will be created on the go, via mobile, by the mechanics/foreman on the ground as they work.
- I've chosen only to show invoices with 'open' status, and remove filter views of 'pending' (ready to send to customers) and 'inactive' (complete invoices) to remove complexity from mobile devices. Tablets will be the same as mobiles with just the structures edited slightly where needed.
- The invoices will follow a path and each user will only be able to access the invoice when the status corresponds to their position. This is intended to keep their view of the list of 'active' invoices as relevant as possible. Invoices can be moved forward and backwards along the path/journey if mistakes are made.
- I've chosen not to give the customer a login, or a view of their previous invoices, just a link to download the invoice and store it themselves. The reason for this is to focus on the users in the garage and their experience. The customer won't need a login or history view if the garage staff don't move from paper invoices to online.
- Invoices and customers will have a search bar which will search for multiple fields in the database; vehicle registration, name, date etc. rather than have multiple filter fields, again for simplicity.
- Bootstrap alerts will be used to provide the user with feedback when making changes to the database etc. A confirmation or error page will be used for customers paying through Stripe.
- I plan to make good use of Bootstrap throughout the project and keep custom css styling to a minimum; this can be updated at a later time.
- Bootstrap modals will be used for much of the new entries to the database (adding parts/labour/starting an invoice etc.)

### Security
- Django comes with lots of safety features and I plan to use their forms feature where possible to protect the database. I will include my own validation where applicable.
- There is a potential security risk to customer data, where they are following a link to access and pay their invoice. Although I can't see why anyone would want to gain access to the link and pay their bill, in the future customers should have a login, especially if their invoice history is added as a feature.

### Wireframes
Desktop wireframes:
![Desktop wireframes](/wages_calculator/static/images/wireframes/project3_desktop_wf.png)


Mobile wireframes:
![Mobile wireframes](/wages_calculator/static/images/wireframes/project3_mobile_wf.png)



### Additional diagrams

- 



### Colour scheme
The colour scheme was constructed on [coolors.co](https://coolors.co/03120e-00469b-ffffff-31e981-ff7f11). The scheme is based on the colour of the logo of the company this project is designed for.
- (colour scheme picture)

### Form data validation
#### 
- 

### End design similarity/difference
- 


### Future features to include/update
- 


## Testing 
[Testing.md](./TESTING.md)


### Issues
- 
#### JS
- 

#### CSS
- 

#### Features
-


### Validators

- HTML
  - 

- CSS
  - 

- JS
  - 

### Lighthouse




## Deployment




## Credits
- The colour pallet was found on: https://www.canva.com/learn/website-color-schemes/
- A helpful article on [Stack overflow](https://stackoverflow.com/questions/19216334/python-give-start-and-end-of-week-data-from-a-given-date) gave me the solution to finding the start and end date of the week from a given date.
- [SQLAlchemy docs](https://docs.sqlalchemy.org/en/20) were used a lot to determine how to query the database via ORM.
- This [Stack overflow](https://www.tutorialspoint.com/how-to-check-an-element-with-specific-id-exist-using-javascript) explained how to check an element for a particular Id, which I had needed for the Javascript to only show Mondays on the wages calculator datepicker.
- [Stack overflow](https://stackoverflow.com/questions/51205600/datepicker-materializecss-disabled-days-function) This article explained how to use the disable days funtion of the Materialize datepicker.
- [Stack overflow](https://stackoverflow.com/questions/21991820/style-active-navigation-element-with-a-flask-jinja2-macro) and [TTL25's Jinja2 tutorial](https://ttl255.com/jinja2-tutorial-part-5-macros/) were both used when constructing the nav_link macro, used to determine which navigation link should be active. The Stack overflow thread gave me the basic structure of the macro, and the tutorial allowed me to understand Jinja's varargs keyword so that I could expand the macro to also take into account sub-menu pages.
- [Stack overflow](https://stackoverflow.com/questions/73961938/flask-sqlalchemy-db-create-all-raises-runtimeerror-working-outside-of-applicat) - This article helped me update my ElephantSQL database with my tables, running the newest version of Flask-SQLAlchemy.
- [Medium](https://ed-a-nunes.medium.com/field-validation-for-backend-apis-with-python-flask-and-sqlalchemy-30e8cc0d260c) and [stack overflow](https://stackoverflow.com/questions/18982610/difference-between-except-and-except-exception-as-e) helped with form validation at the back end.
- This article on [Stack overflow](https://stackoverflow.com/questions/29017379/how-to-make-fadeout-effect-with-pure-javascript) helped me with transitioning out flash messages using css and Javascript.