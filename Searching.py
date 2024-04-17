#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pymongo
from datetime import datetime

def check_number_plate(collection):
    # Get input from the user
    number_plate = input("Enter number plate: ")

    # Query MongoDB for the given number plate
    query = {"Number Plate": number_plate}
    result = collection.find_one(query)

    if result:
        # Get today's date
        today_date = datetime.now().date()
        
        # Extract data from the result
        plate = result["Number Plate"]
        slot = result["Parking slot"]
        date = result["date"]
        
        if date.date() == today_date:
            print(f"Number Plate: {plate}, Parking Slot: {slot}")
        elif date.date() > today_date:
            print("The date is in the future.")
        else:
            print("The date has expired.")
    else:
        print("Number plate does not exist.")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://thathsarani20211422:Bx2NtjbW3g3XYDKs@edgeai.kgqujac.mongodb.net/?retryWrites=true&w=majority&appName=edgeai")
db = client["edgeai_test1"]
collection = db["test_data2"]

# Call the function
check_number_plate(collection)

# Close the MongoDB connection
client.close()

