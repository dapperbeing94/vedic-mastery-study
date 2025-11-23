#!/usr/bin/env python3
"""
Update the vedic_knowledge.db database with the 25 texts from Session 3.
"""

import sqlite3
import json
from datetime import datetime

def update_database():
    conn = sqlite3.connect('/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db')
    cursor = conn.cursor()
    
    # Load the parallel research results
    with open('/home/ubuntu/vedic_texts_parallel_research.json', 'r') as f:
        data = json.load(f)
    
    results = data['results']
    
    # Define the categories
    categories = {
        "Yoga Texts": ["Hatha Yoga Pradipika", "Yoga Vasistha", "Gheranda Samhita", "Shiva Samhita", "Goraksha Shataka"],
        "Commentaries": ["Shankaracharya", "Ramanuja", "Madhvacharya", "Nimbarka", "Vallabhacharya", "Chaitanya", "Abhinavagupta", "Gangesha", "Sriharsha", "Vijnanabhikshu"],
        "Regional Literature": ["Ramcharitmanas", "Jnanesvari", "Tirukkural", "Tevaram"],
        "Modern Interpretations": ["Vivekananda", "Aurobindo", "Sivananda", "Radhakrishnan"]
    }
    
    texts_added = 0
    texts_skipped = 0
    
    # Process each result
    for result in results:
        text_data = result['output']
        text_name = text_data['text_name']
        
        # Check if text already exists
        cursor.execute('SELECT id FROM texts WHERE name = ?', (text_name,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"Skipping {text_name} - already exists in database")
            texts_skipped += 1
            continue
        
        # Determine category
        category = "Uncategorized"
        for cat, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in text_name.lower() or keyword.lower() in result['input'].lower():
                    category = cat
                    break
            if category != "Uncategorized":
                break
        
        # Determine file path based on category
        file_path_map = {
            "Yoga Texts": "/home/ubuntu/vedic-mastery-study/study_documents_session3/yoga_texts_comprehensive.md",
            "Commentaries": "/home/ubuntu/vedic-mastery-study/study_documents_session3/commentaries_comprehensive.md",
            "Regional Literature": "/home/ubuntu/vedic-mastery-study/study_documents_session3/regional_literature_comprehensive.md",
            "Modern Interpretations": "/home/ubuntu/vedic-mastery-study/study_documents_session3/modern_interpretations_comprehensive.md"
        }
        
        # Insert into texts table
        cursor.execute('''
            INSERT INTO texts (name, category, subcategory, approximate_date, tradition, 
                             study_status, study_date, file_path, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            text_name,
            category,
            '',
            text_data.get('historical_period', ''),
            text_data.get('author_tradition', ''),
            'completed',
            datetime.now().strftime('%Y-%m-%d'),
            file_path_map.get(category, ''),
            f"Session 3 - Completed using parallel wide research on {datetime.now().strftime('%Y-%m-%d')}"
        ))
        
        text_id = cursor.lastrowid
        texts_added += 1
        
        # Insert key concepts
        key_concepts = text_data.get('key_concepts', '')
        if key_concepts:
            cursor.execute('''
                INSERT INTO concepts (text_id, concept_name, sanskrit_term, definition, context, practical_application)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                text_id,
                f"Core Concepts of {text_name}",
                '',
                key_concepts,
                text_data.get('core_teachings', ''),
                text_data.get('practical_applications', '')
            ))
        
        # Insert key verses
        key_verses = text_data.get('key_verses', '')
        if key_verses:
            cursor.execute('''
                INSERT INTO verses (text_id, chapter, verse_number, sanskrit_text, transliteration, translation, commentary, significance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                text_id,
                '',
                'Key Passages',
                '',
                '',
                key_verses,
                text_data.get('core_teachings', ''),
                text_data.get('cross_references', '')
            ))
        
        # Update study_progress table
        cursor.execute('''
            INSERT INTO study_progress (text_name, status, start_date, completion_date, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            text_name,
            'completed',
            datetime.now().strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d'),
            f"Completed in Session 3 using parallel wide research. Study document: {file_path_map.get(category, '')}"
        ))
    
    conn.commit()
    conn.close()
    print(f"\n✅ Database update complete!")
    print(f"   - Texts added: {texts_added}")
    print(f"   - Texts skipped (already exist): {texts_skipped}")
    print(f"   - Total processed: {len(results)}")

if __name__ == "__main__":
    update_database()
