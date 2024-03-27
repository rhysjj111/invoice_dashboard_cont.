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
- The invoices will follow a path of status'; 'open', 'work on hold', 'to be processed', 'to be verified', 'sent to customer' and paid. Each status will determine which users can access the invoice. This is intended to keep their view of the list of 'active' invoices as relevant as possible. Invoices can be moved forward and backwards along the path/journey if mistakes are made.
- An invoice number will only be created when an invoice has the status 'paid'. Once an invoice has been marked paid it can't be changed again for editting and the invoice number permanent.
- I've chosen not to give the customer a login, or a view of their previous invoices, just a link to download the invoice and store it themselves. The reason for this is to focus on the users in the garage and their experience. The customer won't need a login or history view if the garage staff don't move from paper invoices to online.
- Invoices and customers will have a search bar which will search for multiple fields in the database; vehicle registration, name, date etc. rather than have multiple filter fields, again for simplicity.
- Bootstrap alerts will be used to provide the user with feedback when making changes to the database etc. A confirmation or error page will be used for customers paying through Stripe.
- I plan to make good use of Bootstrap throughout the project and keep custom css styling to a minimum; this can be updated at a later time.
- Bootstrap modals will be used for much of the new entries to the database (adding parts/labour/starting an invoice etc.)

##### Forms
- Crispy forms has been used with the Bootstrap 5 add on to style the forms. You can conveniently use the Layout function to add bootstrap classes and components. I added the floating fields component to each field.

### Security
- Django comes with lots of safety features and I plan to use their forms feature where possible to protect the database. I will include my own validation where applicable.
- There is a potential security risk to customer data, where they are following a link to access and pay their invoice. Although I can't see why anyone would want to gain access to the link and pay their bill, in the future customers should have a login, especially if their invoice history is added as a feature.
- Another security risk, is that I have removed password validation for new users. The purpose of this is to make it as easy as possible to get users set up at first, then if the garage staff take to the MVP, improving security by adding password validation and getting users to change their passwords.

### Wireframes
Desktop wireframes:
![Desktop wireframes](/)


Mobile wireframes:
![Mobile wireframes](/)



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

- Using Django crispy forms to configure forms for both add and edit customer, I ran into the problem of needing a different 'action' url depending on whether I was adding or editing an entry. One solution was to create the 'form' html outside of the crispy tag. However, I wanted to retain control of the form in the back end, so I made a function which gave the add, or edit, url depending on whether an instance of the form was present when the form initialised.

- I needed to hide the customer foreign key and pre-populate it when adding a vehicle, based on which customer summary the user was on. I found a helpful article on [Stack Overflow](https://stackoverflow.com/questions/1882616/pass-an-initial-value-to-a-django-form-field) which showed me how to use django's initial keyword. [Django Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/layouts.html) gave me a way to hide the field using their Layout functionality.

- I needed to somehow display only the vehicles which are linked up to a customer when the user is creating an invoice. I could see two options: 1. select customer first and then produce another form with the filtered vehicles at the backend; 2. only show vehicles that correspond to the selected customer using Javascript. I chose to go with the Javascript option and so my next question was how to label each option class with the corresponding customer primary key. This wasn't very easy and after much googling, I knew I had to create a custom select widget and change each option class from there but couldn't figure out how to configure it exactly to my problem. [ChatGPT](https://chat.openai.com/) proved to be very useful as it could similate the conditions I needed and gave me a template to use to create a class with the value of the corresponding customer primary key for each vehicle option. From there I could manipulate the list using JS.

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
- I used the walkthrough for Boutique Ado for many things in the project. Maybe most notably was to help with the invoice model, using a function and signal to calculate the grand total depending on whether parts or labour are edited in the database.
- An article by [geeksforgeeks](https://www.geeksforgeeks.org/how-to-perform-a-real-time-search-and-filter-on-a-html-table/) gave me the jQuery needed to filter a list of values while the user types. I coupled this code with an article from [Stack Overflow](https://stackoverflow.com/questions/9127498/how-to-perform-a-real-time-search-and-filter-on-a-html-table) which gave a function to 'debounce' which gives a delay of typing, which is much better user experience than using built in time delay function.
- I used the [Django Crispy forms](https://crispy-forms-foundation.readthedocs.io/en/latest/index.html) documentation a lot when constructing forms.
- I used [chatGPT](chat.openai.com) to help with creating available_options function of invoice>views.py.