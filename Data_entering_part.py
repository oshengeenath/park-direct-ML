#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from datetime import datetime

def insert_data_to_mongodb(number_plate, parking_slot, date_str):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://thathsarani20211422:Bx2NtjbW3g3XYDKs@edgeai.kgqujac.mongodb.net/?retryWrites=true&w=majority&appName=edgeai")
    db = client["edgeai_test1"]
    collection = db["test_data2"]
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d") 
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD format.")
        client.close()
        return
    
    # Create a document
    user_data = {
        "Number Plate": number_plate,
        "Parking slot": parking_slot,
        "date": date
    }

    # Insert the document into MongoDB
    result = collection.insert_one(user_data)

    # Check if the insertion was successful
    if result.inserted_id:
        print("Data inserted successfully with ID:", result.inserted_id)
    else:
        print("Failed to insert data")

    # Close the MongoDB connection
    client.close()

# Get input from the user
number_plate = input("Enter number plate: ")
parking_slot = input("Enter parking slot: ")
date_str = input("Enter date (YYYY-MM-DD): ")

# Call the function
insert_data_to_mongodb(number_plate, parking_slot, date_str)

