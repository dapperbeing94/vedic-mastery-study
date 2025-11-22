#!/usr/bin/env python3
from knowledge_manager import VedicKnowledgeBase

kb = VedicKnowledgeBase()

# Add key concepts from Nasadiya Sukta
concepts = [
    {
        'concept_name': 'Nāsadīya - Neither Being nor Non-Being',
        'sanskrit_term': 'Nāsad/Asat (नासद्/असत्)',
        'definition': 'The primordial state that transcends both existence and non-existence',
        'context': 'RV 10.129.1 - Opening of creation hymn',
        'practical_application': 'Understanding ultimate reality as beyond all dualities and categories'
    },
    {
        'concept_name': 'Tad Ekam - That One',
        'sanskrit_term': 'Tad Ekam (तद् एकम्)',
        'definition': 'The singular, unified absolute reality from which all emerges',
        'context': 'RV 10.129.2 - First positive statement about primordial reality',
        'practical_application': 'Seeking the underlying unity behind all multiplicity; foundation of non-dualism'
    },
    {
        'concept_name': 'Tapas - Cosmic Heat/Austerity',
        'sanskrit_term': 'Tapas (तपस्)',
        'definition': 'The primordial creative energy; spiritual heat that generates manifestation',
        'context': 'RV 10.129.3 - By tapas the One was born',
        'practical_application': 'Spiritual discipline and concentrated will as creative forces'
    },
    {
        'concept_name': 'Kāma - Primordial Desire',
        'sanskrit_term': 'Kāma (काम)',
        'definition': 'The first impulse toward creation; cosmic desire; seed of mind',
        'context': 'RV 10.129.4 - Desire arose in the beginning',
        'practical_application': 'Understanding desire as the fundamental creative impulse; channeling desire toward spiritual goals'
    },
    {
        'concept_name': 'Epistemological Humility',
        'sanskrit_term': 'Ko veda (को वेद - Who knows?)',
        'definition': 'Recognition of the limits of knowledge regarding ultimate origins',
        'context': 'RV 10.129.6-7 - Perhaps even the creator knows not',
        'practical_application': 'Cultivating intellectual humility; embracing mystery; avoiding dogmatism'
    },
    {
        'concept_name': 'Puruṣa - Cosmic Person',
        'sanskrit_term': 'Puruṣa (पुरुष)',
        'definition': 'The primordial cosmic being from whose sacrifice the universe emerges',
        'context': 'RV 10.90 - Entire hymn dedicated to Puruṣa',
        'practical_application': 'Seeing the universe as the body of the divine; recognizing divinity in all'
    },
    {
        'concept_name': 'Mahā-Yajña - Cosmic Sacrifice',
        'sanskrit_term': 'Mahā-Yajña (महायज्ञ)',
        'definition': 'The primordial sacrifice from which creation emerges; sacrifice as cosmic principle',
        'context': 'RV 10.90.6-16 - Creation through sacrifice of Puruṣa',
        'practical_application': 'Life as sacrifice; selfless service; giving for the benefit of all'
    },
    {
        'concept_name': 'Pāda - Quarter Principle',
        'sanskrit_term': 'Pāda (पाद)',
        'definition': 'One-fourth of Puruṣa is manifest; three-fourths remains transcendent',
        'context': 'RV 10.90.3 - All creatures are one-fourth of him',
        'practical_application': 'Understanding that manifest reality is only a fraction of ultimate reality'
    },
    {
        'concept_name': 'Bandhu - Cosmic Correspondence',
        'sanskrit_term': 'Bandhu (बन्धु)',
        'definition': 'The hidden connections between macrocosm and microcosm; kinship of all things',
        'context': 'RV 10.90.13-14 - Universe as body of Puruṣa; RV 10.129.4 - kinship of sat and asat',
        'practical_application': 'Recognizing oneself as microcosm of the universe; self-knowledge as cosmic knowledge'
    }
]

for concept in concepts:
    kb.add_concept("Ṛg Veda", concept)
    print(f"✓ Added concept: {concept['concept_name']}")

