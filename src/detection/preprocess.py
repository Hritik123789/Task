import cv2
import numpy as np

def preprocess_plate(image, bbox):
    """Crop, grayscale, denoise plate region for OCR."""
    x1, y1, x2, y2 = bbox
    cropped = image[y1:y2, x1:x2]
    
    # Skip if too small
    if cropped.shape[0] < 10 or cropped.shape[1] < 30:
        return None
    
    # Resize to better size for OCR
    h, w = cropped.shape[:2]
    if w < 300:
        scale = 300 / w
        cropped = cv2.resize(cropped, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    
    # Try to enhance if image is blurry (motion blur from video)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    # Otsu's thresholding
    _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh
