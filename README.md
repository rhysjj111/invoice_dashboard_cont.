# An invoice dashboard for a vehicle repair workshop.

Live site: https://invoice-project-9aaf4928352b.herokuapp.com/ <br>
Github repository: https://github.com/rhysjj111/project_4_invoice_dashboard

Credentials (values are both username and password):
- mechanic
- foreman
- accounts
(each account has a different level of access of what invoice status they need to see. Accounts has the most access, mechanic has the least.)

I have a few customers added with my own email address added to test confirmation emails work through Heroku. If you'd like to check this works, please change a customers email to your own.

### Overview

This project is MS4 for The Code Academy. It is an MVP for an invoice dashboard with the purpose of providing a basic app which can catalyse the migration from invoices on paper to electronic invoices. It comprises of two main sections for configuration; 'invoices' and 'customers', three user types, who can use the software; 'mechanic', 'foreman' and 'accounts'. A finished invoice will be sent the the customer who will have the opportunity to view the invoice and pay securely via 'Stripe'.

## UX

### Site owner/developer goals
To construct a working MVP that can provide the most basic level of functionality for an invoice dashboard, for a workshop, which can either be iterated upon, changed or scrapped with little loss, depending on results. 

### External users goals
* Eliminate the need for paper invoices which will save time when; constructing and editing and finding invoices, and save money on paper. 
* Provide a constant record of which invoices are at which stage, making sure invoices are double checked by multiple staff members before they go out.
* Provide a record of who has paid, which invoices are due, which means customers can be reminded before payments are overdue. 
* Automate sending reminder emails so they can be constructed with the click of a button to save time and keep emails consistent.
* Provide customers with an easy and safe way of paying an invoice.

### Proposed features
- Users can input customer and vehicle data which can be used to construct invoices.
- Users can add parts and labour entries to an invoice which will total costs and add VAT for the final bill to be presented to the customer.
- Automated reminder emails for payments nearly due.
- Send customers the invoice via email which they can follow a link to secure payment.

The features listed are the core functionality required to move from paper invoicing to online. I believe these are achievable with the technology and timeframe available.

### User stories
![User stories](/static/readme_images/user_stories.jpg)

## Design

### Design choices
- I've designed the wireframes 'mobile-first' to minimise unnecessary features or content. Another reason this design choice is it's anticipated the invoices will be created on the go, via mobile, by the mechanics/foreman on the ground as they work.
- I've chosen only to show invoices with 'open' status, and remove filter views of 'pending' (ready to send to customers) and 'inactive' (complete invoices) to remove complexity from mobile devices. Tablets will be the same as mobiles with just the structures edited slightly where needed.
- The invoices will follow a path of status'; 'open', 'work on hold', 'to be processed', 'to be verified', 'sent to customer' and paid. Each status will determine which users can access the invoice. This is intended to keep their view of the list of 'active' invoices as relevant as possible. Invoices can be moved forward and backwards along the path/journey if mistakes are made.
- An invoice number will only be created when an invoice has the status 'sent to customer'. Once an invoice has been marked sent to customer it can't be editted again. The invoice will also have to undergo some sort of validation at this stage so that they are complete to a minimum standard. The reason I have chosen to include the validation at this late stage, instead of when each element is created, is to keep the invoices flexible. It's to recreate how the garage uses paper invoices now. A mechanic might open a job card and start work without knowing the customer name. Eventually the invoice is filled in fully by the time it gets to the customer.
- I've chosen not to give the customer a login, or a view of their previous invoices, just a link to download the invoice and store it themselves. The reason for this is to focus on the users in the garage and their experience. The customer won't need a login or history view if the garage staff don't move from paper invoices to online.
- Invoices and customers will have a search bar which will search for multiple fields in the database; vehicle registration, name, date etc. rather than have multiple filter fields, again for simplicity.
- Bootstrap alerts will be used to provide the user with feedback when making changes to the database etc. A confirmation or error page will be used for customers paying through Stripe.
- I plan to make good use of Bootstrap throughout the project and keep custom css styling to a minimum; this can be updated at a later time.
- Bootstrap modals will be used for much of the new entries to the database (adding parts/labour/starting an invoice etc.)

#### Forms
- Crispy forms has been used with the Bootstrap 5 add on to style the forms. You can conveniently use the Layout function to add bootstrap classes and components. I added the floating fields component to each field.

### Security
- Django comes with lots of safety features and I plan to use their forms feature where possible to protect the database. I will include my own validation where applicable.
- There is a potential security risk to customer data, where they are following a link to access and pay their invoice. Although I can't see why anyone would want to gain access to the link and pay their bill, in the future customers should have a login, especially if their invoice history is added as a feature.
- Another security risk, is that I have removed password validation for new users. The purpose of this is to make it as easy as possible to get users set up at first, then if the garage staff take to the MVP, improving security by adding password validation and getting users to change their passwords.

### Wireframes
Desktop wireframes:
![Desktop wireframes](/static/readme_images/Desktop%20-%20project%204.png)


Mobile wireframes:
![Mobile wireframes](/static/readme_images/Mobile-%20project%204.png)