# Add key verses
verses = [
    {
        'chapter': 'Book 10, Hymn 129 (Nāsadīya Sūkta)',
        'verse_number': '1',
        'sanskrit_text': 'नासदासीन्नो सदासीत्तदानीं नासीद्रजो नो व्योमा परो यत् । किमावरीवः कुह कस्य शर्मन्नम्भः किमासीद्गहनं गभीरम् ॥',
        'transliteration': 'nāsad āsīn no sad āsīt tadānīṃ nāsīd rajo no vyomā paro yat | kim āvarīvaḥ kuha kasya śarmann ambhaḥ kim āsīd gahanaṃ gabhīram ||',
        'translation': 'Then was not non-existent nor existent: there was no realm of air, no sky beyond it. What covered in, and where? and what gave shelter? Was water there, unfathomed depth of water?',
        'commentary': 'Opens with negation of both being and non-being, establishing primordial state beyond all categories',
        'significance': 'Foundation of apophatic theology and neti-neti method; most famous verse in Rig Veda'
    },
    {
        'chapter': 'Book 10, Hymn 129',
        'verse_number': '2',
        'sanskrit_text': 'न मृत्युरासीदमृतं न तर्हि न रात्र्या अह्न आसीत्प्रकेतः । आनीदवातं स्वधया तदेकं तस्माद्धान्यन्न परः किं चनास ॥',
        'transliteration': 'na mṛtyur āsīd amṛtaṃ na tarhi na rātryā ahna āsīt praketaḥ | ānīd avātaṃ svadhayā tad ekaṃ tasmād dhānyan na paraḥ kiṃ canāsa ||',
        'translation': 'Death was not then, nor was there aught immortal: no sign was there, the day\'s and night\'s divider. That One Thing, breathless, breathed by its own nature: apart from it was nothing whatsoever.',
        'commentary': 'First positive statement: Tad Ekam (That One) - self-sustaining, absolute unity',
        'significance': 'Introduces concept of the One that becomes foundation of Advaita Vedanta'
    },
    {
        'chapter': 'Book 10, Hymn 129',
        'verse_number': '4',
        'sanskrit_text': 'कामस्तदग्रे समवर्तताधि मनसो रेतः प्रथमं यदासीत् । सतो बन्धुमसति निरविन्दन्हृदि प्रतीष्याकवयो मनीषा ॥',
        'transliteration': 'kāmas tad agre samavartatādhi manaso retaḥ prathamaṃ yad āsīt | sato bandhum asati niravindan hṛdi pratīṣyā kavayo manīṣā ||',
        'translation': 'Thereafter rose Desire in the beginning, Desire, the primal seed and germ of Spirit. Sages who searched with their heart\'s thought discovered the existent\'s kinship in the non-existent.',
        'commentary': 'Kāma (desire) as first creative impulse; method of contemplative inquiry',
        'significance': 'Establishes desire as creative principle and heart-based inquiry as method'
    },
    {
        'chapter': 'Book 10, Hymn 129',
        'verse_number': '7',
        'sanskrit_text': 'इयं विसृष्टिर्यत आबभूव यदि वा दधे यदि वा न । यो अस्याध्यक्षः परमे व्योमन्त्सो अङ्ग वेद यदि वा न वेद ॥',
        'transliteration': 'iyaṃ visṛṣṭir yata ābabhūva yadi vā dadhe yadi vā na | yo asyādhyakṣaḥ parame vyoman tso aṅga veda yadi vā na veda ||',
        'translation': 'He, the first origin of this creation, whether he formed it all or did not form it, Whose eye controls this world in highest heaven, he verily knows it, or perhaps he knows not.',
        'commentary': 'Concludes with radical agnosticism: perhaps even the creator knows not',
        'significance': 'Unique in ancient religious literature; epistemological humility; embrace of mystery'
    },
    {
        'chapter': 'Book 10, Hymn 90 (Puruṣa Sūkta)',
        'verse_number': '1',
        'sanskrit_text': 'सहस्रशीर्षा पुरुषः सहस्राक्षः सहस्रपात् । स भूमिं विश्वतो वृत्वात्यतिष्ठद्दशाङुलम् ॥',
        'transliteration': 'sahasraśīrṣā puruṣaḥ sahasrākṣaḥ sahasrapāt | sa bhūmiṃ viśvato vṛtvātyatiṣṭhad daśāṅgulam ||',
        'translation': 'A thousand heads hath Puruṣa, a thousand eyes, a thousand feet. On every side pervading earth he fills a space ten fingers wide.',
        'commentary': 'Opens with description of cosmic person as infinite and all-pervading',
        'significance': 'Establishes universe as body of divine being; foundation of devotional theology'
    },
    {
        'chapter': 'Book 10, Hymn 90',
        'verse_number': '3',
        'sanskrit_text': 'एतावानस्य महिमातो ज्यायांश्च पूरुषः । पादोऽस्य विश्वा भूतानि त्रिपादस्यामृतं दिवि ॥',
        'transliteration': 'etāvān asya mahimāto jyāyāṃśca pūruṣaḥ | pādo\'sya viśvā bhūtāni tripād asyāmṛtaṃ divi ||',
        'translation': 'So mighty is his greatness; yea, greater than this is Puruṣa. All creatures are one-fourth of him, three-fourths eternal life in heaven.',
        'commentary': 'Establishes pāda principle: manifest world is one-fourth, three-fourths transcendent',
        'significance': 'Foundation of immanence-transcendence doctrine; God both in and beyond creation'
    },
    {
        'chapter': 'Book 10, Hymn 90',
        'verse_number': '13-14',
        'sanskrit_text': 'चन्द्रमा मनसो जातश्चक्षोः सूर्यो अजायत । मुखादिन्द्रश्चाग्निश्च प्राणाद्वायुरजायत ॥ नाभ्या आसीदन्तरिक्षं शीर्ष्णो द्यौः समवर्तत । पद्भ्यां भूमिर्दिशः श्रोत्रात्तथा लोकाँ अकल्पयन् ॥',
        'transliteration': 'candrāmā manaso jātaścakṣoḥ sūryo ajāyata | mukhād indraścāgniśca prāṇād vāyur ajāyata || nābhyā āsīd antarikṣaṃ śīrṣṇo dyauḥ samavartata | padbhyāṃ bhūmir diśaḥ śrotrāt tathā lokām̐ akalpayan ||',
        'translation': 'The Moon was gendered from his mind, and from his eye the Sun had birth; Indra and Agni from his mouth were born, and Vāyu from his breath. Forth from his navel came mid-air the sky was fashioned from his head Earth from his feet, and from his ear the regions. Thus they formed the worlds.',
        'commentary': 'Complete cosmic correspondences between body of Puruṣa and elements of universe',
        'significance': 'Foundation of microcosm-macrocosm doctrine; basis of all yoga and tantra'
    }
]

