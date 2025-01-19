This is a RESTful API for an e-commerce platform, built with Flask, SQLAlchemy, and Marshmallow. It includes endpoints for managing users, products, and orders.

Features
User Management: Create, retrieve, update, and delete user information.
Product Management: Create, retrieve, update, and delete product information.
Order Management: Create orders, add or remove products from orders, and retrieve orders and related products.
Prerequisites
Python 3.6+
MySQL
Flask
Flask-SQLAlchemy
Flask-Marshmallow
Marshmallow-SQLAlchemy
SQLAlchemy
MySQL Connector
Installation
Clone the repository:

git clone https://billyh1982/mod_3_project.git
cd your-repository
Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install the required packages:

pip install -r requirements.txt
Set up MySQL database:

Ensure you have MySQL installed and running. Create a database for your project.

CREATE DATABASE flask_api_project;
Update configuration:

Update your app.py with the correct MySQL connection string.

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/flask_api_project'
Run the application:
