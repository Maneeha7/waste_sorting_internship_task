# AI Waste Sorting & Recycling Assistant

This project analyzes images containing one or more waste objects, detects the objects, classifies their waste category, determines recyclability, and provides an appropriate disposal recommendation — through a simple Flask web app.

I built this as an internship task to apply object detection to a real-world sustainability problem: helping people figure out how to correctly dispose of waste just from a photo.

## Overview

Upload a photo of waste (a single item or a cluttered scene with multiple objects), and the app will:

1. Detect every waste object in the image using a trained **YOLO** object detection model.
2. Classify each detected object into a waste category (e.g., plastic, metal, glass, paper, organic).
3. Look up recycling guidance for that category from a rules file.
4. Return an annotated image (with bounding boxes) plus a per-object breakdown of category, confidence score, recyclability, and disposal instructions.

## Features

- **Multi-object detection** — handles images with more than one waste item at a time.
- **Category classification** — maps each detected object to a waste type.
- **Recyclability check** — flags whether an item is recyclable.
- **Disposal recommendations** — suggests the correct disposal method per object, driven by `waste_guidance.json`.
- **Visual output** — returns the uploaded image annotated with bounding boxes and labels.
- **Simple web UI** — upload and view results directly in the browser, no coding required.

## Tech Stack

| Component | Technology |
|---|---|
| Backend | Flask (Python) |
| Object detection | YOLO ([Ultralytics](https://github.com/ultralytics/ultralytics)) |
| Image processing | OpenCV |
| File handling | Werkzeug |
| Frontend | HTML templates (Jinja2) |

## Project Structure

```
waste_sorting_internship_task/
├── app.py                          # Flask application entry point
├── final_waste_model.pt            # Trained YOLO model weights (not included — see below)
├── waste_guidance.json             # Category → recyclability/disposal rules
├── requirements.txt                # Python dependencies
├── templates/                      # HTML templates (index page, results view)
├── static/
│   ├── uploads/                    # User-uploaded images (auto-created)
│   └── results/                    # Annotated output images (auto-created)
├── test_images/                    # Sample images for testing
└── recycling_assistant_screenshots/ # App screenshots / demo images
```

## Getting Started

I've kept setup as minimal as possible so anyone can clone this and run it locally.

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Maneeha7/waste_sorting_internship_task.git
   cd waste_sorting_internship_task
   ```

2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure the trained model file `final_waste_model.pt` is placed in the project root — the app loads it from there (see [Model](#model) below).

### Running the App

```bash
python app.py
```

The app will start in debug mode. Open your browser and go to:

```
http://127.0.0.1:5000
```

Upload an image on the home page, and the app will return the detected objects along with their category, confidence, recyclability status, and disposal instructions.

## Model

The app expects a YOLO model checkpoint named `final_waste_model.pt` in the project root. This is the model I trained to detect and classify common waste object categories. If you're retraining or swapping in your own model:

- Update `MODEL_PATH` in `app.py` if you use a different filename.
- Make sure the class names your model outputs match the keys in `waste_guidance.json`, so each detection maps to the correct recycling guidance. Any label not found in `waste_guidance.json` falls back to a default "Other / manual inspection recommended" response.

## Customizing Recycling Rules

`waste_guidance.json` is where I store the recycling rules — it maps each detectable class name to:

```json
{
  "example_class_name": {
    "category": "Plastic",
    "recyclable": true,
    "disposal": "Rinse and place in the recycling bin."
  }
}
```

You can add, remove, or edit entries here to change how a category is classified or what disposal advice is shown — no code changes needed.

## Sample Data

I've included some sample images in `test_images/` so you can try the app without needing your own photos, and a few example results in `recycling_assistant_screenshots/`.

## Future Improvements

Things I'd like to add if I keep working on this:

- Support for batch/multiple image uploads
- A wider waste category taxonomy and more detailed guidance rules
- Deployment to a cloud host for public access
- A confidence threshold slider in the UI

## About

I built this project to apply object detection (YOLO) to a real-world sustainability use case — helping automate waste sorting and giving people clear, actionable recycling guidance.