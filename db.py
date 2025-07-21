import sqlite3
from datetime import datetime


def create_table():
    conn = sqlite3.connect("resume_analysis.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_file TEXT,
            job_role TEXT,
            jd_match TEXT,
            matched_keywords TEXT,
            missing_keywords TEXT,
            profile_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def insert_analysis(resume_filename, job_role, jd_match, matched_keywords, missing_keywords, profile_summary):
    conn = sqlite3.connect("resume_analysis.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses (resume_file, job_role, jd_match, matched_keywords, missing_keywords, profile_summary)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (resume_filename, job_role, jd_match, matched_keywords, missing_keywords, profile_summary))
    conn.commit()
    conn.close()


def get_all_analysis(fetch_all=False):
    conn = sqlite3.connect("resume_analysis.db")
    cursor = conn.cursor()
    if fetch_all:
        cursor.execute('SELECT * FROM analyses ORDER BY id DESC')
    else:
        cursor.execute('SELECT * FROM analyses ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return rows



