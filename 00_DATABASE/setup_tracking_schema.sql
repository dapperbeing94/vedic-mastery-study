-- Vedic Mastery Study - Tracking System Database Schema
-- Date: November 22, 2025

-- 1. Categories table (hierarchical structure)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- 2. Subcategories table
CREATE TABLE IF NOT EXISTS subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    expected_text_count INTEGER,  -- How many texts should be in this subcategory
    target_depth_score INTEGER DEFAULT 8,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 3. Progress tracking table
CREATE TABLE IF NOT EXISTS progress_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- 4. Depth criteria table
CREATE TABLE IF NOT EXISTS depth_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    criterion_name TEXT NOT NULL,  -- e.g., "verse_analysis", "commentary_comparison"
    criterion_met BOOLEAN DEFAULT 0,
    evidence_file_path TEXT,
    last_checked TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);

-- 5. Gap analysis table
CREATE TABLE IF NOT EXISTS gap_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

-- 6. Session log table
CREATE TABLE IF NOT EXISTS session_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date TEXT NOT NULL,
    session_number INTEGER,
    focus_area TEXT,
    texts_studied TEXT,  -- JSON array of text IDs
    breadth_delta REAL,  -- Change in overall breadth
    depth_delta REAL,    -- Change in overall depth
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_progress_text ON progress_tracking(text_id);
CREATE INDEX IF NOT EXISTS idx_progress_category ON progress_tracking(category_id);
CREATE INDEX IF NOT EXISTS idx_depth_criteria_text ON depth_criteria(text_id);
CREATE INDEX IF NOT EXISTS idx_gap_analysis_priority ON gap_analysis(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_gap_analysis_resolved ON gap_analysis(resolved);

-- Insert main categories based on master_index.md
INSERT OR IGNORE INTO categories (name, level, display_order, description, target_breadth_score, target_depth_score) VALUES
('Core Vedic Foundation', 1, 1, 'Śruti texts: Vedas, Brahmanas, Aranyakas, Upanishads, Vedangas', 10, 9),
('Smṛti Texts', 1, 2, 'Epics, Dharma Shastras, Puranas', 10, 8),
('Darśanas', 1, 3, 'Six Philosophical Schools', 10, 9),
('Tantra & Agamas', 1, 4, 'Shaiva, Shakta, Vaishnava Agamas and Tantras', 10, 7),
('Yogic Corpus', 1, 5, 'Hatha Yoga and related texts', 10, 7),
('Sciences & Knowledge Systems', 1, 6, 'Ayurveda, Vastu, Natya, Astronomy, etc.', 10, 6),
('Commentarial Traditions', 1, 7, 'Major Acharyas and scholars', 10, 7),
('Regional Canonical Texts', 1, 8, 'Tamil, Hindi, Marathi devotional literature', 10, 6),
('Modern Synthesizers', 1, 9, 'Vivekananda, Aurobindo, Radhakrishnan, Sivananda', 10, 6),
('Synthesis Work', 1, 10, 'Cross-cutting thematic documents', 10, 9);

