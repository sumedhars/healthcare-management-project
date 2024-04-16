# main file where we will define our Flask application and REST API endpoints.

from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


# MongoDB Atlas connection string (update with your actual URI)
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']

@app.route('/patients', methods=['POST'])
def add_patient():
    patient_data = request.json
    result = db.patients.insert_one(patient_data)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = db.patients.find_one({"_id": ObjectId(patient_id)})
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 404
    except:
        return jsonify({"error": "Invalid patient ID format"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)