# py -m venv venv | python3 -m venv venv - create virtual env
# venv\Scripts\activate | source venv/bin/activate - activate virtual env 
# pip install Flask Flask-SQLAlchemy Flask-Marshmallow mysql-connector-python marshmallow-sqlalchemy
# create flask_api_project database in workbench
# pip freeze > requirements.txt - Saving list of installed packages
 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import ForeignKey, Table, String, Column, DateTime, Float, func
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from marshmallow import fields, Schema

# Initialize Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:abc123@localhost/flask_api_project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creating our Base Model

class Base(DeclarativeBase):
    pass
# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

#The association table between Users and Orders
user_orders = Table(
	"user_orders",
	Base.metadata,
	Column("user_id", ForeignKey("users.user_id")),
	Column("order_id", ForeignKey("orders.order_id")),
)
#The association table between Orders and Products
order_products = Table(
    "order_products",
    Base.metadata,
    Column("order_id", ForeignKey("orders.order_id")),
    Column("product_id", ForeignKey("products.product_id")),   
)
# User model
class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(300))
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200))
    
# Defines the many to many relationship with the Order class	
    orders: Mapped[List["Order"]] = relationship(secondary=user_orders, back_populates="users")

#Order model    
class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(),nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    
# Defines the many to many relationship with the User and Product classes    
    users: Mapped[List["User"]] = relationship(secondary=user_orders, back_populates="orders")
    products: Mapped[List["Product"]] = relationship(secondary=order_products, back_populates="orders")

#Product model
class Product(Base):
    __tablename__ = "products"
    
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(200))
    product_price: Mapped[float] = mapped_column(Float)

#Defines the many to many relationship with the Order class   
    orders: Mapped[List["Order"]] = relationship(secondary=order_products, back_populates="products")

#Defines the schema for serializing User object    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
#Defines the schema for serializing Order object          
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
    user_id = ma.auto_field()
    # products = ma.auto_field(required = True)

#class PlaceOrderSchema(ma.Schema):
 #   user_id = ma.Integer(required=True)
  #  product_ids = ma.List(ma.Integer(), required=True)

class PlaceOrderSchema(Schema): # Using Schema directly from Marshmallow
    user_id = fields.Integer(required=True)  # Explicitly mark as required
    product_ids = fields.List(fields.Integer(), required=True)  # Required is good here




#Defines the schema for serializing Product object          
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        
#Intiliizes schema for multiple and single objects
user_schema = UserSchema()
users_schema = UserSchema(many=True) 
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
place_order_schema = PlaceOrderSchema()
place_orders_schema = PlaceOrderSchema(many=True)
product_schema = ProductSchema()
products_schemas = ProductSchema(many=True)