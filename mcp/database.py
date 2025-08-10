import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class ContextDatabase:
    def __init__(self, db_path: str = "data/context_web.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the database and tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                size INTEGER,
                modified_time TEXT,
                indexed_at TEXT,
                content_hash TEXT,
                content TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized with tables.")
    
    def save_file(self, file_info: Dict[str, Any]):
        """Save or update file information in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        modified_time = file_info['modified_time']
        if hasattr(modified_time, 'isoformat'):
            modified_time = modified_time.isoformat()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO files 
                (path, name, size, modified_time, indexed_at, content)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                file_info['path'],
                file_info['name'], 
                file_info['size'],
                modified_time,
                datetime.now().isoformat(),
                file_info.get('content', '')
            ))
            file_id = cursor.lastrowid
            conn.commit()
            return file_id
        except sqlite3.IntegrityError as e:
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            conn.close()