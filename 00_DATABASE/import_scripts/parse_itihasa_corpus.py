#!/usr/bin/env python3
"""
Itihasa Translation Corpus Parser
Parses parallel Sanskrit-English text files from the Itihasa corpus.

Input: /home/ubuntu/itihasa-corpus/data/*.{sn,en}
Output: /home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/itihasa_corpus.jsonl
"""

import json
import os

class ItihasaCorpusParser:
    def __init__(self, corpus_dir, output_file):
        self.corpus_dir = corpus_dir
        self.output_file = output_file
        self.entries_parsed = 0
        
    def parse_parallel_files(self, sanskrit_file, english_file, dataset_type):
        """Parse a pair of parallel Sanskrit-English files"""
        print(f"   Processing {dataset_type} set...")
        
        with open(sanskrit_file, 'r', encoding='utf-8') as sn_f, \
             open(english_file, 'r', encoding='utf-8') as en_f:
            
            sanskrit_lines = sn_f.readlines()
            english_lines = en_f.readlines()
            
            # Verify parallel alignment
            if len(sanskrit_lines) != len(english_lines):
                print(f"   ⚠️  Warning: Line count mismatch in {dataset_type} set")
                print(f"      Sanskrit: {len(sanskrit_lines)}, English: {len(english_lines)}")
                # Use the minimum length to avoid index errors
                min_length = min(len(sanskrit_lines), len(english_lines))
            else:
                min_length = len(sanskrit_lines)
            
            entries = []
            for i in range(min_length):
                sanskrit_text = sanskrit_lines[i].strip()
                english_text = english_lines[i].strip()
                
                # Skip empty lines
                if not sanskrit_text or not english_text:
                    continue
                
                entry = {
                    'sanskrit_text': sanskrit_text,
                    'english_translation': english_text,
                    'source': 'itihasa-corpus',
                    'source_reference': f'Mahabharata/Ramayana ({dataset_type} set)',  # Itihasa = epics
                    'translator': 'M. N. Dutt',
                    'translation_quality_score': 8.5,  # High quality scholarly translation
                    'validated': True  # Pre-validated scholarly translation
                }
                
                entries.append(entry)
                self.entries_parsed += 1
            
            print(f"      Parsed {len(entries)} parallel pairs")
            return entries
    
    def parse_corpus(self):
        """Parse the entire Itihasa corpus"""
        print(f"📖 Parsing Itihasa Translation Corpus...")
        print(f"   Input: {self.corpus_dir}")
        print(f"   Output: {self.output_file}")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        all_entries = []
        
        # Parse training set
        train_sn = os.path.join(self.corpus_dir, 'train.sn')
        train_en = os.path.join(self.corpus_dir, 'train.en')
        all_entries.extend(self.parse_parallel_files(train_sn, train_en, 'train'))
        
        # Parse development set
        dev_sn = os.path.join(self.corpus_dir, 'dev.sn')
        dev_en = os.path.join(self.corpus_dir, 'dev.en')
        all_entries.extend(self.parse_parallel_files(dev_sn, dev_en, 'dev'))
        
        # Parse test set
        test_sn = os.path.join(self.corpus_dir, 'test.sn')
        test_en = os.path.join(self.corpus_dir, 'test.en')
        all_entries.extend(self.parse_parallel_files(test_sn, test_en, 'test'))
        
        # Write all entries to JSONL file
        print(f"\n   Writing to output file...")
        with open(self.output_file, 'w', encoding='utf-8') as out_f:
            for entry in all_entries:
                out_f.write(json.dumps(entry, ensure_ascii=False) + '\n')
        
        print(f"\n✅ Parsing Complete!")
        print(f"   Total entries parsed: {self.entries_parsed}")
        print(f"   Output file: {self.output_file}")
        
        return self.entries_parsed


def main():
    corpus_dir = "/home/ubuntu/itihasa-corpus/data"
    output_file = "/home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/itihasa_corpus.jsonl"
    
    if not os.path.exists(corpus_dir):
        print(f"❌ Error: Corpus directory not found: {corpus_dir}")
        return
    
    parser = ItihasaCorpusParser(corpus_dir, output_file)
    entries_count = parser.parse_corpus()
    
    # Sample output
    print(f"\n📄 Sample entries:")
    with open(output_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            entry = json.loads(line)
            print(f"\n{i+1}. Sanskrit: {entry['sanskrit_text'][:80]}...")
            print(f"   English: {entry['english_translation'][:80]}...")
            print(f"   Source: {entry['source_reference']}")


if __name__ == "__main__":
    main()
