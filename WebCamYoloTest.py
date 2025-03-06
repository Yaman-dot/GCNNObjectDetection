import cv2
import os
import supervision as sv
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('YoloModel/best.pt')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the annotators
bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break

    # Perform object detection
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)
    # Display the resulting frame
    cv2.imshow('YOLO Object Detection', frame)
    
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()