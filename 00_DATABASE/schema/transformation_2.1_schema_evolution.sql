-- TRANSFORMATION 2.1 SCHEMA EVOLUTION
-- Purpose: Add foundational columns and tables for AI/ML capabilities
-- Status: Foundation only - NO DATA POPULATION
-- Activation: Transformation 3.0

-- ============================================================================
-- SECTION 1: ENABLE PGVECTOR EXTENSION
-- ============================================================================

-- Enable pgvector for embedding storage
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- SECTION 2: ADD EMBEDDING COLUMNS TO EXISTING TABLES
-- ============================================================================

-- Add embedding columns to verses table
ALTER TABLE verses 
ADD COLUMN IF NOT EXISTS embedding_vector vector(1536),
ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(50),
ADD COLUMN IF NOT EXISTS embedding_generated_at TIMESTAMP;

-- Add embedding columns to pre_translated_corpus table
ALTER TABLE pre_translated_corpus
ADD COLUMN IF NOT EXISTS embedding_vector vector(1536),
ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(50),
ADD COLUMN IF NOT EXISTS embedding_generated_at TIMESTAMP;

-- Add embedding columns to dictionary_entries table
ALTER TABLE dictionary_entries
ADD COLUMN IF NOT EXISTS embedding_vector vector(1536),
ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(50),
ADD COLUMN IF NOT EXISTS embedding_generated_at TIMESTAMP;

-- Add embedding columns to concepts table
ALTER TABLE concepts
ADD COLUMN IF NOT EXISTS embedding_vector vector(1536),
ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(50),
ADD COLUMN IF NOT EXISTS embedding_generated_at TIMESTAMP;

-- ============================================================================
-- SECTION 3: CREATE AI INTERACTION LOGGING TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_interaction_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    provider VARCHAR(50) NOT NULL,  -- 'openai', 'anthropic', 'perplexity'
    model VARCHAR(100) NOT NULL,    -- 'gpt-4-turbo', 'claude-3-sonnet', etc.
    operation VARCHAR(50) NOT NULL, -- 'generate', 'embed', 'validate'
    tokens_used INTEGER,
    cost DECIMAL(10, 6),
    verse_id INTEGER REFERENCES verses(id),
    request_data JSONB,
    response_data JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_interaction_timestamp ON ai_interaction_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_ai_interaction_provider ON ai_interaction_log(provider);
CREATE INDEX IF NOT EXISTS idx_ai_interaction_verse ON ai_interaction_log(verse_id);

