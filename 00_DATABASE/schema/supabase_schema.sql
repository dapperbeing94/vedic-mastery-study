-- VEDIC MASTERY STUDY - POSTGRESQL SCHEMA FOR SUPABASE
-- Generated from SQLite database schema
-- Transformation 2.0 - Phase 1: Infrastructure Setup

-- Enable UUID extension for potential future use
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Disable foreign key checks during schema creation
SET session_replication_role = 'replica';


-- Table: analysis_history
CREATE TABLE IF NOT EXISTS analysis_history (
    id SERIAL PRIMARY KEY ,
    analysis_id INTEGER NOT NULL,
    old_text TEXT,
    new_text TEXT NOT NULL,
    change_reason TEXT,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER DEFAULT 1,
    FOREIGN KEY (analysis_id) REFERENCES verse_analysis(id)
);

-- Table: categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY ,
    name TEXT NOT NULL UNIQUE,
    parent_id INTEGER,
    level INTEGER NOT NULL,  -- 1=main, 2=sub, 3=sub-sub
    display_order INTEGER,
    description TEXT,
    target_breadth_score INTEGER DEFAULT 10,
    target_depth_score INTEGER DEFAULT 8,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

-- Table: classification_conflicts
CREATE TABLE IF NOT EXISTS classification_conflicts (
    id SERIAL PRIMARY KEY ,
    verse_id INTEGER NOT NULL,
    proposed_classifications TEXT,
    conflict_type TEXT NOT NULL,
    detected_date TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: classification_log
CREATE TABLE IF NOT EXISTS classification_log (
    id SERIAL PRIMARY KEY ,
    verse_id INTEGER,
    old_classification TEXT,
    new_classification TEXT NOT NULL,
    reason TEXT,
    changed_by TEXT DEFAULT 'system',
    changed_date TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: commentaries
CREATE TABLE IF NOT EXISTS commentaries (
            id SERIAL PRIMARY KEY ,
            verse_id INTEGER NOT NULL,
            commentator_id INTEGER NOT NULL,
            commentary_text TEXT,
            commentary_analysis TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP, commentary_source TEXT, is_original BOOLEAN DEFAULT FALSE, external_source_id INTEGER REFERENCES external_sources(id),
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (commentator_id) REFERENCES commentators(id)
        );

-- Table: commentators
CREATE TABLE IF NOT EXISTS commentators (
            id SERIAL PRIMARY KEY ,
            name TEXT NOT NULL,
            school TEXT,
            period TEXT,
            bio TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        , sanskrit_name TEXT, bio_summary TEXT);

-- Table: concept_relationships
CREATE TABLE IF NOT EXISTS concept_relationships (
    id SERIAL PRIMARY KEY ,
    concept_id_from INTEGER NOT NULL,
    concept_id_to INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,
    strength REAL DEFAULT 0.5,
    notes TEXT,
    FOREIGN KEY (concept_id_from) REFERENCES concepts(concept_id),
    FOREIGN KEY (concept_id_to) REFERENCES concepts(concept_id)
);

-- Table: concepts
CREATE TABLE IF NOT EXISTS concepts (
                id SERIAL PRIMARY KEY ,
                text_id INTEGER,
                concept_name TEXT NOT NULL,
                sanskrit_term TEXT,
                definition TEXT,
                context TEXT,
                practical_application TEXT, etymology TEXT, philosophical_context TEXT, category TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            );

-- Table: cross_references
CREATE TABLE IF NOT EXISTS cross_references (
                id SERIAL PRIMARY KEY ,
                source_text_id INTEGER,
                target_text_id INTEGER,
                connection_type TEXT,
                description TEXT, source_verse_id INTEGER, target_verse_id INTEGER, relationship_type TEXT,
                FOREIGN KEY (source_text_id) REFERENCES texts(id),
                FOREIGN KEY (target_text_id) REFERENCES texts(id)
            );

-- Table: deepening_queue
CREATE TABLE IF NOT EXISTS deepening_queue (
    id SERIAL PRIMARY KEY ,
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

-- Table: depth_criteria
CREATE TABLE IF NOT EXISTS depth_criteria (
    id SERIAL PRIMARY KEY ,
    text_id INTEGER NOT NULL,
    criterion_name TEXT NOT NULL,  -- e.g., "verse_analysis", "commentary_comparison"
    criterion_met BOOLEAN DEFAULT 0,
    evidence_file_path TEXT,
    last_checked TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- Table: external_sources
CREATE TABLE IF NOT EXISTS external_sources (
    id SERIAL PRIMARY KEY ,
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

-- Table: gap_analysis
CREATE TABLE IF NOT EXISTS gap_analysis (
    id SERIAL PRIMARY KEY ,
    category_id INTEGER,
    subcategory_id INTEGER,
    text_id INTEGER,
    gap_type TEXT NOT NULL,  -- "breadth", "depth", "synthesis"
    priority_score REAL,  -- Calculated priority
    recommendation TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    resolved BOOLEAN DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id),
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- Table: import_decisions
CREATE TABLE IF NOT EXISTS import_decisions (
    id SERIAL PRIMARY KEY ,
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

-- Table: progress_tracking
CREATE TABLE IF NOT EXISTS progress_tracking (
    id SERIAL PRIMARY KEY ,
    text_id INTEGER,
    category_id INTEGER,
    subcategory_id INTEGER,
    breadth_score INTEGER DEFAULT 0,
    depth_score INTEGER DEFAULT 0,
    combined_score REAL DEFAULT 0.0,
    last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (subcategory_id) REFERENCES subcategories(id)
);

-- Table: quality_metrics
CREATE TABLE IF NOT EXISTS quality_metrics (
    id SERIAL PRIMARY KEY ,
    verse_id INTEGER NOT NULL,
    analysis_completeness REAL DEFAULT 0.0,
    cross_ref_quality REAL DEFAULT 0.0,
    commentary_depth REAL DEFAULT 0.0,
    concept_clarity REAL DEFAULT 0.0,
    overall_quality REAL DEFAULT 0.0,
    last_assessed TEXT DEFAULT CURRENT_TIMESTAMP, commentary_integration REAL, cross_ref_density REAL, conceptual_clarity REAL, provenance REAL, assessment_date TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: reading_progress
CREATE TABLE IF NOT EXISTS reading_progress (
    id SERIAL PRIMARY KEY ,
    text_id INTEGER NOT NULL,
    verse_id INTEGER UNIQUE NOT NULL,
    read_status TEXT DEFAULT 'unread',
    read_date TEXT,
    analyzed_date TEXT,
    notes TEXT,
    FOREIGN KEY (text_id) REFERENCES texts(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: sanskrit_glossary
CREATE TABLE IF NOT EXISTS sanskrit_glossary (
                id SERIAL PRIMARY KEY ,
                term TEXT NOT NULL UNIQUE,
                transliteration TEXT,
                literal_meaning TEXT,
                contextual_meaning TEXT,
                related_terms TEXT,
                usage_examples TEXT
            );

-- Table: sanskrit_terms
CREATE TABLE IF NOT EXISTS sanskrit_terms (
    id SERIAL PRIMARY KEY ,
    term TEXT NOT NULL UNIQUE,
    sanskrit TEXT,
    meaning TEXT,
    source_text TEXT,
    usage_context TEXT
);

-- Table: session_log
CREATE TABLE IF NOT EXISTS session_log (
    id SERIAL PRIMARY KEY ,
    session_date TEXT NOT NULL,
    session_number INTEGER,
    focus_area TEXT,
    texts_studied TEXT,  -- JSON array of text IDs
    breadth_delta REAL,  -- Change in overall breadth
    depth_delta REAL,    -- Change in overall depth
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Table: source_texts
CREATE TABLE IF NOT EXISTS source_texts (
    id SERIAL PRIMARY KEY ,
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

-- Table: study_progress
CREATE TABLE IF NOT EXISTS study_progress (
    id SERIAL PRIMARY KEY ,
    text_name TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'not_started',
    start_date DATE,
    completion_date DATE,
    notes TEXT
);

-- Table: subcategories
CREATE TABLE IF NOT EXISTS subcategories (
    id SERIAL PRIMARY KEY ,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    expected_text_count INTEGER,  -- How many texts should be in this subcategory
    target_depth_score INTEGER DEFAULT 8,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Table: synthesis_documents
CREATE TABLE IF NOT EXISTS synthesis_documents (
    id SERIAL PRIMARY KEY ,
    title TEXT NOT NULL,
    synthesis_type TEXT,
    file_path TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    last_updated TEXT
);

-- Table: synthesis_sources
CREATE TABLE IF NOT EXISTS synthesis_sources (
    id SERIAL PRIMARY KEY ,
    synthesis_id INTEGER NOT NULL,
    verse_id INTEGER NOT NULL,
    contribution_type TEXT,
    notes TEXT,
    FOREIGN KEY (synthesis_id) REFERENCES synthesis_documents(id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: taxonomy
CREATE TABLE IF NOT EXISTS taxonomy (
    id SERIAL PRIMARY KEY ,
    classification_code TEXT UNIQUE NOT NULL,
    level INTEGER NOT NULL,
    parent_code TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_canonical BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (parent_code) REFERENCES taxonomy(classification_code)
);

-- Table: taxonomy_migrations
CREATE TABLE IF NOT EXISTS taxonomy_migrations (
    id SERIAL PRIMARY KEY ,
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

-- Table: taxonomy_proposals
CREATE TABLE IF NOT EXISTS taxonomy_proposals (
    id SERIAL PRIMARY KEY ,
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

-- Table: taxonomy_versions
CREATE TABLE IF NOT EXISTS taxonomy_versions (
    id SERIAL PRIMARY KEY ,
    version_number TEXT NOT NULL,
    taxonomy_snapshot TEXT,
    change_summary TEXT,
    created_date TEXT DEFAULT CURRENT_TIMESTAMP,
    is_current BOOLEAN DEFAULT FALSE
);

-- Table: texts
CREATE TABLE IF NOT EXISTS texts (
                id SERIAL PRIMARY KEY ,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                subcategory TEXT,
                language TEXT,
                approximate_date TEXT,
                tradition TEXT,
                source_url TEXT,
                study_status TEXT DEFAULT 'not_started',
                study_date TEXT,
                file_path TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            , classification_code TEXT REFERENCES taxonomy(classification_code));

-- Table: themes
CREATE TABLE IF NOT EXISTS themes (
            id SERIAL PRIMARY KEY ,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

-- Table: verse_analysis
CREATE TABLE IF NOT EXISTS verse_analysis (
    id SERIAL PRIMARY KEY ,
    verse_id INTEGER NOT NULL,
    analysis_text TEXT NOT NULL,
    keywords TEXT,
    author_id INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP, literal_meaning TEXT, philosophical_implication TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id)
);

-- Table: verse_classification
CREATE TABLE IF NOT EXISTS verse_classification (
    id SERIAL PRIMARY KEY ,
    verse_id INTEGER NOT NULL,
    classification_code TEXT NOT NULL,
    confidence_level TEXT DEFAULT 'definitive',
    classified_by TEXT DEFAULT 'system',
    classified_date TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (classification_code) REFERENCES taxonomy(classification_code)
);

-- Table: verse_concepts
CREATE TABLE IF NOT EXISTS verse_concepts (
    verse_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    relevance_score INTEGER DEFAULT 5,
    notes TEXT,
    PRIMARY KEY (verse_id, concept_id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id)
);

-- Table: verse_to_concept
CREATE TABLE IF NOT EXISTS verse_to_concept (
            verse_id INTEGER NOT NULL,
            concept_id INTEGER NOT NULL,
            PRIMARY KEY (verse_id, concept_id),
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (concept_id) REFERENCES concepts(id)
        );

-- Table: verse_to_theme
CREATE TABLE IF NOT EXISTS verse_to_theme (
            verse_id INTEGER NOT NULL,
            theme_id INTEGER NOT NULL,
            PRIMARY KEY (verse_id, theme_id),
            FOREIGN KEY (verse_id) REFERENCES verses(id),
            FOREIGN KEY (theme_id) REFERENCES themes(id)
        );

-- Table: verses
CREATE TABLE IF NOT EXISTS verses (
                id SERIAL PRIMARY KEY ,
                text_id INTEGER,
                chapter TEXT,
                verse_number TEXT,
                sanskrit_text TEXT,
                transliteration TEXT,
                translation TEXT,
                commentary TEXT,
                significance TEXT, word_by_word_analysis TEXT, commentary_summary TEXT, source_text_id INTEGER REFERENCES source_texts(id), source_translation TEXT, source_metadata TEXT, devanagari TEXT,
                FOREIGN KEY (text_id) REFERENCES texts(id)
            );

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


-- Re-enable foreign key checks
SET session_replication_role = 'origin';

-- Schema creation complete
