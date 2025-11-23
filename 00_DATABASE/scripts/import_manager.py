#!/usr/bin/env python3
"""
Import Manager - Vedic Mastery Study v2.0
Manages the systematic import of source texts from external repositories.
"""

import sqlite3
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class ImportManager:
    def __init__(self, db_path: str = "../vedic_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self.current_import_id = None
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def register_external_source(self, repo_name: str, repo_url: str, 
                                license_info: str, authority_score: float = 0.8) -> int:
        """Register an external data source."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO external_sources 
            (repo_name, repo_url, license, authority_score, import_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (repo_name, repo_url, license_info, authority_score))
        self.conn.commit()
        return cursor.lastrowid
    
    def start_import(self, external_source_id: int, source_file: str) -> int:
        """Initialize a new import operation."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO import_decisions 
            (external_source_id, source_file, import_date, status)
            VALUES (?, ?, datetime('now'), 'in_progress')
        """, (external_source_id, source_file))
        self.conn.commit()
        self.current_import_id = cursor.lastrowid
        return self.current_import_id
    
    def import_from_json(self, json_file: Path, text_name: str, 
                        external_source_id: int, language: str = 'sanskrit') -> Dict:
        """
        Import verses from a JSON file.
        
        Args:
            json_file: Path to the JSON file
            text_name: Name of the text being imported
            external_source_id: ID of the external source
            language: Language of the text
        
        Returns:
            Dict with import statistics
        """
        import_id = self.start_import(external_source_id, str(json_file))
        
        stats = {
            'verses_imported': 0,
            'verses_skipped': 0,
            'errors': []
        }
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Get text_id
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM texts WHERE name = ?", (text_name,))
            row = cursor.fetchone()
            
            if not row:
                stats['errors'].append(f"Text '{text_name}' not found in database")
                return stats
            
            text_id = row['id']
            
            # Process verses
            for verse_data in data:
                try:
                    self._import_verse(verse_data, text_id, external_source_id, language)
                    stats['verses_imported'] += 1
                except Exception as e:
                    stats['verses_skipped'] += 1
                    stats['errors'].append(str(e))
            
            # Update import decision
            cursor.execute("""
                UPDATE import_decisions 
                SET status = 'completed',
                    verses_imported = ?,
                    verses_skipped = ?,
                    completion_date = datetime('now')
                WHERE id = ?
            """, (stats['verses_imported'], stats['verses_skipped'], import_id))
            self.conn.commit()
            
        except Exception as e:
            stats['errors'].append(f"Fatal error: {str(e)}")
            cursor.execute("""
                UPDATE import_decisions 
                SET status = 'failed',
                    completion_date = datetime('now')
                WHERE id = ?
            """, (import_id,))
            self.conn.commit()
        
        return stats
    
    def _import_verse(self, verse_data: Dict, text_id: int, 
                     external_source_id: int, language: str):
        """Import a single verse (atomic transaction)."""
        cursor = self.conn.cursor()
        
        # Extract verse data
        chapter = verse_data.get('chapter', 0)
        verse_number = verse_data.get('verse', 0)
        devanagari = verse_data.get('devanagari', '')
        transliteration = verse_data.get('transliteration', '')
        translation = verse_data.get('translation', '')
        metadata = json.dumps(verse_data.get('metadata', {}))
        
        # Create source_texts entry
        cursor.execute("""
            INSERT INTO source_texts 
            (text_id, external_source_id, language, is_original, import_date)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (text_id, external_source_id, language, True))
        source_text_id = cursor.lastrowid
        
        # Insert verse
        cursor.execute("""
            INSERT INTO verses 
            (text_id, chapter, verse_number, devanagari, transliteration, 
             source_translation, source_metadata, source_text_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (text_id, chapter, verse_number, devanagari, transliteration, 
              translation, metadata, source_text_id))
        verse_id = cursor.lastrowid
        
        # Initialize reading progress
        cursor.execute("""
            INSERT INTO reading_progress 
            (verse_id, read_status, last_read_date)
            VALUES (?, 'unread', NULL)
        """, (verse_id,))
        
        self.conn.commit()
    
    def get_import_stats(self, import_id: int) -> Dict:
        """Get statistics for a specific import operation."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM import_decisions WHERE id = ?
        """, (import_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return {}

def main():
    """Example usage."""
    manager = ImportManager()
    manager.connect()
    
    # Example: Register a source
    source_id = manager.register_external_source(
        "DharmicData",
        "https://github.com/bhavykhatri/DharmicData",
        "MIT License",
        0.9
    )
    
    print(f"Registered external source with ID: {source_id}")
    
    manager.close()

if __name__ == "__main__":
    main()
