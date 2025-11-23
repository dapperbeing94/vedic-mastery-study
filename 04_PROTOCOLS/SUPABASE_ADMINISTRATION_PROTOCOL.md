# Supabase Administration Protocol

**Version:** 2.0  
**Last Updated:** November 23, 2024  
**Status:** Active  
**Transformation:** Post-Transformation 2.0

---

## Purpose

This protocol establishes comprehensive guidelines for administering, maintaining, and evolving the Vedic Mastery Study Supabase database infrastructure.

---

## Database Architecture

### **Primary Database**
- **Platform:** Supabase (PostgreSQL)
- **Project URL:** https://yvcyprwldvoubyytptqu.supabase.co
- **Authentication:** API key-based (anon key for public access)

### **Schema Overview**
- **Total Tables:** 42
- **Total Records:** ~580,000
- **Primary Categories:**
  - Core Vedic Content (verses, texts, commentaries)
  - Translation Layer (dictionary, corpus, cache)
  - Taxonomy & Classification
  - Study Progress & Analytics
  - Quality Metrics & Gap Analysis

---

## Table Categories

### **1. Core Content Tables** (5 tables)
- `verses` - 100,729 Vedic verses
- `texts` - 92 sacred texts
- `commentaries` - Commentary entries
- `commentators` - Commentary authors
- `source_texts` - 100,651 source text records

### **2. Translation Layer Tables** (5 tables)
- `dictionary_entries` - 286,535 Monier-Williams entries
- `pre_translated_corpus` - 92,030 Itihasa translations
- `word_stems` - Morphological analysis
- `grammatical_rules` - Sanskrit grammar rules
- `translation_cache` - LLM translation tracking

### **3. Taxonomy Tables** (9 tables)
- `categories` - Top-level categories
- `subcategories` - Sub-category definitions
- `taxonomy` - Classification system
- `taxonomy_versions` - Version control
- `taxonomy_migrations` - Migration history
- `taxonomy_proposals` - Proposed changes
- `classification_log` - Classification history
- `classification_conflicts` - Conflict resolution
- `verse_classification` - Verse-taxonomy mappings

### **4. Concept & Theme Tables** (6 tables)
- `concepts` - 197 philosophical concepts
- `themes` - 15 thematic categories
- `concept_relationships` - Concept interconnections
- `verse_concepts` - Verse-concept mappings
- `verse_to_concept` - Verse-concept junction
- `verse_to_theme` - Verse-theme junction

### **5. Study Progress Tables** (7 tables)
- `reading_progress` - User reading tracking
- `study_progress` - Study session records
- `session_log` - Session activity log
- `progress_tracking` - Progress metrics
- `deepening_queue` - Priority study queue
- `quality_metrics` - Quality assessments
- `gap_analysis` - Knowledge gap tracking

### **6. External & Source Tables** (3 tables)
- `external_sources` - External repository tracking
- `cross_references` - Cross-reference mappings
- `import_decisions` - Import decision log

### **7. Analysis Tables** (4 tables)
- `verse_analysis` - Verse-level analysis
- `analysis_history` - Analysis version history
- `synthesis_documents` - Synthesis outputs
- `synthesis_sources` - Synthesis source tracking

### **8. Glossary Tables** (2 tables)
- `sanskrit_terms` - Sanskrit terminology
- `sanskrit_glossary` - Glossary definitions

### **9. Depth Criteria Table** (1 table)
- `depth_criteria` - Depth scoring criteria

---

## Data Integrity Protocols

### **1. Primary Key Management**
- All tables use `SERIAL PRIMARY KEY` (auto-incrementing)
- Never manually set primary keys during imports
- Use Supabase's auto-increment for new records

### **2. Foreign Key Relationships**
- Currently **no foreign key constraints** (simplified for migration)
- Referential integrity maintained through application logic
- Future enhancement: Add FK constraints after data stabilization

### **3. Data Validation**
- **Required fields:** Validate before insert
- **Text fields:** Use UTF-8 encoding for Sanskrit
- **Timestamps:** Use PostgreSQL `CURRENT_TIMESTAMP`
- **Boolean fields:** Default to `FALSE` unless specified

### **4. Batch Import Guidelines**
- **Batch size:** 1,000 records per transaction
- **Error handling:** Log failed batches, continue processing
- **Progress tracking:** Report every batch completion
- **Rollback strategy:** Clear tables before re-import if needed

---

## Backup & Recovery

### **1. Backup Strategy**
- **Frequency:** Daily automated backups (Supabase default)
- **Retention:** 7-day rolling backup window
- **Manual backups:** Before major schema changes
- **Export format:** SQL dump or CSV for portability

