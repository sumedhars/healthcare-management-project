from flask import Flask, request, jsonify
from flask_cors import CORS  
from pymongo import MongoClient
from bson import ObjectId

# store comprehensive clinical data about patients

app = Flask(__name__)
CORS(app)  

# MongoDB Atlas connection string - uri
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']

@app.route('/medical-records', methods=['POST'])
def add_medical_record():
    record_data = request.json
    if db['medical-records'].find_one({"_id": record_data.get('_id')}):
        return jsonify({'error': 'Record ID already exists'}), 400
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
