import sqlite3

def init_db(db_path):
    """Create tables if they don't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plate_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            confidence REAL,
            image_path TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whitelist (
            plate_number TEXT PRIMARY KEY
        )
    """)
    
    conn.commit()
    conn.close()