-- ============================================================================
-- SECTION 4: CREATE AI-GENERATED INSIGHTS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_generated_insights (
    id SERIAL PRIMARY KEY,
    verse_id INTEGER NOT NULL REFERENCES verses(id),
    insight_type VARCHAR(50) NOT NULL, -- 'philosophical', 'practical', 'historical', 'conceptual'
    content TEXT NOT NULL,
    model VARCHAR(100) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    confidence_score DECIMAL(3, 2), -- 0.00 to 1.00
    human_validated BOOLEAN DEFAULT FALSE,
    validator_notes TEXT,
    source_references JSONB, -- Array of source citations
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_insights_verse ON ai_generated_insights(verse_id);
CREATE INDEX IF NOT EXISTS idx_ai_insights_type ON ai_generated_insights(insight_type);
CREATE INDEX IF NOT EXISTS idx_ai_insights_validated ON ai_generated_insights(human_validated);

-- ============================================================================
-- SECTION 5: CREATE KNOWLEDGE EVOLUTION LOG TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS knowledge_evolution_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    evolution_type VARCHAR(50) NOT NULL, -- 'schema_change', 'data_addition', 'insight_generation', 'relationship_discovery'
    component VARCHAR(100) NOT NULL,     -- 'verses', 'concepts', 'taxonomy', etc.
    change_description TEXT NOT NULL,
    triggered_by VARCHAR(50),            -- 'human', 'ai', 'automated'
    impact_assessment JSONB,             -- What was affected by this change
    rollback_data JSONB,                 -- Data needed to rollback if necessary
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_evolution_timestamp ON knowledge_evolution_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_evolution_type ON knowledge_evolution_log(evolution_type);
CREATE INDEX IF NOT EXISTS idx_evolution_component ON knowledge_evolution_log(component);

-- ============================================================================
-- SECTION 6: CREATE DATA VALIDATION QUEUE TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS data_validation_queue (
    id SERIAL PRIMARY KEY,
    data_type VARCHAR(50) NOT NULL,     -- 'verse', 'commentary', 'concept', etc.
    data_payload JSONB NOT NULL,
    validation_status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    validation_stage VARCHAR(50),       -- 'format', 'duplicate', 'contradiction', 'quality', 'authenticity'
    validation_report JSONB,
    quality_score DECIMAL(3, 2),
    priority INTEGER DEFAULT 5,         -- 1-10, higher = more urgent
    reviewer VARCHAR(100),
    review_notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    reviewed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_validation_status ON data_validation_queue(validation_status);
CREATE INDEX IF NOT EXISTS idx_validation_priority ON data_validation_queue(priority DESC);
CREATE INDEX IF NOT EXISTS idx_validation_created ON data_validation_queue(created_at);

-- ============================================================================
-- SECTION 7: CREATE SYSTEM HEALTH LOG TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS system_health_log (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    health_score DECIMAL(3, 2) NOT NULL, -- 0.00 to 1.00
    check_results JSONB NOT NULL,        -- Array of individual check results
    issues_found INTEGER DEFAULT 0,
    auto_repairs_performed INTEGER DEFAULT 0,
    alerts_sent INTEGER DEFAULT 0,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_health_timestamp ON system_health_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_health_score ON system_health_log(health_score);

-- ============================================================================
-- SECTION 8: CREATE SEMANTIC SEARCH CACHE TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS semantic_search_cache (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    query_embedding vector(1536) NOT NULL,
    results JSONB NOT NULL,              -- Cached search results
    result_count INTEGER NOT NULL,
    search_parameters JSONB,             -- Filters, limits, etc.
    hit_count INTEGER DEFAULT 1,
    last_accessed TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_semantic_cache_embedding ON semantic_search_cache 
USING ivfflat (query_embedding vector_cosine_ops);

-- ============================================================================
-- SECTION 9: CREATE MODEL FINE-TUNING TRACKING TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS model_fine_tuning_log (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    base_model VARCHAR(100) NOT NULL,
    training_dataset VARCHAR(200),
    training_started TIMESTAMP,
    training_completed TIMESTAMP,
    training_status VARCHAR(50),         -- 'pending', 'in_progress', 'completed', 'failed'
    performance_metrics JSONB,
    cost DECIMAL(10, 2),
    deployment_status VARCHAR(50),       -- 'not_deployed', 'staging', 'production'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_fine_tuning_status ON model_fine_tuning_log(training_status);
CREATE INDEX IF NOT EXISTS idx_fine_tuning_deployment ON model_fine_tuning_log(deployment_status);

-- ============================================================================
-- SECTION 10: CREATE VECTOR INDEXES (FOR FUTURE USE)
-- ============================================================================

-- Note: These indexes will be created but not used until embeddings are populated in 3.0

-- Verses embedding index
CREATE INDEX IF NOT EXISTS idx_verses_embedding ON verses 
USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 100);

-- Corpus embedding index
CREATE INDEX IF NOT EXISTS idx_corpus_embedding ON pre_translated_corpus 
USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 100);

-- Dictionary embedding index
CREATE INDEX IF NOT EXISTS idx_dictionary_embedding ON dictionary_entries 
USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 100);

-- Concepts embedding index
CREATE INDEX IF NOT EXISTS idx_concepts_embedding ON concepts 
USING ivfflat (embedding_vector vector_cosine_ops)
WITH (lists = 10);

-- ============================================================================
-- SECTION 11: ADD METADATA COLUMNS FOR PROVENANCE TRACKING
-- ============================================================================

-- Add provenance tracking to key tables
ALTER TABLE verses
ADD COLUMN IF NOT EXISTS data_source VARCHAR(100),
ADD COLUMN IF NOT EXISTS import_batch_id VARCHAR(50),
ADD COLUMN IF NOT EXISTS last_validated TIMESTAMP,
ADD COLUMN IF NOT EXISTS validation_status VARCHAR(20) DEFAULT 'unvalidated';

ALTER TABLE commentaries
ADD COLUMN IF NOT EXISTS data_source VARCHAR(100),
ADD COLUMN IF NOT EXISTS import_batch_id VARCHAR(50),
ADD COLUMN IF NOT EXISTS last_validated TIMESTAMP,
ADD COLUMN IF NOT EXISTS validation_status VARCHAR(20) DEFAULT 'unvalidated';

ALTER TABLE concepts
ADD COLUMN IF NOT EXISTS data_source VARCHAR(100),
ADD COLUMN IF NOT EXISTS import_batch_id VARCHAR(50),
ADD COLUMN IF NOT EXISTS last_validated TIMESTAMP,
ADD COLUMN IF NOT EXISTS validation_status VARCHAR(20) DEFAULT 'unvalidated';

-- ============================================================================
-- SECTION 12: CREATE DEPENDENCY TRACKING TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS component_dependencies (
    id SERIAL PRIMARY KEY,
    component_name VARCHAR(100) NOT NULL,
    component_type VARCHAR(50) NOT NULL, -- 'database', 'api', 'service', 'protocol', 'ml'
    depends_on VARCHAR(100) NOT NULL,
    dependency_type VARCHAR(50) NOT NULL, -- 'database', 'api', 'service', 'protocol', 'ml'
    relationship VARCHAR(50),             -- 'requires', 'triggers', 'uses'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dependencies_component ON component_dependencies(component_name);
CREATE INDEX IF NOT EXISTS idx_dependencies_depends_on ON component_dependencies(depends_on);

-- ============================================================================
-- SECTION 13: VERIFICATION QUERIES
-- ============================================================================

-- Verify pgvector extension is enabled
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Count new tables created
SELECT COUNT(*) as new_tables_count FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'ai_interaction_log',
    'ai_generated_insights',
    'knowledge_evolution_log',
    'data_validation_queue',
    'system_health_log',
    'semantic_search_cache',
    'model_fine_tuning_log',
    'component_dependencies'
);

-- Verify embedding columns added to verses
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'verses' 
AND column_name IN ('embedding_vector', 'embedding_model', 'embedding_generated_at');

-- Verify all new indexes created
SELECT indexname FROM pg_indexes 
WHERE tablename IN (
    'verses', 
    'pre_translated_corpus', 
    'dictionary_entries', 
    'concepts',
    'ai_interaction_log',
    'ai_generated_insights',
    'knowledge_evolution_log',
    'data_validation_queue',
    'system_health_log',
    'semantic_search_cache'
)
AND indexname LIKE 'idx_%'
ORDER BY tablename, indexname;

-- ============================================================================
-- TRANSFORMATION 2.1 SCHEMA EVOLUTION COMPLETE
-- ============================================================================

-- Summary:
-- - pgvector extension enabled
-- - 4 tables enhanced with embedding columns (verses, corpus, dictionary, concepts)
-- - 8 new tables created for AI/ML operations
-- - 15+ indexes created for performance
-- - Provenance tracking added to key tables
-- - Dependency tracking infrastructure created
--
-- Status: Foundation established, ready for Transformation 3.0 activation
-- Cost Impact: $0 (no data populated, no API calls)
-- Next Steps: Documented in TRANSFORMATION_2.1_TACTICAL_EXECUTION_PLAN.md
