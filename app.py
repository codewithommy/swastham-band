# from flask import Flask, request, jsonify
# from pymongo import MongoClient, errors
# from datetime import datetime
# import os

# app = Flask(__name__)  # Corrected __name__

# # MongoDB connection string from environment variables (replace with hardcoded if needed)
# mongo_uri = os.getenv("MONGO_URI")

# # Function to check MongoDB connection
# def check_mongo_connection():
#     try:
#         client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
#         client.admin.command('ping')  # Ping the MongoDB server
#         return client, "MongoDB connection successful"
#     except errors.ServerSelectionTimeoutError as err:
#         return None, f"MongoDB connection failed: {err}"

# # Check MongoDB connection when the app starts
# client, mongo_status = check_mongo_connection()

# if client:
#     db = client["healthdata"]
#     collection = db["sensorsdata"]
# else:
#     db = None
#     collection = None

# @app.route('/api/data', methods=['POST'])
# def store_data():
#     if collection is None:
#         return jsonify({"status": "error", "message": "No MongoDB connection"}), 500

#     try:
#         data = request.json  # Get JSON data from the request
#         print("Received data:", data)  # Print to console for debugging

#         # Check for required fields, including body temperature
#         if not all(k in data for k in ["heartRate", "spo2", "bodyTemp"]):
#             return jsonify({"status": "error", "message": "Missing heartRate, spo2, or bodyTemp data"}), 400

#         sensor_data = {
#             "heartRate": data["heartRate"],
#             "spo2": data["spo2"],
#             "bodyTemp": data["bodyTemp"],  # Add body temperature to the data
#             "timestamp": datetime.utcnow()
#         }

#         result = collection.insert_one(sensor_data)  # Insert into MongoDB
#         print(f"Inserted data with ID: {result.inserted_id}")

#         return jsonify({"status": "success", "id": str(result.inserted_id)}), 201

#     except errors.PyMongoError as e:
#         print(f"MongoDB error: {e}")
#         return jsonify({"status": "error", "message": "MongoDB insert failed"}), 500

#     except Exception as e:
#         print(f"General error: {e}")
#         return jsonify({"status": "error", "message": str(e)}), 500

# @app.route('/check_mongo', methods=['GET'])
# def check_mongo():
#     return jsonify({"mongo_status": mongo_status})

# if __name__ == '__main__':  # Corrected __name__
#     print(mongo_status)  # Print MongoDB connection status
#     app.run(host='0.0.0.0', port=3000, debug=True)  # Optional: Enable debug mode


from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
from datetime import datetime
import os

app = Flask(__name__)  # Corrected __name__

# MongoDB connection string from environment variables (replace with hardcoded if needed)
mongo_uri = os.getenv("MONGO_URI")

# Function to check MongoDB connection
def check_mongo_connection():
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Ping the MongoDB server
        return client, "MongoDB connection successful"
    except errors.ServerSelectionTimeoutError as err:
        return None, f"MongoDB connection failed: {err}"

# Check MongoDB connection when the app starts
client, mongo_status = check_mongo_connection()

if client:
    db = client["healthdata"]
    collection = db["sensorsdata"]
else:
    db = None
    collection = None

# Welcome route
@app.route('/', methods=['GET'])
def welcome():
    return jsonify({"message": "Welcome to the website!"}), 200

@app.route('/api/data', methods=['POST'])
def store_data():
    if collection is None:
        return jsonify({"status": "error", "message": "No MongoDB connection"}), 500

    try:
        data = request.json  # Get JSON data from the request
        print("Received data:", data)  # Print to console for debugging

        # Check for required fields, including body temperature
        if not all(k in data for k in ["heartRate", "spo2", "bodyTemp"]):
            return jsonify({"status": "error", "message": "Missing heartRate, spo2, or bodyTemp data"}), 400

        sensor_data = {
            "heartRate": data["heartRate"],
            "spo2": data["spo2"],
            "bodyTemp": data["bodyTemp"],  # Add body temperature to the data
            "timestamp": datetime.utcnow()
        }

        result = collection.insert_one(sensor_data)  # Insert into MongoDB
        print(f"Inserted data with ID: {result.inserted_id}")

        return jsonify({"status": "success", "id": str(result.inserted_id)}), 201

    except errors.PyMongoError as e:
        print(f"MongoDB error: {e}")
        return jsonify({"status": "error", "message": "MongoDB insert failed"}), 500

    except Exception as e:
        print(f"General error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check_mongo', methods=['GET'])
def check_mongo():
    return jsonify({"mongo_status": mongo_status})

if __name__ == '__main__':  # Corrected __name__
    print(mongo_status)  # Print MongoDB connection status
    app.run(host='0.0.0.0', port=3000, debug=True)  # Optional: Enable debug mode
