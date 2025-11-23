#!/usr/bin/env python3
"""
Vedic Knowledge Base Manager
Manages the systematic study, storage, and retrieval of Hindu Vedic texts
"""

import sqlite3
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class VedicKnowledgeBase:
    """Database manager for Vedic knowledge corpus"""
    
    def __init__(self, db_path: str = "/home/ubuntu/vedic_mastery/database/vedic_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database schema for storing Vedic knowledge"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # Main texts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                subcategory TEXT,
                language TEXT,
                approximate_date TEXT,
                tradition TEXT,
                source_url TEXT,
                study_status TEXT DEFAULT 'not_started',
                study_date TEXT,
                file_path TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Key concepts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id INTEGER,
                concept_name TEXT NOT NULL,
                sanskrit_term TEXT,
                definition TEXT,
                context TEXT,
                practical_application TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            )
        """)
        
        # Verses/passages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id INTEGER,
                chapter TEXT,
                verse_number TEXT,
                sanskrit_text TEXT,
                transliteration TEXT,
                translation TEXT,
                commentary TEXT,
                significance TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            )
        """)
        
        # Cross-references table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cross_references (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_text_id INTEGER,
                target_text_id INTEGER,
                connection_type TEXT,
                description TEXT,
                FOREIGN KEY (source_text_id) REFERENCES texts(id),
                FOREIGN KEY (target_text_id) REFERENCES texts(id)
            )
        """)
        
        # Sanskrit glossary table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sanskrit_glossary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                term TEXT NOT NULL UNIQUE,
                transliteration TEXT,
                literal_meaning TEXT,
                contextual_meaning TEXT,
                related_terms TEXT,
                usage_examples TEXT
            )
        """)
        
        # Study progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS study_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id INTEGER,
                milestone TEXT,
                completed BOOLEAN DEFAULT 0,
                completion_date TEXT,
                notes TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            )
        """)
        
        self.conn.commit()
        print(f"Database initialized at: {self.db_path}")
    
    def add_text(self, name: str, category: str, **kwargs) -> int:
        """Add a new text to the database"""
        cursor = self.conn.cursor()
        
        fields = ['name', 'category']
        values = [name, category]
        
        for key, value in kwargs.items():
            if value is not None:
                fields.append(key)
                values.append(value)
        
        placeholders = ', '.join(['?' for _ in values])
        field_names = ', '.join(fields)
        
        cursor.execute(f"""
            INSERT INTO texts ({field_names})
            VALUES ({placeholders})
        """, values)
        
        self.conn.commit()
        return cursor.lastrowid
    
    def update_text_status(self, text_name: str, status: str, notes: str = None):
        """Update the study status of a text"""
        cursor = self.conn.cursor()
        update_fields = ['study_status = ?', 'study_date = ?', 'updated_at = ?']
        values = [status, datetime.now().isoformat(), datetime.now().isoformat()]
        
        if notes:
            update_fields.append('notes = ?')
            values.append(notes)
        
        values.append(text_name)
        
        cursor.execute(f"""
            UPDATE texts 
            SET {', '.join(update_fields)}
            WHERE name = ?
        """, values)
        
        self.conn.commit()
    
    def add_concept(self, text_name: str, concept_data: Dict):
        """Add a key concept from a text"""
        cursor = self.conn.cursor()
        
        # Get text_id
        cursor.execute("SELECT id FROM texts WHERE name = ?", (text_name,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Text '{text_name}' not found in database")
        
        text_id = result[0]
        
        cursor.execute("""
            INSERT INTO concepts (text_id, concept_name, sanskrit_term, definition, context, practical_application)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            text_id,
            concept_data.get('concept_name'),
            concept_data.get('sanskrit_term'),
            concept_data.get('definition'),
            concept_data.get('context'),
            concept_data.get('practical_application')
        ))
        
        self.conn.commit()
    
    def add_verse(self, text_name: str, verse_data: Dict):
        """Add a verse or passage from a text"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM texts WHERE name = ?", (text_name,))
        result = cursor.fetchone()
        if not result:
            raise ValueError(f"Text '{text_name}' not found in database")
        
        text_id = result[0]
        
        cursor.execute("""
            INSERT INTO verses (text_id, chapter, verse_number, sanskrit_text, 
                              transliteration, translation, commentary, significance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            text_id,
            verse_data.get('chapter'),
            verse_data.get('verse_number'),
            verse_data.get('sanskrit_text'),
            verse_data.get('transliteration'),
            verse_data.get('translation'),
            verse_data.get('commentary'),
            verse_data.get('significance')
        ))
        
        self.conn.commit()
    
    def add_cross_reference(self, source_text: str, target_text: str, 
                           connection_type: str, description: str):
        """Add a cross-reference between texts"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT id FROM texts WHERE name = ?", (source_text,))
        source_id = cursor.fetchone()[0]
        
        cursor.execute("SELECT id FROM texts WHERE name = ?", (target_text,))
        target_id = cursor.fetchone()[0]
        
        cursor.execute("""
            INSERT INTO cross_references (source_text_id, target_text_id, connection_type, description)
            VALUES (?, ?, ?, ?)
        """, (source_id, target_id, connection_type, description))
        
        self.conn.commit()
    
    def add_sanskrit_term(self, term_data: Dict):
        """Add a Sanskrit term to the glossary"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO sanskrit_glossary 
            (term, transliteration, literal_meaning, contextual_meaning, related_terms, usage_examples)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            term_data.get('term'),
            term_data.get('transliteration'),
            term_data.get('literal_meaning'),
            term_data.get('contextual_meaning'),
            term_data.get('related_terms'),
            term_data.get('usage_examples')
        ))
        
        self.conn.commit()
    
    def get_text_info(self, text_name: str) -> Optional[Dict]:
        """Retrieve information about a specific text"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM texts WHERE name = ?", (text_name,))
        result = cursor.fetchone()
        
        if result:
            return dict(result)
        return None
    
    def get_all_texts_by_category(self, category: str) -> List[Dict]:
        """Get all texts in a specific category"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM texts WHERE category = ? ORDER BY name", (category,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_study_progress(self) -> Dict:
        """Get overall study progress statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT 
                category,
                COUNT(*) as total,
                SUM(CASE WHEN study_status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN study_status = 'in_progress' THEN 1 ELSE 0 END) as in_progress
            FROM texts
            GROUP BY category
        """)
        
        results = cursor.fetchall()
        progress = {}
        
        for row in results:
            progress[row[0]] = {
                'total': row[1],
                'completed': row[2],
                'in_progress': row[3],
                'percentage': (row[2] / row[1] * 100) if row[1] > 0 else 0
            }
        
        return progress
    
    def search_concepts(self, search_term: str) -> List[Dict]:
        """Search for concepts across all texts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.*, t.name as text_name
            FROM concepts c
            JOIN texts t ON c.text_id = t.id
            WHERE c.concept_name LIKE ? OR c.sanskrit_term LIKE ? OR c.definition LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def search_verses(self, search_term: str) -> List[Dict]:
        """Search for verses across all texts"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT v.*, t.name as text_name
            FROM verses v
            JOIN texts t ON v.text_id = t.id
            WHERE v.sanskrit_text LIKE ? OR v.translation LIKE ? OR v.commentary LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def export_to_json(self, output_path: str):
        """Export entire database to JSON"""
        cursor = self.conn.cursor()
        
        export_data = {
            'texts': [],
            'concepts': [],
            'verses': [],
            'cross_references': [],
            'sanskrit_glossary': []
        }
        
        for table in export_data.keys():
            cursor.execute(f"SELECT * FROM {table}")
            export_data[table] = [dict(row) for row in cursor.fetchall()]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"Database exported to: {output_path}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    """Initialize the knowledge base"""
    kb = VedicKnowledgeBase()
    print("Vedic Knowledge Base initialized successfully!")
    print(f"Database location: {kb.db_path}")
    
    # Test the database
    progress = kb.get_study_progress()
    print(f"\nCurrent study progress: {progress}")
    
    kb.close()

if __name__ == "__main__":
    main()
