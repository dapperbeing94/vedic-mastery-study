'''
import json
import os

def generate_study_documents():
    output_dir = '/home/ubuntu/vedic-mastery-study/study_documents_session3'
    os.makedirs(output_dir, exist_ok=True)

    with open('/home/ubuntu/vedic_texts_parallel_research.json', 'r') as f:
        data = json.load(f)

    results = data['results']

    categories = {
        "Yoga Texts": ["Hatha Yoga Pradipika", "Yoga Vasistha", "Gheranda Samhita", "Shiva Samhita", "Goraksha Shataka"],
        "Commentaries": ["Shankaracharya", "Ramanuja", "Madhvacharya", "Nimbarka", "Vallabhacharya", "Chaitanya", "Abhinavagupta", "Gangesha", "Sriharsha", "Vijnanabhikshu"],
        "Regional Literature": ["Ramcharitmanas", "Jnanesvari", "Tirukkural", "Tevaram"],
        "Modern Interpretations": ["Vivekananda", "Aurobindo", "Sivananda", "Radhakrishnan"]
    }

    categorized_texts = {category: [] for category in categories}

    for result in results:
        text_name = result['output']['text_name']
        categorized = False
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in text_name.lower() or keyword.lower() in result['input'].lower():
                    categorized_texts[category].append(result['output'])
                    categorized = True
                    break
            if categorized:
                break

    for category, texts in categorized_texts.items():
        file_name = category.lower().replace(' ', '_') + '_comprehensive.md'
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as f:
            f.write(f"# {category} - Comprehensive Study\n\n")
            for text in texts:
                f.write(f"## {text.get('text_name', 'N/A')}\n\n")
                f.write(f"**Author/Tradition**: {text.get('author_tradition', 'N/A')}\n\n")
                f.write(f"**Historical Period**: {text.get('historical_period', 'N/A')}\n\n")
                f.write(f"### Core Teachings\n{text.get('core_teachings', 'N/A')}\n\n")
                f.write(f"### Key Concepts\n{text.get('key_concepts', 'N/A')}\n\n")
                f.write(f"### Structure\n{text.get('structure', 'N/A')}\n\n")
                f.write(f"### Practical Applications\n{text.get('practical_applications', 'N/A')}\n\n")
                f.write(f"### Key Verses/Passages\n{text.get('key_verses', 'N/A')}\n\n")
                f.write(f"### Cross-References\n{text.get('cross_references', 'N/A')}\n\n")
                f.write(f"### Authoritative Sources\n{text.get('sources', 'N/A')}\n\n")

if __name__ == "__main__":
    generate_study_documents()
'''
