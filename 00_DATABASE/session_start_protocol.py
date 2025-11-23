#!/usr/bin/env python3
"""
Session Start Protocol
Run this at the beginning of every new chat session.
"""

import sqlite3
import os
from datetime import datetime

def sanity_check_database(db_path='vedic_knowledge.db'):
    """Comprehensive sanity check of the Vedic knowledge database."""
    
    print("🔍 Running Database Sanity Check...")
    
    if not os.path.exists(db_path):
        print("❌ ERROR: Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check 1: Database integrity
        c.execute("PRAGMA integrity_check")
        integrity = c.fetchone()[0]
        if integrity == "ok":
            print("✅ Database integrity: OK")
        else:
            print(f"❌ Database integrity issues: {integrity}")
            return False
        
        # Check 2: All tables exist
        required_tables = ['texts', 'concepts', 'verses', 'sanskrit_terms', 
                          'cross_references', 'study_progress']
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in c.fetchall()]
        
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ Table '{table}': exists")
            else:
                print(f"❌ Table '{table}': MISSING")
                return False
        
        # Check 3: Row counts
        for table in required_tables:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            print(f"📊 Table '{table}': {count} rows")
        
        conn.close()
        print("\n✅ Sanity check PASSED - Database is healthy\n")
        return True
        
    except Exception as e:
        print(f"❌ Sanity check FAILED: {str(e)}")
        return False


def session_start_protocol():
    """Complete protocol to run at session start."""
    
    print("=" * 70)
    print("🕉️  VEDIC MASTERY - SESSION START PROTOCOL")
    print("=" * 70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Verify repository
    if not os.path.exists('vedic_knowledge.db'):
        print("❌ ERROR: Not in database directory!")
        print("📂 Please cd to: vedic-mastery-study/database/")
        return False
    
    print("✅ Database directory verified")
    
    # Step 2: Run sanity check
    if not sanity_check_database():
        print("❌ Database sanity check failed!")
        return False
    
    # Step 3: Load progress
    conn = sqlite3.connect('vedic_knowledge.db')
    c = conn.cursor()
    
    try:
        c.execute("""
            SELECT text_name, status, completion_date 
            FROM study_progress 
            WHERE status = 'completed' 
            ORDER BY completion_date
        """)
        completed = c.fetchall()
        
        print("📚 COMPLETED TEXTS:")
        if completed:
            for text, status, date in completed:
                print(f"   ✅ {text} (completed: {date})")
        else:
            print("   (None yet - beginning the journey!)")
        
        print()
        
        # Step 4: Show next texts
        c.execute("""
            SELECT text_name 
            FROM study_progress 
            WHERE status = 'not_started' 
            ORDER BY id 
            LIMIT 5
        """)
        upcoming = c.fetchall()
        
        print("📖 NEXT IN ROADMAP:")
        if upcoming:
            for i, (text,) in enumerate(upcoming, 1):
                print(f"   {i}. {text}")
        else:
            print("   (All texts completed!)")
        
    except Exception as e:
        print(f"⚠️  Could not load progress: {str(e)}")
    
    conn.close()
    
    print()
    print("=" * 70)
    print("✅ SESSION START PROTOCOL COMPLETE")
    print("=" * 70)
    print()
    
    return True

if __name__ == "__main__":
    session_start_protocol()
