import cv2
import tempfile
import os

def extract_frames(video_path, fps=1):
    """Extract frames from video at specified FPS."""
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)
    
    frames = []
    frame_count = 0
    success = True
    
    while success:
        success, frame = cap.read()
        if success and frame_count % frame_interval == 0:
            frames.append(frame)
        frame_count += 1
    
    cap.release()
    return frames

def save_uploaded_video(uploaded_file):
    """Save uploaded video to temp file."""
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    tfile.close()
    return tfile.name
