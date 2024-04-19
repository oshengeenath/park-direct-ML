import cv2
import pymongo
import tempfile
from PIL import Image
from datetime import datetime
from Num_plate_read import bbox_crop
from ultralytics import YOLO
from integrated_code import main
import tkinter as tk
from tkinter import messagebox

def convert_to_yolo_input():
    frame = main()
    
    # Resize the frame to match YOLO input size
    resized_frame = cv2.resize(frame, (416, 416))  # Adjust the size according to your YOLO model's input size
    
    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    
    # Convert NumPy array to PIL Image
    pil_image = Image.fromarray(rgb_frame)
    
    # Save PIL Image to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_file_path = temp_file.name
    pil_image.save(temp_file_path)
    
    return temp_file_path

image_folder = convert_to_yolo_input()
model = YOLO("YOLO.pt")

def display_info(plate, slot, arrival_time, departure_time, booking_status):
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Vehicle Information")
    
    # Set up the window's geometry
    root.geometry("400x200")  # width x height
    
    # Define labels for displaying the vehicle information
    tk.Label(root, text=f"Vehicle Number: {plate}").pack()
    tk.Label(root, text=f"Parking Slot: {slot}").pack()
    tk.Label(root, text=f"Arrival Time: {arrival_time}").pack()
    tk.Label(root, text=f"Departure Time: {departure_time}").pack()
    tk.Label(root, text=f"Booking Status: {booking_status}").pack()
    
    # Button to close the window
    tk.Button(root, text="Close", command=root.destroy).pack()
    
    # Start the Tkinter event loop
    root.mainloop()

def display_message(message):
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("Message")

    # Set up the window's geometry
    root.geometry("300x100")  # width x height

    # Define a label to display the message
    tk.Label(root, text=message, padx=10, pady=10).pack()

    # Button to close the window
    tk.Button(root, text="Close", command=root.destroy).pack()

    # Start the Tkinter event loop
    root.mainloop()    

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
            display_info(plate, slot, arrival_time, departure_time, booking_status)
        elif date > today_date:
            print("The date is in the future.")
            display_message("The date is in the future.")
        else:
            print("The date has expired.")
            display_message("The date has expired.")
    else:
        print("Vehicle Number does not exist.")
        display_message("Vehicle Number does not exist.")

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://arul20210434:Ze3zWYFSym1wEuuE@edgeai.2feeugm.mongodb.net/?retryWrites=true&w=majority&appName=edgeAI")
db = client["test"]
collection = db["bookings"]

# Call the function
check_number_plate(collection)

# Close the MongoDB connection
client.close()

