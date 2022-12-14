from asyncio.windows_events import NULL
from contextlib import nullcontext
import cv2
import numpy as np
import glob
import random

print(cv2.__version__)

# Load Yolo
net = cv2.dnn.readNet("yolov3_training_last (New).weights", "yolov3_testing.cfg")

# Name custom object
classes = ["RubiksCube"]

# Images path
images_path = glob.glob(r"C:\Users\tusha\Documents\Python Projects\OpenCV Test\Cubes\*.jpg")
img_path = r"C:\Users\tusha\Documents\Python Projects\OpenCV Test\Cubes\001.jpg"

layer_names = net.getLayerNames()
print(layer_names)

print(net.getUnconnectedOutLayers())

output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

def GrabVideo():
    return cv2.VideoCapture(r'C:\Users\tusha\Documents\Python Projects\OpenCV Test\Cubes\RubiksCube7.mp4')

capture = GrabVideo()

while True:
    isTrue, frame = capture.read()
    if (isTrue):
        img = cv2.resize(frame, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 2)


        cv2.imshow("Image", img)
        
        if cv2.waitKey(1) & 0xFF == ord('d'):
            break
    else:
        capture = GrabVideo()

# Insert here the path of your images
random.shuffle(images_path)
# loop through all the images
    # Loading image

key = cv2.waitKey(0)

cv2.destroyAllWindows()