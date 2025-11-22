#!/usr/bin/env python3
"""
Populate the Vedic Knowledge Base with all texts from the mastery list
"""

from knowledge_manager import VedicKnowledgeBase

def populate_database():
    """Add all texts from the Hindu Vedic mastery list to the database"""
    kb = VedicKnowledgeBase()
    
    print("Populating database with Vedic texts...")
    
    # 1. Core Vedic Foundation (Śruti)
    texts = [
        # Vedas
        ("Ṛg Veda", "Vedas", "vedas", "Sanskrit", "1500-1200 BCE", "Vedic"),
        ("Yajur Veda (Śukla)", "Vedas", "vedas", "Sanskrit", "1200-1000 BCE", "Vedic"),
        ("Yajur Veda (Kṛṣṇa)", "Vedas", "vedas", "Sanskrit", "1200-1000 BCE", "Vedic"),
        ("Sāma Veda", "Vedas", "vedas", "Sanskrit", "1200-1000 BCE", "Vedic"),
        ("Atharva Veda", "Vedas", "vedas", "Sanskrit", "1000-900 BCE", "Vedic"),
        
        # Vedic Literature
        ("Brāhmaṇas", "Vedas", "vedas", "Sanskrit", "900-700 BCE", "Vedic"),
        ("Āraṇyakas", "Vedas", "vedas", "Sanskrit", "800-600 BCE", "Vedic"),
        
        # Upanishads
        ("Īśa Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Kena Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Kaṭha Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Praśna Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Muṇḍaka Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Māṇḍūkya Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Taittirīya Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Aitareya Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Chāndogya Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Bṛhadāraṇyaka Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "800-400 BCE", "Vedic"),
        ("Śvetāśvatara Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "400-200 BCE", "Vedic"),
        ("Kaivalya Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "300-100 BCE", "Vedic"),
        ("Maitrāyaṇī Upaniṣad", "Upanishads", "upanishads", "Sanskrit", "300-100 BCE", "Vedic"),
        
        # Vedangas
        ("Śikṣā (Phonetics)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        ("Chandas (Prosody)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        ("Vyākaraṇa (Grammar)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        ("Nirukta (Etymology)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        ("Kalpa (Ritual)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        ("Jyotiṣa (Astronomy)", "Vedangas", "vedas", "Sanskrit", "800-500 BCE", "Vedic"),
        
        # 2. Smṛti - Epics
        ("Mahābhārata", "Epics", "epics", "Sanskrit", "400 BCE-400 CE", "Itihasa"),
        ("Bhagavad Gītā", "Epics", "epics", "Sanskrit", "200 BCE-200 CE", "Itihasa"),
        ("Rāmāyaṇa", "Epics", "epics", "Sanskrit", "500-100 BCE", "Itihasa"),
        
        # Dharma Shastra
        ("Manu Smṛti", "Dharma Shastra", "epics", "Sanskrit", "200 BCE-200 CE", "Dharma"),
        ("Yājñavalkya Smṛti", "Dharma Shastra", "epics", "Sanskrit", "100-300 CE", "Dharma"),
        ("Nārada Smṛti", "Dharma Shastra", "epics", "Sanskrit", "100-400 CE", "Dharma"),
        ("Apastamba Dharma Sūtra", "Dharma Shastra", "epics", "Sanskrit", "600-300 BCE", "Dharma"),
        
        # 18 Maha Puranas
        ("Bhāgavata Purāṇa", "Puranas", "puranas", "Sanskrit", "500-1000 CE", "Vaishnava"),
        ("Vishnu Purāṇa", "Puranas", "puranas", "Sanskrit", "300-600 CE", "Vaishnava"),
        ("Shiva Purāṇa", "Puranas", "puranas", "Sanskrit", "500-1000 CE", "Shaiva"),
        ("Brahma Purāṇa", "Puranas", "puranas", "Sanskrit", "700-1000 CE", "Brahma"),
        ("Padma Purāṇa", "Puranas", "puranas", "Sanskrit", "750-1000 CE", "Vaishnava"),
        ("Agni Purāṇa", "Puranas", "puranas", "Sanskrit", "800-1100 CE", "Mixed"),
        ("Skanda Purāṇa", "Puranas", "puranas", "Sanskrit", "600-1200 CE", "Shaiva"),
        ("Markandeya Purāṇa", "Puranas", "puranas", "Sanskrit", "250-700 CE", "Mixed"),
        ("Linga Purāṇa", "Puranas", "puranas", "Sanskrit", "500-1000 CE", "Shaiva"),
        ("Kurma Purāṇa", "Puranas", "puranas", "Sanskrit", "600-900 CE", "Vaishnava"),
        ("Matsya Purāṇa", "Puranas", "puranas", "Sanskrit", "250-500 CE", "Mixed"),
        ("Varaha Purāṇa", "Puranas", "puranas", "Sanskrit", "1000-1100 CE", "Vaishnava"),
        ("Vamana Purāṇa", "Puranas", "puranas", "Sanskrit", "900-1100 CE", "Vaishnava"),
        ("Brahmāṇḍa Purāṇa", "Puranas", "puranas", "Sanskrit", "400-600 CE", "Shaiva"),
        ("Brahmavaivarta Purāṇa", "Puranas", "puranas", "Sanskrit", "1000-1500 CE", "Vaishnava"),
        ("Garuda Purāṇa", "Puranas", "puranas", "Sanskrit", "800-1000 CE", "Vaishnava"),
        ("Narada Purāṇa", "Puranas", "puranas", "Sanskrit", "900-1100 CE", "Vaishnava"),
        ("Bhavishya Purāṇa", "Puranas", "puranas", "Sanskrit", "500-1900 CE", "Mixed"),
        
        # 3. Darshanas
        ("Nyāya Sūtras", "Darshanas", "darshanas", "Sanskrit", "200 BCE-100 CE", "Nyaya"),
        ("Vaiśeṣika Sūtra", "Darshanas", "darshanas", "Sanskrit", "200 BCE-100 CE", "Vaisheshika"),
        ("Sāṅkhya Kārikā", "Darshanas", "darshanas", "Sanskrit", "350-450 CE", "Sankhya"),
        ("Yoga Sūtras", "Darshanas", "darshanas", "Sanskrit", "200 BCE-500 CE", "Yoga"),
        ("Pūrva Mīmāṃsā Sūtras", "Darshanas", "darshanas", "Sanskrit", "200 BCE-200 CE", "Mimamsa"),
        ("Brahma Sūtras", "Darshanas", "darshanas", "Sanskrit", "200 BCE-200 CE", "Vedanta"),
        
        # 4. Tantra & Agamas
        ("Shaiva Agamas", "Tantra", "tantras", "Sanskrit", "500-1200 CE", "Shaiva"),
        ("Shakta Tantras", "Tantra", "tantras", "Sanskrit", "500-1500 CE", "Shakta"),
        ("Pañcarātra Samhitās", "Tantra", "tantras", "Sanskrit", "300-1000 CE", "Vaishnava"),
        ("Nārada Bhakti Sūtra", "Bhakti", "tantras", "Sanskrit", "1000-1300 CE", "Bhakti"),
        ("Shandilya Bhakti Sūtra", "Bhakti", "tantras", "Sanskrit", "1000-1400 CE", "Bhakti"),
        
        # 5. Yogic Corpus
        ("Hatha Yoga Pradipika", "Yoga", "yoga", "Sanskrit", "1400-1500 CE", "Hatha Yoga"),
        ("Gheranda Samhita", "Yoga", "yoga", "Sanskrit", "1600-1700 CE", "Hatha Yoga"),
        ("Shiva Samhita", "Yoga", "yoga", "Sanskrit", "1500-1700 CE", "Hatha Yoga"),
        ("Goraksha Shataka", "Yoga", "yoga", "Sanskrit", "1200-1400 CE", "Hatha Yoga"),
        ("Yoga Vasiṣṭha", "Yoga", "yoga", "Sanskrit", "1000-1400 CE", "Advaita Vedanta"),
        
        # 6. Sciences - Ayurveda
        ("Charaka Samhita", "Ayurveda", "sciences", "Sanskrit", "100 BCE-200 CE", "Ayurveda"),
        ("Sushruta Samhita", "Ayurveda", "sciences", "Sanskrit", "600 BCE-100 CE", "Ayurveda"),
        ("Ashtanga Hridaya", "Ayurveda", "sciences", "Sanskrit", "600-700 CE", "Ayurveda"),
        
        # Other Sciences
        ("Vāstu Śāstra", "Architecture", "sciences", "Sanskrit", "500-1500 CE", "Architecture"),
        ("Nāṭya Śāstra", "Performing Arts", "sciences", "Sanskrit", "200 BCE-200 CE", "Arts"),
        ("Sangita Ratnakara", "Music", "sciences", "Sanskrit", "1210-1247 CE", "Music"),
        ("Sūrya Siddhānta", "Astronomy", "sciences", "Sanskrit", "400-500 CE", "Jyotisha"),
        ("Āryabhaṭīya", "Astronomy", "sciences", "Sanskrit", "499 CE", "Jyotisha"),
        ("Brahmasphuṭasiddhānta", "Astronomy", "sciences", "Sanskrit", "628 CE", "Jyotisha"),
        
        # 7. Commentarial Traditions
        ("Śaṅkara - Advaita Vedanta", "Commentaries", "commentaries", "Sanskrit", "788-820 CE", "Advaita"),
        ("Rāmānuja - Vishishtadvaita", "Commentaries", "commentaries", "Sanskrit", "1017-1137 CE", "Vishishtadvaita"),
        ("Madhva - Dvaita", "Commentaries", "commentaries", "Sanskrit", "1238-1317 CE", "Dvaita"),
        ("Vallabha - Shuddhadvaita", "Commentaries", "commentaries", "Sanskrit", "1479-1531 CE", "Shuddhadvaita"),
        ("Nimbarka - Dvaitadvaita", "Commentaries", "commentaries", "Sanskrit", "1130-1200 CE", "Dvaitadvaita"),
        ("Chaitanya - Achintya Bhedabheda", "Commentaries", "commentaries", "Sanskrit", "1486-1534 CE", "Gaudiya Vaishnavism"),
        ("Abhinavagupta", "Commentaries", "commentaries", "Sanskrit", "950-1016 CE", "Kashmir Shaivism"),
        ("Vijnanabhikshu", "Commentaries", "commentaries", "Sanskrit", "1550-1600 CE", "Yoga-Vedanta"),
        ("Śrīharṣa", "Commentaries", "commentaries", "Sanskrit", "1125-1180 CE", "Advaita"),
        ("Gaṅgeśa", "Commentaries", "commentaries", "Sanskrit", "1325-1400 CE", "Navya-Nyaya"),
        
        # 8. Regional Texts
        ("Tirukkural", "Regional", "regional", "Tamil", "300 BCE-500 CE", "Tamil"),
        ("Tevaram & Tirumurai", "Regional", "regional", "Tamil", "600-900 CE", "Tamil Shaivism"),
        ("Ramcharitmanas", "Regional", "regional", "Awadhi", "1574-1576 CE", "Bhakti"),
        ("Jñāneśvarī", "Regional", "regional", "Marathi", "1290 CE", "Bhakti"),
        
        # 9. Modern Synthesizers
        ("Swami Vivekananda - Complete Works", "Modern", "modern", "English", "1863-1902 CE", "Vedanta"),
        ("Sri Aurobindo - The Life Divine", "Modern", "modern", "English", "1872-1950 CE", "Integral Yoga"),
        ("Sri Aurobindo - Synthesis of Yoga", "Modern", "modern", "English", "1872-1950 CE", "Integral Yoga"),
        ("Sri Aurobindo - Secret of the Veda", "Modern", "modern", "English", "1872-1950 CE", "Integral Yoga"),
        ("S. Radhakrishnan - Indian Philosophy", "Modern", "modern", "English", "1888-1975 CE", "Philosophy"),
        ("Swami Sivananda - Major Works", "Modern", "modern", "English", "1887-1963 CE", "Yoga Vedanta"),
    ]
    
    count = 0
    for text_data in texts:
        try:
            name, category, subcategory, language, date, tradition = text_data
            kb.add_text(
                name=name,
                category=category,
                subcategory=subcategory,
                language=language,
                approximate_date=date,
                tradition=tradition,
                file_path=f"/home/ubuntu/vedic_mastery/{subcategory}/{name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')}_study.md"
            )
            count += 1
            print(f"✓ Added: {name}")
        except Exception as e:
            print(f"✗ Error adding {text_data[0]}: {e}")
    
    print(f"\n{count} texts added to the database successfully!")
    
    # Display progress
    progress = kb.get_study_progress()
    print("\n=== Study Progress by Category ===")
    for category, stats in progress.items():
        print(f"{category}: {stats['total']} texts")
    
    kb.close()

if __name__ == "__main__":
    populate_database()
