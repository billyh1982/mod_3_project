from app import app, db, User, Order, user_schema, users_schema, order_schema 
from app import orders_schema, Product, product_schema, products_schemas, place_order_schema

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

#The route for creating a new user
@app.route('/users', methods=['POST'])
def create_user():
    #loads the JSON data with User schema
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        #Returns error messages for validation if any
        return jsonify(e.messages), 400
    
    #Create New user object with data
    new_user = User(name=user_data['name'],
                    email=user_data['email'], 
                    address=user_data['address']
                    )
    
    try:
        #Add the new user to the database session and commit
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        #Rollback for integrity error
        db.session.rollback()
        return jsonify({"error": "Email already exists."}), 400
    #returns created user as JSON
    return user_schema.jsonify(new_user), 201

#Returns all users in DB
@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200

# Returns one user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200
# Updates one user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    #update the user's information
    user.name = user_data['name']
    user.address = user_data['address']
    user.email = user_data['email']
    #commit changes
    db.session.commit()
    #returns updated user as JSON response
    return user_schema.jsonify(user), 200
#Deletes a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not User:
        return jsonify({"message": "Invalid user id"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {user.name}"}), 200

@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    new_product = Product(
        product_name=product_data['product_name'],
        product_price=product_data['product_price'],
        )
    try:
        db.session.add(new_product)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Could not add product"}), 400
    return product_schema.jsonify(new_product), 201

#Returns all products in DB
@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schemas.jsonify(products), 200

#Returns one product in DB
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
    product.product_name = product_data['product_name']
    product.product_price = product_data['product_price']
    
    #commit changes
    db.session.commit()
    #returns updated user as JSON response
    return product_schema.jsonify(product), 200

#Deletes a product
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)
    if not Product:
        return jsonify({"message": "Invalid product id"}), 400
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"successfully deleted {product.product_name}"}), 200


#Creates new order
@app.route('/orders', methods=['POST'])
def create_order():
    #Attempt to load JSON
    try:
        order_data = place_order_schema.load(request.json)
        #Get user_id and product_ids from loaded JSON
        user_id = order_data['user_id']
        product_ids = order_data['product_ids']
        #Return Error if exists
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    
    #Gets user from DB using ID
    user = db.session.get(User, user_id)
    #errors if user doesnt exist
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    #creates a new object and associates it with user
    new_order = Order(user_id=user_id)
    new_order.users.append(user)
    
    #loop through product_ids and add the products to the order
    for product_id in product_ids:
        print(type(product_id))
        product = db.session.get(Product, int(product_id))
        if product:
            new_order.products.append(product)
    
    #add created order to DB and commit      
    db.session.add(new_order)
    db.session.commit()
    
    #return newly created order as JSON 
    return order_schema.jsonify(new_order), 201

#Adds a product to an order while checking for duplicates
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['GET'])
def product_to_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "invalid product id"}), 400
    
    if product in order.products:
        return jsonify({"message": "Product already in order"}), 400            
    order.products.append(product)
    db.session.commit()
    
    return order_schema.jsonify(order), 200

#Removes a product from order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    
    if product not in order.products:
        return jsonify({"message": "Product not in order"}), 400
    
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message": f"Successfully removed product {product_id} from order {order_id}"}), 200

# Gets all orders for a user
@app.route('/orders/user/<int:user_id>', methods=['GET'])
def orders_for_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400

    orders = user.orders
    return orders_schema.jsonify(orders), 200

# Gets all products from order
@app.route('/orders/<int:order_id>/products', methods=['GET'])
def products_for_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400

    products = order.products
    return products_schemas.jsonify(products), 200
 
if __name__ == '__main__':    
    #Creates all database tables
    with app.app_context():
        db.create_all() 
        print("Created Successfully")
    #Runs the Flask server    
    app.run(debug=True)