from flask import Flask, jsonify, request
from pymongo import MongoClient
import random
import string
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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

class UserResource(Resource):
    def get(self, user_id=None):
        user_collection = get_user_collection()
        if user_id is None:
            users = list(user_collection.find({}, {'_id': 0}))
            return jsonify(users)
        user = user_collection.find_one({'id': int(user_id)}, {'_id': 0})
        if user:
            return jsonify(user)
        return jsonify({'message': 'User not found'}), 404

    def post(self):
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
        # Create a JSON response with the user_id
        response_data = {"id": user_collection_new_str}
        return response_data, 201

    def put(self, user_id):
        user_collection = get_user_collection()
        data = request.get_json()
        updated_user = {
            'name': data.get('name'),
            'email': data.get('email'),
            'password': data.get('password'),
        }
        user_collection_updated = user_collection.update_one({'id': int(user_id)}, {'$set': updated_user}, upsert=True)
        user_collection_updated_str = str(user_collection_updated)
        response_data = {"id": user_collection_updated_str}
        return response_data, 201

    def delete(self, user_id):
        user_collection = get_user_collection()
        result = user_collection.delete_one({'id': int(user_id)})
        if result.deleted_count > 0:
            return jsonify({'message': 'User deleted successfully'})
        return jsonify({'message': 'User not found'}), 404

# Add UserResource to the API with the route /users and /users/<string:user_id>
api.add_resource(UserResource, '/users', '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
