

# Smart ANPR System

Automated Number Plate Recognition system using YOLOv8, EasyOCR, and Groq LLM.

## Features

- **Plate Detection**: YOLOv8-based vehicle plate detection from images and videos
- **OCR**: EasyOCR with enhanced accuracy and error correction
- **Video Processing**: Extract and process frames at configurable FPS
- **Logging**: SQLite database with local timestamps
- **Whitelist Management**: Track authorized vehicles
- **Natural Language Queries**: Ask questions about logs using Groq LLM

## Setup

Add your Groq API key in Space Settings → Repository secrets:
- Name: `GROQ_API_KEY`
- Value: Your API key from console.groq.com

## Usage

1. **Detect Image Tab**: Upload vehicle images for plate detection
2. **Detect Video Tab**: Upload videos and process at selected FPS
3. **Log Tab**: View all detected plates with timestamps and whitelist status
4. **Ask Tab**: Query logs using natural language

## Tech Stack

- Detection: YOLOv8 (Ultralytics)
- OCR: EasyOCR
- Frontend: Streamlit
- LLM: Groq API (Llama 3.3)
- Database: SQLite
