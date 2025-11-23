#!/usr/bin/env python3
# ============================================================================
# VEDIC MASTERY STUDY - DEPTH DATA VALIDATOR
# ============================================================================
# Purpose: Validates the integrity of verse-level and commentary data.
# Version: 1.0
# Date: November 23, 2025
# ============================================================================

import sqlite3
import pandas as pd

DB_PATH = '00_DATABASE/vedic_knowledge.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_orphan_commentaries():
    """Finds commentaries linked to non-existent verses."""
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT c.commentary_id, c.verse_id
        FROM commentaries c
        LEFT JOIN verses v ON c.verse_id = v.verse_id
        WHERE v.verse_id IS NULL
    """, conn)
    conn.close()
    return df

def check_orphan_cross_references():
    """Finds cross-references linked to non-existent verses."""
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT cr.cross_ref_id, cr.source_verse_id, cr.target_verse_id
        FROM cross_references cr
        LEFT JOIN verses v1 ON cr.source_verse_id = v1.verse_id
        LEFT JOIN verses v2 ON cr.target_verse_id = v2.verse_id
        WHERE v1.verse_id IS NULL OR v2.verse_id IS NULL
    """, conn)
    conn.close()
    return df

def check_duplicate_verses():
    """Finds duplicate verses (same text, chapter, and verse number)."""
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT text_id, chapter, verse_number, COUNT(*)
        FROM verses
        GROUP BY text_id, chapter, verse_number
        HAVING COUNT(*) > 1
    """, conn)
    conn.close()
    return df

def main():
    print("="*80)
    print("DEPTH DATA INTEGRITY VALIDATION REPORT")
    print("="*80)

    # Test 1: Orphan Commentaries
    orphan_comms = check_orphan_commentaries()
    if not orphan_comms.empty:
        print("\n[FAIL] Found Orphan Commentaries:")
        print(orphan_comms)
    else:
        print("\n[PASS] No orphan commentaries found.")

    # Test 2: Orphan Cross-References
    orphan_refs = check_orphan_cross_references()
    if not orphan_refs.empty:
        print("\n[FAIL] Found Orphan Cross-References:")
        print(orphan_refs)
    else:
        print("\n[PASS] No orphan cross-references found.")

    # Test 3: Duplicate Verses
    duplicate_verses = check_duplicate_verses()
    if not duplicate_verses.empty:
        print("\n[FAIL] Found Duplicate Verses:")
        print(duplicate_verses)
    else:
        print("\n[PASS] No duplicate verses found.")

    print("="*80)

if __name__ == "__main__":
    main()
