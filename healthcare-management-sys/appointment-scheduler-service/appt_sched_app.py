from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)


# MongoDB Atlas connection string (update with your actual URI)
uri = "mongodb+srv://sumedhars:srsanjeev@cluster0.jhkpjqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['healthcare']