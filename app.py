import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import config
from src.db.schema import init_db
from src.db.store import insert_log_entry, get_logs, is_whitelisted, add_to_whitelist
from src.detection.plate_detector import PlateDetector
from src.detection.preprocess import preprocess_plate
from src.ocr.plate_reader import PlateReader
from src.llm.groq_client import GroqClient
from src.llm.prompts import log_summary_prompt, whitelist_alert_prompt, qa_prompt
from src.utils.image_utils import draw_boxes
from src.utils.video_utils import extract_frames, save_uploaded_video
import os
import torch

# Initialize
Path("data").mkdir(exist_ok=True)
Path("models").mkdir(exist_ok=True)
init_db(config.DB_PATH)

st.set_page_config(page_title="Smart ANPR System", layout="wide")

# GPU Status in sidebar
with st.sidebar:
    st.header("System Info")
    if torch.cuda.is_available():
        st.success(f"🚀 GPU: {torch.cuda.get_device_name(0)}")
        st.info(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        st.warning("💻 Running on CPU")
    st.divider()

st.title("🚗 Smart ANPR System")

# Initialize models
@st.cache_resource
def load_models():
    detector = PlateDetector(config.MODEL_PATH)
    reader = PlateReader()
    llm = GroqClient()
    return detector, reader, llm

detector, reader, llm = load_models()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Detect Image", "🎥 Detect Video", "📋 Log", "💬 Ask"])

# Tab 1: Image Detection
with tab1:
    st.header("Upload Image for Plate Detection")
    uploaded_file = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        if st.button("Detect Plates"):
            with st.spinner("Detecting plates..."):
                boxes = detector.detect_plates(image)
                st.session_state['boxes'] = boxes
                st.session_state['image'] = image
        
        # Display results if available
        if 'boxes' in st.session_state and st.session_state['boxes']:
            boxes = st.session_state['boxes']
            image = st.session_state['image']
            
            annotated = draw_boxes(image, boxes)
            
            with col2:
                st.subheader("Detection Result")
                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
            
            st.success(f"Found {len(boxes)} plate(s)")
            
            for idx, box in enumerate(boxes):
                with st.expander(f"Plate {idx+1} (Confidence: {box['confidence']:.2f})", expanded=True):
                    preprocessed = preprocess_plate(image, box['bbox'])
                    plate_text, ocr_conf = reader.read_plate(preprocessed)
                    
                    if plate_text:
                        st.write(f"**Plate Number:** {plate_text}")
                        st.write(f"**OCR Confidence:** {ocr_conf:.2f}")
                        
                        whitelisted = is_whitelisted(config.DB_PATH, plate_text)
                        st.write(f"**Whitelist Status:** {'✅ Whitelisted' if whitelisted else '⚠️ Not Whitelisted'}")
                        
                        if st.button(f"Save to Log", key=f"save_{idx}"):
                            try:
                                insert_log_entry(config.DB_PATH, plate_text, ocr_conf, uploaded_file.name)
                                st.success(f"✅ Saved {plate_text} to database!")
                                st.balloons()
                            except Exception as e:
                                st.error(f"Error saving: {e}")
                    else:
                        st.warning("Could not read plate text. Try adjusting image quality.")
        elif 'boxes' in st.session_state and not st.session_state['boxes']:
            st.warning("No plates detected")

# Tab 2: Video Detection
with tab2:
    st.header("Upload Video for Plate Detection")
    uploaded_video = st.file_uploader("Choose a video", type=['mp4', 'avi', 'mov', 'mkv'])
    
    if uploaded_video:
        st.video(uploaded_video)
        
        fps = st.slider("Frames to process per second", 0.5, 3.0, 1.0, 0.5)
        
        if st.button("Process Video"):
            with st.spinner("Processing video..."):
                # Save video temporarily
                video_path = save_uploaded_video(uploaded_video)
                
                try:
                    # Extract frames
                    frames = extract_frames(video_path, fps=fps)
                    st.info(f"Processing {len(frames)} frames...")
                    
                    detected_plates = {}
                    all_detections = []  # For debugging
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, frame in enumerate(frames):
                        status_text.text(f"Processing frame {idx+1}/{len(frames)}...")
                        boxes = detector.detect_plates(frame)
                        
                        for box in boxes:
                            preprocessed = preprocess_plate(frame, box['bbox'])
                            
                            # Skip if preprocessing failed
                            if preprocessed is None:
                                continue
                                
                            plate_text, ocr_conf = reader.read_plate(preprocessed)
                            
                            # Store all attempts for debugging
                            all_detections.append({
                                'frame': idx+1,
                                'text': plate_text,
                                'conf': ocr_conf,
                                'bbox': box['bbox']
                            })
                            
                            # Relaxed filtering: just needs some text and reasonable confidence
                            if plate_text and len(plate_text) >= 8 and ocr_conf > 0.3:
                                if plate_text not in detected_plates or detected_plates[plate_text]['conf'] < ocr_conf:
                                    detected_plates[plate_text] = {
                                        'conf': ocr_conf,
                                        'frame': frame,
                                        'box': box
                                    }
                        
                        progress_bar.progress((idx + 1) / len(frames))
                    
                    status_text.empty()
                    
                    # Show debug info
                    with st.expander("🔍 Debug Info - All Detections"):
                        st.write(f"Total detections attempted: {len(all_detections)}")
                        for det in all_detections[:20]:  # Show first 20
                            st.write(f"Frame {det['frame']}: '{det['text']}' (conf: {det['conf']:.2f}, len: {len(det['text'])})")
                    
                    st.success(f"Found {len(detected_plates)} unique plate(s)")
                    
                    if detected_plates:
                        for plate_num, data in detected_plates.items():
                            with st.expander(f"Plate: {plate_num} (Confidence: {data['conf']:.2f})", expanded=True):
                                annotated = draw_boxes(data['frame'], [data['box']])
                                st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB))
                                
                                whitelisted = is_whitelisted(config.DB_PATH, plate_num)
                                st.write(f"**Whitelist Status:** {'✅ Whitelisted' if whitelisted else '⚠️ Not Whitelisted'}")
                                
                                if st.button(f"Save to Log", key=f"vid_save_{plate_num}"):
                                    try:
                                        insert_log_entry(config.DB_PATH, plate_num, data['conf'], uploaded_video.name)
                                        st.success(f"✅ Saved {plate_num} to database!")
                                        st.balloons()
                                    except Exception as e:
                                        st.error(f"Error saving: {e}")
                    else:
                        st.warning("No plates detected in video. Check debug info above to see what was detected.")
                
                finally:
                    # Cleanup temp file
                    if os.path.exists(video_path):
                        os.unlink(video_path)

