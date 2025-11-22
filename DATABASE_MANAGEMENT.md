# 🗄️ Database Management & Validation Protocol

## Purpose

This document ensures the SQLite database remains clean, validated, and properly maintained across all chat sessions. It provides protocols for sanity checks, data validation, entry management, and database integrity.

---

## Database Overview

**Location**: `database/vedic_knowledge.db`  
**Type**: SQLite 3  
**Purpose**: Persistent storage of all Vedic knowledge - concepts, verses, terms, cross-references

### Database Schema

```sql
-- Texts table: All 96+ texts being studied
CREATE TABLE texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Concepts table: Key philosophical concepts
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER,
    concept_name TEXT NOT NULL,
    sanskrit_term TEXT,
    definition TEXT,
    context TEXT,
    practical_application TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- Verses table: Important verses with Sanskrit
CREATE TABLE verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_text TEXT NOT NULL,
    chapter_verse TEXT,
    verse_id TEXT UNIQUE,
    sanskrit_text TEXT,
    transliteration TEXT,
    translation TEXT,
    commentary TEXT,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sanskrit terms glossary
CREATE TABLE sanskrit_terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term TEXT NOT NULL UNIQUE,
    sanskrit TEXT,
    meaning TEXT,
    source_text TEXT,
    usage_context TEXT
);

-- Cross-references between texts
CREATE TABLE cross_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_text TEXT NOT NULL,
    target_text TEXT NOT NULL,
    relationship TEXT,
    notes TEXT
);

-- Study progress tracking
CREATE TABLE study_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_name TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'not_started',
    start_date DATE,
    completion_date DATE,
    notes TEXT
);
```

---

## 🔍 Sanity Check Protocol

### Run at Start of Every Session

```python
import sqlite3
import os

def sanity_check_database(db_path='database/vedic_knowledge.db'):
    """
    Comprehensive sanity check of the Vedic knowledge database.
    Run this at the start of every session.
    """
    
    print("🔍 Running Database Sanity Check...")
    
    if not os.path.exists(db_path):
        print("❌ ERROR: Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check 1: Database integrity
        c.execute("PRAGMA integrity_check")
        integrity = c.fetchone()[0]
        if integrity == "ok":
            print("✅ Database integrity: OK")
        else:
            print(f"❌ Database integrity issues: {integrity}")
            return False
        
        # Check 2: All tables exist
        required_tables = ['texts', 'concepts', 'verses', 'sanskrit_terms', 
                          'cross_references', 'study_progress']
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in c.fetchall()]
        
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ Table '{table}': exists")
            else:
                print(f"❌ Table '{table}': MISSING")
                return False
        
        # Check 3: Row counts
        for table in required_tables:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"📊 Table '{table}': {count} rows")
        
        # Check 4: Check for completed texts
        c.execute("SELECT COUNT(*) FROM study_progress WHERE status='completed'")
        completed = c.fetchone()[0]
        print(f"✅ Completed texts: {completed}")
        
        # Check 5: Verify key data exists
        c.execute("SELECT COUNT(*) FROM verses WHERE source_text LIKE '%Upanishad%'")
        upanishad_verses = c.fetchone()[0]
        print(f"📖 Upanishad verses: {upanishad_verses}")
        
        c.execute("SELECT COUNT(*) FROM concepts WHERE concept_name='Brahman'")
        brahman_concept = c.fetchone()[0]
        if brahman_concept > 0:
            print("✅ Core concepts present (Brahman found)")
        
        conn.close()
        print("\n✅ Sanity check PASSED - Database is healthy\n")
        return True
        
    except Exception as e:
        print(f"❌ Sanity check FAILED: {str(e)}")
        return False

# Run this at session start
if __name__ == "__main__":
    sanity_check_database()
```

---

## 🧹 Database Cleaning Protocol

### Remove Duplicates and Invalid Entries

