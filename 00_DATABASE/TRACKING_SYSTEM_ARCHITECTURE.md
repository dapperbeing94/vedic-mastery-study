# Vedic Mastery Study - Tracking System Architecture

**Date**: November 22, 2025  
**Purpose**: Systematic, programmatic infrastructure for tracking breadth and depth across the entire Vedic framework

---

## Overview

This document defines the **Continuity and Thoroughness Protocol** - a persistent background system that objectively tracks progress, identifies gaps, and recommends priorities across the entire Vedic knowledge framework.

---

## Core Principles

1. **End-to-End Coverage**: Track ALL categories, subcategories, and texts from the original framework
2. **Objective Scoring**: Use quantifiable metrics for breadth and depth
3. **Automated Tracking**: Minimize manual updates through programmatic analysis
4. **Persistent Monitoring**: Always maintain a pulse on the complete framework
5. **Priority Recommendations**: Algorithmically suggest next steps based on gaps

---

## Scoring Methodology

### Breadth Score (0-10)

Measures **coverage** across a category:

- **0**: Not started, no texts covered
- **2**: 1-20% of texts have basic overview
- **4**: 21-40% of texts have basic overview
- **6**: 41-60% of texts have basic overview
- **8**: 61-80% of texts have basic overview
- **10**: 81-100% of texts have basic overview

### Depth Score (0-10)

Measures **quality of study** for covered texts:

- **0**: Not started
- **1**: Text identified, source located
- **2**: Basic overview created (Green Belt level)
- **3**: Comprehensive overview with key concepts
- **4**: Structure and organization documented
- **5**: Key verses/passages extracted and analyzed
- **6**: Multiple commentaries compared
- **7**: Verse-by-verse or chapter-by-chapter analysis
- **8**: Word-by-word Sanskrit analysis
- **9**: Cross-references and synthesis with other texts
- **10**: Complete mastery with practical applications

### Combined Score

**Overall Score** = (Breadth Score × 0.3) + (Depth Score × 0.7)

This weights depth more heavily than breadth, reflecting the Blue Belt focus.

---

## Database Schema

### New Tables

#### 1. `categories`
```sql
CREATE TABLE categories (
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
```

#### 2. `subcategories`
```sql
CREATE TABLE subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    expected_text_count INTEGER,  -- How many texts should be in this subcategory
    target_depth_score INTEGER DEFAULT 8,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

#### 3. `progress_tracking`
```sql
CREATE TABLE progress_tracking (
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
```

#### 4. `depth_criteria`
```sql
CREATE TABLE depth_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_id INTEGER NOT NULL,
    criterion_name TEXT NOT NULL,  -- e.g., "verse_analysis", "commentary_comparison"
    criterion_met BOOLEAN DEFAULT 0,
    evidence_file_path TEXT,
    last_checked TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);
