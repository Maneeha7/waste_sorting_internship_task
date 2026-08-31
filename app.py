from flask import Flask, render_template, request
from ultralytics import YOLO
from werkzeug.utils import secure_filename

import os
import json
import uuid


app = Flask(__name__)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER


# --------------------------------------------------
# Load trained YOLO model
# --------------------------------------------------

MODEL_PATH = "final_waste_model.pt"

model = YOLO(MODEL_PATH)

print("YOLO model loaded successfully.")
print("Number of classes:", len(model.names))


# --------------------------------------------------
# Load recycling rules
# --------------------------------------------------

with open("waste_guidance.json", "r") as f:
    waste_guidance = json.load(f)


# --------------------------------------------------
# Analyze image
# --------------------------------------------------

def analyze_image(image_path):

    results = model.predict(
        source=image_path,
        imgsz=640,
        conf=0.25,
        verbose=False
    )

    result = results[0]

    objects = []

    if result.boxes is not None:

        for i in range(len(result.boxes)):

            class_id = int(result.boxes.cls[i].item())

            confidence = float(
                result.boxes.conf[i].item()
            )

            bbox = (
                result.boxes.xyxy[i]
                .cpu()
                .numpy()
                .tolist()
            )

            label = model.names[class_id]

            guidance = waste_guidance.get(
                label,
                {
                    "category": "Other",
                    "recyclable": False,
                    "disposal": "Manual inspection recommended."
                }
            )

            objects.append({
                "label": label,
                "category": guidance["category"],
                "confidence": round(confidence * 100, 2),
                "recyclable": guidance["recyclable"],
                "disposal": guidance["disposal"],
                "bbox": bbox
            })

    # Save annotated image
    annotated = result.plot()

    filename = f"{uuid.uuid4().hex}.jpg"

    result_path = os.path.join(
        app.config["RESULT_FOLDER"],
        filename
    )

    import cv2
    cv2.imwrite(result_path, annotated)

    return objects, filename


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# --------------------------------------------------
# Analyze uploaded image
# --------------------------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    if "image" not in request.files:

        return render_template(
            "index.html",
            error="Please upload an image."
        )

    file = request.files["image"]

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )

    filename = secure_filename(file.filename)

    unique_filename = (
        uuid.uuid4().hex + "_" + filename
    )

    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    file.save(image_path)

    objects, result_filename = analyze_image(
        image_path
    )

    return render_template(
        "index.html",
        objects=objects,
        result_image=result_filename
    )


# --------------------------------------------------
# Run Flask application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )