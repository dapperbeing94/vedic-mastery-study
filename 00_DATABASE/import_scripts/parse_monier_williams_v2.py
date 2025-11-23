#!/usr/bin/env python3
"""
Monier-Williams Dictionary Parser V2
Correctly parses the MW dictionary from csl-orig format.

Input: /home/ubuntu/csl-orig/v02/mw/mw.txt
Output: /home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/mw_dictionary.jsonl
"""

import re
import json
import os

class MonierWilliamsParserV2:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.entries_parsed = 0
        self.entries_skipped = 0
        
    def clean_text(self, text):
        """Remove XML-like tags and clean text"""
        if not text:
            return ""
        
        # Remove common markup tags but preserve content
        text = re.sub(r'<s>([^<]+)</s>', r'\1', text)  # Sanskrit terms
        text = re.sub(r'<s1>([^<]+)</s1>', r'\1', text)  # Proper nouns
        text = re.sub(r'<lex>([^<]+)</lex>', r'[\1]', text)  # Lexical info
        text = re.sub(r'<ab>([^<]+)</ab>', r'\1', text)  # Abbreviations
        text = re.sub(r'<ls>([^<]+)</ls>', r'', text)  # Literature sources (remove)
        text = re.sub(r'<lang>([^<]+)</lang>', r'\1', text)  # Language names
        text = re.sub(r'<gk>([^<]+)</gk>', r'\1', text)  # Greek text
        text = re.sub(r'<etym>([^<]+)</etym>', r'\1', text)  # Etymology
        text = re.sub(r'<hom>([^<]+)</hom>', r'(\1)', text)  # Homonym number
        text = re.sub(r'<info[^>]*>', '', text)  # Info tags
        text = re.sub(r'<[^>]+>', '', text)  # Remove remaining tags
        
        # Clean up special characters
        text = text.replace('¦', '')
        text = text.replace('&c.', 'etc.')
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def extract_part_of_speech(self, text):
        """Extract part of speech from entry text"""
        # Look for <lex> tags first
        lex_match = re.search(r'<lex>([^<]+)</lex>', text)
        if lex_match:
            pos = lex_match.group(1)
            # Map common abbreviations
            pos_map = {
                'mfn.': 'adjective',
                'm.': 'masculine noun',
                'f.': 'feminine noun',
                'n.': 'neuter noun',
                'mf.': 'masculine/feminine noun',
                'ind.': 'indeclinable',
                'adj.': 'adjective',
                'adv.': 'adverb'
            }
            return pos_map.get(pos, pos)
        
        return None
    
    def extract_headword_devanagari(self, text):
        """Extract Devanagari headword if present"""
        # Look for Devanagari in <s> tags
        dev_match = re.search(r'<s>([^\x00-\x7F]+)</s>', text)
        if dev_match:
            return dev_match.group(1)
        return None
    
    def parse_entry(self, entry_lines):
        """Parse a single dictionary entry from its lines"""
        if not entry_lines:
            return None
        
        # First line contains metadata
        first_line = entry_lines[0]
        
        # Extract headword (k1 field - the main headword)
        headword_match = re.search(r'<k1>([^<]+)</k1>', first_line)
        if not headword_match:
            return None
        
        headword = headword_match.group(1)
        
        # Skip very short headwords (likely sub-entries or markers)
        if len(headword) < 1:
            return None
        
        # Combine all content lines (skip first metadata line)
        content_lines = [line for line in entry_lines[1:] if line.strip() and not line.strip().startswith('<L>')]
        
        if not content_lines:
            return None
        
        content = ' '.join(content_lines)
        
        # Extract definition (clean text)
        definition = self.clean_text(content)
        
        # Skip if definition is too short or empty
        if not definition or len(definition) < 5:
            return None
        
        # Skip if it's just a cross-reference (contains only "See ..." or similar)
        if re.match(r'^(see|cf\.|vide)\s+', definition, re.IGNORECASE) and len(definition) < 50:
            return None
        
        # Extract part of speech
        pos = self.extract_part_of_speech(content)
        
        # Extract Devanagari
        devanagari = self.extract_headword_devanagari(content)
        
        # Extract etymology (look for "fr." = "from")
        etymology = None
        etym_match = re.search(r'fr\.\s+([^;,\.]+)', content)
        if etym_match:
            etymology = f"from {self.clean_text(etym_match.group(1))}"
        
        # Extract usage examples (text within quotes)
        examples = []
        example_matches = re.findall(r'"([^"]+)"', content)
        if example_matches:
            examples = [self.clean_text(ex) for ex in example_matches[:3]]  # Limit to 3
        
        usage_examples = '; '.join(examples) if examples else None
        
        return {
            'headword': headword,
            'headword_devanagari': devanagari,
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
        print(f"📖 Parsing Monier-Williams Dictionary (V2)...")
        print(f"   Input: {self.input_file}")
        print(f"   Output: {self.output_file}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Read and parse file line by line
        current_entry_lines = []
        total_raw_entries = 0
        
        with open(self.input_file, 'r', encoding='utf-8') as in_f, \
             open(self.output_file, 'w', encoding='utf-8') as out_f:
            
            for line in in_f:
                line = line.rstrip('\n')
                
                # Check if this is the start of a new entry
                if line.startswith('<L>'):
                    # Process previous entry if exists
                    if current_entry_lines:
                        total_raw_entries += 1
                        entry = self.parse_entry(current_entry_lines)
                        
                        if entry:
                            out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                            self.entries_parsed += 1
                        else:
                            self.entries_skipped += 1
                        
                        # Progress indicator
                        if total_raw_entries % 10000 == 0:
                            print(f"   Processed {total_raw_entries} raw entries... "
                                  f"(Parsed: {self.entries_parsed}, Skipped: {self.entries_skipped})")
                    
                    # Start new entry
                    current_entry_lines = [line]
                
                elif line.startswith('<LEND>'):
                    # End of entry marker - don't include it
                    continue
                
                else:
                    # Add line to current entry
                    if current_entry_lines:
                        current_entry_lines.append(line)
            
            # Process last entry
            if current_entry_lines:
                total_raw_entries += 1
                entry = self.parse_entry(current_entry_lines)
                if entry:
                    out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')
                    self.entries_parsed += 1
                else:
                    self.entries_skipped += 1
        
        print(f"\n✅ Parsing Complete!")
        print(f"   Total raw entries: {total_raw_entries}")
        print(f"   Total entries parsed: {self.entries_parsed}")
        print(f"   Total entries skipped: {self.entries_skipped}")
        print(f"   Parse rate: {(self.entries_parsed / total_raw_entries * 100):.1f}%")
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
    parser = MonierWilliamsParserV2(input_file, output_file)
    entries_count = parser.parse_file()
    
    # Sample output
    print(f"\n📄 Sample entries:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            entry = json.loads(line)
            print(f"\n{i+1}. Headword: {entry['headword']}")
            if entry.get('headword_devanagari'):
                print(f"   Devanagari: {entry['headword_devanagari']}")
            print(f"   POS: {entry.get('part_of_speech', 'N/A')}")
            print(f"   Definition: {entry['definition'][:150]}...")


if __name__ == "__main__":
    main()
