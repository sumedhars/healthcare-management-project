from flask import Flask, request, jsonify
from flask_cors import CORS 
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
import os
import csv

# manages all data related to scheduling and tracking appointments

app = Flask(__name__)
CORS(app)  

# MongoDB Atlas connection string (update with your actual URI)
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']


# load doctor data from csv file - need to review
def load_doctors():
    doctors_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'doctors.csv')
    with open(doctors_path, mode='r') as file:
        reader = csv.DictReader(file)
        return {row['doctorID']: row['doctorname'] for row in reader}


doctors = load_doctors()


@app.route('/appointment-scheduler', methods=['POST'])
def create_appointment():
    appointment_data = request.json
    appointment_id = appointment_data.get('appointmentID')
    patient_id = appointment_data.get('patientID')
    patient = db['patients'].find_one({"patientID": patient_id})
    if not patient:
        return jsonify({'error': 'PatientID does not exist'}), 400
    if db['appointment-scheduler'].find_one({"appointmentID": appointment_id}):
        return jsonify({'error': 'Appointment ID already exists'}), 400
    appointment_data['_id'] = appointment_id
    result = db['appointment-scheduler'].insert_one(appointment_data)
    return jsonify({'id': appointment_id}), 201


@app.route('/appointment-scheduler/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = db['appointment-scheduler'].find_one({"appointmentID": appointment_id})
    if appointment:
        if '_id' in appointment:
            appointment['_id'] = str(appointment['_id'])
        return jsonify(appointment), 200
    return jsonify({"error": "Appointment not found"}), 404


@app.route('/appointment-scheduler/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    updated_data = request.json
    result = db['appointment-scheduler'].update_one({"appointmentID": appointment_id}, {"$set": updated_data})
    if result.modified_count:
        return jsonify({"success": "Appointment updated"}), 200
    return jsonify({"error": "No changes made or appointment not found"}), 404


@app.route('/appointment-scheduler/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    result = db['appointment-scheduler'].delete_one({"appointmentID": appointment_id})
    if result.deleted_count:
        return jsonify({"success": "Appointment deleted"}), 200
    return jsonify({"error": "Appointment not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)