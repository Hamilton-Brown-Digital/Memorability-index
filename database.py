import sqlite3
from datetime import datetime

DB_FILE = "scores.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
      CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        visual_score REAL,
        summary TEXT,
        timestamp TEXT,
        cognitive_score REAL
      )
    ''')
    conn.commit()
    conn.close()

def save_result(url, visual_score, summary, cognitive_score):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
      INSERT INTO analysis_results 
        (url, visual_score, summary, timestamp, cognitive_score)
      VALUES (?, ?, ?, ?, ?)
    ''', (
        url,
        visual_score,
        summary,
        datetime.utcnow().isoformat(),
        cognitive_score
    ))
    conn.commit()
    conn.close()

def get_recent_results(limit=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
      SELECT url, visual_score, summary, timestamp, cognitive_score
      FROM analysis_results
      ORDER BY timestamp DESC
      LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows