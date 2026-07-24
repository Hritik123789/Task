import os
from dotenv import load_dotenv

load_dotenv()

# Try to get from Hugging Face Spaces secrets first, then .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
DB_PATH = "data/plate_log.db"
MODEL_PATH = "models/yolov8n.pt"

if not GROQ_API_KEY:
    print("⚠️ Warning: GROQ_API_KEY not found. Please set it in environment variables or .env file")
