> **Note**: This document contains the specific SQL commands for migrating the database from v1 (14 tables) to v2 (34 tables). The complete architecture is described in `ARCHITECTURE_DOCUMENTATION.md`.

---

## 1. Summary of Changes

-   **New Tables**: 20
-   **Modified Tables**: 4
-   **Total Tables (v2)**: 34

This migration introduces the Source/Analytical layer separation, a hierarchical taxonomy system, quality and progress tracking, and self-evolution capabilities.

---

## 2. Migration Script (`migrate_to_v2.sql`)

```sql
-- VEDIC MASTERY STUDY - DATABASE MIGRATION SCRIPT V1 TO V2

PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- GROUP 1: SOURCE LAYER TABLES (NEW)
-- Stores metadata about external repositories
CREATE TABLE external_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_name TEXT UNIQUE NOT NULL,
    repo_url TEXT,
    commit_hash TEXT,
    license TEXT,
    import_date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    authority_score REAL DEFAULT 5.0,
    authority_basis TEXT,
    peer_reviewed BOOLEAN DEFAULT FALSE,
    institutional_source TEXT
);

-- Stores metadata about specific files/datasets from external sources
CREATE TABLE source_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER,
    external_source_id INTEGER,
    language TEXT NOT NULL,
    format TEXT,
    file_path TEXT NOT NULL,
    import_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_original BOOLEAN DEFAULT TRUE, -- True for original language, False for translation
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (external_source_id) REFERENCES external_sources(id)
);

-- GROUP 2: ANALYTICAL LAYER TABLES (NEW)
-- Stores our detailed analysis of each verse
CREATE TABLE verse_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    analysis_text TEXT NOT NULL,
    keywords TEXT,
    author_id INTEGER DEFAULT 1, -- 1 for Manus AI
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Tracks the history of changes to our analysis
CREATE TABLE analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id INTEGER NOT NULL,
    old_text TEXT,
    new_text TEXT NOT NULL,
    change_reason TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER DEFAULT 1,
    FOREIGN KEY (analysis_id) REFERENCES verse_analysis(id)
);

-- GROUP 3: TAXONOMY SYSTEM TABLES (NEW)
-- The hierarchical classification system (our Dewey Decimal system)
CREATE TABLE taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classification_code TEXT UNIQUE NOT NULL,
    level INTEGER NOT NULL, -- 1=Category, 2=Subcategory, 3=Division, 4=Section, 5=Verse
    parent_code TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_canonical BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_code) REFERENCES taxonomy(classification_code)
);

-- Links each verse to its classification in the taxonomy
CREATE TABLE verse_classification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    classification_code TEXT NOT NULL,
    confidence_level TEXT DEFAULT 'definitive', -- 'definitive', 'probable', 'provisional'
    classified_by TEXT DEFAULT 'system', -- 'system', 'manual', 'ai'
    classified_date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (classification_code) REFERENCES taxonomy(classification_code)
);

-- Logs all classification decisions and changes for audit purposes
CREATE TABLE classification_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER,
    old_classification TEXT,
    new_classification TEXT NOT NULL,
    reason TEXT,
    changed_by TEXT DEFAULT 'system',
    changed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- GROUP 4: TRANSFORMATION & EVOLUTION TABLES (NEW)
-- Automatically logs verses that are difficult to classify
CREATE TABLE classification_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    proposed_classifications TEXT, -- JSON array of possible codes
    conflict_type TEXT NOT NULL, -- 'multiple_matches', 'no_match', 'hybrid'
    detected_date TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Stores AI-generated proposals for new taxonomy branches
CREATE TABLE taxonomy_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_type TEXT NOT NULL, -- 'new_branch', 'hybrid', 'restructure'
    proposed_code TEXT,
    proposed_name TEXT,
    proposed_parent_code TEXT,
    justification TEXT,
    affected_verses INTEGER,
    proposed_by TEXT DEFAULT 'system',
    proposed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending', -- 'pending', 'approved', 'rejected', 'implemented'
    reviewed_by TEXT,
    reviewed_date TEXT
);

-- Logs all schema migration scripts for the taxonomy
CREATE TABLE taxonomy_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_name TEXT NOT NULL,
    from_structure TEXT, -- JSON snapshot of old taxonomy
    to_structure TEXT, -- JSON snapshot of new taxonomy
    migration_script TEXT,
    rollback_script TEXT,
    executed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    executed_by TEXT DEFAULT 'system',
    success BOOLEAN,
    error_log TEXT
);

-- Provides version control for the taxonomy itself
CREATE TABLE taxonomy_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_number TEXT NOT NULL,
    taxonomy_snapshot TEXT, -- JSON of entire taxonomy at this version
    change_summary TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT FALSE
);

-- GROUP 5: QUALITY & PROGRESS TRACKING TABLES (NEW)
-- Stores quality scores for our analysis on a per-verse basis
CREATE TABLE quality_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    analysis_completeness REAL DEFAULT 0.0,
    cross_ref_quality REAL DEFAULT 0.0,
    commentary_depth REAL DEFAULT 0.0,
    concept_clarity REAL DEFAULT 0.0,
    overall_quality REAL DEFAULT 0.0,
    last_assessed TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Tracks the reading status for every verse in the database
CREATE TABLE reading_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    verse_id INTEGER UNIQUE NOT NULL,
    read_status TEXT DEFAULT 'unread', -- 'unread', 'read', 'analyzed', 'deep_dive'
    read_date TEXT,
    analyzed_date TEXT,
    notes TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- A prioritized to-do list of texts that require further deepening
CREATE TABLE deepening_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER UNIQUE NOT NULL,
    current_depth_score REAL DEFAULT 0.0,
    target_depth_score REAL DEFAULT 8.0,
    priority_score REAL DEFAULT 0.0,
    gaps_identified TEXT, -- JSON array of gaps
    next_action TEXT,
    assigned_to TEXT DEFAULT 'vedic_sage',
    status TEXT DEFAULT 'pending', -- 'pending', 'in_progress', 'complete'
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- GROUP 6: LOGGING & PROVENANCE TABLES (NEW)
-- Logs every import operation
CREATE TABLE import_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_file TEXT NOT NULL,
    verse_count INTEGER,
    classification_assigned TEXT,
    auto_classified_count INTEGER,
    manual_classified_count INTEGER,
    conflicts_detected INTEGER,
    import_date TEXT DEFAULT CURRENT_TIMESTAMP,
    imported_by TEXT DEFAULT 'system',
    notes TEXT
);

-- GROUP 7: SYNTHESIS & CONCEPT HIERARCHY TABLES (NEW)
-- Defines the ontology of concepts
CREATE TABLE concept_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id_from INTEGER NOT NULL,
    concept_id_to INTEGER NOT NULL,
    relationship_type TEXT NOT NULL, -- 'is_a', 'part_of', 'leads_to', 'opposes'
    strength REAL DEFAULT 0.5,
    notes TEXT,
    FOREIGN KEY (concept_id_from) REFERENCES concepts(concept_id),
    FOREIGN KEY (concept_id_to) REFERENCES concepts(concept_id)
);

-- Catalogs our high-level synthesis documents
CREATE TABLE synthesis_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    synthesis_type TEXT, -- 'thematic', 'conceptual', 'comparative'
    file_path TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT
);

-- Links a synthesis document back to every source verse that contributed to it
CREATE TABLE synthesis_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synthesis_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    contribution_type TEXT, -- 'primary', 'supporting', 'contrasting'
    notes TEXT,
    FOREIGN KEY (synthesis_id) REFERENCES synthesis_documents(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- MODIFY EXISTING TABLES

-- Add source tracking and Devanagari script to verses table
ALTER TABLE verses ADD COLUMN source_text_id INTEGER REFERENCES source_texts(id);
ALTER TABLE verses ADD COLUMN source_translation TEXT;
ALTER TABLE verses ADD COLUMN source_metadata TEXT;
ALTER TABLE verses ADD COLUMN devanagari TEXT;

-- Add source tracking to commentaries table
ALTER TABLE commentaries ADD COLUMN commentary_source TEXT;
ALTER TABLE commentaries ADD COLUMN is_original BOOLEAN DEFAULT FALSE;
ALTER TABLE commentaries ADD COLUMN external_source_id INTEGER REFERENCES external_sources(id);

-- Add document type to study_documents table
ALTER TABLE study_documents ADD COLUMN document_type TEXT DEFAULT 'analytical';

-- Add classification code to texts table
ALTER TABLE texts ADD COLUMN classification_code TEXT REFERENCES taxonomy(classification_code);

COMMIT;
PRAGMA foreign_keys=on;

```

