#!/usr/bin/env python3
"""
Evolve the vedic_knowledge.db database schema for blue belt depth-first study.
Adds new tables and modifies existing ones to support verse-level analysis,
commentaries, themes, and complex cross-referencing.
"""

import sqlite3
from datetime import datetime

def evolve_schema():
    conn = sqlite3.connect('vedic_knowledge.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("EVOLVING DATABASE SCHEMA FOR BLUE BELT")
    print("=" * 80)
    print()
    
    # 1. Add new columns to verses table
    print("1. Evolving 'verses' table...")
    try:
        cursor.execute("ALTER TABLE verses ADD COLUMN word_by_word_analysis TEXT")
        print("  - Added 'word_by_word_analysis' column")
    except sqlite3.OperationalError:
        print("  - 'word_by_word_analysis' column already exists")
    
    try:
        cursor.execute("ALTER TABLE verses ADD COLUMN commentary_summary TEXT")
        print("  - Added 'commentary_summary' column")
    except sqlite3.OperationalError:
        print("  - 'commentary_summary' column already exists")
    
    # 2. Add new columns to concepts table
    print("\n2. Evolving 'concepts' table...")
    try:
        cursor.execute("ALTER TABLE concepts ADD COLUMN etymology TEXT")
        print("  - Added 'etymology' column")
    except sqlite3.OperationalError:
        print("  - 'etymology' column already exists")
    
    try:
        cursor.execute("ALTER TABLE concepts ADD COLUMN philosophical_context TEXT")
        print("  - Added 'philosophical_context' column")
    except sqlite3.OperationalError:
        print("  - 'philosophical_context' column already exists")
    
    try:
        cursor.execute("ALTER TABLE concepts ADD COLUMN practical_application TEXT")
        print("  - Added 'practical_application' column")
    except sqlite3.OperationalError:
        print("  - 'practical_application' column already exists")
    
    # 3. Create commentators table
    print("\n3. Creating 'commentators' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commentators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            school TEXT,
            period TEXT,
            bio TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  - 'commentators' table created")
    
    # 4. Create commentaries table
    print("\n4. Creating 'commentaries' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commentaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            verse_id INTEGER NOT NULL,
            commentator_id INTEGER NOT NULL,
            commentary_text TEXT,
            commentary_analysis TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (commentator_id) REFERENCES commentators(id)
        )
    """)
    print("  - 'commentaries' table created")
    
    # 5. Create themes table
    print("\n5. Creating 'themes' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("  - 'themes' table created")
    
    # 6. Create verse_to_concept junction table
    print("\n6. Creating 'verse_to_concept' junction table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verse_to_concept (
            verse_id INTEGER NOT NULL,
            concept_id INTEGER NOT NULL,
            PRIMARY KEY (verse_id, concept_id),
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (concept_id) REFERENCES concepts(id)
        )
    """)
    print("  - 'verse_to_concept' table created")
    
    # 7. Create verse_to_theme junction table
    print("\n7. Creating 'verse_to_theme' junction table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verse_to_theme (
            verse_id INTEGER NOT NULL,
            theme_id INTEGER NOT NULL,
            PRIMARY KEY (verse_id, theme_id),
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (theme_id) REFERENCES themes(id)
        )
    """)
    print("  - 'verse_to_theme' table created")
    
    # 8. Insert some initial themes
    print("\n8. Inserting initial themes...")
    initial_themes = [
        ("Dharma", "Righteousness, duty, moral law"),
        ("Karma", "Action, causality, the law of cause and effect"),
        ("Moksha", "Liberation, freedom from the cycle of rebirth"),
        ("Atman", "The Self, the eternal soul"),
        ("Brahman", "The Ultimate Reality, the Absolute"),
        ("Yoga", "Union, spiritual discipline, practices for liberation"),
        ("Bhakti", "Devotion, loving devotion to the divine"),
        ("Jnana", "Knowledge, wisdom, spiritual insight"),
        ("Maya", "Illusion, the phenomenal world"),
        ("Samsara", "The cycle of birth, death, and rebirth"),
        ("Renunciation", "Detachment, letting go of worldly attachments"),
        ("Non-dualism", "Advaita, the philosophy of non-duality"),
        ("Sacrifice", "Yajna, ritual offering, selfless action"),
        ("Meditation", "Dhyana, contemplation, focused awareness"),
        ("Ethics", "Moral principles, right conduct")
    ]
    
    for name, description in initial_themes:
        try:
            cursor.execute("INSERT INTO themes (name, description) VALUES (?, ?)", (name, description))
        except sqlite3.IntegrityError:
            pass  # Theme already exists
    
    print(f"  - Inserted {len(initial_themes)} initial themes")
    
    # 9. Insert some initial commentators
    print("\n9. Inserting initial commentators...")
    initial_commentators = [
        ("Adi Shankaracharya", "Advaita Vedanta", "8th century CE", "Founder of Advaita Vedanta, wrote commentaries on Upanishads, Bhagavad Gita, and Brahma Sutras"),
        ("Ramanujacharya", "Vishishtadvaita Vedanta", "11th-12th century CE", "Founder of Vishishtadvaita, wrote Sri Bhashya on Brahma Sutras"),
        ("Madhvacharya", "Dvaita Vedanta", "13th century CE", "Founder of Dvaita, wrote commentaries emphasizing dualism"),
        ("Swami Krishnananda", "Advaita Vedanta", "20th century CE", "Modern Advaita teacher, extensive commentaries on Upanishads"),
        ("Eknath Easwaran", "Universal", "20th century CE", "Modern translator and commentator, accessible interpretations"),
        ("S. Radhakrishnan", "Academic", "20th century CE", "Philosopher and scholar, academic translations and commentaries")
    ]
    
    for name, school, period, bio in initial_commentators:
        try:
            cursor.execute("INSERT INTO commentators (name, school, period, bio) VALUES (?, ?, ?, ?)", 
                         (name, school, period, bio))
        except sqlite3.IntegrityError:
            pass  # Commentator already exists
    
    print(f"  - Inserted {len(initial_commentators)} initial commentators")
    
    # Commit all changes
    conn.commit()
    
    # 10. Verify the schema
    print("\n" + "=" * 80)
    print("SCHEMA EVOLUTION COMPLETE - VERIFICATION")
    print("=" * 80)
    print()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    print(f"Total tables: {len(tables)}")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]}: {count} entries")
    
    print("\n✅ Database schema successfully evolved for blue belt!")
    
    conn.close()

if __name__ == "__main__":
    evolve_schema()
