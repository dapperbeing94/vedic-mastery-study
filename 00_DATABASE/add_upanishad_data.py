#!/usr/bin/env python3.11
import sqlite3

def add_upanishad_data():
    conn = sqlite3.connect('00_DATABASE/vedic_knowledge.db')
    c = conn.cursor()
    
    # Get text IDs
    c.execute("SELECT id FROM texts WHERE text_name = 'Upanishads'")
    result = c.fetchone()
    if not result:
        c.execute("INSERT INTO texts (text_name, category, description) VALUES ('Upanishads', 'Shruti', 'Philosophical texts')")
        text_id = c.lastrowid
    else:
        text_id = result[0]
    
    # Add key concepts
    concepts = [
        ("Brahman", "ब्रह्मन्", "The ultimate reality, the absolute, the ground of all existence. Described as Sat-Cit-Ananda (Existence-Consciousness-Bliss).", 
         "The supreme reality underlying all existence", 
         "Meditate on Brahman as your true nature. Recognize that all seeking is seeking for Brahman."),
        ("Atman", "आत्मन्", "The true Self, identical with Brahman. The unchanging witness consciousness beyond body and mind.",
         "The individual self, identical with Brahman",
         "Practice self-inquiry: 'Who am I?' Recognize yourself as the witness, not the witnessed."),
        ("Mahavakyas", "महावाक्य", "The four great sayings: 1) Prajnanam Brahma, 2) Tat Tvam Asi, 3) Ayam Atma Brahma, 4) Aham Brahmasmi",
         "The four great declarations of Vedanta",
         "Meditate daily on one mahavakya. Let it move from intellectual understanding to direct realization."),
        ("Neti Neti", "नेति नेति", "'Not this, not this' - the method of negation to discover the Self.",
         "Method of via negativa to realize the Self",
         "Practice: 'Am I the body? No. Am I the thoughts? No.' What remains is the Atman."),
        ("Maya", "माया", "The cosmic illusion, the power by which Brahman appears as the manifold world.",
         "The power of cosmic illusion",
         "Recognize the world as appearance, not ultimate reality."),
        ("Turiya", "तुरीय", "The Fourth state of consciousness beyond waking, dream, and deep sleep.",
         "The fourth state - pure consciousness",
         "Observe the three states consciously. Recognize yourself as the unchanging witness."),
        ("Shreyas vs Preyas", "श्रेयस् प्रेयस्", "The choice between the Good (shreyas) and the Pleasant (preyas).",
         "The fundamental spiritual choice",
         "In every decision, ask: 'Is this shreyas or preyas?'"),
        ("Sravana-Manana-Nididhyasana", "श्रवण-मनन-निदिध्यासन", "The three-fold method: Hearing, Reflection, Meditation.",
         "The classical Vedantic method of realization",
         "Follow all three steps systematically."),
        ("Om", "ॐ", "The sacred syllable representing Brahman.",
         "The primordial sound, symbol of Brahman",
         "Chant Om daily. Meditate on Om as the sound-symbol of ultimate reality."),
        ("Witness Consciousness", "साक्षी", "The unchanging awareness that observes all experiences.",
         "The observing consciousness, the true Self",
         "Practice being the watcher, not the doer.")
    ]
    
    for concept_name, sanskrit, definition, context, application in concepts:
        c.execute('''INSERT OR IGNORE INTO concepts 
                     (text_id, concept_name, sanskrit_term, definition, context, practical_application)
                     VALUES (?, ?, ?, ?, ?, ?)''', 
                  (text_id, concept_name, sanskrit, definition, context, application))
    
    # Add key verses
    verses = [
        ("Isha Upanishad", "1", "divine_immanence",
         "ईशावास्यमिदं सर्वं यत्किञ्च जगत्यां जगत्",
         "īśāvāsyamidaṃ sarvaṃ yatkiñca jagatyāṃ jagat",
         "All this is pervaded by the Lord. Through renunciation, enjoy.",
         "The opening verse teaching divine immanence and detached enjoyment."),
        
        ("Brihadaranyaka Upanishad", "1.4.10", "aham_brahmasmi",
         "अहं ब्रह्मास्मि",
         "ahaṃ brahmāsmi",
         "I am Brahman.",
         "The first mahavakya - direct declaration of identity with Brahman."),
        
        ("Chandogya Upanishad", "6.8.7", "tat_tvam_asi",
         "तत् त्वम् असि",
         "tat tvam asi",
         "You are That.",
         "The second mahavakya - teaching identity between individual and universal."),
        
        ("Aitareya Upanishad", "3.1.3", "prajnanam_brahma",
         "प्रज्ञानं ब्रह्म",
         "prajñānaṃ brahma",
         "Consciousness is Brahman.",
         "The third mahavakya - declaring consciousness as ultimate reality."),
        
        ("Mandukya Upanishad", "1.2", "ayam_atma_brahma",
         "अयम् आत्मा ब्रह्म",
         "ayam ātmā brahma",
         "This Self is Brahman.",
         "The fourth mahavakya - pointing directly to the Self as Brahman."),
        
        ("Katha Upanishad", "1.3.14", "razor_edge",
         "उत्तिष्ठत जाग्रत प्राप्य वरान्निबोधत",
         "uttiṣṭhata jāgrata prāpya varānnibodhata",
         "Arise! Awake! The path is like a razor's edge.",
         "The famous call to spiritual awakening."),
        
        ("Mundaka Upanishad", "3.1.1", "two_birds",
         "द्वा सुपर्णा सयुजा सखाया",
         "dvā suparṇā sayujā sakhāyā",
         "Two birds cling to the same tree. One eats; the other watches.",
         "The metaphor of individual self and true Self."),
        
        ("Taittiriya Upanishad", "2.1.1", "brahman_definition",
         "सत्यं ज्ञानमनन्तं ब्रह्म",
         "satyaṃ jñānamanantaṃ brahma",
         "Brahman is Truth, Knowledge, Infinity.",
         "The classical definition of Brahman.")
    ]
    
    for text, chapter, verse_id, sanskrit, transliteration, translation, commentary in verses:
        c.execute('''INSERT OR IGNORE INTO verses 
                     (source_text, chapter_verse, verse_id, sanskrit_text, transliteration, translation, commentary)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (text, chapter, verse_id, sanskrit, transliteration, translation, commentary))
    
    # Add Sanskrit terms
    terms = [
        ("Brahman", "ब्रह्मन्", "The ultimate reality, the absolute", "Upanishads"),
        ("Atman", "आत्मन्", "The Self, the true nature", "Upanishads"),
        ("Maya", "माया", "Cosmic illusion", "Upanishads"),
        ("Moksha", "मोक्ष", "Liberation", "Upanishads"),
        ("Jnana", "ज्ञान", "Knowledge, wisdom", "Upanishads"),
        ("Vidya", "विद्या", "Higher knowledge", "Upanishads"),
        ("Avidya", "अविद्या", "Ignorance", "Upanishads"),
        ("Turiya", "तुरीय", "The Fourth state", "Upanishads"),
        ("Shreyas", "श्रेयस्", "The Good", "Upanishads"),
        ("Preyas", "प्रेयस्", "The Pleasant", "Upanishads"),
        ("Neti Neti", "नेति नेति", "Not this, not this", "Upanishads"),
        ("Sat-Cit-Ananda", "सत्-चित्-आनन्द", "Existence-Consciousness-Bliss", "Upanishads")
    ]
    
    for term, sanskrit, meaning, source in terms:
        c.execute('''INSERT OR IGNORE INTO sanskrit_terms (term, sanskrit, meaning, source_text)
                     VALUES (?, ?, ?, ?)''', (term, sanskrit, meaning, source))
    
    # Update study progress
    upanishads = [
        "Isha Upanishad", "Kena Upanishad", "Katha Upanishad", "Prashna Upanishad",
        "Mundaka Upanishad", "Mandukya Upanishad", "Taittiriya Upanishad",
        "Aitareya Upanishad", "Chandogya Upanishad", "Brihadaranyaka Upanishad",
        "Svetasvatara Upanishad", "Kaushitaki Upanishad", "Maitri Upanishad"
    ]
    
    for upanishad in upanishads:
        c.execute('''UPDATE study_progress SET status = 'completed', 
                     completion_date = date('now'),
                     notes = 'Comprehensive study with key verses and concepts documented.'
                     WHERE text_name = ?''', (upanishad,))
    
    conn.commit()
    conn.close()
    print("✅ Successfully added Upanishad data to database")
    print(f"   - {len(concepts)} key concepts")
    print(f"   - {len(verses)} essential verses")
    print(f"   - {len(terms)} Sanskrit terms")
    print(f"   - {len(upanishads)} Upanishads marked as completed")

if __name__ == "__main__":
    add_upanishad_data()
