# app/__init__.py
from flask import Flask
from flask_session import Session
from flask_wtf import CSRFProtect
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()  # Ensure this is called at the very beginning

app = Flask(__name__)

# Load configuration from .env file
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
app.config['MONGODB_DATABASE'] = os.getenv('MONGODB_DATABASE')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or os.urandom(24)  # Ensure SECRET_KEY is set

# Print the loaded environment variables for debugging
print("URI:", app.config['MONGODB_URI'])
print("Database Name:", app.config['MONGODB_DATABASE'])

app.config['SESSION_TYPE'] = 'filesystem'

# Initialize session and CSRF protection
Session(app)
csrf = CSRFProtect(app)

# MongoDB connection
uri = app.config['MONGODB_URI']
client = MongoClient(uri)
db_name = app.config['MONGODB_DATABASE']

if not db_name:
    raise ValueError("MONGODB_DATABASE environment variable not set or is empty.")

db = client[db_name]

# Ensure text index is created
try:
    db.agents.create_index([("name", "text"), ("email", "text"), ("phone", "text")], name="text_index")
    print("Text index created.")
except errors.OperationFailure as e:
    if "IndexOptionsConflict" in str(e):
        print("Text index already exists with a different name.")
    else:
        raise e

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print("Error connecting to MongoDB:", e)

# Import routes to register them with the app
from app import routes

if __name__ == '__main__':
    app.run(debug=True)
