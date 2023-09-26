import csv
import os
from pymongo import MongoClient

# Connect to your MongoDB

if os.environ.get("mongoUri"):
    client = MongoClient(os.environ.get("mongoUri"))
else:
    client = MongoClient('localhost', 27017) 
  # Replace with your MongoDB connection string
db = client['your_database_name']  # Replace with your database name
collection = db['Agent']  # Replace with your collection name

# Perform the MongoDB query
cursor = collection.find()

# Specify the CSV file path
csv_file_path = 'agents.csv'

# Open the CSV file for writing
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=cursor[0].keys())

    # Write the header row
    csv_writer.writeheader()

    # Write the data
    for document in cursor:
        csv_writer.writerow(document)

print(f'Data has been exported to {csv_file_path}')
