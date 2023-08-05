# CRUD_flask
*) Pre-requisites:-
  Running instance of MongoDB with known connection parameters.
  Python installed.
  Postman installed.
*) Steps to Run the Code
1) Create a new Python environment and pip install the following modules:
   a) random
   b) string
   c) Flask
   e) bson
2) Clone the repository and start the environment.
3) Run the only cell present in the data.ipynb
4) Now the database is created in MongoDB with the DB name as mydb for MongoDB running on 'localhost' at port 27017 for defined collection names as users.
5) Run the api.py and start the flask rest APIs if followed correctly and if the port is not already occupied the flask will start the app on localhost:5000. Now using the correct bodies we can test API data in Postman as shown below:
  a) GET /users - Returns a list of all users.
![image](https://github.com/Vedantjaiswal4352/CRUD_flask/assets/69847543/7ed33f08-326e-47c0-8fea-f6a2c4a22a8d)
  b) GET /users/<id> - Returns the user with the specified ID.
![image](https://github.com/Vedantjaiswal4352/CRUD_flask/assets/69847543/00199b11-19ce-4be6-a3fd-8d9b9ae0454e)
  c) POST /users - Creates a new user with the specified data.
![image](https://github.com/Vedantjaiswal4352/CRUD_flask/assets/69847543/a759be81-c452-4702-ac08-751bc094c0e5)
  d) PUT /users/<id> - Updates the user with the specified ID with the new data.
![image](https://github.com/Vedantjaiswal4352/CRUD_flask/assets/69847543/cad75c76-3094-461e-864c-3476791cf83b)
  e) DELETE /users/<id> - Deletes the user with the specified ID.
![image](https://github.com/Vedantjaiswal4352/CRUD_flask/assets/69847543/17e637c0-bc04-4b42-bd39-1e8cde8e09b8)


