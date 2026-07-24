# Quick Start Guide

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Setup

1. Your `.env` file is already configured with Groq API key
2. YOLOv8 model will auto-download on first run

## Run the App

```bash
streamlit run app.py
```

## First Time Usage

1. **Test Detection**:
   - Place a vehicle image in `data/` folder
   - Go to "Detect" tab
   - Upload the image
   - Click "Detect Plates"
   - Save detected plates to log

2. **View Log**:
   - Check "Log" tab to see all entries
   - Add plates to whitelist

3. **Ask Questions**:
   - Try: "Which vehicles entered today?"
   - Try: "Show me non-whitelisted plates"

## Sample Whitelist

Add these in the app or directly via SQL:
```
ABC123
XYZ789
DEF456
```

## Troubleshooting

- **No plates detected**: Use images with visible license plates
- **OCR not accurate**: Image quality matters - clear, well-lit plates work best
- **Groq API error**: Check your API key in `.env` file
