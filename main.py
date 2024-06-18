from flask import Flask, request, jsonify, session, make_response
from flask_cors import CORS
from flask_pymongo import PyMongo
from pymongo import MongoClient
import bcrypt
import jwt
import datetime
import os
import secrets
from bson import json_util, ObjectId
import json
import random
import string

app = Flask(__name__)
CORS(app)
app.secret_key = secrets.token_hex(24)
client = MongoClient("mongodb+srv://davidkanin18:0909D.KANIN@cluster0.vbhzniv.mongodb.net/")

db = client.DMleasing
cars = db.cars
contact = db.contact

users = db.users
tokenlist = db.tokenlist

def generate_token(email):
    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.secret_key, algorithm='HS256')
    tokenlist.insert_one({'token': token})
    return token

@app.route('/cars', methods=['GET'])
def get_orders():
    if request.method == 'GET':

        query = {}
        car_type = request.args.getlist('type')

        if car_type:
            query["type"] = {"$in":car_type}

        result = cars.find(query)
        car_list = list(result)
        return json_util.dumps(car_list)
        
@app.route('/contact', methods=['POST'])
def contact_handler():
    if request.method == 'POST':
        contact_data = request.json
        contact.insert_one(contact_data)
        return json_util.dumps(contact_data)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    existing_user = users.find_one({'email': data['email']})

    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = {
        'email': data['email'],
        'password': hashed_password,
    }
    users.insert_one(user)

    new_user = users.find_one({'email': data['email']})
    email = new_user['email']

    token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.secret_key, algorithm='HS256')
    tokenlist.insert_one({'token': token})

    response = make_response(jsonify({'message': 'User registered successfully', 'email': email}), 201)
    response.set_cookie('token', token, httponly=True, samesite='Strict')

    return response

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users.find_one({'email': data['email']})

    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        token = jwt.encode({'email': data['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, app.secret_key, algorithm='HS256')
        tokenlist.insert_one({'token': token})

        response = make_response(jsonify({'message': 'Login successful', 'email': data['email'], 'token': token}))
        response.set_cookie('token', token, httponly=True, samesite='Strict')

        return response
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    token = request.cookies.get('token')
    if token:
        tokenlist.delete_one({'token': token})
        response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
        response.delete_cookie('token')
        return response
    else:
        return jsonify({'message': 'Token missing'}), 400

if __name__ == '__main__':
    app.run(debug=True)