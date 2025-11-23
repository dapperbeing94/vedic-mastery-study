#!/usr/bin/env python3
"""
Clear Core Tables in Supabase
Clears all existing data from core Vedic tables (preserving linguistic resources).

This prepares the database for a fresh migration from SQLite.
"""

from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"

# Tables to clear (in reverse dependency order)
# NOTE: We preserve dictionary_entries, pre_translated_corpus, word_stems, 
# grammatical_rules, and translation_cache (Translation Layer tables)
TABLES_TO_CLEAR = [
    # Import tracking
    'import_decisions',
    
    # Glossary
    'sanskrit_glossary',
    'sanskrit_terms',
    
    # Synthesis and depth
    'depth_criteria',
    'synthesis_sources',
    'synthesis_documents',
    
    # Taxonomy management
    'classification_conflicts',
    'classification_log',
    'taxonomy_proposals',
    'taxonomy_migrations',
    'taxonomy_versions',
    
    # Study progress
    'deepening_queue',
    'progress_tracking',
    'session_log',
    'study_progress',
    'reading_progress',
    
    # Analysis and quality
    'gap_analysis',
    'quality_metrics',
    'analysis_history',
    'verse_analysis',
    
    # Verse relationships
    'cross_references',
    'verse_classification',
    'verse_to_theme',
    'verse_to_concept',
    'verse_concepts',
    
    # Concepts and relationships
    'concept_relationships',
    'themes',
    'concepts',
    
    # Core content
    'commentators',
    'commentaries',
    'verses',
    
    # Source and text metadata
    'source_texts',
    'texts',
    'external_sources',
    
    # Core taxonomy and categorization
    'taxonomy',
    'subcategories',
    'categories',
]


def clear_tables():
    """Clear all core tables in Supabase"""
    print("🗑️  Clearing Core Tables in Supabase...")
    print(f"   Target: {SUPABASE_URL}")
    print(f"   Tables to clear: {len(TABLES_TO_CLEAR)}")
    print("\n   ⚠️  This will DELETE all data from core tables!")
    print("   ✅ Translation Layer tables will be PRESERVED")
    
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    cleared_count = 0
    failed_count = 0
    
    for table_name in TABLES_TO_CLEAR:
        try:
            print(f"\n   Clearing {table_name}...", end=" ")
            
            # Delete all rows from the table
            # Using a large limit to ensure we get all rows
            result = supabase.table(table_name).delete().neq('id', 0).execute()
            
            print(f"✅ Cleared")
            cleared_count += 1
            
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            failed_count += 1
    
    print(f"\n\n{'='*60}")
    print(f"CLEARING SUMMARY:")
    print(f"  Tables cleared: {cleared_count}")
    print(f"  Tables failed: {failed_count}")
    print(f"{'='*60}")
    
    if failed_count == 0:
        print("\n✅ All core tables cleared successfully!")
        print("   Ready for fresh migration from SQLite")
    else:
        print(f"\n⚠️  {failed_count} tables failed to clear")
        print("   Please review errors above")


if __name__ == "__main__":
    clear_tables()
