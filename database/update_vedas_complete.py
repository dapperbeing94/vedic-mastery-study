#!/usr/bin/env python3
import sqlite3

db_path = "/home/ubuntu/vedic_mastery/database/vedic_knowledge.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update all Four Vedas as completed
vedas = ["Ṛg Veda", "Yajur Veda", "Sāma Veda", "Atharva Veda"]

for veda in vedas:
    cursor.execute("""
        UPDATE texts 
        SET study_status = 'completed',
            notes = 'Comprehensive study completed with key concepts, verses, and practical applications documented'
        WHERE title = ?
    """, (veda,))
    print(f"✓ Marked {veda} as completed")

conn.commit()

# Add key concepts
from knowledge_manager import VedicKnowledgeBase
kb = VedicKnowledgeBase()

concepts = [
    {
        'text_name': 'Yajur Veda',
        'concept_name': 'Yajña-Vidhi - Ritual Precision',
        'sanskrit_term': 'Yajña-Vidhi (यज्ञ-विधि)',
        'definition': 'The precise methodology of ritual performance; every action must be exact',
        'context': 'Central principle of Yajur Veda',
        'practical_application': 'Discipline and precision in spiritual practice; attention to details'
    },
    {
        'text_name': 'Sāma Veda',
        'concept_name': 'Nāda Brahman - Sound as Ultimate Reality',
        'sanskrit_term': 'Nāda Brahman (नाद ब्रह्मन्)',
        'definition': 'The universe emerged from primordial sound; sound is fundamental reality',
        'context': 'Core teaching of Sāma Veda',
        'practical_application': 'Mantra yoga, sound healing, conscious listening, music as spiritual practice'
    },
    {
        'text_name': 'Atharva Veda',
        'concept_name': 'Prāṇa - Vital Life Force',
        'sanskrit_term': 'Prāṇa (प्राण)',
        'definition': 'The vital breath; universal life force; supreme principle underlying all existence',
        'context': 'Prāṇa Sūkta (AV 10.2)',
        'practical_application': 'Prāṇāyāma (breath control), prāṇa healing, understanding subtle energy'
    }
]

for concept in concepts:
    kb.add_concept(concept['text_name'], {k: v for k, v in concept.items() if k != 'text_name'})
    print(f"✓ Added concept: {concept['concept_name']}")

print("\n" + "="*50)
print("FOUR VEDAS STUDY COMPLETED!")
print("="*50)
print("\nSummary:")
print("- Ṛg Veda: Hymns of praise and cosmic vision")
print("- Yajur Veda: Ritual formulas and precise action")
print("- Sāma Veda: Melodies and devotional chanting")
print("- Atharva Veda: Practical magic and holistic wisdom")
print("\nReady to proceed to Upaniṣads study!")

kb.close()
conn.close()
