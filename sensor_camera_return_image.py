import serial
import cv2
import os
import time
import numpy as np
from Num_plate_read import bbox_crop
from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt
from Num_plate_read import bbox_crop

plt.figure(figsize = (20, 20))

# Establish a connection to the Arduino on COM6
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

def find_camera_index():
    index = 0
    while True:
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            cap.release()
            index += 1
        else:
            print(f"Camera found at index {index}")
            cap.release()
            return index

def capture_and_process_image(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Cannot open camera at index", camera_index)
        return None, None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None, None

    # Encode frame to JPEG format
    _, jpeg = cv2.imencode('.jpg', frame)
    return frame, jpeg.tobytes() # Return both the raw frame and the JPEG data

model = YOLO('YOLO.pt')

def use_image_for_ml(jpeg_data):
    print("Processing image in ML model...")
    detected_plate = bbox_crop(jpeg_data, model)
    print(detected_plate)
    return detected_plate

# def bbox_crop(jpeg_data, model):
#     # Convert JPEG data to a file-like object
#     from io import BytesIO
#     image_stream = BytesIO(jpeg_data)
#     img = Image.open(image_stream)
#     # Process the image with the model
#     result = model.detect(img)
#     return result

def main():
    camera_index = find_camera_index()
    if camera_index is None:
        print("No valid camera found. Exiting...")
        return

    last_capture_time = 0
    delay_between_captures = 60  # 60 seconds for testing, adjust as needed

    try:
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print("Received:", data)
                parts = data.split(' ')
                if parts and parts[0].isdigit():
                    distance = int(parts[0])
                    print(f"Distance: {distance} cm")
                    current_time = time.time()
                    if distance == 10 and (current_time - last_capture_time > delay_between_captures):
                        print("Distance is 10 cm, obtaining image.")
                        frame, jpeg_data = capture_and_process_image(camera_index)
                        if jpeg_data is not None:
                            result = use_image_for_ml(jpeg_data)
                            print("Result from ML model:", result)
                        last_capture_time = current_time  # Update the last capture time
                else:
                    print("Data not in correct numeric format.")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        arduino.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
