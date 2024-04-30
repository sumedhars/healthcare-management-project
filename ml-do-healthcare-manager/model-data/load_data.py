from pymongo.mongo_client import MongoClient
import pandas as pd
from datetime import datetime

# Replace the placeholder with your Atlas connection string
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri)

# get database and collection
db = client["healthcare"]
patient_collection = db["patients"]
medical_records_collection = db["medical-records"]

df = pd.DataFrame(columns=["patientID","age","diagnosis",
                           "TreatmentPlan","TestResults","ImmunizationStatus","InsuranceStatus","RiskLabel"])

def calculate_age(born):
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

for patient_document in patient_collection.find():
    dob_str = patient_document.get("dateOfBirth")  # Get the DOB from the document
    dob = datetime.strptime(dob_str, '%Y-%m-%d') if dob_str else None  # Convert DOB string to datetime object
    age = calculate_age(dob) if dob else None  # Calculate age if DOB is not None

    # Get medical record by patientID
    medical_record = medical_records_collection.find_one({"patientID": patient_document.get("patientID")})
    
    if medical_record:
        new_row = pd.DataFrame([{
            "patientID": patient_document.get("patientID"),
            "age": age, 
            "diagnosis": medical_record.get("diagnosis", None) if medical_record else None,
            "TreatmentPlan": medical_record.get("treatmentPlan", None) if medical_record else None,
            # "TestResults": medical_record.get("testResults", None) if medical_record else None,
            "ImmunizationStatus": 1 if medical_record.get("immunizationRecords") else 0,
            "InsuranceStatus": 1 if patient_document.get("insuranceCompany") else 0,
        }])

    df = pd.concat([df, new_row], ignore_index=True)

df.to_csv('training_data.csv')


# TreatmentResults Categories:
# Improved
# Worsened
# NoChange