import pymongo
from datetime import datetime
from Num_plate_read import bbox_crop
from ultralytics import YOLO


image_folder = "./test_image.jpg"
model = YOLO('YOLO.pt')

def check_number_plate(collection):
    # Get input from the user
    number_plate = bbox_crop(image_folder=image_folder, model=model)

    # Query MongoDB for the given number plate
    query = {"vehicleNumber": number_plate}
    result = collection.find_one(query)

    if result:
        # Get today's date
        today_date = datetime.now().date()
        
        # Extract data from the result
        plate = result["vehicleNumber"]
        slot = result["parkingSlotId"]
        date_str = result["date"]
        date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert string to date
        arrival_time = result['arrivalTime']
        departure_time = result['leaveTime']
        booking_status = result['status']
        
        if date == today_date:
            print(f"Vehicle Number: {plate}, \nParking Slot: {slot}, \nArrival Time: {arrival_time}, \nDeparture Time: {departure_time}, \nBooking Status: {booking_status}")
        elif date > today_date:
            print("The date is in the future.")
        else:
            print("The date has expired.")
    else:
        print("Vehicle Number does not exist.")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://arul20210434:Ze3zWYFSym1wEuuE@edgeai.2feeugm.mongodb.net/?retryWrites=true&w=majority&appName=edgeAI")
db = client["test"]
collection = db["bookings"]

# Call the function
check_number_plate(collection)

# Close the MongoDB connection
client.close()