---

## 3. Rollback Script (`rollback_from_v2.sql`)

This script will revert the database to its v1 state. **Warning: This is a destructive operation and will delete all data in the new tables.**

```sql
-- VEDIC MASTERY STUDY - DATABASE ROLLBACK SCRIPT V2 TO V1

PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- DROP ALL NEW TABLES
DROP TABLE IF EXISTS external_sources;
DROP TABLE IF EXISTS source_texts;
DROP TABLE IF EXISTS verse_analysis;
DROP TABLE IF EXISTS analysis_history;
DROP TABLE IF EXISTS taxonomy;
DROP TABLE IF EXISTS verse_classification;
DROP TABLE IF EXISTS classification_log;
DROP TABLE IF EXISTS classification_conflicts;
DROP TABLE IF EXISTS taxonomy_proposals;
DROP TABLE IF EXISTS taxonomy_migrations;
DROP TABLE IF EXISTS taxonomy_versions;
DROP TABLE IF EXISTS quality_metrics;
DROP TABLE IF EXISTS reading_progress;
DROP TABLE IF EXISTS deepening_queue;
DROP TABLE IF EXISTS import_decisions;
DROP TABLE IF EXISTS concept_relationships;
DROP TABLE IF EXISTS synthesis_documents;
DROP TABLE IF EXISTS synthesis_sources;

-- RECREATE MODIFIED TABLES TO REMOVE NEW COLUMNS

-- Recreate verses table
CREATE TABLE verses_v1 (
    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    chapter INTEGER,
    verse_number INTEGER,
    sanskrit_text TEXT,
    transliteration TEXT,
    translation TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);
INSERT INTO verses_v1 (verse_id, text_id, chapter, verse_number, sanskrit_text, transliteration, translation, notes, created_at)
SELECT verse_id, text_id, chapter, verse_number, sanskrit_text, transliteration, translation, notes, created_at FROM verses;
DROP TABLE verses;
ALTER TABLE verses_v1 RENAME TO verses;

-- Recreate commentaries table
CREATE TABLE commentaries_v1 (
    commentary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    commentator_id INTEGER,
    commentary_text TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (commentator_id) REFERENCES commentators(id)
);
INSERT INTO commentaries_v1 (commentary_id, verse_id, commentator_id, commentary_text, created_at)
SELECT commentary_id, verse_id, commentator_id, commentary_text, created_at FROM commentaries;
DROP TABLE commentaries;
ALTER TABLE commentaries_v1 RENAME TO commentaries;

-- Recreate study_documents table
CREATE TABLE study_documents_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER,
    file_path TEXT NOT NULL,
    word_count INTEGER,
    version TEXT,
    last_updated TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);
INSERT INTO study_documents_v1 (id, text_id, file_path, word_count, version, last_updated)
SELECT id, text_id, file_path, word_count, version, last_updated FROM study_documents;
DROP TABLE study_documents;
ALTER TABLE study_documents_v1 RENAME TO study_documents;

-- Recreate texts table
CREATE TABLE texts_v1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    description TEXT,
    word_count INTEGER,
    author TEXT,
    period TEXT
);
INSERT INTO texts_v1 (id, title, category, description, word_count, author, period)
SELECT id, title, category, description, word_count, author, period FROM texts;
DROP TABLE texts;
ALTER TABLE texts_v1 RENAME TO texts;

COMMIT;
PRAGMA foreign_keys=on;

```
