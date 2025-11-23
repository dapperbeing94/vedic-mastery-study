#!/usr/bin/env python3
"""
Generate comprehensive study documents for the 14 extension texts of the Vedic mastery roadmap.
"""

import json

def generate_extension_docs():
    # Load the parallel research results
    with open("/home/ubuntu/extension_texts_research.json", "r") as f:
        data = json.load(f)
    
    results = data["results"]
    
    # Define the categories and their associated keywords
    categories = {
        "Vedangas": ["shiksha", "chandas", "vyakarana", "nirukta", "kalpa", "jyotisha"],
        "Astronomy and Mathematics": ["surya siddhanta", "aryabhatiya", "brahmasphutasiddhanta"],
        "Bhakti Sutras": ["narada bhakti sutra", "shandilya bhakti sutra"],
        "Arts and Sciences": ["natya shastra", "sangita ratnakara", "vastu shastra"]
    }
    
    # Create a dictionary to hold the content for each category
    category_content = {cat: "" for cat in categories}
    
    # Process each result and categorize it
    for result in results:
        text_data = result["output"]
        text_name = text_data["text_name"]
        
        # Determine category
        category = "Uncategorized"
        for cat, keywords in categories.items():
            for keyword in keywords:
                if keyword.lower() in text_name.lower() or keyword.lower() in result["input"].lower():
                    category = cat
                    break
            if category != "Uncategorized":
                break
        
        if category != "Uncategorized":
            # Format the content for the study document
            content = f"## {text_name}\n\n"
            content += f"**Author/Tradition**: {text_data.get('author_tradition', 'N/A')}\n\n"
            content += f"**Historical Period**: {text_data.get('historical_period', 'N/A')}\n\n"
            content += f"### Core Teachings\n{text_data.get('core_teachings', 'N/A')}\n\n"
            content += f"### Key Concepts\n{text_data.get('key_concepts', 'N/A')}\n\n"
            content += f"### Structure\n{text_data.get('structure', 'N/A')}\n\n"
            content += f"### Practical Applications\n{text_data.get('practical_applications', 'N/A')}\n\n"
            content += f"### Key Verses/Passages\n{text_data.get('key_verses', 'N/A')}\n\n"
            content += f"### Cross-References\n{text_data.get('cross_references', 'N/A')}\n\n"
            content += f"### Authoritative Sources\n{text_data.get('sources', 'N/A')}\n\n"
            
            category_content[category] += content

    # Write the content to the respective study documents
    for category, content in category_content.items():
        filename = f"/home/ubuntu/vedic-mastery-study/study_documents_extensions/{category.lower().replace(' ', '_')}_comprehensive.md"
        with open(filename, "w") as f:
            f.write(f"# {category} - Comprehensive Study\n\n{content}")
        print(f"Successfully created {filename}")

if __name__ == "__main__":
    generate_extension_docs()
