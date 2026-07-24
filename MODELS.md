# Model Information

## Current Model

The app uses **YOLOv8n** (general object detection) which can detect vehicles but isn't specifically trained for license plates.

## Better Detection Options

For improved plate detection, you can use a plate-specific model:

### Option 1: Download Pre-trained Plate Model

1. Visit [Roboflow Universe - License Plate Detection](https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e/model/)
2. Download a YOLOv8 plate detection model
3. Place it in `models/` folder
4. Update `config.py`: `MODEL_PATH = "models/your_plate_model.pt"`

### Option 2: Use Existing Models

Some good pre-trained models:
- **YOLOv8-plate** from Ultralytics Hub
- **ANPR models** from Roboflow
- Fine-tuned models from Kaggle

## Why This Matters

- **General YOLOv8n**: Detects cars/bikes/people (not ideal for plates)
- **Plate-specific model**: Trained specifically on license plates (much better accuracy)

## Performance

With general YOLOv8n:
- May detect entire vehicles instead of plates
- Works OK on clear, front-facing plates
- Needs aspect ratio filtering

With plate-specific model:
- Directly detects only plates
- Much faster and more accurate
- No false detections
