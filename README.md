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
- Another security risk, is that I have removed password validation for new users. The purpose of this is to make it as easy as possible to get users set up at first, then if the garage staff take to the MVP, improving security by adding password validation and getting users to change their passwords.

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
- I had an issue styling the allauths login template to look the same as the preceding login prompt. I got round this by adding bootstrap to the allauth base.html and customising the 'button.html' element found in allauth>elements to accept a class for the buttons and styled it with bootstrap classes. I wrapped the whole thing in bootstrap container and relevant classes using 'entrance.html'; I got that trick from the Boutique Ado walkthrough.

- While trying to make a bootstrap table row clickable, I found there were no solutions from bootstrap out of the box. After much research, I settled for the solution of putting an anchor in each cell and changing it's display to block. There were other solutions proposed on [Stack overflow](https://stackoverflow.com/questions/17147821/how-to-make-a-whole-row-in-a-table-clickable-as-a-link) but I found this one to be best as one user pointed out, for assistive software rather than using javascript/css.

- There is a 4 column table in invoice_list.html and customer_list.html, this posed a problem for mobile. I got around this by condesing the information into one column for mobile and showing the full table for large screens and above.

- I wanted to use Django choices field in a couple of the models and wanted to use the most up to date version of doing this. An article on [Stack Overflow](https://stackoverflow.com/questions/63418135/using-choices-in-a-field-in-django-models) gave me a few ways to go about it (new and old) and I went with the most recent way using built in Django feature IntegerChoices.

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
- The boilerplate used in base.html was taken from [bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) and edited.
- [Stack overflow](https://stackoverflow.com/) was used many times and referenced throughout the readme for specific examples.
- I got the idea of using slugs for easier to understand URLs from a tutorial on how to build an invoice platform, on [Youtube](https://www.youtube.com/watch?v=KU_taqbG00U&t=8159s).