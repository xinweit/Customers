# User Guide

Simple RESTful application to keep track of customers
<br>

## Setup instructions:

1. Download and install postgreSQL.
2. Create a 'customers' database in PostgreSQL using psql or pgAdmin.
3. Download the entire repository as a ZIP folder and extract the Klinify folder.
4. In line 10 of the api.py file, for the line app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{owner}:{password}@localhost/customers', input the owner name and password of the 'customers' database.  
For app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/customers', the owner name is 'postgres' and password is 'password'.

__OR__

1. Download and install postgreSQL.
2. Create a 'customers' database in PostgreSQL using psql or pgAdmin.
3. Make sure Python is installed on your machine.
4. Create a folder for your project.
5. Copy the contents of the api.py file in the repository into your own api.py file and put it in the project folder.
6. Run the following commands in the project folder in terminal:  
'pip install pipenv'  
'pipenv shell'  
-> activates a virtualenv
'pipenv install flask'  
'pipenv install flask-SQLAlchemy'  
'pipenv install sqlalchemy'  
'pipenv install psycopg2' or 'pipev install psycopg2-binary'  
-> psycopg2 for production or psycopg2-binary for development and testing  
'pipenv install pyjwt'
7. In line 10 of the api.py file, for the line app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{owner}:{password}@localhost/customers', input the owner name and password of the 'customers' database.  
For app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/customers', the owner name is 'postgres' and password is 'password'.

<br>

## Usage instructions:

Run 'pipenv shell', then 'python api.py' in your project folder path to run the Application Programming Interface (API). The application is set to run on port 5000 by default on the URL http://127.0.0.1:5000.
<br>
[ ] is used a placeholder for text in the URLs below.

<br>

### Authentication using JSON Web Token

To generate a JSON Web Token (JWT) for access to the API endpoints, use this URL http://127.0.0.1:5000/login on Postman. In the Authorization tab, input any username and 'password' as the default password to generate a token. Send the request and the response containing the token will be generated. 

![login_image](images/login.png)

<br>

### Create a customer

To add a customer, use http://127.0.0.1:5000/customers/create?token=[generated_token] where generated_token is the token generated after login. Include the name and date of birth of the customer as JSON in the request body.

![login_image](images/create.png)

<br>

### Read all customers

To get a list of all the customers, use http://127.0.0.1:5000/customers/read?token=[generated_token] where generated_token is the token generated after login.

![login_image](images/read.png)

<br>

### Update a customer

To update a customer, use http://127.0.0.1:5000/customers/update?update_id=[customer_id]&token=[generated_token] where customer_id is the id of the customer to be updated and generated_token is the token generated after login. Include the new name and date of birth of the customer as JSON in the request body.

![login_image](images/update.png)

<br>

### Delete a customer

To delete a customer, use http://127.0.0.1:5000/customers/delete?delete_id=[customer_id]&token=[generated_token] where customer_id is the id of the customer to be deleted and generated_token is the token generated after login.

![login_image](images/delete.png)

<br>

### List the n youngest customers ordered by date of birth

To get a list of n youngest customers ordered by date of birth, use http://127.0.0.1:5000/customers/youngest?n=[n]&token=[generated_token] where n is the number of customers and generated_token is the token generated after login. The list in the response body will show the n youngest customers in descending date of birth.

![login_image](images/youngest.png)
