#!/usr/bin/env python3
"""
Clean and optimize the vedic_knowledge.db database.
- Standardize category names
- Remove duplicate entries
- Update data quality
"""

import sqlite3
from datetime import datetime

def clean_database():
    conn = sqlite3.connect('vedic_knowledge.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("DATABASE CLEANING AND OPTIMIZATION")
    print("=" * 80)
    print()
    
    # 1. Standardize category names
    print("1. Standardizing category names...")
    
    category_mappings = {
        # Merge similar categories
        "Yoga": "Yoga Texts",
        "Modern": "Modern Interpretations",
        "Regional": "Regional Literature",
        "Tantra": "Tantric Texts",
        "Ayurveda": "Āyurveda",
        "Purāṇas": "Puranas",
        "Darshanas": "Darśanas (Philosophical Schools)",
        "Bhakti": "Bhakti Literature",
        "Astronomy": "Astronomy and Mathematics",
        "Architecture": "Arts and Sciences",
        "Music": "Arts and Sciences",
        "Performing Arts": "Arts and Sciences",
        "Dharma Shastra": "Dharmasastras",
    }
    
    for old_cat, new_cat in category_mappings.items():
        cursor.execute("UPDATE texts SET category = ? WHERE category = ?", (new_cat, old_cat))
        if cursor.rowcount > 0:
            print(f"  - Merged '{old_cat}' → '{new_cat}' ({cursor.rowcount} texts)")
    
    conn.commit()
    
    # 2. Remove duplicate "not_started" entries that have completed equivalents
    print("\n2. Removing duplicate 'not_started' entries...")
    
    # Get all completed text names
    cursor.execute("SELECT name FROM texts WHERE study_status = 'completed'")
    completed_names = [row[0] for row in cursor.fetchall()]
    
    # Find and remove not_started texts with same names
    removed = 0
    for name in completed_names:
        cursor.execute("""
            DELETE FROM texts 
            WHERE name = ? AND study_status = 'not_started'
        """, (name,))
        if cursor.rowcount > 0:
            removed += cursor.rowcount
    
    print(f"  - Removed {removed} duplicate 'not_started' entries")
    conn.commit()
    
    # 3. Remove truly unnecessary "not_started" entries (from old roadmap)
    print("\n3. Removing outdated 'not_started' entries...")
    
    # These are the old individual Puranas and Upanishads that we studied as groups
    outdated_entries = [
        "Agni Purāṇa", "Bhavishya Purāṇa", "Bhāgavata Purāṇa", "Brahma Purāṇa",
        "Brahmavaivarta Purāṇa", "Brahmāṇḍa Purāṇa", "Garuda Purāṇa", "Kurma Purāṇa",
        "Linga Purāṇa", "Markandeya Purāṇa", "Matsya Purāṇa", "Narada Purāṇa",
        "Padma Purāṇa", "Shiva Purāṇa", "Skanda Purāṇa", "Vamana Purāṇa",
        "Varaha Purāṇa", "Vishnu Purāṇa",
        "Aitareya Upaniṣad", "Bṛhadāraṇyaka Upaniṣad", "Chāndogya Upaniṣad",
        "Kaivalya Upaniṣad", "Kaṭha Upaniṣad", "Kena Upaniṣad", "Maitrāyaṇī Upaniṣad",
        "Muṇḍaka Upaniṣad", "Māṇḍūkya Upaniṣad", "Praśna Upaniṣad",
        "Taittirīya Upaniṣad", "Īśa Upaniṣad", "Śvetāśvatara Upaniṣad",
        "Ṛg Veda", "Yajur Veda (Kṛṣṇa)", "Yajur Veda (Śukla)", "Sāma Veda",
        "Atharva Veda", "Brāhmaṇas", "Āraṇyakas",
        "Nyāya Sūtras", "Pūrva Mīmāṃsā Sūtras", "Sāṅkhya Kārikā",
        "Vaiśeṣika Sūtra", "Yoga Sūtras",
        "Bhagavad Gītā",
        "Apastamba Dharma Sūtra", "Nārada Smṛti", "Yājñavalkya Smṛti",
        "Charaka Samhita", "Sushruta Samhita", "Ashtanga Hridaya",
        "Pañcarātra Samhitās", "Shaiva Agamas", "Shakta Tantras",
        "Chandas (Prosody)", "Jyotiṣa (Astronomy)", "Kalpa (Ritual)",
        "Nirukta (Etymology)", "Vyākaraṇa (Grammar)", "Śikṣā (Phonetics)",
        "Gheranda Samhita", "Goraksha Shataka", "Hatha Yoga Pradipika",
        "Shiva Samhita", "Yoga Vasiṣṭha",
        "Abhinavagupta", "Chaitanya - Achintya Bhedabheda", "Gaṅgeśa",
        "Madhva - Dvaita", "Nimbarka - Dvaitadvaita", "Rāmānuja - Vishishtadvaita",
        "Vallabha - Shuddhadvaita", "Vijnanabhikshu", "Śaṅkara - Advaita Vedanta",
        "Śrīharṣa",
        "Jñāneśvarī", "Ramcharitmanas", "Tevaram & Tirumurai", "Tirukkural",
        "S. Radhakrishnan - Indian Philosophy", "Sri Aurobindo - Secret of the Veda",
        "Sri Aurobindo - Synthesis of Yoga", "Sri Aurobindo - The Life Divine",
        "Swami Sivananda - Major Works", "Swami Vivekananda - Complete Works",
        "Nārada Bhakti Sūtra", "Shandilya Bhakti Sūtra"
    ]
    
    removed_outdated = 0
    for name in outdated_entries:
        cursor.execute("""
            DELETE FROM texts 
            WHERE name = ? AND study_status = 'not_started'
        """, (name,))
        if cursor.rowcount > 0:
            removed_outdated += cursor.rowcount
    
    print(f"  - Removed {removed_outdated} outdated 'not_started' entries")
    conn.commit()
    
    # 4. Update the study_progress table to match texts table
    print("\n4. Synchronizing study_progress table...")
    
    # Get all completed texts
    cursor.execute("SELECT id, name, category FROM texts WHERE study_status = 'completed'")
    completed_texts = cursor.fetchall()
    
    synced = 0
    for text_id, name, category in completed_texts:
        # Check if exists in study_progress
        cursor.execute("SELECT id FROM study_progress WHERE text_name = ?", (name,))
        if not cursor.fetchone():
            # Add to study_progress
            cursor.execute("""
                INSERT INTO study_progress (text_name, status, completion_date)
                VALUES (?, ?, ?)
            """, (name, "completed", datetime.now().strftime("%Y-%m-%d")))
            synced += 1
    
    print(f"  - Synchronized {synced} entries to study_progress")
    conn.commit()
    
    # 5. Final statistics
    print("\n" + "=" * 80)
    print("CLEANING COMPLETE - FINAL STATISTICS")
    print("=" * 80)
    print()
    
    cursor.execute("SELECT COUNT(*) FROM texts")
    total = cursor.fetchone()[0]
    print(f"Total texts: {total}")
    
    cursor.execute("SELECT study_status, COUNT(*) FROM texts GROUP BY study_status")
    for status, count in cursor.fetchall():
        print(f"  - {status}: {count}")
    
    cursor.execute("SELECT COUNT(DISTINCT category) FROM texts")
    categories = cursor.fetchone()[0]
    print(f"\nTotal categories: {categories}")
    
    cursor.execute("SELECT category, COUNT(*) FROM texts GROUP BY category ORDER BY COUNT(*) DESC")
    print("\nTexts by category:")
    for category, count in cursor.fetchall():
        print(f"  - {category}: {count}")
    
    print("\n✅ Database cleaned and optimized!")
    
    conn.close()

if __name__ == "__main__":
    clean_database()
