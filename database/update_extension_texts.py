#!/usr/bin/env python3
"""
Update the vedic_knowledge.db database with the 14 extension texts.
"""

import sqlite3
import json
from datetime import datetime

def update_extension_texts():
    # Connect to the database
    conn = sqlite3.connect('vedic_knowledge.db')
    cursor = conn.cursor()
    
    # Load the parallel research results
    with open("/home/ubuntu/extension_texts_research.json", "r") as f:
        data = json.load(f)
    
    results = data["results"]
    
    # Define the categories
    category_mapping = {
        "shiksha": "Vedangas",
        "chandas": "Vedangas",
        "vyakarana": "Vedangas",
        "ashtadhyayi": "Vedangas",
        "nirukta": "Vedangas",
        "kalpa": "Vedangas",
        "jyotisha": "Vedangas",
        "surya siddhanta": "Astronomy and Mathematics",
        "aryabhatiya": "Astronomy and Mathematics",
        "brahmasphutasiddhanta": "Astronomy and Mathematics",
        "narada bhakti sutra": "Bhakti Sutras",
        "shandilya bhakti sutra": "Bhakti Sutras",
        "natya shastra": "Arts and Sciences",
        "sangita ratnakara": "Arts and Sciences",
        "vastu shastra": "Arts and Sciences"
    }
    
    # Process each result
    added_count = 0
    for result in results:
        text_data = result["output"]
        text_name = text_data["text_name"]
        input_text = result["input"].lower()
        
        # Determine category
        category = "Vedangas"  # default
        for keyword, cat in category_mapping.items():
            if keyword in input_text:
                category = cat
                break
        
        # Check if text already exists
        cursor.execute("SELECT id FROM texts WHERE name = ?", (text_name,))
        existing = cursor.fetchone()
        
        if not existing:
            # Insert the text
            cursor.execute("""
                INSERT INTO texts (name, category, study_status, study_date)
                VALUES (?, ?, ?, ?)
            """, (text_name, category, "completed", datetime.now().strftime("%Y-%m-%d")))
            added_count += 1
            print(f"Added: {text_name} ({category})")
        else:
            print(f"Already exists: {text_name}")
    
    # Commit changes
    conn.commit()
    
    # Verify the total count
    cursor.execute("SELECT COUNT(*) FROM texts WHERE study_status = 'completed'")
    total = cursor.fetchone()[0]
    
    print(f"\n✅ Database update complete!")
    print(f"Added {added_count} new texts")
    print(f"Total completed texts in database: {total}")
    
    conn.close()

if __name__ == "__main__":
    update_extension_texts()
