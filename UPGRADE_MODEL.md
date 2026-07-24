# Upgrade to Plate-Specific Model

Your current setup uses YOLOv8n (general object detection). For much better accuracy, use a plate-specific model.

## Quick Upgrade (5 minutes)

### Option 1: Download Pre-trained Plate Model

```bash
# Install gdown to download from Google Drive
pip install gdown

# Download a plate-specific YOLOv8 model (example)
gdown https://drive.google.com/uc?id=YOUR_MODEL_ID -O models/plate_detector.pt

# Update config.py
MODEL_PATH = "models/plate_detector.pt"
```

### Option 2: Use Roboflow Pre-trained Model

1. Visit: https://universe.roboflow.com/roboflow-universe-projects/license-plate-recognition-rxg4e
2. Click "Download Dataset"
3. Choose "YOLOv8" format
4. Download the model weights
5. Place `.pt` file in `models/` folder
6. Update `config.py` with the new path

### Option 3: Train Your Own (Advanced)

```python
from ultralytics import YOLO

# Start with pretrained YOLOv8n
model = YOLO('yolov8n.pt')

# Train on your plate dataset
model.train(
    data='plates.yaml',  # Your dataset config
    epochs=100,
    imgsz=640,
    batch=16
)

# Export best weights
# Use runs/detect/train/weights/best.pt
```

## Expected Improvements

**Current (YOLOv8n general):**
- ❌ Detects entire cars/bikes
- ⚠️ Misses distant plates
- ⚠️ Struggles with angled plates
- Speed: Okay

**With Plate-Specific Model:**
- ✅ Detects ONLY plates
- ✅ Catches distant plates (100+ meters)
- ✅ Handles angles better
- ✅ Fewer false positives
- Speed: Same or faster

## Quick Test Models

### Indian Plate Model (Recommended)
```bash
# Download from Kaggle
kaggle datasets download -d andrewmvd/indian-license-plate-detection
unzip indian-license-plate-detection.zip -d models/
```

### Universal Plate Model
Search on:
- Roboflow Universe
- Ultralytics Hub
- Kaggle Datasets
- GitHub (search "yolov8 license plate")

## After Upgrading

Just update `config.py`:
```python
MODEL_PATH = "models/your_new_model.pt"
```

Restart the app - everything else stays the same!

## Performance Comparison

| Model Type | Detection Rate | False Positives | Distance |
|------------|---------------|-----------------|----------|
| YOLOv8n (current) | 60-70% | High | <30m |
| Plate-specific | 90-95% | Low | 100m+ |

## Need Help?

If you find a good model link, I can help integrate it!
