from PIL import Image
import numpy as np
import cv2
from paddleocr import PaddleOCR

"""
This script send the images through the YOLOV8 network and get the bounding boxes coordinates and store it in num_plate 
variable and run the ocr function through it
"""
def bbox_crop(image_folder,model):
        img = Image.open(image_folder)
        #convert the images into grayscale and add then to a numpy array
        results = model(source=image_folder)
        img = img.convert('L')
        numpy_image = np.array(img)
        # by using the objects cropped get the bounding box co-ordinates
        for r in results:
            numpy_boxes = (((r.boxes.xyxy).cpu().detach().numpy()))
            for box in numpy_boxes:
                # Extract the region of interest (ROI) from the image array
                num_plate = numpy_image[int(box[1]):int(box[3]), int(box[0]): int(box[2])]
                detected_plate = ocr(num_plate)
        return detected_plate


"""
This script takes the bounding box coordinates from the YOLOv8 network and then run an OCR function to get the text
of the detected number plates then did some post processing only to get the index 0 that means only the number plates.
"""
def ocr(num_plate):
    characters = PaddleOCR(use_angle_cls=True,lang='en')
    cv2.waitKey(5)
    result = characters.ocr(num_plate, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            pass

    result = result[0]
    plate = [line[1][0] for line in result]
    plate_number = plate[0]
    plate_space = plate_number.replace(" ", "")
    detected_plate = plate_space[-7:]
    return detected_plate
