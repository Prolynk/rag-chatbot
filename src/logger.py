import sqlite3
import os
from datetime import datetime

# Path to the SQLite database file
DB_PATH = "logs/feedback.db"

def init_db():
    """Create the logs folder and database table if they don't exist."""
    os.makedirs("logs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            feedback INTEGER DEFAULT NULL
        )
    """)
    conn.commit()
    conn.close()

def log_query(query: str, response: str) -> int:
    """Log a query and response. Returns the row ID for feedback updates."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO query_logs (timestamp, query, response)
        VALUES (?, ?, ?)
    """, (datetime.now().isoformat(), query, response))
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return row_id

def log_feedback(row_id: int, feedback: int):
    """Update a log entry with user feedback. 1 = helpful, 0 = not helpful."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE query_logs SET feedback = ? WHERE id = ?
    """, (feedback, row_id))
    conn.commit()
    conn.close()

def get_low_solve_rate_queries():
    """Return all queries that received negative feedback."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, query, response 
        FROM query_logs 
        WHERE feedback = 0
        ORDER BY timestamp DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")