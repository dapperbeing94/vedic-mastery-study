> **Vedic Mastery Study v2.0 - Source Layer Import Protocol v2.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol governs the process of importing raw, word-for-word source texts from external repositories into our **Supabase database's Source Layer**. Its purpose is to ensure that all imports are systematic, consistent, validated, and fully traceable.

**The core principle of this protocol is that the Source Layer is immutable. Once imported, this data should never be modified.**

---

## 2. SCOPE

This protocol applies to all data imported from external sources, including:
-   Git submodules (e.g., DharmicData).
-   API endpoints (e.g., vedicscriptures Bhagavad Gita API).
-   Manually downloaded datasets (e.g., from academic websites).

---

## 3. PRE-REQUISITES

Before an import can begin, the following must be in place:

1.  **External Source Registered**: The source repository/API must be registered in the `external_sources` table, including its URL, license, and an initial authority score.
2.  **Taxonomy Prepared**: The relevant branches of the `taxonomy` table must exist for the texts being imported. If not, the `SELF_EVOLVING_DATABASE_PROTOCOL` must be triggered first.
3.  **Import Script Ready**: The `import_manager.py` script must be configured for the specific format of the source data (JSON, CSV, etc.).

---

## 4. IMPORT WORKFLOW

This workflow is executed by the `import_manager.py` script.

### 4.1. Step 1: Initialization

-   The script is invoked with the `external_source_id` and the path to the source file(s).
-   It creates a new entry in the `import_decisions` table to log the start of the operation.

### 4.2. Step 2: Data Parsing & Validation

-   The script reads the source file (e.g., a large JSON file).
-   It validates the data against a predefined schema for that source type, checking for:
    -   Required fields (e.g., `verse_number`, `text`).
    -   Correct data types.
    -   Structural integrity.
-   Any records that fail validation are logged and skipped.

### 4.3. Step 3: Verse-by-Verse Processing (Loop)

For each verse in the source file, the script performs the following actions in a single database transaction:

1.  **Classification**: It calls the `taxonomy_manager.py` to get the correct `classification_code` for the verse based on its text, chapter, and verse number.
    -   If a conflict occurs, it is logged to `classification_conflicts`, and the verse is skipped for now.
2.  **Create `source_texts` Entry**: A record is created in the `source_texts` table linking the verse to its source file and language.
3.  **Insert into `verses` Table**: A new record is inserted into the `verses` table with all the raw data from the source:
    -   `devanagari`
    -   `transliteration`
    -   `source_translation`
    -   `source_metadata` (e.g., chandas, rishi)
4.  **Insert into `verse_classification`**: A record is created linking the new `verse_id` to its `classification_code`.
5.  **Insert into `reading_progress`**: A new record is created for the verse with a `read_status` of `'unread'`.
6.  **Handle Commentaries** (if present):
    -   If the source data includes commentaries, they are inserted into the `commentaries` table with `is_original` set to `TRUE`.

### 4.4. Step 4: Post-Import Processing

-   After the loop is complete, the script updates the initial `import_decisions` record with the final counts (verses imported, conflicts detected, etc.).
-   It adds the newly imported text(s) to the `deepening_queue` with a default priority, making them available for the Vedic Sage persona to begin analysis.
-   It runs a final validation check to ensure foreign key constraints are intact.

---

## 5. DATA PROVENANCE & TRACEABILITY

This protocol ensures that every verse in our database can be traced back to its origin.

-   `verses.source_text_id` → `source_texts.id`
-   `source_texts.external_source_id` → `external_sources.id`

This chain allows us to ask questions like, "Show me all verses that came from the DharmicData repository, specifically from the `Rigveda.json` file, and were imported on November 23, 2025."

---

## 6. ERROR HANDLING & ROLLBACK

-   **Transactional Integrity**: The processing for each verse is atomic. If any step fails (e.g., classification fails), the entire transaction for that verse is rolled back, and the verse is logged as an error.
-   **Batch Rollback**: If a large-scale import is found to be corrupt, the `import_decisions` log can be used to identify all verses from that batch, and a targeted deletion script can be run to remove them cleanly (as defined in the `ROLLBACK_PROCEDURES.md`).
-   **No Partial Imports**: The system is designed to either import a verse completely and correctly or not at all.
