# database.py – SQLite3 functions for reports and users (email-based login)

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "reports.db")


# Connect to the SQLite database (creates the file if it does not exist)
def get_connection():
    return sqlite3.connect(DB_PATH)


# Create both tables on first run; safe to call multiple times (IF NOT EXISTS)
def init_db():
    conn = get_connection()
    # Users table: stores email and a hashed password – never plain text
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    # Reports table: user_id links each report to its owner
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            role    TEXT NOT NULL,
            score   REAL NOT NULL,
            data    TEXT NOT NULL,
            user_id INTEGER,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# Insert a new user row; password_hash is already hashed before calling this
def create_user(email, password_hash):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users (email, password_hash) VALUES (?, ?)",
        (email, password_hash)
    )
    conn.commit()
    conn.close()


# Return a user dict by email, or None if not found
def get_user(email):
    conn = get_connection()
    row = conn.execute(
        "SELECT id, email, password_hash FROM users WHERE email = ?",
        (email,)
    ).fetchone()
    conn.close()
    if row:
        return {"id": row[0], "email": row[1], "password_hash": row[2]}
    return None


# Save a report and link it to the logged-in user via user_id
def save_report(name, role, score, report_dict, user_id=None):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO reports (name, role, score, data, user_id) VALUES (?, ?, ?, ?, ?)",
        (name, role, score, json.dumps(report_dict), user_id)
    )
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


# Return summary rows for history; filter by user_id so each user sees only their own
def list_reports(user_id=None):
    conn = get_connection()
    if user_id:
        rows = conn.execute(
            "SELECT id, name, role, score, created FROM reports WHERE user_id = ? ORDER BY created DESC",
            (user_id,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, name, role, score, created FROM reports ORDER BY created DESC"
        ).fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "score": r[3], "created": r[4]} for r in rows]


# Return one full report dict by its id, or None if not found
def get_report(report_id):
    conn = get_connection()
    row = conn.execute("SELECT data FROM reports WHERE id = ?", (report_id,)).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None