```python
def clean_database(db_path='database/vedic_knowledge.db'):
    """
    Clean the database by removing duplicates and invalid entries.
    Run periodically to maintain data quality.
    """
    
    print("🧹 Cleaning Database...")
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Remove duplicate Sanskrit terms
    c.execute("""
        DELETE FROM sanskrit_terms 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM sanskrit_terms 
            GROUP BY term
        )
    """)
    deleted_terms = c.rowcount
    print(f"🗑️  Removed {deleted_terms} duplicate Sanskrit terms")
    
    # Remove duplicate verses
    c.execute("""
        DELETE FROM verses 
        WHERE id NOT IN (
            SELECT MIN(id) 
            FROM verses 
            GROUP BY verse_id
        )
    """)
    deleted_verses = c.rowcount
    print(f"🗑️  Removed {deleted_verses} duplicate verses")
    
    # Remove orphaned concepts (text_id doesn't exist)
    c.execute("""
        DELETE FROM concepts 
        WHERE text_id NOT IN (SELECT id FROM texts)
        AND text_id IS NOT NULL
    """)
    deleted_concepts = c.rowcount
    print(f"🗑️  Removed {deleted_concepts} orphaned concepts")
    
    # Vacuum to reclaim space
    c.execute("VACUUM")
    print("✅ Database vacuumed and optimized")
    
    conn.commit()
    conn.close()
    
    print("✅ Database cleaning complete\n")
```

---

## ✅ Data Validation Protocol

### Validate New Entries Before Adding

```python
def validate_verse_entry(verse_data):
    """
    Validate a verse entry before adding to database.
    
    Args:
        verse_data: dict with keys: source_text, sanskrit_text, 
                    transliteration, translation, commentary
    
    Returns:
        (is_valid, error_message)
    """
    
    required_fields = ['source_text', 'translation']
    
    for field in required_fields:
        if field not in verse_data or not verse_data[field]:
            return False, f"Missing required field: {field}"
    
    # Check Sanskrit text is in Devanagari or empty
    if 'sanskrit_text' in verse_data and verse_data['sanskrit_text']:
        sanskrit = verse_data['sanskrit_text']
        # Basic check: contains Devanagari characters
        if not any('\u0900' <= char <= '\u097F' for char in sanskrit):
            return False, "Sanskrit text should contain Devanagari characters"
    
    # Check transliteration uses IAST
    if 'transliteration' in verse_data and verse_data['transliteration']:
        trans = verse_data['transliteration']
        # Should contain IAST diacritics or be plain ASCII
        # This is a basic check
        if len(trans) == 0:
            return False, "Transliteration is empty"
    
    return True, "Valid"


def validate_concept_entry(concept_data):
    """
    Validate a concept entry before adding to database.
    
    Args:
        concept_data: dict with keys: concept_name, definition, 
                      practical_application
    
    Returns:
        (is_valid, error_message)
    """
    
    required_fields = ['concept_name', 'definition']
    
    for field in required_fields:
        if field not in concept_data or not concept_data[field]:
            return False, f"Missing required field: {field}"
    
    # Check concept name is not empty or just whitespace
    if not concept_data['concept_name'].strip():
        return False, "Concept name cannot be empty"
    
    # Check definition has substance (at least 20 characters)
    if len(concept_data['definition']) < 20:
        return False, "Definition too short (minimum 20 characters)"
    
    return True, "Valid"
```

---

## 📥 Safe Entry Management

### Add Entries with Validation and Error Handling

