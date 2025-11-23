#!/usr/bin/env python3
"""
Populate tracking data from existing study documents
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = "/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db"
STUDY_DOCS_PATH = "/home/ubuntu/vedic-mastery-study/01_STUDY_DOCUMENTS"

# Category mapping from folder names to database categories
CATEGORY_MAP = {
    '01_Vedas': 'Core Vedic Foundation',
    '02_Upanishads': 'Core Vedic Foundation',
    '03_Vedangas': 'Core Vedic Foundation',
    '04_Puranas': 'Smṛti Texts',
    '05_Itihasa': 'Smṛti Texts',
    '06_Darsanas': 'Darśanas',
    '07_Brahma_Sutras': 'Darśanas',
    '08_Synthesis_Documents': 'Synthesis Work',
    'Tantra': 'Tantra & Agamas',
    'Yoga': 'Yogic Corpus',
    'Ayurveda': 'Sciences & Knowledge Systems'
}

def analyze_study_documents():
    """
    Analyze the file system to determine what has been studied
    """
    study_docs = Path(STUDY_DOCS_PATH)
    
    if not study_docs.exists():
        print(f"Study documents path not found: {STUDY_DOCS_PATH}")
        return {}
    
    results = {}
    
    for category_dir in study_docs.iterdir():
        if not category_dir.is_dir():
            continue
        
        category_name = category_dir.name
        db_category = CATEGORY_MAP.get(category_name, 'Unknown')
        
        if db_category not in results:
            results[db_category] = {
                'texts': [],
                'total_size': 0,
                'file_count': 0
            }
        
        # Recursively find all .md files
        for md_file in category_dir.rglob('*.md'):
            file_size = md_file.stat().st_size
            results[db_category]['texts'].append({
                'name': md_file.stem,
                'path': str(md_file),
                'size': file_size
            })
            results[db_category]['total_size'] += file_size
            results[db_category]['file_count'] += 1
    
    return results

def calculate_depth_from_file(file_info):
    """
    Calculate depth score based on file characteristics
    """
    score = 0
    size = file_info['size']
    name = file_info['name'].lower()
    
    # Base score for existence
    score += 2
    
    # Size-based scoring
    if size > 3000:  # >3KB = comprehensive overview
        score += 1
    if size > 8000:  # >8KB = detailed study
        score += 1
    if size > 15000:  # >15KB = deep dive
        score += 2
    if size > 25000:  # >25KB = very deep dive
        score += 1
    
    # Content-based scoring (from filename)
    if 'comprehensive' in name or 'deep_dive' in name:
        score += 1
    if 'verse' in name or 'chapter' in name or 'sutra' in name:
        score += 1
    if 'commentary' in name:
        score += 1
    
    return min(10, score)

def populate_tracking_data():
    """
    Populate the tracking database from file system analysis
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get category IDs
    cursor.execute("SELECT id, name FROM categories WHERE level = 1")
    categories = {row[1]: row[0] for row in cursor.fetchall()}
    
    # Analyze documents
    results = analyze_study_documents()
    
    print("\nPopulating tracking data...\n")
    
    for category_name, data in results.items():
        if category_name not in categories:
            print(f"Warning: Category '{category_name}' not found in database")
            continue
        
        category_id = categories[category_name]
        
        # Calculate scores
        text_count = data['file_count']
        if text_count == 0:
            breadth_score = 0
            depth_score = 0
        else:
            # Breadth: based on file count (rough estimate)
            breadth_score = min(10, text_count)
            
            # Depth: average of all file depth scores
            depth_scores = [calculate_depth_from_file(text) for text in data['texts']]
            depth_score = round(sum(depth_scores) / len(depth_scores), 1) if depth_scores else 0
        
        combined_score = round((breadth_score * 0.3) + (depth_score * 0.7), 1)
        
        # Update or insert progress tracking
        cursor.execute("""
            INSERT OR REPLACE INTO progress_tracking 
            (category_id, breadth_score, depth_score, combined_score, last_updated, notes)
            VALUES (?, ?, ?, ?, datetime('now'), ?)
        """, (
            category_id,
            breadth_score,
            depth_score,
            combined_score,
            f"{text_count} files, {data['total_size']} bytes total"
        ))
        
        print(f"{category_name}:")
        print(f"  Files: {text_count}")
        print(f"  Total Size: {data['total_size']:,} bytes")
        print(f"  Breadth Score: {breadth_score}/10")
        print(f"  Depth Score: {depth_score}/10")
        print(f"  Combined Score: {combined_score}/10")
        print()
    
    conn.commit()
    conn.close()
    
    print("Tracking data populated successfully!")

if __name__ == "__main__":
    populate_tracking_data()
