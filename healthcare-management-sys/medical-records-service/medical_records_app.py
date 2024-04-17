from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)  

uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']

@app.route('/medical-records', methods=['POST'])
def add_medical_record():
    record_data = request.json
    result = db['medical-records'].insert_one(record_data)
    return jsonify({'id': str(result.inserted_id)}), 201

@app.route('/medical-records/<record_id>', methods=['GET'])
def get_medical_record(record_id):
    try:
        record = db['medical-records'].find_one({"_id": ObjectId(record_id)})
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"error": "Medical record not found"}), 404
    except:
        return jsonify({"error": "Invalid record ID format"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
