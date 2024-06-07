import os
from dotenv import load_dotenv
from pymongo import MongoClient, TEXT

# Load environment variables
load_dotenv()

# Connect to MongoDB
uri = os.getenv("MONGODB_URI")
db_name = os.getenv("MONGODB_DATABASE")

client = MongoClient(uri)
db = client[db_name]

# Get the agents collection
agents_collection = db['agents']

# Drop the existing text index if it exists
existing_indexes = agents_collection.index_information()
for index_name, index_info in existing_indexes.items():
    if index_info['key'][0][0] in ['name', 'email', 'phone']:
        agents_collection.drop_index(index_name)

# Create a new text index on the 'name', 'email', and 'phone' fields
agents_collection.create_index(
    [
        ('name', TEXT),
        ('email', TEXT),
        ('phone', TEXT)
    ],
    name='text_index'
)

print("Indexes created successfully!")
