---
title: Smart ANPR System
emoji: 🚗
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: "1.28.1"
app_file: app.py
pinned: false
license: mit
---

# Smart ANPR System

Automated Number Plate Recognition system with YOLOv8, EasyOCR, and Groq LLM.

## Features
- Vehicle plate detection from images/videos
- OCR text extraction
- Natural language queries via Groq
- Whitelist management
- SQLite logging

## Setup
Add your Groq API key in Settings → Repository secrets → New secret:
- Name: `GROQ_API_KEY`
- Value: Your API key from console.groq.com

## Usage
1. Upload image/video in Detect tabs
2. View logs in Log tab
3. Ask questions in Ask tab
