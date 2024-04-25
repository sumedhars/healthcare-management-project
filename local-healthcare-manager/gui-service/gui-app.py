from flask import Flask, render_template, jsonify
import pymongo
from pymongo import MongoClient
from time import sleep

app = Flask(__name__)

# MongoDB connection setup
def check_mongodb_connection():
    try:
        client = MongoClient("mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
        db = client["healthcare"]
        db.command("serverStatus")
        return {"status": "connected", "message": "Successfully connected to MongoDB."}
    except Exception as e:
        return {"status": "not connected", "message": f"Error connecting to MongoDB: {e}"}

@app.route('/check-mongodb')
def mongodb_status():
    connection_status = check_mongodb_connection()
    return jsonify(connection_status)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/medical-records-form')
def medical_records_form():
    return render_template('medical_records_form.html')

@app.route('/patients-form')
def patients_form():
    return render_template('patient_form.html')

@app.route('/appt-sched-form')
def appt_sched_form():
    return render_template('appt_sched_form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
