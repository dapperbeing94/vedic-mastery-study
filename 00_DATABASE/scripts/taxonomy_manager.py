#!/usr/bin/env python3
"""
Taxonomy Manager - Vedic Mastery Study v2.0
Manages the hierarchical classification system for all Vedic content.
"""

import sqlite3
import re
from typing import Dict, List, Tuple, Optional

class TaxonomyManager:
    def __init__(self, db_path: str = "../vedic_knowledge.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def classify_verse(self, text_name: str, chapter: int, verse_number: int, 
                      verse_text: str) -> Tuple[str, float]:
        """
        Classify a verse and return its classification code and confidence score.
        
        Args:
            text_name: Name of the text (e.g., "Brihadaranyaka Upanishad")
            chapter: Chapter number
            verse_number: Verse number
            verse_text: The actual verse text for content analysis
        
        Returns:
            Tuple of (classification_code, confidence_score)
        """
        # Get text metadata
        cursor = self.conn.cursor()
        cursor.execute("SELECT category FROM texts WHERE name = ?", (text_name,))
        row = cursor.fetchone()
        
        if not row:
            return ("0.000.000", 0.0)  # Unknown
        
        category = row['category']
        
        # Map category to taxonomy code
        category_codes = {
            "Vedas": "1",
            "Upanishads": "2",
            "Bhagavad Gita": "3",
            "Brahma Sutras": "4",
            "Itihasas": "5",
            "Puranas": "6",
            "Dharma Shastras": "7",
            "Darshanas": "8",
            "Agamas/Tantras": "9",
            "Stotras/Devotional": "10"
        }
        
        level1 = category_codes.get(category, "0")
        
        # Get subcategory (text-specific)
        level2 = self._get_text_code(text_name, category)
        
        # Get verse-level code (chapter.verse)
        level3 = f"{chapter:03d}"
        level4 = f"{verse_number:03d}"
        
        classification_code = f"{level1}.{level2}.{level3}.{level4}"
        confidence = 1.0  # High confidence for metadata-based classification
        
        return (classification_code, confidence)
    
    def _get_text_code(self, text_name: str, category: str) -> str:
        """Get the 3-digit text code within a category."""
        # Simplified mapping - in production, this would query the taxonomy table
        text_codes = {
            # Upanishads
            "Brihadaranyaka Upanishad": "100",
            "Chandogya Upanishad": "200",
            "Taittiriya Upanishad": "300",
            "Katha Upanishad": "400",
            "Mundaka Upanishad": "500",
            "Mandukya Upanishad": "600",
            # Vedas
            "Rigveda": "100",
            "Yajurveda": "200",
            "Samaveda": "300",
            "Atharvaveda": "400",
            # Itihasas
            "Mahabharata": "100",
            "Ramayana": "200",
            "Ramcharitmanas": "300",
            # Default
            "default": "999"
        }
        
        return text_codes.get(text_name, text_codes["default"])
    
    def detect_classification_conflict(self, verse_id: int) -> Optional[Dict]:
        """
        Check if a verse has classification conflicts.
        
        Returns:
            Dict with conflict details if found, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM verse_classification 
            WHERE verse_id = ?
        """, (verse_id,))
        
        count = cursor.fetchone()['count']
        
        if count > 1:
            return {
                'verse_id': verse_id,
                'conflict_type': 'multiple_classifications',
                'count': count
            }
        
        return None
    
    def log_classification(self, verse_id: int, classification_code: str, 
                          confidence: float, reasoning: str):
        """Log a classification decision with reasoning."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO classification_log 
            (verse_id, classification_code, confidence_score, reasoning, timestamp)
            VALUES (?, ?, ?, ?, datetime('now'))
        """, (verse_id, classification_code, confidence, reasoning))
        self.conn.commit()

def main():
    """Example usage."""
    manager = TaxonomyManager()
    manager.connect()
    
    # Example: Classify a verse from Brihadaranyaka Upanishad
    code, confidence = manager.classify_verse(
        "Brihadaranyaka Upanishad", 
        1, 
        4, 
        "Aham Brahmasmi"
    )
    
    print(f"Classification Code: {code}")
    print(f"Confidence: {confidence}")
    
    manager.close()

if __name__ == "__main__":
    main()
