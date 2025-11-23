#!/usr/bin/env python3
"""
DharmicData Importer - Vedic Mastery Study v2.0
Specialized importer for the DharmicData repository format.
"""

import sqlite3
import json
import os
from pathlib import Path
from typing import Dict, List

class DharmicDataImporter:
    def __init__(self, db_path: str = "/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self.external_source_id = 1  # DharmicData is registered as ID 1
        self.stats = {
            'total_imported': 0,
            'total_skipped': 0,
            'by_text': {}
        }
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.commit()
            self.conn.close()
    
    def import_all(self, dharmic_data_path: str):
        """Import all texts from DharmicData repository."""
        base_path = Path(dharmic_data_path)
        
        # Import Rigveda (10 mandalas)
        print("Importing Rigveda...")
        self._import_veda(base_path / "Rigveda", "Rigveda", "rigveda", "mandala")
        
        # Import Yajurveda
        print("Importing Yajurveda...")
        self._import_veda(base_path / "Yajurveda", "Yajurveda", "yajurveda", "adhyaya")
        
        # Import Atharvaveda (20 kaandas)
        print("Importing Atharvaveda...")
        self._import_veda(base_path / "AtharvaVeda", "Atharvaveda", "atharvaveda", "kaanda")
        
        # Import Bhagavad Gita
        print("Importing Bhagavad Gita...")
        self._import_gita(base_path / "SrimadBhagvadGita")
        
        # Import Mahabharata
        print("Importing Mahabharata...")
        self._import_epic(base_path / "Mahabharata", "Mahabharata", "parva")
        
        # Import Ramayana
        print("Importing Ramayana...")
        self._import_epic(base_path / "ValmikiRamayana", "Ramayana", "kaanda")
        
        # Import Ramcharitmanas
        print("Importing Ramcharitmanas...")
        self._import_epic(base_path / "Ramcharitmanas", "Ramcharitmanas", "kaanda")
        
        return self.stats
    
    def _import_veda(self, veda_path: Path, text_name: str, veda_key: str, chapter_key: str):
        """Import a Veda from JSON files."""
        # Get text_id
        text_id = self._get_text_id(text_name)
        if not text_id:
            print(f"  Warning: {text_name} not found in database, skipping")
            return
        
        # Find all JSON files
        json_files = sorted(veda_path.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for entry in data:
                    if entry.get('veda') == veda_key:
                        chapter = entry.get(chapter_key, 0)
                        sukta = entry.get('sukta', 0)
                        text = entry.get('text', '')
                        
                        self._insert_verse(text_id, chapter, sukta, text, str(json_file))
                        self.stats['total_imported'] += 1
                
                print(f"  Imported {json_file.name}")
            
            except Exception as e:
                print(f"  Error importing {json_file.name}: {e}")
                self.stats['total_skipped'] += 1
        
        self.stats['by_text'][text_name] = self.stats['total_imported']
    
    def _import_gita(self, gita_path: Path):
        """Import Bhagavad Gita."""
        text_id = self._get_text_id("Bhagavad Gita")
        if not text_id:
            print("  Warning: Bhagavad Gita not found in database, skipping")
            return
        
        json_files = sorted(gita_path.glob("*.json"))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for entry in data:
                    chapter = entry.get('chapter', 0)
                    verse = entry.get('verse', 0)
                    text = entry.get('text', '')
                    
                    self._insert_verse(text_id, chapter, verse, text, str(json_file))
                    self.stats['total_imported'] += 1
                
                print(f"  Imported {json_file.name}")
            
            except Exception as e:
                print(f"  Error importing {json_file.name}: {e}")
                self.stats['total_skipped'] += 1
        
        self.stats['by_text']['Bhagavad Gita'] = self.stats['total_imported']
    
    def _import_epic(self, epic_path: Path, text_name: str, chapter_key: str):
        """Import an epic (Mahabharata, Ramayana, Ramcharitmanas)."""
        text_id = self._get_text_id(text_name)
        if not text_id:
            print(f"  Warning: {text_name} not found in database, skipping")
            return
        
        json_files = sorted(epic_path.glob("**/*.json"), key=lambda x: x.name)
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                for entry in data:
                    chapter = entry.get(chapter_key, 0)
                    verse = entry.get('verse', 0) or entry.get('shloka', 0)
                    text = entry.get('text', '')
                    
                    self._insert_verse(text_id, chapter, verse, text, str(json_file))
                    self.stats['total_imported'] += 1
                
                print(f"  Imported {json_file.name}")
            
            except Exception as e:
                print(f"  Error importing {json_file.name}: {e}")
                self.stats['total_skipped'] += 1
        
        self.stats['by_text'][text_name] = self.stats['total_imported']
    
    def _get_text_id(self, text_name: str) -> int:
        """Get the text_id for a given text name."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM texts WHERE name = ?", (text_name,))
        row = cursor.fetchone()
        return row['id'] if row else None
    
    def _insert_verse(self, text_id: int, chapter: int, verse_number: int, devanagari_text: str, file_path: str = 'unknown'):
        """Insert a single verse into the database."""
        cursor = self.conn.cursor()
        
        try:
            # Create source_texts entry
            cursor.execute("""
                INSERT INTO source_texts 
                (text_id, external_source_id, language, format, file_path, is_original, import_date)
                VALUES (?, ?, 'sanskrit', 'json', ?, TRUE, datetime('now'))
            """, (text_id, self.external_source_id, file_path))
            source_text_id = cursor.lastrowid
            
            # Insert verse
            cursor.execute("""
                INSERT INTO verses 
                (text_id, chapter, verse_number, devanagari, source_text_id)
                VALUES (?, ?, ?, ?, ?)
            """, (text_id, chapter, verse_number, devanagari_text, source_text_id))
            verse_id = cursor.lastrowid
            
            # Initialize reading progress
            cursor.execute("""
                INSERT INTO reading_progress 
                (verse_id, read_status)
                VALUES (?, 'unread')
            """, (verse_id,))
            
            # Commit every 100 verses for safety
            if self.stats['total_imported'] % 100 == 0:
                self.conn.commit()
        
        except sqlite3.IntegrityError:
            # Duplicate verse, skip
            self.stats['total_skipped'] += 1
        except Exception as e:
            print(f"    Error inserting verse {chapter}.{verse_number}: {e}")
            self.stats['total_skipped'] += 1

def main():
    """Execute the import."""
    importer = DharmicDataImporter()
    importer.connect()
    
    dharmic_data_path = "/home/ubuntu/vedic-mastery-study/02_EXTERNAL_SOURCES/DharmicData"
    stats = importer.import_all(dharmic_data_path)
    
    print("\n" + "="*50)
    print("IMPORT COMPLETE")
    print("="*50)
    print(f"Total verses imported: {stats['total_imported']}")
    print(f"Total verses skipped: {stats['total_skipped']}")
    print("\nBreakdown by text:")
    for text, count in stats['by_text'].items():
        print(f"  {text}: {count} verses")
    
    importer.close()

if __name__ == "__main__":
    main()
