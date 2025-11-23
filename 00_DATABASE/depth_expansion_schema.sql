-- ============================================================================
-- VEDIC MASTERY STUDY - DEPTH EXPANSION SCHEMA
-- ============================================================================
-- Purpose: Evolve the database schema to support verse-level analysis,
--          commentaries, and cross-references for depth expansion.
-- Version: 1.0
-- Date: November 23, 2025
-- ============================================================================

-- ============================================================================
-- 1. VERSES TABLE
-- ============================================================================
-- Stores individual verses from key texts (Upanishads, Gita, Sutras, etc.)
-- ============================================================================

CREATE TABLE IF NOT EXISTS verses (
    verse_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    chapter INTEGER,
    section TEXT,
    verse_number INTEGER NOT NULL,
    sanskrit_text TEXT,
    transliteration TEXT,
    translation TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

CREATE INDEX IF NOT EXISTS idx_verses_text_id ON verses(text_id);
CREATE INDEX IF NOT EXISTS idx_verses_chapter ON verses(chapter);
CREATE INDEX IF NOT EXISTS idx_verses_verse_number ON verses(verse_number);

-- ============================================================================
-- 2. COMMENTATORS TABLE
-- ============================================================================
-- Stores information about commentators (Shankara, Ramanuja, Madhva, etc.)
-- ============================================================================

CREATE TABLE IF NOT EXISTS commentators (
    commentator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    sanskrit_name TEXT,
    school TEXT,
    period TEXT,
    bio_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert major commentators
INSERT OR IGNORE INTO commentators (name, sanskrit_name, school, period) VALUES
    ('Adi Shankara', 'आदि शङ्कर', 'Advaita Vedanta', '8th century CE'),
    ('Ramanuja', 'रामानुज', 'Vishishtadvaita Vedanta', '11th-12th century CE'),
    ('Madhvacharya', 'मध्वाचार्य', 'Dvaita Vedanta', '13th century CE'),
    ('Vallabhacharya', 'वल्लभाचार्य', 'Shuddhadvaita Vedanta', '15th-16th century CE'),
    ('Nimbarka', 'निम्बार्क', 'Dvaitadvaita Vedanta', '13th century CE'),
    ('Abhinavagupta', 'अभिनवगुप्त', 'Kashmir Shaivism', '10th-11th century CE'),
    ('Gaudapada', 'गौडपाद', 'Advaita Vedanta', '6th-7th century CE'),
    ('Vijnanabhikshu', 'विज्ञानभिक्षु', 'Synthesis', '16th century CE');

-- ============================================================================
-- 3. COMMENTARIES TABLE
-- ============================================================================
-- Links commentaries to specific verses
-- ============================================================================

CREATE TABLE IF NOT EXISTS commentaries (
    commentary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    verse_id INTEGER NOT NULL,
    commentator_id INTEGER NOT NULL,
    commentary_text TEXT NOT NULL,
    key_concepts TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (commentator_id) REFERENCES commentators(commentator_id)
);

CREATE INDEX IF NOT EXISTS idx_commentaries_verse_id ON commentaries(verse_id);
CREATE INDEX IF NOT EXISTS idx_commentaries_commentator_id ON commentaries(commentator_id);

-- ============================================================================
-- 4. CROSS_REFERENCES TABLE
-- ============================================================================
-- Maps relationships between verses and concepts across the entire corpus
-- ============================================================================

CREATE TABLE IF NOT EXISTS cross_references (
    cross_ref_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_verse_id INTEGER NOT NULL,
    target_verse_id INTEGER NOT NULL,
    relationship_type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (target_verse_id) REFERENCES verses(verse_id)
);

CREATE INDEX IF NOT EXISTS idx_cross_ref_source ON cross_references(source_verse_id);
CREATE INDEX IF NOT EXISTS idx_cross_ref_target ON cross_references(target_verse_id);
CREATE INDEX IF NOT EXISTS idx_cross_ref_type ON cross_references(relationship_type);

-- Common relationship types:
-- 'parallel' - Similar concept or teaching
-- 'contrast' - Contrasting or opposing view
-- 'elaboration' - One verse elaborates on another
-- 'quotation' - One text quotes another
-- 'commentary' - One text comments on another

-- ============================================================================
-- 5. CONCEPTS TABLE
-- ============================================================================
-- Stores key philosophical concepts for tagging and cross-referencing
-- ============================================================================

CREATE TABLE IF NOT EXISTS concepts (
    concept_id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept_name TEXT NOT NULL UNIQUE,
    sanskrit_term TEXT,
    category TEXT,
    definition TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert core concepts
INSERT OR IGNORE INTO concepts (concept_name, sanskrit_term, category) VALUES
    ('Brahman', 'ब्रह्मन्', 'Metaphysics'),
    ('Atman', 'आत्मन्', 'Metaphysics'),
    ('Maya', 'माया', 'Metaphysics'),
    ('Moksha', 'मोक्ष', 'Soteriology'),
    ('Karma', 'कर्म', 'Ethics'),
    ('Dharma', 'धर्म', 'Ethics'),
    ('Bhakti', 'भक्ति', 'Practice'),
    ('Jnana', 'ज्ञान', 'Epistemology'),
    ('Yoga', 'योग', 'Practice'),
    ('Samadhi', 'समाधि', 'Practice'),
    ('Prakriti', 'प्रकृति', 'Metaphysics'),
    ('Purusha', 'पुरुष', 'Metaphysics'),
    ('Gunas', 'गुण', 'Metaphysics'),
    ('Samsara', 'संसार', 'Cosmology'),
    ('Nirvana', 'निर्वाण', 'Soteriology');

-- ============================================================================
-- 6. VERSE_CONCEPTS TABLE (Junction Table)
-- ============================================================================
-- Links verses to the concepts they discuss
-- ============================================================================

CREATE TABLE IF NOT EXISTS verse_concepts (
    verse_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    relevance_score INTEGER DEFAULT 5,
    notes TEXT,
    PRIMARY KEY (verse_id, concept_id),
    FOREIGN KEY (verse_id) REFERENCES verses(verse_id),
    FOREIGN KEY (concept_id) REFERENCES concepts(concept_id)
);

CREATE INDEX IF NOT EXISTS idx_verse_concepts_verse ON verse_concepts(verse_id);
CREATE INDEX IF NOT EXISTS idx_verse_concepts_concept ON verse_concepts(concept_id);

-- ============================================================================
-- 7. UPDATE DEPTH_CRITERIA TABLE
-- ============================================================================
-- Add new criteria for verse-level depth assessment
-- ============================================================================

INSERT OR IGNORE INTO depth_criteria (category_id, criterion, weight) VALUES
    (1, 'Verse-level translation coverage', 0.25),
    (1, 'Multiple commentary coverage', 0.20),
    (1, 'Cross-reference density', 0.15),
    (2, 'Verse-level translation coverage', 0.25),
    (2, 'Multiple commentary coverage', 0.20),
    (2, 'Cross-reference density', 0.15),
    (3, 'Verse-level translation coverage', 0.20),
    (3, 'Multiple commentary coverage', 0.15),
    (3, 'Cross-reference density', 0.10);

-- ============================================================================
-- 8. CREATE VIEWS FOR ANALYSIS
-- ============================================================================

-- View: Verses with commentary count
CREATE VIEW IF NOT EXISTS verse_commentary_count AS
SELECT 
    v.verse_id,
    v.text_id,
    t.title AS text_title,
    v.chapter,
    v.verse_number,
    COUNT(c.commentary_id) AS commentary_count
FROM verses v
LEFT JOIN commentaries c ON v.verse_id = c.verse_id
LEFT JOIN texts t ON v.text_id = t.id
GROUP BY v.verse_id;

-- View: Verses with cross-reference count
CREATE VIEW IF NOT EXISTS verse_cross_ref_count AS
SELECT 
    v.verse_id,
    v.text_id,
    t.title AS text_title,
    v.chapter,
    v.verse_number,
    COUNT(DISTINCT cr1.cross_ref_id) + COUNT(DISTINCT cr2.cross_ref_id) AS cross_ref_count
FROM verses v
LEFT JOIN cross_references cr1 ON v.verse_id = cr1.source_verse_id
LEFT JOIN cross_references cr2 ON v.verse_id = cr2.target_verse_id
LEFT JOIN texts t ON v.text_id = t.id
GROUP BY v.verse_id;

-- View: Text depth metrics
CREATE VIEW IF NOT EXISTS text_depth_metrics AS
SELECT 
    t.id AS text_id,
    t.title,
    t.category,
    COUNT(DISTINCT v.verse_id) AS total_verses,
    SUM(CASE WHEN v.translation IS NOT NULL THEN 1 ELSE 0 END) AS verses_with_translation,
    SUM(CASE WHEN v.translation IS NOT NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT v.verse_id) AS translation_coverage_pct,
    AVG(vcc.commentary_count) AS avg_commentaries_per_verse,
    AVG(vcrc.cross_ref_count) AS avg_cross_refs_per_verse
FROM texts t
LEFT JOIN verses v ON t.id = v.text_id
LEFT JOIN verse_commentary_count vcc ON v.verse_id = vcc.verse_id
LEFT JOIN verse_cross_ref_count vcrc ON v.verse_id = vcrc.verse_id
GROUP BY t.id;

-- ============================================================================
-- SCHEMA EVOLUTION COMPLETE
-- ============================================================================
