from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import json_util, ObjectId
import random
from flask import Flask, request, json
from bson import json_util
from pymongo import MongoClient
import string

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb+srv://davidkanin18:0909D.KANIN@cluster0.vbhzniv.mongodb.net/")

db = client.DMleasing
cars = db.cars
contact = db.contact

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

if __name__ == '__main__':
    app.run(debug=True)