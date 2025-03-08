import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
from PIL import Image
import numpy as np


# Title of the app
st.title("Pistol Object Detection App ")
st.write("Upload an image, and let Our AI Model detect Pistols in it!")

# Load the YOLO model
model = YOLO("E:\Documents\Codes\Python\GCNN Object Detection\YoloModel\best.pt")  # You can use other versions like yolov8s, yolov8m, etc.

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert the image to OpenCV format
    image_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Run YOLO model on the image
    results = model(image_cv2)

    # Plot the results on the image
    annotated_image = results[0].plot()

    # Convert the annotated image back to PIL format for display
    annotated_image_pil = Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))

    # Display the annotated image
    st.image(annotated_image_pil, caption="Detected Objects", use_column_width=True)

    # Add a download button for the annotated image
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmpfile:
        annotated_image_pil.save(tmpfile.name, format="JPEG")
        st.download_button(
            label="Download Annotated Image",
            data=open(tmpfile.name, "rb").read(),
            file_name="annotated_image.jpg",
            mime="image/jpeg",
        )