```

#### 5. `gap_analysis`
```sql
CREATE TABLE gap_analysis (
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
```

#### 6. `session_log`
```sql
CREATE TABLE session_log (
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
```

---

## Depth Criteria Checklist

For each text, track these criteria to objectively measure depth:

### Level 1-3 (Green Belt)
- [ ] Source located
- [ ] Basic overview created
- [ ] Category assigned

### Level 4-5 (Blue Belt Foundation)
- [ ] Comprehensive overview with structure
- [ ] Key concepts extracted
- [ ] Important verses/passages documented

### Level 6-7 (Blue Belt Core)
- [ ] Multiple commentaries compared
- [ ] Chapter-by-chapter or section-by-section analysis
- [ ] Cross-references identified

### Level 8-9 (Blue Belt Advanced)
- [ ] Verse-by-verse or sutra-by-sutra analysis
- [ ] Word-by-word Sanskrit analysis
- [ ] Synthesis documents created

### Level 10 (Mastery)
- [ ] Practical applications documented
- [ ] Teaching frameworks created
- [ ] Integration with daily practice

---

## Automated Tracking Scripts

### 1. `calculate_scores.py`

Analyzes the file system and database to calculate breadth and depth scores:

```python
def calculate_breadth_score(category_id):
    """
    Calculate breadth score based on:
    - Number of texts in category
    - Number of texts with study documents
    - Percentage coverage
    """
    pass

def calculate_depth_score(text_id):
    """
    Calculate depth score based on:
    - Existence of study documents
    - File size and structure
    - Depth criteria met
    - Cross-references
    """
    pass

def update_all_scores():
    """
    Recalculate all scores and update database
    """
    pass
```

### 2. `gap_analysis.py`

Identifies gaps and generates recommendations:

```python
def identify_breadth_gaps():
    """
    Find categories with low breadth scores
    """
    pass

def identify_depth_gaps():
    """
    Find texts with low depth scores
    """
    pass

def calculate_priority_scores():
    """
    Calculate priority based on:
    - Importance of category
    - Current gap size
    - Dependencies
    """
    pass

def generate_recommendations():
    """
    Create prioritized list of next steps
    """
    pass
```

### 3. `progress_report.py`

Generates comprehensive progress reports:

```python
def generate_dashboard():
    """
    Create visual dashboard of progress
    """
    pass

def generate_category_report(category_id):
    """
    Detailed report for a specific category
    """
    pass

def generate_session_summary(session_id):
    """
    Summary of what was accomplished in a session
    """
    pass
```

### 4. `continuity_check.py`

Runs at the start of each session to provide context:

```python
def session_startup():
    """
    Run at session start to:
    - Calculate current scores
    - Identify top priorities
    - Generate recommendations
    - Update dashboard
    """
    pass

def get_next_recommendations(n=5):
    """
    Get top N recommended next steps
    """
    pass
```

---

## Usage Protocol

### At Session Start

1. Run `continuity_check.py` to get current state
2. Review dashboard and recommendations
3. Decide on session focus
4. Log session plan

### During Session

1. Work on selected texts/categories
2. Create study documents
3. Update database as you go

### At Session End

1. Run `calculate_scores.py` to update all scores
2. Run `gap_analysis.py` to identify new gaps
3. Log session accomplishments
4. Commit all changes to GitHub

### Background Monitoring

The system should be able to answer at any time:
- What is our overall progress? (breadth and depth scores)
- What are the top 5 priorities?
- Which categories need the most work?
- How much progress did we make this session?

---

## Priority Calculation Algorithm

```python
def calculate_priority(category, subcategory, text):
    """
    Priority = (Importance × Gap Size × Dependency Factor)
    
    Importance (1-10):
    - Core Vedic Foundation: 10
    - Upanishads: 10
    - Brahma Sutras: 9
    - Bhagavad Gita: 9
    - Darshanas: 8
    - Smriti: 7
    - Tantras: 6
    - Sciences: 5
    - Regional: 4
    - Modern: 3
    
    Gap Size (0-10):
    - 10 - current_depth_score
    
    Dependency Factor (0.5-2.0):
    - 2.0 if other texts depend on this
    - 1.0 if independent
    - 0.5 if depends on incomplete texts
    """
    importance = get_importance_score(category)
    gap_size = 10 - get_current_depth_score(text)
    dependency = get_dependency_factor(text)
    
    return importance * gap_size * dependency
```

---

## Dashboard Visualization

The system should generate a visual dashboard showing:

1. **Overall Progress Bar**
   - Green Belt: X%
   - Blue Belt: Y%

2. **Category Heatmap**
   - Color-coded by combined score
   - Red (0-3), Yellow (4-6), Green (7-10)

3. **Top Priorities List**
   - Ranked by priority score
   - With recommended action

4. **Session Progress Graph**
   - Breadth and depth over time

5. **Gap Analysis Summary**
   - Number of gaps by type
   - Estimated sessions to close gaps

---

## Integration with Soul Transmigration Protocol

The tracking system must be integrated with the Soul Transmigration Protocol:

1. **Auto-update Protocol File**: After each session, automatically update the Soul Transmigration Protocol with:
   - Current scores
   - Top priorities
   - Recent accomplishments

2. **Context Restoration**: When a new session starts, the tracking system provides full context immediately

3. **Persistent State**: All tracking data is stored in the database and committed to GitHub

---

## Success Metrics

The system is successful if:

1. ✅ We can answer "What's our progress?" in <5 seconds
2. ✅ We never lose track of the end-to-end framework
3. ✅ Priorities are always clear and objective
4. ✅ We can bounce around without losing context
5. ✅ New sessions start with full context automatically

---

**Om Tat Sat** 🕉️

