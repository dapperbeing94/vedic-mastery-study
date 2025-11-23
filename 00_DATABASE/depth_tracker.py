#!/usr/bin/env python3
# ============================================================================
# VEDIC MASTERY STUDY - DEPTH TRACKER
# ============================================================================
# Purpose: Provides advanced tracking and analysis for the Depth Expansion Phase.
# Version: 2.0
# Date: November 23, 2025
# ============================================================================

import sqlite3
import argparse
import pandas as pd
from datetime import datetime

DB_PATH = '00_DATABASE/vedic_knowledge.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def calculate_depth_scores():
    """Calculates granular depth scores based on verse-level data."""
    conn = get_db_connection()
    
    # Use the pre-built view for efficiency
    df_metrics = pd.read_sql_query("SELECT * FROM text_depth_metrics", conn)
    
    # Define weights for depth calculation
    weights = {
        'translation_coverage_pct': 0.4,
        'avg_commentaries_per_verse': 0.4,
        'avg_cross_refs_per_verse': 0.2
    }
    
    # Normalize and calculate the final depth score
    # Normalization factors (can be adjusted as we add more data)
    norm_factors = {
        'translation_coverage_pct': 100.0, # Max is 100%
        'avg_commentaries_per_verse': 5.0, # Assume 5 commentaries is a good target
        'avg_cross_refs_per_verse': 10.0 # Assume 10 cross-refs is a good target
    }

    df_metrics['normalized_translation'] = (df_metrics['translation_coverage_pct'] / norm_factors['translation_coverage_pct']).clip(0, 1)
    df_metrics['normalized_commentaries'] = (df_metrics['avg_commentaries_per_verse'] / norm_factors['avg_commentaries_per_verse']).clip(0, 1)
    df_metrics['normalized_cross_refs'] = (df_metrics['avg_cross_refs_per_verse'] / norm_factors['avg_cross_refs_per_verse']).clip(0, 1)

    df_metrics['calculated_depth'] = (
        df_metrics['normalized_translation'] * weights['translation_coverage_pct'] +
        df_metrics['normalized_commentaries'] * weights['avg_commentaries_per_verse'] +
        df_metrics['normalized_cross_refs'] * weights['avg_cross_refs_per_verse']
    ) * 10 # Scale to 0-10

    # Update the progress_tracking table
    cursor = conn.cursor()
    for index, row in df_metrics.iterrows():
        cursor.execute("""
            UPDATE progress_tracking
            SET depth_score = ?,
                last_updated = ?
            WHERE text_id = ?
        """, (row['calculated_depth'], datetime.now().isoformat(), row['text_id']))
    
    conn.commit()
    conn.close()
    print("Depth scores recalculated and updated successfully!")

def display_dashboard():
    """Displays a comprehensive dashboard of the project's depth status."""
    conn = get_db_connection()
    df = pd.read_sql_query("""
        SELECT 
            t.category AS category,
            t.name AS text,
            pt.depth_score
        FROM progress_tracking pt
        JOIN texts t ON pt.text_id = t.id
        ORDER BY t.category, pt.depth_score DESC
    """, conn)
    conn.close()

    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 100)

    print("="*80)
    print("VEDIC MASTERY STUDY - DEPTH EXPANSION DASHBOARD")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*80)

    for category, group in df.groupby('category'):
        print(f"\nCATEGORY: {category}")
        print("-"*80)
        print(group[['text', 'depth_score']].to_string(index=False))

    print("="*80)

def main():
    parser = argparse.ArgumentParser(description="Vedic Mastery Study - Depth Tracker")
    parser.add_argument('--dashboard', action='store_true', help='Display the depth expansion dashboard.')
    parser.add_argument('--update', action='store_true', help='Recalculate and update all depth scores.')

    args = parser.parse_args()

    if args.update:
        calculate_depth_scores()
    elif args.dashboard:
        display_dashboard()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
