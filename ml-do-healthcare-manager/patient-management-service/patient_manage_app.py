from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import joblib
from datetime import datetime

app = Flask(__name__)
CORS(app)  

# load the model i.e. pkl file
model = joblib.load('../model-data/patient_risk_model.pkl')

uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']


@app.route('/patients', methods=['POST'])
def add_patient():
    patient_data = request.json
    patient_id = patient_data.get('patientID')  
    if db['patients'].find_one({"patientID": patient_id}):
        return jsonify({'error': 'Patient ID already exists'}), 400
    patient_data['_id'] = patient_id
    result = db.patients.insert_one(patient_data)
    return jsonify({'id': patient_id}), 201


@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = db['patients'].find_one({"patientID": patient_id})
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 404
    except:
        return jsonify({"error": "Invalid patient ID format"}), 400


@app.route('/predict-risk/<patient_id>', methods=['GET'])
def predict_risk(patient_id):
    patient = db['patients'].find_one({"patientID": patient_id})
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    # Prepare the patient data for prediction
    patient_data = prepare_patient_data(patient)
    if patient_data is None:
        return jsonify({"error": "Insufficient data for prediction"}), 400

    # Predicting risk
    risk_prediction = model.predict([patient_data])[0]
    return jsonify({'patientID': patient_id, 'risk': bool(risk_prediction)}), 200


def prepare_patient_data(patient):
    date_of_birth = datetime.strptime(patient.get('dateOfBirth', '1900-01-01'), "%Y-%m-%d")
    age = calculate_age(date_of_birth)
    medical_record = db['medical-records'].find_one({"patientID": patient['patientID']})
    if not medical_record:
        return None  
    # Extract required features for the prediction model
    features = [
        age,
        medical_record.get('diagnosis', 'unknown'),
        medical_record.get('TreatmentPlan', 'none'),
        1 if medical_record.get('immunizationRecords') else 0, 
        1 if patient.get('insuranceCompany') else 0,
    ]
    return features


def calculate_age(born):
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)