### **2. Recovery Procedures**
1. Identify failure point and scope
2. Stop all write operations
3. Restore from most recent backup
4. Re-run incremental imports if needed
5. Verify data integrity post-recovery

---

## Migration Protocols

### **1. SQLite to Supabase Migration**
- **Source:** `00_DATABASE/vedic_knowledge.db`
- **Scripts:** `00_DATABASE/import_scripts/migrate_sqlite_to_supabase.py`
- **Pre-migration:** Clear existing data with `clear_core_tables.py`
- **Post-migration:** Verify row counts match source

### **2. Schema Evolution**
- **Version control:** Track schema changes in `00_DATABASE/schema/`
- **Naming convention:** `supabase_schema_v{version}.sql`
- **Testing:** Test schema changes in development before production
- **Documentation:** Update `ARCHITECTURE_DOCUMENTATION.md`

---

## Performance Optimization

### **1. Indexing Strategy**
- **Primary indexes:** Auto-created on primary keys
- **Custom indexes:** Created for frequent query patterns
  - `idx_corpus_sanskrit` on `pre_translated_corpus(sanskrit_text)`
  - `idx_quality_metrics_verse_id` on `quality_metrics(verse_id)`
  - `idx_reading_progress_text_id` on `reading_progress(text_id)`
  - `idx_deepening_queue_priority` on `deepening_queue(priority_score DESC)`

### **2. Query Optimization**
- Use `LIMIT` for large result sets
- Use `ILIKE` for case-insensitive searches
- Avoid `SELECT *` - specify required columns
- Use pagination for API responses

---

## Security & Access Control

### **1. API Key Management**
- **Anon key:** Public read access (safe for client-side)
- **Service key:** Full admin access (server-side only)
- **Rotation:** Rotate keys if compromised
- **Environment variables:** Store keys in `.env` files (never commit)

### **2. Row-Level Security (RLS)**
- Currently **disabled** for development
- Future: Enable RLS for multi-user access
- Define policies for read/write permissions per table

---

## Monitoring & Maintenance

### **1. Health Checks**
- **API endpoint:** `GET /stats` (Translation Layer API)
- **Metrics to monitor:**
  - Total record counts per table
  - API response times
  - Error rates
  - Database size

### **2. Routine Maintenance**
- **Weekly:** Review error logs
- **Monthly:** Analyze query performance
- **Quarterly:** Review and optimize indexes
- **Annually:** Major schema review and optimization

---

## Translation Layer Integration

### **1. API Service**
- **Location:** `05_SERVICES/translation_layer_api.py`
- **Port:** 8000
- **Endpoints:**
  - `GET /` - Health check
  - `POST /dictionary/lookup` - Dictionary queries
  - `POST /corpus/search` - Corpus searches
  - `POST /translate` - Full translation service
  - `GET /stats` - Database statistics

### **2. Service Management**
- **Start:** `python3 05_SERVICES/translation_layer_api.py &`
- **Stop:** `pkill -f translation_layer_api`
- **Logs:** `/tmp/translation_api.log`
- **Auto-restart:** Configure systemd service (future enhancement)

---

## Evolution & Scalability

### **1. Future Enhancements**
- Add foreign key constraints for referential integrity
- Implement Row-Level Security (RLS) for multi-user access
- Create materialized views for complex queries
- Add full-text search indexes for Sanskrit text
- Implement caching layer (Redis) for frequent queries

### **2. Scaling Considerations**
- **Vertical scaling:** Upgrade Supabase plan for more resources
- **Horizontal scaling:** Implement read replicas for heavy read workloads
- **Partitioning:** Partition large tables (verses, corpus) by date or category
- **Archival:** Archive old analysis records to reduce active dataset size

---

## Protocol Compliance

### **Agent Responsibilities**
1. **Always** verify Supabase connection before operations
2. **Always** use batch imports for large datasets
3. **Always** log import/export operations
4. **Never** expose service keys in client-side code
5. **Never** modify schema without updating documentation

### **User Responsibilities**
1. Provide Supabase credentials when requested
2. Confirm major schema changes before execution
3. Review migration summaries for accuracy
4. Report any data inconsistencies immediately

---

## Related Protocols
- `TRANSLATION_LAYER_PROTOCOL.md` - Translation Layer operations
- `SOUL_TRANSMIGRATION_PROTOCOL.md` - Context transfer procedures
- `00_DATABASE/ARCHITECTURE_DOCUMENTATION.md` - Detailed schema reference

---

**End of Protocol**
