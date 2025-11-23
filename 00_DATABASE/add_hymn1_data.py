#!/usr/bin/env python3
"""Add Hymn I data to the knowledge base"""

from knowledge_manager import VedicKnowledgeBase

kb = VedicKnowledgeBase()

# Update Rig Veda status
kb.update_text_status("Ṛg Veda", "in_progress", "Started with Book 1, Hymn I")

# Add key concepts from Hymn I
concepts = [
    {
        'concept_name': 'Agni as Divine Mediator',
        'sanskrit_term': 'Agni (अग्नि)',
        'definition': 'Fire deity who serves as the mediator between heaven and earth, carrying offerings from humans to gods',
        'context': 'RV 1.1 - Opening hymn establishes Agni as the chosen priest',
        'practical_application': 'Represents the principle of consciousness that bridges material and spiritual realms'
    },
    {
        'concept_name': 'Hotar - The Invoking Priest',
        'sanskrit_term': 'Hotar (होतर्)',
        'definition': 'The priest who recites Ṛg Vedic verses during sacrifice',
        'context': 'RV 1.1.1 - Agni is called the hotar',
        'practical_application': 'Symbolizes the voice of invocation and the power of sacred speech'
    },
    {
        'concept_name': 'Ṛta - Cosmic Order',
        'sanskrit_term': 'Ṛta (ऋत)',
        'definition': 'The fundamental cosmic order, truth, and natural law that governs the universe',
        'context': 'RV 1.1.8 - Agni is the guardian of ṛta',
        'practical_application': 'Living in harmony with natural and moral law; alignment with truth'
    },
    {
        'concept_name': 'Satya-dharman',
        'sanskrit_term': 'Satya-dharman (सत्यधर्मन्)',
        'definition': 'One whose law is truth; truthful nature',
        'context': 'RV 1.1.5 - Describes Agni as embodiment of truth',
        'practical_application': 'Practice of absolute truthfulness in thought, word, and deed'
    },
    {
        'concept_name': 'Daily Spiritual Practice',
        'sanskrit_term': 'Abhyāsa (अभ्यास)',
        'definition': 'Consistent, repeated practice performed day by day',
        'context': 'RV 1.1.7 - "day by day with prayer"',
        'practical_application': 'Establishing daily spiritual routines for gradual transformation'
    }
]

for concept in concepts:
    kb.add_concept("Ṛg Veda", concept)
    print(f"✓ Added concept: {concept['concept_name']}")

# Add important verses
verses = [
    {
        'chapter': 'Book 1, Hymn 1',
        'verse_number': '1',
        'sanskrit_text': 'अग्निमीळे पुरोहितं यज्ञस्य देवमृत्विजम् । होतारं रत्नधातमम् ॥',
        'transliteration': 'Agnim īḷe purohitaṃ yajñasya devam ṛtvijam | hotāraṃ ratnadhātamam ||',
        'translation': 'I Laud Agni, the chosen Priest, God, minister of sacrifice, The hotar, lavishest of wealth.',
        'commentary': 'The very first verse of the Ṛg Veda establishes Agni as the primary deity and divine priest',
        'significance': 'Opening invocation of the entire Vedic corpus; sets the tone for all Vedic spirituality'
    },
    {
        'chapter': 'Book 1, Hymn 1',
        'verse_number': '5',
        'sanskrit_text': 'अग्ने यं यज्ञमध्वरं विश्वतः परिभूरसि । स इद्देवेषु गच्छति ॥',
        'transliteration': 'Agne yaṃ yajñam adhvaraṃ viśvataḥ paribhūr asi | sa id deveṣu gacchati ||',
        'translation': 'May Agni, sapient-minded Priest, truthful, most gloriously great, The God, come hither with the Gods.',
        'commentary': 'Emphasizes Agni as kavi-kratu (sage-minded) and satya-dharman (truthful)',
        'significance': 'Reveals Agni as cosmic intelligence and embodiment of truth'
    },
    {
        'chapter': 'Book 1, Hymn 1',
        'verse_number': '9',
        'sanskrit_text': 'सुपायनो न एधि सुपितेव । अग्ने स्वस्तये ॥',
        'transliteration': 'Supāyano na edhi supiteva | agne svastaye ||',
        'translation': 'Be to us easy of approach, even as a father to his son: Agni, be with us for our weal.',
        'commentary': 'Closing verse establishes intimate, personal relationship with the divine',
        'significance': 'Shows that Vedic spirituality is not cold philosophy but warm devotion'
    }
]

for verse in verses:
    kb.add_verse("Ṛg Veda", verse)
    print(f"✓ Added verse: {verse['chapter']}.{verse['verse_number']}")

# Add Sanskrit terms to glossary
terms = [
    {
        'term': 'अग्नि',
        'transliteration': 'Agni',
        'literal_meaning': 'Fire',
        'contextual_meaning': 'The fire deity; divine priest; mediator between earth and heaven; cosmic intelligence',
        'related_terms': 'Hotar, Purohita, Jātavedas, Vaiśvānara',
        'usage_examples': 'RV 1.1 - entire hymn dedicated to Agni'
    },
    {
        'term': 'पुरोहित',
        'transliteration': 'Purohita',
        'literal_meaning': 'Placed in front',
        'contextual_meaning': 'The chosen priest; chief priest; one who stands before the gods on behalf of humans',
        'related_terms': 'Hotar, Ṛtvij',
        'usage_examples': 'RV 1.1.1 - Agni as purohita'
    },
    {
        'term': 'होतर्',
        'transliteration': 'Hotar',
        'literal_meaning': 'One who pours oblations; invoker',
        'contextual_meaning': 'The priest who recites Ṛg Vedic mantras during sacrifice',
        'related_terms': 'Adhvaryu, Udgātar, Brahman (priest)',
        'usage_examples': 'RV 1.1.1 - Agni as hotar'
    },
    {
        'term': 'ऋत',
        'transliteration': 'Ṛta',
        'literal_meaning': 'That which is properly joined; order; truth',
        'contextual_meaning': 'Cosmic order; natural law; truth; harmony; the fundamental principle governing the universe',
        'related_terms': 'Satya, Dharma',
        'usage_examples': 'RV 1.1.8 - Agni as guardian of ṛta'
    },
    {
        'term': 'सत्यधर्मन्',
        'transliteration': 'Satya-dharman',
        'literal_meaning': 'One whose law/nature is truth',
        'contextual_meaning': 'Truthful; embodiment of truth; one who upholds truth',
        'related_terms': 'Satya, Ṛta',
        'usage_examples': 'RV 1.1.5 - describes Agni'
    }
]

for term in terms:
    kb.add_sanskrit_term(term)
    print(f"✓ Added term: {term['term']} ({term['transliteration']})")

print("\n✓ Hymn I data successfully added to knowledge base!")
kb.close()
