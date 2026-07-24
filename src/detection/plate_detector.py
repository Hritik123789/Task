from ultralytics import YOLO
import numpy as np
import torch

class PlateDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        # Auto-detect GPU
        self.device = 0 if torch.cuda.is_available() else 'cpu'
        if self.device == 0:
            print(f"✓ Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("✓ Using CPU for detection")
    
    def detect_plates(self, image):
        """Detect license plates in image. Returns list of bounding boxes."""
        # Run inference with GPU if available
        results = self.model(image, conf=0.15, iou=0.5, verbose=False, imgsz=640, device=self.device)
        boxes = []
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                
                # Filter by aspect ratio and size
                width = x2 - x1
                height = y2 - y1
                aspect_ratio = width / height if height > 0 else 0
                area = width * height
                
                # Plates can be at angles, so be flexible with ratio
                # Must be reasonably sized (at least 40x15 pixels)
                if 1.0 <= aspect_ratio <= 10.0 and area > 600:
                    boxes.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': conf
                    })
        
        return boxes
