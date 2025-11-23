
import json

print("Starting JSON test script...")
try:
    with open('/home/ubuntu/vedic_texts_parallel_research.json', 'r') as f:
        data = json.load(f)
    print(f"Successfully loaded JSON data. Found {len(data.get('results', []))} results.")
except Exception as e:
    print(f"An error occurred: {e}")