```python
def safe_add_verse(conn, verse_data):
    """
    Safely add a verse to the database with validation.
    
    Returns:
        (success, message)
    """
    
    # Validate first
    is_valid, error_msg = validate_verse_entry(verse_data)
    if not is_valid:
        return False, f"Validation failed: {error_msg}"
    
    try:
        c = conn.cursor()
        
        # Check for duplicates
        if 'verse_id' in verse_data and verse_data['verse_id']:
            c.execute("SELECT id FROM verses WHERE verse_id = ?", 
                     (verse_data['verse_id'],))
            if c.fetchone():
                return False, f"Verse {verse_data['verse_id']} already exists"
        
        # Insert
        c.execute("""
            INSERT INTO verses 
            (source_text, chapter_verse, verse_id, sanskrit_text, 
             transliteration, translation, commentary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            verse_data.get('source_text'),
            verse_data.get('chapter_verse'),
            verse_data.get('verse_id'),
            verse_data.get('sanskrit_text'),
            verse_data.get('transliteration'),
            verse_data.get('translation'),
            verse_data.get('commentary')
        ))
        
        conn.commit()
        return True, f"Successfully added verse: {verse_data.get('verse_id', 'unnamed')}"
        
    except Exception as e:
        return False, f"Database error: {str(e)}"


def safe_add_concept(conn, concept_data):
    """
    Safely add a concept to the database with validation.
    
    Returns:
        (success, message)
    """
    
    # Validate first
    is_valid, error_msg = validate_concept_entry(concept_data)
    if not is_valid:
        return False, f"Validation failed: {error_msg}"
    
    try:
        c = conn.cursor()
        
        # Check for duplicates
        c.execute("""
            SELECT id FROM concepts 
            WHERE concept_name = ? AND text_id = ?
        """, (concept_data['concept_name'], concept_data.get('text_id')))
        
        if c.fetchone():
            return False, f"Concept '{concept_data['concept_name']}' already exists for this text"
        
        # Insert
        c.execute("""
            INSERT INTO concepts 
            (text_id, concept_name, sanskrit_term, definition, 
             context, practical_application)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            concept_data.get('text_id'),
            concept_data['concept_name'],
            concept_data.get('sanskrit_term'),
            concept_data['definition'],
            concept_data.get('context'),
            concept_data.get('practical_application')
        ))
        
        conn.commit()
        return True, f"Successfully added concept: {concept_data['concept_name']}"
        
    except Exception as e:
        return False, f"Database error: {str(e)}"
```

---

## 🔄 Session Start Protocol

### What to Do at the Beginning of Every Chat Session

```python
#!/usr/bin/env python3
"""
Session Start Protocol
Run this at the beginning of every new chat session.
"""

import sqlite3
import os
from datetime import datetime

def session_start_protocol():
    """
    Complete protocol to run at session start.
    """
    
    print("=" * 70)
    print("🕉️  VEDIC MASTERY - SESSION START PROTOCOL")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Verify repository
    if not os.path.exists('database/vedic_knowledge.db'):
        print("❌ ERROR: Not in vedic-mastery-study repository!")
        print("📥 Please clone: git clone https://github.com/dapperbeing94/vedic-mastery-study.git")
        return False
    
    print("✅ Repository verified")
    
    # Step 2: Run sanity check
    if not sanity_check_database():
        print("❌ Database sanity check failed!")
        return False
    
    # Step 3: Load progress
    conn = sqlite3.connect('database/vedic_knowledge.db')
    c = conn.cursor()
    
    c.execute("""
        SELECT text_name, status, completion_date 
        FROM study_progress 
        WHERE status = 'completed' 
        ORDER BY completion_date
    """)
    completed = c.fetchall()
    
    print("📚 COMPLETED TEXTS:")
    for text, status, date in completed:
        print(f"   ✅ {text} (completed: {date})")
    
    print()
    
    # Step 4: Show next texts
    c.execute("""
        SELECT text_name 
        FROM study_progress 
        WHERE status = 'not_started' 
        ORDER BY id 
        LIMIT 5
    """)
    upcoming = c.fetchall()
    
    print("📖 NEXT IN ROADMAP:")
    for i, (text,) in enumerate(upcoming, 1):
        print(f"   {i}. {text}")
    
    conn.close()
    
    print()
    print("=" * 70)
    print("✅ SESSION START PROTOCOL COMPLETE")
    print("=" * 70)
    print()
    
    return True

if __name__ == "__main__":
    session_start_protocol()
```

---

## 📊 Session End Protocol

### What to Do at the End of Every Chat Session

