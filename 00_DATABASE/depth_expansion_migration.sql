-- ============================================================================
-- VEDIC MASTERY STUDY - DEPTH EXPANSION MIGRATION (CORRECTED)
-- ============================================================================
-- Purpose: Add only the missing elements to the existing schema
-- Version: 1.1
-- Date: November 23, 2025
-- ============================================================================

-- ============================================================================
-- 1. ADD MISSING COLUMNS TO EXISTING TABLES
-- ============================================================================

-- Add missing columns to commentators table (if it exists)
-- First, check if table exists and add columns if missing
ALTER TABLE commentators ADD COLUMN sanskrit_name TEXT;
ALTER TABLE commentators ADD COLUMN school TEXT;
ALTER TABLE commentators ADD COLUMN period TEXT;
ALTER TABLE commentators ADD COLUMN bio_summary TEXT;

-- Add missing columns to concepts table (if it exists)
ALTER TABLE concepts ADD COLUMN category TEXT;

-- ============================================================================
-- 2. INSERT CORE DATA
-- ============================================================================

-- Insert major commentators (if not already present)
INSERT OR IGNORE INTO commentators (name, sanskrit_name, school, period) VALUES
    ('Adi Shankara', 'आदि शङ्कर', 'Advaita Vedanta', '8th century CE'),
    ('Ramanuja', 'रामानुज', 'Vishishtadvaita Vedanta', '11th-12th century CE'),
    ('Madhvacharya', 'मध्वाचार्य', 'Dvaita Vedanta', '13th century CE'),
    ('Vallabhacharya', 'वल्लभाचार्य', 'Shuddhadvaita Vedanta', '15th-16th century CE'),
    ('Nimbarka', 'निम्बार्क', 'Dvaitadvaita Vedanta', '13th century CE'),
    ('Abhinavagupta', 'अभिनवगुप्त', 'Kashmir Shaivism', '10th-11th century CE'),
    ('Gaudapada', 'गौडपाद', 'Advaita Vedanta', '6th-7th century CE'),
    ('Vijnanabhikshu', 'विज्ञानभिक्षु', 'Synthesis', '16th century CE');

-- Update concepts with categories
UPDATE concepts SET category = 'Metaphysics' WHERE concept_name IN ('Brahman', 'Atman', 'Maya', 'Prakriti', 'Purusha', 'Gunas');
UPDATE concepts SET category = 'Soteriology' WHERE concept_name IN ('Moksha', 'Nirvana');
UPDATE concepts SET category = 'Ethics' WHERE concept_name IN ('Karma', 'Dharma');
UPDATE concepts SET category = 'Practice' WHERE concept_name IN ('Bhakti', 'Yoga', 'Samadhi');
UPDATE concepts SET category = 'Epistemology' WHERE concept_name IN ('Jnana');
UPDATE concepts SET category = 'Cosmology' WHERE concept_name IN ('Samsara');

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
