import easyocr
import re
import torch

class PlateReader:
    def __init__(self):
        # Auto-detect GPU
        gpu = torch.cuda.is_available()
        self.reader = easyocr.Reader(['en'], gpu=gpu)
        if gpu:
            print(f"✓ Using GPU for OCR: {torch.cuda.get_device_name(0)}")
        else:
            print("✓ Using CPU for OCR")
    
    def read_plate(self, image):
        """Extract text from preprocessed plate image."""
        # Use allowlist to restrict to alphanumeric only
        results = self.reader.readtext(
            image, 
            detail=1,
            allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            paragraph=False
        )
        
        if not results:
            return "", 0.0
        
        # Sort by x-coordinate and filter by confidence
        results = sorted(results, key=lambda x: x[0][0][0])
        results = [r for r in results if r[2] > 0.3]
        
        if not results:
            return "", 0.0
        
        text = "".join([res[1] for res in results])
        confidence = sum([res[2] for res in results]) / len(results)
        
        # Clean
        cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Indian plate pattern: 2 letters, 2 digits, 1-2 letters, 4 digits
        match = re.search(r'([A-Z]{2}\d{2}[A-Z]{1,2}\d{4})', cleaned)
        if match:
            cleaned = match.group(1)
        
        return cleaned, confidence