```python
#!/usr/bin/env python3
"""
Session End Protocol
Run this at the end of every chat session to save progress.
"""

import subprocess
from datetime import datetime

def session_end_protocol(session_summary):
    """
    Complete protocol to run at session end.
    
    Args:
        session_summary: Brief description of what was accomplished
    """
    
    print("=" * 70)
    print("🕉️  VEDIC MASTERY - SESSION END PROTOCOL")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Run database cleaning
    print("🧹 Cleaning database...")
    clean_database()
    
    # Step 2: Git status
    print("📝 Checking for changes...")
    result = subprocess.run(['git', 'status', '--short'], 
                          capture_output=True, text=True)
    if result.stdout:
        print("📄 Modified files:")
        print(result.stdout)
    else:
        print("ℹ️  No changes to commit")
        return
    
    # Step 3: Git add all
    print("➕ Staging changes...")
    subprocess.run(['git', 'add', '.'])
    
    # Step 4: Git commit
    commit_message = f"""Session update: {datetime.now().strftime('%Y-%m-%d')}

{session_summary}

Auto-committed by session end protocol.
"""
    
    print("💾 Committing changes...")
    subprocess.run(['git', 'commit', '-m', commit_message])
    
    # Step 5: Git push
    print("☁️  Pushing to GitHub...")
    result = subprocess.run(['git', 'push', 'origin', 'master'],
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Successfully pushed to GitHub!")
    else:
        print(f"❌ Push failed: {result.stderr}")
        return False
    
    print()
    print("=" * 70)
    print("✅ SESSION END PROTOCOL COMPLETE")
    print("=" * 70)
    print()
    print("🔗 Repository: https://github.com/dapperbeing94/vedic-mastery-study")
    print("🕉️  Om Tat Sat - Until next session")
    print()
    
    return True

# Example usage:
if __name__ == "__main__":
    summary = """
    Completed study of Ramayana
    - Created comprehensive 50-page document
    - Added 15 key verses to database
    - Documented 10 major concepts
    - Updated progress tracking
    """
    session_end_protocol(summary)
```

---

## 🎯 Quick Reference Commands

### For Manus AI to Run at Session Start:

```bash
cd /path/to/vedic-mastery-study
python3 database/session_start_protocol.py
```

### For Manus AI to Run at Session End:

```bash
cd /path/to/vedic-mastery-study
python3 database/session_end_protocol.py "Summary of session accomplishments"
```

### Manual Database Check:

```bash
sqlite3 database/vedic_knowledge.db "PRAGMA integrity_check;"
sqlite3 database/vedic_knowledge.db "SELECT COUNT(*) FROM study_progress WHERE status='completed';"
```

---

## 📋 Database Maintenance Checklist

### Daily (Every Session):
- [ ] Run sanity check at session start
- [ ] Validate all new entries before adding
- [ ] Run cleaning protocol at session end
- [ ] Commit and push changes to GitHub

### Weekly:
- [ ] Review database size and performance
- [ ] Check for orphaned entries
- [ ] Verify all cross-references are valid
- [ ] Backup database separately (optional)

### Monthly:
- [ ] Full database audit
- [ ] Review and update validation rules
- [ ] Optimize queries if needed
- [ ] Document any schema changes

---

## 🚨 Troubleshooting

### Database Corrupted:
```bash
# Check integrity
sqlite3 database/vedic_knowledge.db "PRAGMA integrity_check;"

# If corrupted, restore from GitHub
git checkout HEAD -- database/vedic_knowledge.db
```

### Duplicate Entries:
```bash
# Run cleaning protocol
python3 database/clean_database.py
```

### Missing Tables:
```bash
# Recreate from schema
python3 database/initialize_database.py
```

---

## 📝 Best Practices

1. **Always validate before inserting** - Use validation functions
2. **Check for duplicates** - Query before inserting
3. **Use transactions** - Commit or rollback as a unit
4. **Handle errors gracefully** - Try-except blocks
5. **Log important operations** - Keep audit trail
6. **Regular backups** - Git commits serve as backups
7. **Document changes** - Clear commit messages
8. **Test queries** - Verify before running on production DB

---

## 🔗 Integration with Session Continuity

This database management protocol integrates seamlessly with the session continuity system:

1. **Session Start**: Clone repo → Run sanity check → Load context
2. **During Session**: Validate entries → Safe additions → Document work
3. **Session End**: Clean database → Commit changes → Push to GitHub

This ensures every session maintains database integrity while building on previous work.

---

**Version**: 1.0  
**Last Updated**: November 22, 2025  
**Status**: Active Protocol

🕉️ **Om Tat Sat**
