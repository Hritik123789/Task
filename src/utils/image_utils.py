import cv2
import numpy as np

def draw_boxes(image, boxes):
    """Draw bounding boxes on image."""
    img_copy = image.copy()
    for box in boxes:
        x1, y1, x2, y2 = box['bbox']
        conf = box['confidence']
        cv2.rectangle(img_copy, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img_copy, f"{conf:.2f}", (x1, y1-10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return img_copy
