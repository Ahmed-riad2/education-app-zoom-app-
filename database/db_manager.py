import sqlite3
import hashlib
import os

DB_PATH = "eduverse.db"

def hash_password(password: str) -> str:
    """Simple SHA-256 hash for passwords."""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initializes the SQLite database and creates required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Seed initial test users if the database is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                       ("Alex Bradley", "student@eduverse.ai", hash_password("student123"), "Student"))
        cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                       ("Dr. Smith", "teacher@eduverse.ai", hash_password("teacher123"), "Teacher"))
        
    conn.commit()
    conn.close()

def get_connection():
    """Returns a new SQLite connection."""
    return sqlite3.connect(DB_PATH)