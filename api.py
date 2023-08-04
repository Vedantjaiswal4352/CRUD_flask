from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import random
import string


app = Flask(__name__)

# Connection URI and database name
uri = 'mongodb://localhost:27017/'
db_name = 'mydb'

# Function to generate random strings for password field
def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to connect to MongoDB and get the user collection
def get_user_collection():
    client = MongoClient(uri)
    db = client[db_name]
    return db['users']

# GET /users - Returns a list of all users
@app.route('/users', methods=['GET'])
def get_all_users():
    user_collection = get_user_collection()
    users = list(user_collection.find({}, {'_id': 0}))
    return jsonify(users)

# GET /users/<id> - Returns the user with the specified ID
@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user_collection = get_user_collection()
    user = user_collection.find_one({'id': int(user_id)}, {'_id': 0})
    if user:
        return jsonify(user)
    return jsonify({'message': 'User not found'}), 404

# POST /users - Creates a new user with the specified data
@app.route('/users', methods=['POST'])
def create_user():
    user_collection = get_user_collection()
    data = request.get_json()
    new_user = {
        'id': data.get('id'),
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password', generate_random_string(10)),
    }
    user_collection_new = user_collection.insert_one(new_user).inserted_id
    # Convert the ObjectId to a string before returning the response
    user_collection_new_str = str(user_collection_new)
    # Return the response with status code 201 (Created)
    return jsonify({"id": user_collection_new_str}), 201

# PUT /users/<id> - Updates the user with the specified ID with the new data
@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user_collection = get_user_collection()
    data = request.get_json()
    updated_user = {
        'name': data.get('name'),
        'email': data.get('email'),
        'password': data.get('password'),
    }
    user_collection_updated = user_collection.update_one({'id': int(user_id)}, {'$set': updated_user}).upserted_id
    user_collection_updated_str = str(user_collection_updated)
    return jsonify({"id": user_collection_updated_str}), 201

# DELETE /users/<id> - Deletes the user with the specified ID
@app.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_collection = get_user_collection()
    result = user_collection.delete_one({'id': int(user_id)})
    if result.deleted_count > 0:
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
