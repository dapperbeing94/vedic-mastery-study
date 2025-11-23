#!/usr/bin/env python3
"""
Monier-Williams Dictionary Parser
Parses the MW dictionary from csl-orig format and prepares it for Supabase import.

Input: /home/ubuntu/csl-orig/v02/mw/mw.txt
Output: /home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/mw_dictionary.jsonl
"""

import re
import json
import os
from pathlib import Path

class MonierWilliamsParser:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.entries_parsed = 0
        self.entries_skipped = 0
        
    def clean_text(self, text):
        """Remove XML-like tags and clean text"""
        if not text:
            return ""
        
        # Remove common markup tags
        text = re.sub(r'<[^>]+>', '', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def extract_part_of_speech(self, text):
        """Extract part of speech from entry text"""
        pos_patterns = [
            (r'<lex>([^<]+)</lex>', 1),
            (r'\b(m\.|f\.|n\.|mf\.|mfn\.|ind\.|adj\.|adv\.)', 0)
        ]
        
        for pattern, group in pos_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(group) if group else match.group(1)
        return None
    
    def extract_etymology(self, text):
        """Extract etymology information if present"""
        # Look for etymology patterns
        etym_match = re.search(r'<etym>([^<]+)</etym>', text)
        if etym_match:
            return self.clean_text(etym_match.group(1))
        
        # Look for root references
        root_match = re.search(r'fr\.\s+([^;,]+)', text)
        if root_match:
            return f"from {root_match.group(1).strip()}"
        
        return None
    
    def parse_entry(self, entry_text):
        """Parse a single dictionary entry"""
        lines = entry_text.strip().split('\n')
        if not lines:
            return None
        
        # First line contains metadata
        first_line = lines[0]
        
        # Extract headword (k1 or k2 field)
        headword_match = re.search(r'<k1>([^<]+)</k1>', first_line)
        if not headword_match:
            headword_match = re.search(r'<k2>([^<]+)</k2>', first_line)
        
        if not headword_match:
            return None
        
        headword = headword_match.group(1)
        
        # Combine all content lines
        content = '\n'.join(lines[1:]) if len(lines) > 1 else ""
        
        # Extract definition (clean text)
        definition = self.clean_text(content)
        
        if not definition or len(definition) < 3:
            return None
        
        # Extract part of speech
        pos = self.extract_part_of_speech(entry_text)
        
        # Extract etymology
        etymology = self.extract_etymology(entry_text)
        
        # Extract usage examples (text within quotes or after 'e.g.')
        examples = []
        example_matches = re.findall(r'"([^"]+)"', content)
        if example_matches:
            examples = example_matches[:3]  # Limit to 3 examples
        
        usage_examples = '; '.join(examples) if examples else None
        
        return {
            'headword': headword,
            'headword_devanagari': None,  # Not available in this format
            'definition': definition[:5000],  # Limit definition length
            'part_of_speech': pos,
            'etymology': etymology,
            'usage_examples': usage_examples,
            'source': 'monier-williams',
            'source_page': None,
            'authority_score': 9.0  # MW is highly authoritative
        }
    
    def parse_file(self):
        """Parse the entire MW dictionary file"""
        print(f"📖 Parsing Monier-Williams Dictionary...")
        print(f"   Input: {self.input_file}")
        print(f"   Output: {self.output_file}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Read the entire file
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into entries (entries start with <L> and end with <LEND>)
        entries = re.split(r'<LEND>', content)
        
        total_entries = len(entries)
        print(f"   Found {total_entries} raw entries")
        
        # Parse and write entries
        with open(self.output_file, 'w', encoding='utf-8') as out_f:
            for i, entry_text in enumerate(entries):
                if not entry_text.strip():
                    continue
                
                entry = self.parse_entry(entry_text)
                
                if entry:
                    # Write as JSONL (one JSON object per line)
                    out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    self.entries_parsed += 1
                else:
                    self.entries_skipped += 1
                
                # Progress indicator
                if (i + 1) % 10000 == 0:
                    print(f"   Processed {i + 1}/{total_entries} entries... "
                          f"(Parsed: {self.entries_parsed}, Skipped: {self.entries_skipped})")
        
        print(f"\n✅ Parsing Complete!")
        print(f"   Total entries parsed: {self.entries_parsed}")
        print(f"   Total entries skipped: {self.entries_skipped}")
        print(f"   Output file: {self.output_file}")
        
        return self.entries_parsed


def main():
    # File paths
    input_file = "/home/ubuntu/csl-orig/v02/mw/mw.txt"
    output_file = "/home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/mw_dictionary.jsonl"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file not found: {input_file}")
        return
    
    # Parse the dictionary
    parser = MonierWilliamsParser(input_file, output_file)
    entries_count = parser.parse_file()
    
    # Sample output
    print(f"\n📄 Sample entries:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            entry = json.loads(line)
            print(f"\n{i+1}. Headword: {entry['headword']}")
            print(f"   Definition: {entry['definition'][:100]}...")
            print(f"   POS: {entry.get('part_of_speech', 'N/A')}")


if __name__ == "__main__":
    main()
