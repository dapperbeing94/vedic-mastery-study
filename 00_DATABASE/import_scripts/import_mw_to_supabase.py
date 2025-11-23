#!/usr/bin/env python3
"""
Import Monier-Williams Dictionary to Supabase
Batch imports parsed MW dictionary entries into the dictionary_entries table.

Input: /home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/mw_dictionary.jsonl
Output: Supabase dictionary_entries table
"""

import json
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"

# Batch size for imports
BATCH_SIZE = 1000

def import_dictionary():
    """Import MW dictionary entries to Supabase"""
    input_file = "/home/ubuntu/vedic-mastery-study/00_DATABASE/import_data/mw_dictionary.jsonl"
    
    print(f"📥 Importing Monier-Williams Dictionary to Supabase...")
    print(f"   Source: {input_file}")
    print(f"   Target: dictionary_entries table")
    print(f"   Batch size: {BATCH_SIZE}")
    
    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Read and batch import
    batch = []
    total_imported = 0
    total_failed = 0
    batch_num = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            try:
                entry = json.loads(line)
                batch.append(entry)
                
                # Import batch when full
                if len(batch) >= BATCH_SIZE:
                    batch_num += 1
                    print(f"   Importing batch {batch_num} ({len(batch)} entries)...")
                    
                    try:
                        result = supabase.table('dictionary_entries').insert(batch).execute()
                        total_imported += len(batch)
                        print(f"   ✅ Batch {batch_num} imported successfully ({total_imported} total)")
                    except Exception as e:
                        print(f"   ❌ Batch {batch_num} failed: {str(e)}")
                        total_failed += len(batch)
                    
                    batch = []
            
            except json.JSONDecodeError as e:
                print(f"   ⚠️  Skipping line {line_num}: Invalid JSON")
                total_failed += 1
    
    # Import remaining entries
    if batch:
        batch_num += 1
        print(f"   Importing final batch {batch_num} ({len(batch)} entries)...")
        
        try:
            result = supabase.table('dictionary_entries').insert(batch).execute()
            total_imported += len(batch)
            print(f"   ✅ Final batch imported successfully")
        except Exception as e:
            print(f"   ❌ Final batch failed: {str(e)}")
            total_failed += len(batch)
    
    print(f"\n✅ Import Complete!")
    print(f"   Total entries imported: {total_imported}")
    print(f"   Total entries failed: {total_failed}")
    print(f"   Success rate: {(total_imported / (total_imported + total_failed) * 100):.1f}%")


if __name__ == "__main__":
    import_dictionary()
