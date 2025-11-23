-- VEDIC MASTERY STUDY - DATABASE MIGRATION SCRIPT V1 TO V2
-- Date: November 23, 2025
-- Purpose: Evolve database from 14 tables to 34 tables with Source/Analytical layer separation

PRAGMA foreign_keys=off;
BEGIN TRANSACTION;

-- GROUP 1: SOURCE LAYER TABLES (NEW)
-- Stores metadata about external repositories
CREATE TABLE IF NOT EXISTS external_sources (
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
CREATE TABLE IF NOT EXISTS source_texts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER,
    external_source_id INTEGER,
    language TEXT NOT NULL,
    format TEXT,
    file_path TEXT NOT NULL,
    import_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_original BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (external_source_id) REFERENCES external_sources(id)
);

-- GROUP 2: ANALYTICAL LAYER TABLES (NEW)
-- Stores our detailed analysis of each verse
CREATE TABLE IF NOT EXISTS verse_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    analysis_text TEXT NOT NULL,
    keywords TEXT,
    author_id INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Tracks the history of changes to our analysis
CREATE TABLE IF NOT EXISTS analysis_history (
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
-- The hierarchical classification system
CREATE TABLE IF NOT EXISTS taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    classification_code TEXT UNIQUE NOT NULL,
    level INTEGER NOT NULL,
    parent_code TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_canonical BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_code) REFERENCES taxonomy(classification_code)
);

-- Links each verse to its classification in the taxonomy
CREATE TABLE IF NOT EXISTS verse_classification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    classification_code TEXT NOT NULL,
    confidence_level TEXT DEFAULT 'definitive',
    classified_by TEXT DEFAULT 'system',
    classified_date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (classification_code) REFERENCES taxonomy(classification_code)
);

-- Logs all classification decisions and changes
CREATE TABLE IF NOT EXISTS classification_log (
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
-- Logs verses that are difficult to classify
CREATE TABLE IF NOT EXISTS classification_conflicts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    proposed_classifications TEXT,
    conflict_type TEXT NOT NULL,
    detected_date TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Stores AI-generated proposals for new taxonomy branches
CREATE TABLE IF NOT EXISTS taxonomy_proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_type TEXT NOT NULL,
    proposed_code TEXT,
    proposed_name TEXT,
    proposed_parent_code TEXT,
    justification TEXT,
    affected_verses INTEGER,
    proposed_by TEXT DEFAULT 'system',
    proposed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'pending',
    reviewed_by TEXT,
    reviewed_date TEXT
);

-- Logs all schema migration scripts
CREATE TABLE IF NOT EXISTS taxonomy_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    migration_name TEXT NOT NULL,
    from_structure TEXT,
    to_structure TEXT,
    migration_script TEXT,
    rollback_script TEXT,
    executed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    executed_by TEXT DEFAULT 'system',
    success BOOLEAN,
    error_log TEXT
);

-- Provides version control for the taxonomy
CREATE TABLE IF NOT EXISTS taxonomy_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_number TEXT NOT NULL,
    taxonomy_snapshot TEXT,
    change_summary TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT FALSE
);

-- GROUP 5: QUALITY & PROGRESS TRACKING TABLES (NEW)
-- Stores quality scores for analysis
CREATE TABLE IF NOT EXISTS quality_metrics (
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

-- Tracks reading status for every verse
CREATE TABLE IF NOT EXISTS reading_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    verse_id INTEGER UNIQUE NOT NULL,
    read_status TEXT DEFAULT 'unread',
    read_date TEXT,
    analyzed_date TEXT,
    notes TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Prioritized to-do list for deepening
CREATE TABLE IF NOT EXISTS deepening_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER UNIQUE NOT NULL,
    current_depth_score REAL DEFAULT 0.0,
    target_depth_score REAL DEFAULT 8.0,
    priority_score REAL DEFAULT 0.0,
    gaps_identified TEXT,
    next_action TEXT,
    assigned_to TEXT DEFAULT 'vedic_sage',
    status TEXT DEFAULT 'pending',
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- GROUP 6: LOGGING & PROVENANCE TABLES (NEW)
-- Logs every import operation
CREATE TABLE IF NOT EXISTS import_decisions (
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
CREATE TABLE IF NOT EXISTS concept_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_id_from INTEGER NOT NULL,
    concept_id_to INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,
    strength REAL DEFAULT 0.5,
    notes TEXT,
    FOREIGN KEY (concept_id_from) REFERENCES concepts(concept_id),
    FOREIGN KEY (concept_id_to) REFERENCES concepts(concept_id)
);

-- Catalogs synthesis documents
CREATE TABLE IF NOT EXISTS synthesis_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    synthesis_type TEXT,
    file_path TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT
);

-- Links synthesis docs to source verses
CREATE TABLE IF NOT EXISTS synthesis_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synthesis_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    contribution_type TEXT,
    notes TEXT,
    FOREIGN KEY (synthesis_id) REFERENCES synthesis_documents(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- MODIFY EXISTING TABLES
-- Add source tracking to verses table
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

-- CREATE INDEXES FOR PERFORMANCE
CREATE INDEX IF NOT EXISTS idx_verse_analysis_verse ON verse_analysis(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_classification_verse ON verse_classification(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_classification_code ON verse_classification(classification_code);
CREATE INDEX IF NOT EXISTS idx_quality_metrics_verse ON quality_metrics(verse_id);
CREATE INDEX IF NOT EXISTS idx_reading_progress_text ON reading_progress(text_id);
CREATE INDEX IF NOT EXISTS idx_reading_progress_verse ON reading_progress(verse_id);
CREATE INDEX IF NOT EXISTS idx_taxonomy_code ON taxonomy(classification_code);
CREATE INDEX IF NOT EXISTS idx_taxonomy_parent ON taxonomy(parent_code);

COMMIT;
PRAGMA foreign_keys=on;
