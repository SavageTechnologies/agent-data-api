import os
import pandas as pd
from pymongo import MongoClient

def import_agents_from_csv(file_path):
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    # Connect to MongoDB
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DATABASE")

    client = MongoClient(uri)
    db = client[db_name]

    # Read CSV file
    df = pd.read_csv(file_path)

    # Insert data into the agents collection
    agents_collection = db['agents']
    agents_collection.insert_many(df.to_dict('records'))

    print("Data imported successfully!")