for verse in verses:
    kb.add_verse("Ṛg Veda", verse)
    print(f"✓ Added verse: {verse['chapter']}.{verse['verse_number']}")

# Add Sanskrit terms
terms = [
    {
        'term': 'तद् एकम्',
        'transliteration': 'Tad Ekam',
        'literal_meaning': 'That One',
        'contextual_meaning': 'The singular absolute reality; the primordial unity from which all emerges; proto-Brahman',
        'related_terms': 'Brahman, Ātman, Puruṣa',
        'usage_examples': 'RV 10.129.2 - That One, breathless, breathed by its own nature'
    },
    {
        'term': 'तपस्',
        'transliteration': 'Tapas',
        'literal_meaning': 'Heat, warmth, austerity',
        'contextual_meaning': 'Cosmic creative energy; spiritual discipline; concentrated will; the power that generates manifestation',
        'related_terms': 'Kāma, Śakti, Icchā',
        'usage_examples': 'RV 10.129.3 - By the great power of Tapas was born that Unit'
    },
    {
        'term': 'काम',
        'transliteration': 'Kāma',
        'literal_meaning': 'Desire, wish, longing',
        'contextual_meaning': 'Primordial creative desire; the first impulse toward manifestation; seed of mind',
        'related_terms': 'Icchā, Spanda, Saṅkalpa',
        'usage_examples': 'RV 10.129.4 - Desire arose in the beginning, the primal seed'
    },
    {
        'term': 'पुरुष',
        'transliteration': 'Puruṣa',
        'literal_meaning': 'Person, man, spirit',
        'contextual_meaning': 'Cosmic Person; primordial being; consciousness principle; the divine as person',
        'related_terms': 'Brahman, Ātman, Īśvara',
        'usage_examples': 'RV 10.90 - entire hymn; later Sāṅkhya as consciousness principle'
    },
    {
        'term': 'यज्ञ',
        'transliteration': 'Yajña',
        'literal_meaning': 'Sacrifice, offering, worship',
        'contextual_meaning': 'Cosmic sacrifice; the principle of self-giving that sustains creation; ritual as participation in cosmic order',
        'related_terms': 'Mahā-yajña, Tapas, Tyāga',
        'usage_examples': 'RV 10.90.6-16 - Creation through sacrifice of Puruṣa'
    },
    {
        'term': 'बन्धु',
        'transliteration': 'Bandhu',
        'literal_meaning': 'Kinship, relation, connection',
        'contextual_meaning': 'Hidden correspondences; cosmic connections; microcosm-macrocosm relationship',
        'related_terms': 'Tat tvam asi, Ātman-Brahman',
        'usage_examples': 'RV 10.129.4 - kinship of existent and non-existent; RV 10.90 - body correspondences'
    }
]

for term in terms:
    kb.add_sanskrit_term(term)
    print(f"✓ Added term: {term['term']} ({term['transliteration']})")

print("\n✓ Book 10 philosophical hymns data successfully added!")
kb.close()
