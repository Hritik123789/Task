# Smart ANPR System

Automated Number Plate Recognition system with natural language query capabilities.

## Features

- **Plate Detection**: YOLOv8-based vehicle plate detection from images and videos
- **OCR**: EasyOCR with enhanced accuracy and error correction
- **Video Processing**: Extract and process frames at configurable FPS
- **Logging**: SQLite database with local timestamps
- **Whitelist Management**: Track authorized vehicles
- **Natural Language Queries**: Ask questions about logs using Groq LLM

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Generate an API key
4. Copy `.env.example` to `.env` and add your key:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 3. Download YOLOv8 Model

The app will auto-download `yolov8n.pt` on first run. For better plate detection, you can use a fine-tuned model in `models/`.

### 4. Add Sample Images

Place test vehicle images in `data/sample_images/` for testing.

## Usage

### Run the App

```bash
streamlit run app.py
```

### 60-Second Demo

1. **Detect Image Tab**: Upload a vehicle image → Click "Detect Plates" → View OCR results → Save to log
2. **Detect Video Tab**: Upload video → Set FPS → Process → Review unique plates → Save to log
3. **Log Tab**: See all detected plates with timestamps → Add plates to whitelist
4. **Ask Tab**: Type questions like "Which vehicles entered today?" or "Show non-whitelisted plates"

## Project Structure

```
anpr-project/
├── app.py              # Streamlit interface
├── config.py           # Configuration
├── src/
│   ├── detection/      # YOLOv8 detection
│   ├── ocr/            # EasyOCR reader
│   ├── llm/            # Groq client
│   ├── db/             # SQLite operations
│   └── utils/          # Helper functions
├── data/               # Database and images
└── models/             # YOLO weights
```

## Example Questions

- "Which vehicles entered after 6pm today?"
- "List all non-whitelisted plates"
- "How many unique vehicles were detected?"
- "Show me the most recent entry"

## Tech Stack

- **Detection**: YOLOv8 (ultralytics)
- **OCR**: EasyOCR
- **Frontend**: Streamlit
- **LLM**: Groq API
- **Database**: SQLite
