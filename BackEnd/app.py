from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
import torch
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)  # Allows requests from frontend

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Load YOLO model
model_path = "E:/Documents/Codes/Python/GCNN Object Detection/YoloModel/best.pt"
try:
    model = YOLO(model_path)
    print("YOLO model loaded successfully")  # Debugging statement
except Exception as e:
    print("Failed to load YOLO model:", e)  # Debugging statement

@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    print("File received:", file.filename)  # Debugging statement

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print("File saved to:", filepath)  # Debugging statement

    # Process with YOLO
    try:
        results = model(filepath)
        print("YOLO processing complete")  # Debugging statement
    except Exception as e:
        print("YOLO processing error:", e)  # Debugging statement
        return jsonify({"error": "YOLO processing failed"}), 500

    processed_filepath = os.path.join(PROCESSED_FOLDER, filename)
    for result in results:
        img = result.plot()  # Draw bounding boxes
        cv2.imwrite(processed_filepath, img)
        print("Processed image saved to:", processed_filepath)  # Debugging statement

    return jsonify({"processed_image": f"processed/{filename}"}), 200

@app.route("/processed/<filename>")
def processed_image(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)