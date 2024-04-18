import serial
import cv2
import os
import time

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

def capture_image(camera_index):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Cannot open camera at index {camera_index}")
        return
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        cap.release()
        return
    img_name = f"image_{time.strftime('%Y%m%d-%H%M%S')}.png"
    img_path = os.path.join('C:\\Users\\User\\Desktop\\images', img_name)
    cv2.imwrite(img_path, frame)
    print(f"Image saved to {img_path}")
    cap.release()

def main():
    camera_index = find_camera_index()
    if camera_index is None:
        print("No valid camera found. Exiting...")
        return
    
    last_capture_time = 0
    delay_between_captures = 60  # 300 seconds == 5 minutes

    try:
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print("Received:", data)  # Debugging print to see what is received
                parts = data.split(' ')
                if parts and parts[0].isdigit():
                    distance = int(parts[0])
                    print(f"Distance: {distance} cm")
                    current_time = time.time()
                    if distance == 10 and (current_time - last_capture_time > delay_between_captures):
                        print("Distance is 10 cm, capturing image.")
                        capture_image(camera_index)
                        last_capture_time = current_time  # Update the last capture time
                else:
                    print("Data not in correct numeric format.")
            time.sleep(0.1)  # Short delay to prevent flooding with data
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        arduino.close()
        print("Serial connection closed.")

if __name__ == "__main__":
    main()
