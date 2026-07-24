import sqlite3
from datetime import datetime

def insert_log_entry(db_path, plate_number, confidence, image_path=None):
    """Insert new plate detection into log."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Use local timestamp
    local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(
        "INSERT INTO plate_log (plate_number, timestamp, confidence, image_path) VALUES (?, ?, ?, ?)",
        (plate_number, local_time, confidence, image_path)
    )
    conn.commit()
    conn.close()

def get_logs(db_path, filters=None):
    """Retrieve log entries, optionally filtered."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM plate_log ORDER BY timestamp DESC"
    cursor.execute(query)
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return logs

def is_whitelisted(db_path, plate_number):
    """Check if plate is on whitelist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM whitelist WHERE plate_number = ?", (plate_number,))
    result = cursor.fetchone()
    conn.close()
    
    return result is not None

def add_to_whitelist(db_path, plate_number):
    """Add plate to whitelist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO whitelist (plate_number) VALUES (?)", (plate_number,))
    conn.commit()
    conn.close()
