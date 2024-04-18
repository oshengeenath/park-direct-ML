import serial
import cv2
import os
import time
import numpy as np

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
        print(f"Cannot open camera at index {camera_index}")
        return None, None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None, None
    
    # Optionally encode to JPEG if needed for saving or transmission
    _, jpeg = cv2.imencode('.jpg', frame)
    
    return frame, jpeg.tobytes()  # Return both the raw frame and the JPEG data

def use_image_for_ml(frame):
    # Placeholder for machine learning model processing
    # Assume `model_predict` is a function that takes a frame and returns some output
    output = model_predict(frame)
    return output

def model_predict(image):
    # Dummy function for ML prediction
    print("Processing image in ML model...")
    # Process the image as needed for your ML model here
    return "Predicted Output"

def main():
    camera_index = find_camera_index()
    if camera_index is None:
        print("No valid camera found. Exiting...")
        return
    
    last_capture_time = 0
    delay_between_captures = 300  # 300 seconds == 5 minutes

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
                        if frame is not None:
                            result = use_image_for_ml(frame)
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
