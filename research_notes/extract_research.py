import json

# Read the JSON file
with open('/home/ubuntu/vedic-mastery-study/research_notes/option_4_major_texts_research.json', 'r') as f:
    data = json.load(f)

# Extract each text's data
for item in data['results']:
    text_input = item['input']
    output = item['output']
    
    # Create a clean filename
    filename = text_input.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace(',', '')
    filename = f"/home/ubuntu/vedic-mastery-study/research_notes/{filename}_research.txt"
    
    # Write to file
    with open(filename, 'w') as f:
        f.write(f"TEXT: {output.get('text_name', 'N/A')}\n")
        f.write("="*80 + "\n\n")
        
        f.write("OVERVIEW:\n")
        f.write(output.get('overview', 'N/A') + "\n\n")
        
        f.write("CORE PHILOSOPHY:\n")
        f.write(output.get('core_philosophy', 'N/A') + "\n\n")
        
        f.write("STRUCTURE:\n")
        f.write(output.get('structure', 'N/A') + "\n\n")
        
        f.write("KEY VERSES:\n")
        f.write(output.get('key_verses', 'N/A') + "\n\n")
        
        f.write("COMMENTATORS:\n")
        f.write(output.get('commentators', 'N/A') + "\n\n")
        
        f.write("THEMES:\n")
        f.write(output.get('themes', 'N/A') + "\n\n")
        
        f.write("PRACTICAL APPLICATION:\n")
        f.write(output.get('practical_application', 'N/A') + "\n\n")
        
        f.write("RELATIONSHIPS:\n")
        f.write(output.get('relationships', 'N/A') + "\n\n")
        
        f.write("SOURCES:\n")
        f.write(output.get('sources', 'N/A') + "\n")
    
    print(f"Created: {filename}")

print("\nExtraction complete!")