### Additional diagrams
ERM:
![ERM](/static/readme_images/project4_erm.png)  

Flows:
![Flows](/static/readme_images/Untitled-2024-02-29-1550.png)



### Colour scheme
The colour scheme was constructed on [coolors.co](https://coolors.co/03120e-00469b-ffffff-31e981-ff7f11). The scheme is based on the colour of the logo of the company this project is designed for.
- (colour scheme picture)

 


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

- When displaying invoices in invoice_list.html (in a bootstrap table), each row needed a class depending on the invoice status number. I didn't like the verbose if statement with multiple conditions in the template, so tried making a map of the class names for each status number in the page view. I then tried using the python get function but kept getting an error. I decided to make a custom filter, using the [Django docs](https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/) for information on setting it up, and put my get function inside.

- I had a few issues creating a Django formset for Part which could display all previous entries and an extra blank form. 
  - I wanted to use django crispy form helper and layout functionality in keeping with the other forms. [ChatGPT](https://chat.openai.com/) pointed me in the direction of creating a base formset and base formset helper class to add the helper and layout functionality to the formset. 
  - I came across another issue when I wanted to use the formsets can_delete option, to provide user with the ability to delete rows in the formset. I didn't want the user to have the option to delete the extra form (poor UX). A solution was to make use of can_delete_extra=False option but this threw an error in the console as the crispy form Layout function was looking for a field 'DELETE' on every row, which wasn't there for the extra form (due to can_delete_extra=False). After much googling and trying to adjust the form configuration, I decided to just hide the delete option on the extra form with Javascript.
  - Finally, I wanted the formset to ignore blank forms on submit so that if the user is just updating an already present field and not adding a new instance to the database, they wouldn't end up with an extra blank row each time they save. [ChatGPT](https://chat.openai.com/) gave me the boilerplate to edit the clean function of the base formset class so that any forms with all blank fields would be deleted before save.

- There was an issue when editing an invoice as the customer and vehicle fields will likely be prepopulated. The problem lies if the user changes the customer and the vehicle option remains selected, resulting in a customer possibly being assigned someone elses vehicle. Originally, I wanted to make the customer field readonly when the user is editing an invoice. This wasn't a good solution, as an invoice can be created blank, with no customer, which would then be uneditable. I decided to leave the customer editable and added a function to reset the registration selection back to the standard '-----'. This was triggered after the function to hide unrelated vehicles, when the customer field is changed. I need to add validation at the backend to ensure a customer can't be assigned an unrelated vehicle in the future.

- I had ran into a few issues when linking stripe up to the app. I didn't want to follow the Boutique Ado walkthrough as it was fairly complex and specific to the websites needs. I wanted a much simpler set up so I set out to follow the Stripe docs to add an embedded form. The first problem was the stripe docs use Flask instead of Django, so although similar, quite a bit of Googling had to be done to decipher the boilerplate code. Secondly, the walkthrough was pointing me towards setting up products on their dashboard and using that, where I only wanted to use one price, which will be dynamically created depending on the invoice. I got round this by passing the invoice id via Javascript and creating custom product data when creating the stripe intent. Another issue I had come across was after successful payment, if the user pressed back at the browser, the user had the chance to pay again. I got round this with Django's never_cache decorator on the payment pages, so a fresh page was loaded each time it was visited, and my logic which avoided second payments would be implimented.

### End design similarity/difference
- I think the end product is fairly similar to the original design in terms of functionality and how it looks on the screen. I stuck with the simple payment flow with little options for the customer to save details or check orders etc. as this was not the main purpose of the project.
- The models were largely similar with a few key differences which were hashed out and decided a better route during development.
- The invoice flow of status was very close, with the difference of when the invoice is sent to customer on the actual project, it can't be moved back a stage, whereas that was originally planned to be allowed.
- I ended up using bootstrap toasts instread of alerts as I believe they take up a lot less room on the screen and compliment the way I've set up the dashboard better.
- Bootstrap modals were made good use of, mostly for adding new items, which I think gives a professional look and feels better as a user, than being directed to another page somehow. You know where you are.


### Future features to include/update
- I would like to include date search funtionality for invoices; date from and date to.
- I didn't manage to include an option to automatically send an email to customers who are late payers. This could be easily implimented in the future.
- Confirmation modals when users are moving between invoice status as they can be fairly permenant and have significant actions, like sending an invoice to a customer. You would want to avoid such accidents.
- Go through views, models, forms and consolidate code where possible, update functions etc. to make it simpler and more uniform.
- Add invoice sent date and invoice due date to invoice so customer can be informed as well as staff.
- Change the ordering of the invoice list, so that status colours are grouped together. Also give the user the option to change make more advanced filters and searches.
- Make invoice status readonly in admin. The invoice status is important and needs to go through the proper channels for an invoice to be successfully validated and payment to work.
- Improve on the validation of the invoice as this is done at the last stage before sending to customer as I wanted to allow blank invoices.
- Open invoice collapsibles automatically.
- Update navigation as it's not the most intuitive. Put more links that make sense and speed up the process. ie. when customer has paid, a link back to his invoice. If a user submits an invalid invoice, a link to the problem ie. edit customer information.
- Update the invoice list at the mobile screen size as this is still cramped.
- Add 'no parts' or 'no labour' to completed invoice template if there are none present.
- Add more information to confirmation emails to customer.
- Improve payment process.
- Improve on security including passwords for users etc.
- I'd like to add more styling such as fonts, and images and add a favicon. I didn't get chance to do these although they were on my list, just ran out of time and had to focus on a working project.
- Improve the testing documentation. I tested extensively as I went along and started the docs strong but they got less an less attention as time ran out. Also put my code through the validators.

#### JS
- I used Javascript to filter names or customers as they type.
- There was also Javascript involved in the Stripe embeded form, most of it from the [Stripe documentation](https://docs.stripe.com/payments/accept-a-payment?locale=en-GB), changed slightly to fit the needs of the project. 
- It was also used to filter vehicles based on selected customer at invoice creation/edit.

#### CSS
- I used bits and pieces of custom css, but a lot of the project relied on bootstrap classes.

#### Features
- Invoice flow of status, where each status has a purpose and can be viewed by specific users.
- Add delete and edit vehicles, customers, invoices, parts and labour to construct an invoice.
- Send the invoice to the customer email.



### Validators

Didn't get chance to use the validators.

### Lighthouse




## Deployment

##### Clone the repository
- Create a Github account & login.
- Locate the GitHub Repository [here](https://github.com/rhysjj111/project_4_invoice_dashboard)
- Locate 'Code' button.
- Copy the URL.
- Open Git Bash or Terminal or Command Prompt/Powershell.
- Enter 'git clone'.
- Enter copied url: `git clone https://github.com/rhysjj111/project_4_invoice_dashboard.git`
- You should have your local clone in the directory you have specified.

#### Deploy with Heroku using CodeInstitute database
##### Elephant SQL
- I used code institute database as it has a recent enough version of Postgres whereas ElephantSQL might not (randomly generated apparently).
- Create a database.
- Copy the URL given in email confirmation.

##### Heroku with Amazon AWS
- Make sure your repository contains your 'requirements.txt' file, which contains relevant packages, and a 'Procfile' which tells Heroku how to start your app.
- Create a Heroku account & login.
- Click 'New' followed by 'Create new app'.
- Choose a name for your app and select a region close to you. Click 'Create app'.
- Go to 'settings' and click 'Reveal Config Vars'.
- Add Key value pairs as below.

|KEY         |VALUE                 |
|------------|----------------------|
|DATABASE_URL|(copied database url) |
|IP          |0.0.0.0               |
|PORT        |5000                  |
|SECRET_KEY  |(your secret key)     |
|DEBUG       |True                  |
|AWS_ACCESS_KEY_ID | (your key) |
|AWS_SECRET_KEY | (key) |

- Set up an Amazon AWS account.
  - Find the console and create an IAM user. Choose policies, and create.
  - Set up and S3 bucket.
  - Save credentials and configure in Heroku as above.
- Debug is set to True in settings if you want to check for any bugs/errors. You can set to False straight away if you do not want debug mode, or once deployed and you are happy.
- Locate 'Deploy' (next to settings). Click 'Connect to GitHub' (look for the logo).
- Connect your repository.
- Locate 'Deploy Branch' of Manual Deploy and click.
- Look for conformation the app is deployed.
- If not, enable automatic deploys and commit and push the repository to GitHub.
- Migrate databases to Heroku app.
- Finally go back to the dashboard and click 'Open app'.
- Use the Heroku documentation if there are any issues.



## Credits
- The boilerplate used in base.html was taken from [bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) and edited.
- [Stack overflow](https://stackoverflow.com/) was used many times and referenced throughout the readme for specific examples.
- I got the idea of using slugs for easier to understand URLs from a tutorial on how to build an invoice platform, on [Youtube](https://www.youtube.com/watch?v=KU_taqbG00U&t=8159s).
- I used the walkthrough for Boutique Ado for many things in the project. Maybe most notably was to help with the invoice model, using a function and signal to calculate the grand total depending on whether parts or labour are edited in the database.
- An article by [geeksforgeeks](https://www.geeksforgeeks.org/how-to-perform-a-real-time-search-and-filter-on-a-html-table/) gave me the jQuery needed to filter a list of values while the user types. I coupled this code with an article from [Stack Overflow](https://stackoverflow.com/questions/9127498/how-to-perform-a-real-time-search-and-filter-on-a-html-table) which gave a function to 'debounce' which gives a delay of typing, which is much better user experience than using built in time delay function.
- I used the [Django Crispy forms](https://crispy-forms-foundation.readthedocs.io/en/latest/index.html) documentation a lot when constructing forms.
- I used [chatGPT](chat.openai.com) to help with creating available_options function of invoice>views.py.
- I relied on [chatGPT](https://chat.openai.com) for explanations, boiler plates of code, possible options of how to attack a situation, as well as docs for [Bootstrap](https://getbootstrap.com/), [Stripe](https://stripe.com/), [Django](https://www.djangoproject.com/), [Crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/), and forums like [Stack Overflow](https://stackoverflow.com/).





