#!/usr/bin/env python3
"""
Generate PostgreSQL-compatible DDL from the existing SQLite database schema.
This script will create the schema for Supabase (PostgreSQL).
"""

import sqlite3
import os
from supabase import create_client, Client

# Configuration
SQLITE_DB_PATH = "00_DATABASE/vedic_knowledge.db"
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"

def get_sqlite_schema():
    """Extract the complete schema from the SQLite database."""
    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()
    
    # Get all table creation statements
    cursor.execute("""
        SELECT name, sql 
        FROM sqlite_master 
        WHERE type='table' 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    conn.close()
    
    return tables

def sqlite_to_postgres_type(sqlite_type):
    """Convert SQLite data types to PostgreSQL data types."""
    sqlite_type = sqlite_type.upper()
    
    type_mapping = {
        'INTEGER': 'INTEGER',
        'TEXT': 'TEXT',
        'REAL': 'REAL',
        'BOOLEAN': 'BOOLEAN',
        'BLOB': 'BYTEA',
    }
    
    # Handle types with modifiers (e.g., VARCHAR(255))
    for sqlite, postgres in type_mapping.items():
        if sqlite in sqlite_type:
            return postgres
    
    # Default to TEXT if unknown
    return 'TEXT'

def convert_sqlite_ddl_to_postgres(sqlite_ddl):
    """Convert SQLite CREATE TABLE statement to PostgreSQL."""
    if not sqlite_ddl:
        return None
    
    # Replace AUTOINCREMENT with SERIAL
    postgres_ddl = sqlite_ddl.replace('AUTOINCREMENT', '')
    postgres_ddl = postgres_ddl.replace('INTEGER PRIMARY KEY', 'SERIAL PRIMARY KEY')
    
    # Replace DEFAULT CURRENT_TIMESTAMP with PostgreSQL equivalent
    postgres_ddl = postgres_ddl.replace('DEFAULT CURRENT_TIMESTAMP', 'DEFAULT CURRENT_TIMESTAMP')
    
    # Add IF NOT EXISTS for safety
    postgres_ddl = postgres_ddl.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    
    return postgres_ddl

def generate_postgres_schema_file():
    """Generate a complete PostgreSQL schema file."""
    tables = get_sqlite_schema()
    
    schema_sql = """-- VEDIC MASTERY STUDY - POSTGRESQL SCHEMA FOR SUPABASE
-- Generated from SQLite database schema
-- Transformation 2.0 - Phase 1: Infrastructure Setup

-- Enable UUID extension for potential future use
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Disable foreign key checks during schema creation
SET session_replication_role = 'replica';

"""
    
    # Add all table creation statements
    for table_name, sqlite_ddl in tables:
        postgres_ddl = convert_sqlite_ddl_to_postgres(sqlite_ddl)
        if postgres_ddl:
            schema_sql += f"\n-- Table: {table_name}\n"
            schema_sql += postgres_ddl + ";\n"
    
    # Add new tables for Translation Layer (from TRANSLATION_LAYER_PROTOCOL.md)
    schema_sql += """
-- ============================================================================
-- TRANSLATION LAYER TABLES (NEW FOR TRANSFORMATION 2.0)
-- ============================================================================

-- Dictionary entries from Monier-Williams and other authoritative sources
CREATE TABLE IF NOT EXISTS dictionary_entries (
    id SERIAL PRIMARY KEY,
    headword TEXT NOT NULL,
    headword_devanagari TEXT,
    definition TEXT NOT NULL,
    part_of_speech TEXT,
    etymology TEXT,
    usage_examples TEXT,
    source TEXT NOT NULL, -- 'monier-williams', 'apte', etc.
    source_page TEXT,
    authority_score REAL DEFAULT 8.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pre-translated corpus from Itihasa and other sources
CREATE TABLE IF NOT EXISTS pre_translated_corpus (
    id SERIAL PRIMARY KEY,
    sanskrit_text TEXT NOT NULL,
    sanskrit_devanagari TEXT,
    english_translation TEXT NOT NULL,
    source TEXT NOT NULL, -- 'itihasa', 'gretil', etc.
    source_reference TEXT,
    translator TEXT,
    translation_quality_score REAL DEFAULT 7.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated BOOLEAN DEFAULT FALSE,
    validated_by TEXT,
    validated_at TIMESTAMP
);

-- Word stems for morphological analysis
CREATE TABLE IF NOT EXISTS word_stems (
    id SERIAL PRIMARY KEY,
    stem TEXT NOT NULL UNIQUE,
    stem_devanagari TEXT,
    root_meaning TEXT,
    grammatical_category TEXT, -- 'verb', 'noun', 'adjective', etc.
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grammatical rules for morphological analysis
CREATE TABLE IF NOT EXISTS grammatical_rules (
    id SERIAL PRIMARY KEY,
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL, -- 'sandhi', 'declension', 'conjugation', etc.
    rule_description TEXT,
    pattern TEXT,
    transformation TEXT,
    examples TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Translation cache to track LLM-generated translations
CREATE TABLE IF NOT EXISTS translation_cache (
    id SERIAL PRIMARY KEY,
    sanskrit_text TEXT NOT NULL UNIQUE,
    english_translation TEXT NOT NULL,
    translation_tier INTEGER NOT NULL, -- 1=dict, 2=corpus, 3=morpho, 4=llm
    llm_model TEXT,
    needs_review BOOLEAN DEFAULT FALSE,
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    review_status TEXT, -- 'pending', 'approved', 'rejected', 'corrected'
    corrected_translation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""
    
    # Add indexes for performance
    schema_sql += """
-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Core tables indexes
CREATE INDEX IF NOT EXISTS idx_verses_text_id ON verses(text_id);
CREATE INDEX IF NOT EXISTS idx_verses_source_text_id ON verses(source_text_id);
CREATE INDEX IF NOT EXISTS idx_commentaries_verse_id ON commentaries(verse_id);
CREATE INDEX IF NOT EXISTS idx_cross_references_source ON cross_references(source_verse_id);
CREATE INDEX IF NOT EXISTS idx_cross_references_target ON cross_references(target_verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_concepts_verse_id ON verse_concepts(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_concepts_concept_id ON verse_concepts(concept_id);

-- Taxonomy indexes
CREATE INDEX IF NOT EXISTS idx_taxonomy_parent_code ON taxonomy(parent_code);
CREATE INDEX IF NOT EXISTS idx_verse_classification_verse_id ON verse_classification(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_classification_code ON verse_classification(classification_code);

-- Translation Layer indexes
CREATE INDEX IF NOT EXISTS idx_dictionary_headword ON dictionary_entries(headword);
CREATE INDEX IF NOT EXISTS idx_dictionary_source ON dictionary_entries(source);
CREATE INDEX IF NOT EXISTS idx_corpus_sanskrit ON pre_translated_corpus(sanskrit_text);
CREATE INDEX IF NOT EXISTS idx_word_stems_stem ON word_stems(stem);
CREATE INDEX IF NOT EXISTS idx_translation_cache_text ON translation_cache(sanskrit_text);

-- Quality and progress indexes
CREATE INDEX IF NOT EXISTS idx_quality_metrics_verse_id ON quality_metrics(verse_id);
CREATE INDEX IF NOT EXISTS idx_reading_progress_text_id ON reading_progress(text_id);
CREATE INDEX IF NOT EXISTS idx_reading_progress_status ON reading_progress(read_status);
CREATE INDEX IF NOT EXISTS idx_deepening_queue_priority ON deepening_queue(priority_score DESC);

"""
    
    # Re-enable foreign key checks
    schema_sql += """
-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Schema creation complete
"""
    
    return schema_sql

def save_schema_to_file(schema_sql):
    """Save the generated schema to a file."""
    output_path = "00_DATABASE/schema/supabase_schema.sql"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(schema_sql)
    
    print(f"✅ PostgreSQL schema saved to: {output_path}")
    return output_path

def main():
    """Main execution function."""
    print("=" * 80)
    print("VEDIC MASTERY STUDY - TRANSFORMATION 2.0")
    print("Phase 1: Infrastructure Setup - Schema Generation")
    print("=" * 80)
    print()
    
    # Generate the schema
    print("📊 Extracting schema from SQLite database...")
    schema_sql = generate_postgres_schema_file()
    
    # Save to file
    print("💾 Saving PostgreSQL schema to file...")
    schema_path = save_schema_to_file(schema_sql)
    
    # Count tables
    table_count = schema_sql.count('CREATE TABLE')
    print(f"\n✅ Schema generation complete!")
    print(f"   - Total tables: {table_count}")
    print(f"   - Schema file: {schema_path}")
    print()
    print("Next step: Execute this schema on Supabase")
    print("=" * 80)

if __name__ == "__main__":
    main()