# Tab 3: Log View
with tab3:
    st.header("Detection Log")
    
    logs = get_logs(config.DB_PATH)
    
    if logs:
        violations = [log for log in logs if not is_whitelisted(config.DB_PATH, log['plate_number'])]
        
        if violations:
            st.error(f"⚠️ {len(violations)} whitelist violation(s) detected!")
        
        for log in logs:
            whitelisted = is_whitelisted(config.DB_PATH, log['plate_number'])
            status = "✅" if whitelisted else "⚠️"
            
            with st.expander(f"{status} {log['plate_number']} - {log['timestamp']}"):
                st.write(f"**Confidence:** {log['confidence']:.2f}")
                st.write(f"**Image:** {log['image_path']}")
                st.write(f"**Status:** {'Whitelisted' if whitelisted else 'Not Whitelisted'}")
    else:
        st.info("No entries in log yet")
    
    # Add to whitelist
    st.subheader("Manage Whitelist")
    new_plate = st.text_input("Add plate to whitelist")
    if st.button("Add to Whitelist"):
        if new_plate:
            add_to_whitelist(config.DB_PATH, new_plate.upper())
            st.success(f"Added {new_plate.upper()} to whitelist!")
            st.rerun()

# Tab 4: Ask Questions
with tab4:
    st.header("Ask Questions About the Log")
    
    question = st.text_input("Enter your question")
    
    if st.button("Get Answer"):
        if question:
            with st.spinner("Thinking..."):
                logs = get_logs(config.DB_PATH)
                
                if logs:
                    prompt = qa_prompt(question, logs)
                    answer = llm.generate(prompt)
                    
                    st.write("**Answer:**")
                    st.write(answer)
                else:
                    st.warning("No log entries to query")
        else:
            st.warning("Please enter a question")
