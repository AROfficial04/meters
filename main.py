from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
MONGO_URI = "mongodb+srv://mass:ayamass@nomc.r8hka.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["nomc"]  # Database name
collection = db["meters"]  # Collection name


@app.route('/meter-check', methods=['GET'])
def check_meter():
    try:
        # Get MeterId from the query parameters
        meter_id = request.args.get('MeterId')
        if not meter_id:
            return jsonify({"success": False, "message": "Meter ID is required"}), 400

        # Find the meter data in MongoDB
        meter_data = collection.find_one({"MeterId": meter_id})

        if meter_data:
            # Convert ObjectId to string and include in the response
            meter_data['_id'] = str(meter_data['_id'])
            return jsonify({"success": True, "data": meter_data}), 200
        else:
            return jsonify({"success": False, "message": "Meter ID not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
