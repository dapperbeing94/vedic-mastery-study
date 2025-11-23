#!/usr/bin/env python3
"""
SQLite to Supabase Migration Script
Migrates all core Vedic data from SQLite to Supabase.

Source: vedic_knowledge.db (SQLite)
Target: Supabase tables
"""

import sqlite3
import json
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"

# SQLite database path
SQLITE_DB = "/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db"

# Batch size for imports
BATCH_SIZE = 1000

class DataMigrator:
    def __init__(self):
        self.sqlite_conn = sqlite3.connect(SQLITE_DB)
        self.sqlite_conn.row_factory = sqlite3.Row  # Access columns by name
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.stats = {}
        
    def migrate_table(self, table_name, transform_fn=None):
        """Migrate a single table from SQLite to Supabase"""
        print(f"\n📦 Migrating table: {table_name}")
        
        # Get all rows from SQLite
        cursor = self.sqlite_conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        total_rows = len(rows)
        print(f"   Found {total_rows} rows in SQLite")
        
        if total_rows == 0:
            print(f"   ⚠️  Table is empty, skipping")
            self.stats[table_name] = {'total': 0, 'imported': 0, 'failed': 0}
            return
        
        # Convert rows to dictionaries
        data = []
        for row in rows:
            row_dict = dict(row)
            
            # Apply transformation if provided
            if transform_fn:
                row_dict = transform_fn(row_dict)
            
            # Remove None values and convert to JSON-compatible types
            row_dict = {k: v for k, v in row_dict.items() if v is not None}
            data.append(row_dict)
        
        # Batch import to Supabase
        imported = 0
        failed = 0
        
        for i in range(0, len(data), BATCH_SIZE):
            batch = data[i:i + BATCH_SIZE]
            batch_num = (i // BATCH_SIZE) + 1
            
            try:
                result = self.supabase.table(table_name).insert(batch).execute()
                imported += len(batch)
                print(f"   ✅ Batch {batch_num} imported ({imported}/{total_rows})")
            except Exception as e:
                print(f"   ❌ Batch {batch_num} failed: {str(e)}")
                failed += len(batch)
        
        self.stats[table_name] = {
            'total': total_rows,
            'imported': imported,
            'failed': failed
        }
        
        print(f"   Completed: {imported} imported, {failed} failed")
    
    def migrate_all(self):
        """Migrate all tables in priority order"""
        print("🚀 Starting SQLite to Supabase Migration...")
        print(f"   Source: {SQLITE_DB}")
        print(f"   Target: Supabase ({SUPABASE_URL})")
        
        # Migration order (respecting dependencies)
        migration_order = [
            # Core taxonomy and categorization
            ('categories', None),
            ('subcategories', None),
            ('taxonomy', None),
            
            # Source and text metadata
            ('external_sources', None),
            ('texts', None),
            ('source_texts', None),
            
            # Core content
            ('verses', None),
            ('commentaries', None),
            ('commentators', None),
            
            # Concepts and relationships
            ('concepts', None),
            ('themes', None),
            ('concept_relationships', None),
            
            # Verse relationships
            ('verse_concepts', None),
            ('verse_to_concept', None),
            ('verse_to_theme', None),
            ('verse_classification', None),
            ('cross_references', None),
            
            # Analysis and quality
            ('verse_analysis', None),
            ('analysis_history', None),
            ('quality_metrics', None),
            ('gap_analysis', None),
            
            # Study progress
            ('reading_progress', None),
            ('study_progress', None),
            ('session_log', None),
            ('progress_tracking', None),
            ('deepening_queue', None),
            
            # Taxonomy management
            ('taxonomy_versions', None),
            ('taxonomy_migrations', None),
            ('taxonomy_proposals', None),
            ('classification_log', None),
            ('classification_conflicts', None),
            
            # Synthesis and depth
            ('synthesis_documents', None),
            ('synthesis_sources', None),
            ('depth_criteria', None),
            
            # Glossary
            ('sanskrit_terms', None),
            ('sanskrit_glossary', None),
            
            # Import tracking
            ('import_decisions', None),
        ]
        
        # Migrate each table
        for table_name, transform_fn in migration_order:
            try:
                self.migrate_table(table_name, transform_fn)
            except Exception as e:
                print(f"   ❌ Error migrating {table_name}: {str(e)}")
                self.stats[table_name] = {'total': 0, 'imported': 0, 'failed': 0, 'error': str(e)}
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print migration summary"""
        print("\n" + "="*60)
        print("📊 MIGRATION SUMMARY")
        print("="*60)
        
        total_rows = 0
        total_imported = 0
        total_failed = 0
        
        for table_name, stats in self.stats.items():
            total_rows += stats.get('total', 0)
            total_imported += stats.get('imported', 0)
            total_failed += stats.get('failed', 0)
            
            if stats.get('total', 0) > 0:
                success_rate = (stats['imported'] / stats['total'] * 100) if stats['total'] > 0 else 0
                print(f"\n{table_name}:")
                print(f"  Total: {stats['total']:,}")
                print(f"  Imported: {stats['imported']:,}")
                print(f"  Failed: {stats['failed']:,}")
                print(f"  Success Rate: {success_rate:.1f}%")
        
        print("\n" + "="*60)
        print(f"OVERALL TOTALS:")
        print(f"  Total Rows: {total_rows:,}")
        print(f"  Successfully Imported: {total_imported:,}")
        print(f"  Failed: {total_failed:,}")
        if total_rows > 0:
            overall_success = (total_imported / total_rows * 100)
            print(f"  Overall Success Rate: {overall_success:.1f}%")
        print("="*60)
    
    def close(self):
        """Close database connections"""
        self.sqlite_conn.close()


def main():
    migrator = DataMigrator()
    
    try:
        migrator.migrate_all()
    finally:
        migrator.close()
    
    print("\n✅ Migration Complete!")


if __name__ == "__main__":
    main()
