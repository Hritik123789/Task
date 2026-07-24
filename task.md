Project: Smart ANPR (Automated Number Plate Recognition) System
1. Objective

A working prototype that detects vehicle number plates from an image/video, reads the plate text via OCR, logs each entry with a timestamp, and lets the user ask natural-language questions over that log (e.g., "which vehicles entered after 6pm today", "flag anything not on the whitelist").

Real-world use case: replaces a manual security-guard register at a gated society, office, or parking lot with an automated, queryable log.

Tech stack (fixed — do not deviate):

Detection: YOLOv8 via ultralytics (PyTorch backend)
Preprocessing: OpenCV
OCR: EasyOCR
Frontend: Streamlit
LLM: Groq API only — free tier, OpenAI-compatible chat completion, fast enough for a live demo. Do not build support for other providers. One provider, one client, no abstraction layer for swapping.
Database: SQLite only. This is a structured log (plate number, timestamp, confidence, whitelist status) — a relational table, not semantic search. No vector DB is needed here. Don't add one.
2. Folder Structure
anpr-project/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── app.py                      # Streamlit entry point
│
├── src/
│   ├── detection/
│   │   ├── plate_detector.py   # YOLOv8 wrapper: load model, run inference, return bounding boxes
│   │   └── preprocess.py       # OpenCV: crop, deskew, denoise plate regions
│   │
│   ├── ocr/
│   │   └── plate_reader.py     # EasyOCR wrapper: read text from cropped plate, clean/validate
│   │
│   ├── llm/
│   │   ├── groq_client.py      # Groq API client, single generate(prompt) -> str function
│   │   └── prompts.py          # Prompt templates: log summary, whitelist alert, Q&A over log
│   │
│   ├── db/
│   │   ├── schema.py           # SQLite table definitions (plate_log, whitelist)
│   │   └── store.py            # insert/query functions for the log and whitelist
│   │
│   └── utils/
│       └── image_utils.py
│
├── data/
│   ├── sample_images/          # USER-PROVIDED — see Section 5
│   ├── sample_videos/          # optional, USER-PROVIDED
│   └── plate_log.db            # created at runtime, gitignored
│
├── models/
│   └── yolov8_plate.pt         # USER-PROVIDED or downloaded — see Section 5
│
└── tests/
    ├── test_detection.py
    ├── test_ocr.py
    └── test_llm.py

No notebooks/, no vector_store/, no multi-provider llm/ package — keep it flat and single-purpose.

3. Build Order
Skeleton: create folders/files above. requirements.txt: ultralytics, opencv-python, easyocr, streamlit, torch, torchvision, python-dotenv, groq. .env.example: GROQ_API_KEY=.
Detection: plate_detector.py loads a pretrained YOLOv8 model, detect_plates(image) -> list[BoundingBox]. Test against sample images before moving on.
Preprocessing: preprocess.py — crop to detected box, grayscale, deskew, denoise. Feed this output to OCR, not the raw crop.
OCR: plate_reader.py — EasyOCR reads the preprocessed crop, regex cleanup strips noise characters, returns (plate_text, confidence).
SQLite: schema.py defines two tables — plate_log(id, plate_number, timestamp, confidence, image_path) and whitelist(plate_number). store.py has insert_log_entry(...), get_logs(filters), is_whitelisted(plate_number).
Groq LLM: groq_client.py — one function, generate(prompt: str) -> str, using the groq Python SDK with a chat completion call. prompts.py has three templates: (a) turn a list of log rows into a plain-English report, (b) flag whitelist violations, (c) answer an ad-hoc question given relevant log rows as context.
Streamlit app (app.py), three sections:
Detect: upload image/video → bounding box shown → OCR'd plate + confidence shown → saved to SQLite.
Log: table of all entries from SQLite, whitelist violations highlighted.
Ask: text input → pulls relevant rows from SQLite → passes to groq_client.generate() with the Q&A prompt template → shows answer.
README: setup steps, how to get a free Groq API key, run command (streamlit run app.py), 60-second demo script.
.gitignore: .env, *.db, __pycache__/, models/*.pt if large.
4. Definition of Done
 Upload image → correct bounding box on the plate
 Cropped plate → correct or near-correct OCR text
 Entry written to SQLite with timestamp
 Log tab shows all entries, whitelist violations flagged
 Ask tab returns a sensible answer grounded in the SQLite log
 README lets someone set this up from scratch in under 10 minutes
5. What the user (not the IDE AI) needs to provide

Do not generate or fabricate these — they come from the user:

Sample vehicle images/short video clips for data/sample_images/ and data/sample_videos/ — needed to test detection + OCR and for the live demo.
Groq API key (free, from console.groq.com) — goes in .env as GROQ_API_KEY.
YOLOv8 weights — a pretrained general YOLOv8 model works to start; if a plate-specific fine-tuned model is wanted later, the user will supply the dataset/weights. Don't attempt to source or fine-tune a dataset unprompted.
Whitelist plate numbers (a short list) to seed the whitelist table for demo purposes.