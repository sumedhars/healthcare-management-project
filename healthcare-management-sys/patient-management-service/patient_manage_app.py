from flask import Flask, request, jsonify
from flask_cors import CORS  
from pymongo import MongoClient
from bson import ObjectId

# handle all aspects of patient profile and demographic data management

app = Flask(__name__)
CORS(app)  

# MongoDB Atlas connection string - uri
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']


@app.route('/patients', methods=['POST'])
def add_patient():
    patient_data = request.json
    patient_id = patient_data.get('patientId')  
    if db['patients'].find_one({"patientId": patient_id}):
        return jsonify({'error': 'Patient ID already exists'}), 400
    patient_data['_id'] = patient_id  # use patientId as the primary key 
    result = db.patients.insert_one(patient_data)
    return jsonify({'id': patient_id}), 201


@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = db['patients'].find_one({"patientId": patient_id})  
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 404
    except:
        return jsonify({"error": "Invalid patient ID format"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)