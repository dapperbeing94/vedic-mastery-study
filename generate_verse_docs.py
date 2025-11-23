#!/usr/bin/env python3
"""
Generate individual markdown files for each verse of the Isha Upanishad
based on the populated database.
"""

import sqlite3
import os

def generate_verse_docs():
    # Connect to the database
    conn = sqlite3.connect("00_DATABASE/vedic_knowledge.db")
    cursor = conn.cursor()
    
    # Get the text_id for Isha Upanishad
    cursor.execute("SELECT id FROM texts WHERE name LIKE '%Isha%Upanishad%'")
    text_id = cursor.fetchone()[0]
    
    # Get all verses for Isha Upanishad
    cursor.execute("SELECT * FROM verses WHERE text_id = ? ORDER BY verse_number", (text_id,))
    verses = cursor.fetchall()
    
    # Create the output directory
    output_dir = "01_STUDY_DOCUMENTS/02_Upanishads/Isha_Upanishad_Verse_Analysis"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 80)
    print("GENERATING ISHA UPANISHAD VERSE DOCUMENTS")
    print("=" * 80)
    print()
    
    for verse in verses:
        verse_id, _, _, verse_num, sanskrit, iast, translation, _, _, word_by_word, commentary_summary = verse
        
        print(f"Generating document for Verse {verse_num}...")
        
        # Get concepts for this verse
        cursor.execute("""
            SELECT c.concept_name
            FROM concepts c
            JOIN verse_to_concept vtc ON c.id = vtc.concept_id
            WHERE vtc.verse_id = ?
        """, (verse_id,))
        concepts = [row[0] for row in cursor.fetchall()]
        
        # Get themes for this verse
        cursor.execute("""
            SELECT t.name
            FROM themes t
            JOIN verse_to_theme vtt ON t.id = vtt.theme_id
            WHERE vtt.verse_id = ?
        """, (verse_id,))
        themes = [row[0] for row in cursor.fetchall()]
        
        # Create the markdown content
        content = f"""# Isha Upanishad - Verse {verse_num}

**Date**: November 22, 2024  
**Status**: ✅ Verse Analysis Complete

---

## 📜 Sanskrit Text

### Devanagari
```
{sanskrit}
```

### IAST Transliteration
```
{iast}
```

---

## 💬 English Translation

> {translation}

---

## 🔬 Word-by-Word Analysis

{word_by_word}

---

## 💭 Commentary Summary

{commentary_summary}

---

## 🔑 Key Concepts

- {" - ".join(concepts) if concepts else "No concepts linked"}

---

## 🎨 Associated Themes

- {" - ".join(themes) if themes else "No themes linked"}

---

## 💡 Philosophical Significance

*This section will be populated with deeper analysis in the next phase.*

---

## 🙏 Practical Application

*This section will be populated with deeper analysis in the next phase.*

---

## 📚 References

*This section will be populated with source URLs from the research phase.*

"""
        
        # Write the file
        file_path = os.path.join(output_dir, f"Verse_{verse_num}.md")
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"  - Created {file_path}")
        
    conn.close()
    print("\n✅ All verse documents generated successfully!")

if __name__ == "__main__":
    generate_verse_docs()
