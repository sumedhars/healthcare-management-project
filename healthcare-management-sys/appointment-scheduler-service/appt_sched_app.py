from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)


# MongoDB Atlas connection string (update with your actual URI)
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']


@app.route('/appointments', methods=['POST'])
def create_appointment():
    appointment_data = request.json
    result = db['appointment-scheduler'].insert_one(appointment_data)
    return jsonify({'id': str(result.inserted_id)}), 201


@app.route('/appointments/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        appointment = db['appointment-scheduler'].find_one({"_id": ObjectId(appointment_id)})
        if appointment:
            appointment['_id'] = str(appointment['_id']) 
            return jsonify(appointment), 200
        return jsonify({"error": "Appointment not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid appointment ID format"}), 400


@app.route('/appointments/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        updated_data = request.json
        result = db['appointment-scheduler'].update_one({"_id": ObjectId(appointment_id)}, {"$set": updated_data})
        if result.modified_count:
            return jsonify({"success": "Appointment updated"}), 200
        return jsonify({"error": "No changes made or appointment not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid appointment ID format"}), 400


@app.route('/appointments/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        result = db['appointment-scheduler'].delete_one({"_id": ObjectId(appointment_id)})
        if result.deleted_count:
            return jsonify({"success": "Appointment deleted"}), 200
        return jsonify({"error": "Appointment not found"}), 404
    except InvalidId:
        return jsonify({"error": "Invalid appointment ID format"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)