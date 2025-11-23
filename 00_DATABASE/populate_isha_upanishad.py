#!/usr/bin/env python3
"""
Populate the vedic_knowledge.db database with all 18 verses of the Isha Upanishad.
Includes verse data, concepts, commentaries, and cross-references.
"""

import sqlite3
import json
from datetime import datetime

def populate_isha_upanishad():
    # Load the parallel research data
    with open('/home/ubuntu/isha_upanishad_verse_research.json', 'r') as f:
        data = json.load(f)
    
    conn = sqlite3.connect('vedic_knowledge.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("POPULATING ISHA UPANISHAD DATA")
    print("=" * 80)
    print()
    
    # Get the text_id for Isha Upanishad
    cursor.execute("SELECT id FROM texts WHERE name LIKE '%Isha%Upanishad%' OR name LIKE '%Ishavasya%'")
    result = cursor.fetchone()
    if result:
        text_id = result[0]
        print(f"Found Isha Upanishad with text_id: {text_id}")
    else:
        # Create the text entry if it doesn't exist
        cursor.execute("""
            INSERT INTO texts (name, category, language, approximate_date, tradition, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "Isha Upanishad",
            "Upanishads",
            "Sanskrit",
            "c. 800-400 BCE",
            "Vedic",
            "One of the shortest and most important Upanishads, consisting of 18 verses. Also known as Ishavasya Upanishad."
        ))
        text_id = cursor.lastrowid
        print(f"Created Isha Upanishad entry with text_id: {text_id}")
    
    # Process each verse
    verses_added = 0
    concepts_added = 0
    
    for item in data['results']:
        verse_data = item['output']
        verse_num = verse_data['verse_number']
        
        print(f"\nProcessing Verse {verse_num}...")
        
        # Insert verse into database
        cursor.execute("""
            INSERT INTO verses (
                text_id, verse_number, sanskrit_text, transliteration,
                translation, word_by_word_analysis, commentary_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            text_id,
            int(verse_num),
            verse_data['sanskrit_devanagari'],
            verse_data['sanskrit_iast'],
            verse_data['translation'],
            verse_data['word_by_word'],
            verse_data['commentary_summary']
        ))
        verse_id = cursor.lastrowid
        verses_added += 1
        print(f"  - Added verse {verse_num} (id: {verse_id})")
        
        # Extract and add key concepts
        key_concepts_text = verse_data.get('key_concepts', '')
        if key_concepts_text:
            # Simple extraction of concept names (this is a basic approach)
            # In a more sophisticated version, we would parse more carefully
            concepts = []
            if '**' in key_concepts_text:
                parts = key_concepts_text.split('**')
                for i in range(1, len(parts), 2):
                    concept_name = parts[i].strip()
                    if concept_name and '(' in concept_name:
                        concept_name = concept_name.split('(')[0].strip()
                    if concept_name:
                        concepts.append(concept_name)
            
            for concept_name in concepts[:5]:  # Limit to first 5 concepts per verse
                # Check if concept exists
                cursor.execute("SELECT id FROM concepts WHERE concept_name = ?", (concept_name,))
                result = cursor.fetchone()
                
                if result:
                    concept_id = result[0]
                else:
                    # Create new concept
                    cursor.execute("""
                        INSERT INTO concepts (text_id, concept_name, definition, context)
                        VALUES (?, ?, ?, ?)
                    """, (
                        text_id,
                        concept_name,
                        f"Key concept from Isha Upanishad verse {verse_num}",
                        "Upanishadic Philosophy"
                    ))
                    concept_id = cursor.lastrowid
                    concepts_added += 1
                
                # Link verse to concept
                try:
                    cursor.execute("""
                        INSERT INTO verse_to_concept (verse_id, concept_id)
                        VALUES (?, ?)
                    """, (verse_id, concept_id))
                except sqlite3.IntegrityError:
                    pass  # Already linked
        
        # Link to themes based on content
        theme_keywords = {
            'Dharma': ['dharma', 'duty', 'righteousness'],
            'Karma': ['karma', 'action', 'work'],
            'Moksha': ['moksha', 'liberation', 'freedom'],
            'Atman': ['atman', 'self', 'soul'],
            'Brahman': ['brahman', 'absolute', 'supreme'],
            'Renunciation': ['renunciation', 'tyakta', 'detachment'],
            'Knowledge': ['jnana', 'knowledge', 'wisdom']
        }
        
        verse_content = (verse_data['translation'] + ' ' + 
                        verse_data.get('philosophical_significance', '')).lower()
        
        for theme_name, keywords in theme_keywords.items():
            if any(keyword in verse_content for keyword in keywords):
                cursor.execute("SELECT id FROM themes WHERE name = ?", (theme_name,))
                result = cursor.fetchone()
                if result:
                    theme_id = result[0]
                    try:
                        cursor.execute("""
                            INSERT INTO verse_to_theme (verse_id, theme_id)
                            VALUES (?, ?)
                        """, (verse_id, theme_id))
                    except sqlite3.IntegrityError:
                        pass  # Already linked
    
    # Commit all changes
    conn.commit()
    
    print("\n" + "=" * 80)
    print("POPULATION COMPLETE")
    print("=" * 80)
    print(f"Verses added: {verses_added}")
    print(f"New concepts created: {concepts_added}")
    
    # Verify
    cursor.execute("SELECT COUNT(*) FROM verses WHERE text_id = ?", (text_id,))
    total_verses = cursor.fetchone()[0]
    print(f"Total verses for Isha Upanishad in database: {total_verses}")
    
    conn.close()
    print("\n✅ Isha Upanishad successfully populated in database!")

if __name__ == "__main__":
    populate_isha_upanishad()
