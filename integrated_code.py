import serial
import cv2
import os
import time
import numpy as np

# Establish a connection to the Arduino on COM6
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

def main():
    index = 0
    last_capture_time = 0
    delay_between_captures = 300  # 300 seconds == 5 minutes

    while True:
        # Find camera index
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if not cap.read()[0]:
            cap.release()
            index += 1
        else:
            print(f"Camera found at index {index}")
            cap.release()
            break  # Exit the loop once the camera index is found

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
                        # Capture and process image
                        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
                        if not cap.isOpened():
                            print(f"Cannot open camera at index {index}")
                            continue
                        ret, frame = cap.read()
                        cap.release()
                        if not ret:
                            print("Can't receive frame (stream end?). Exiting ...")
                            continue
                        
                        # Optionally encode to JPEG if needed for saving or transmission
                        _, jpeg = cv2.imencode('.jpg', frame)
                        
                        # Dummy function for ML prediction
                        print("Processing image in ML model...")
                        # Process the image as needed for your ML model here
                        result = "Predicted Output"

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
    return frame
