> **Vedic Mastery Study - Master Rollback Procedures**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This document provides the specific, ordered procedures for rolling back major changes during the project transformation. It is the primary safety mechanism to ensure that we can recover from a catastrophic failure at any critical phase.

**These procedures should only be executed if a phase fails validation and cannot be fixed, or upon explicit user command.**

---

## 2. GENERAL PRINCIPLES

1.  **Execute in Reverse Order**: Rollbacks must be performed in the reverse order of the migration.
2.  **Use the Correct Backup**: Always use the timestamped backup created immediately before the phase you are rolling back.
3.  **Validate After Rollback**: After a rollback, validate that the system has been restored to its previous state.
4.  **Log Everything**: Every rollback action must be logged with a reason.

---

## 3. PROCEDURE: ROLLBACK DATABASE SCHEMA MIGRATION (v2 to v1)

**When to use**: If the Phase 1 database migration fails, corrupts data, or causes critical errors.

**Prerequisite**: A valid backup of the `vedic_knowledge.db` file created *before* the migration was executed.

### **Steps**:

1.  **Take System Offline**: Announce that a rollback is in progress and no other actions will be taken.
2.  **Locate Pre-Migration Backup**:
    -   Identify the backup file (e.g., `vedic_knowledge_pre_migration_backup.db`).
3.  **Restore from File Backup (Safest Method)**:
    ```bash
    # Navigate to the database directory
    cd /home/ubuntu/vedic-mastery-study/00_DATABASE

    # Remove the corrupted v2 database
    rm vedic_knowledge.db

    # Copy the backup file back to the original name
    cp vedic_knowledge_pre_migration_backup.db vedic_knowledge.db
    ```
4.  **Alternative: Execute Rollback Script (If file backup fails)**:
    ```bash
    # Navigate to the database directory
    cd /home/ubuntu/vedic-mastery-study/00_DATABASE

    # Execute the rollback script
    sqlite3 vedic_knowledge.db < schema/rollback_from_v2.sql
    ```
5.  **Validate Rollback**:
    ```bash
    # Verify the table count has returned to 14
    sqlite3 vedic_knowledge.db "SELECT COUNT(*) FROM sqlite_master WHERE type=\'table\';"

    # Verify that a v2 table (e.g., external_sources) no longer exists
    sqlite3 vedic_knowledge.db "SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'external_sources\';"
    # (Should return nothing)

    # Verify that a v1 table still has its data
    sqlite3 vedic_knowledge.db "SELECT COUNT(*) FROM texts;"
    # (Should return 111 or the pre-migration count)
    ```
6.  **Log the Rollback**: Document the reason for the rollback, the backup used, and the validation results.
7.  **Report Status**: Inform the user that the rollback is complete and the system is stable in its v1 state. Await further instructions.

---

## 4. PROCEDURE: ROLLBACK DIRECTORY RESTRUCTURE

**When to use**: If the Phase 3 directory restructure results in broken links, lost files, or a corrupted repository state.

**Prerequisite**: A full repository backup created before the restructure began.

### **Steps**:

1.  **Take System Offline**.
2.  **Locate Pre-Restructure Backup**:
    -   Identify the full project backup directory (e.g., `/home/ubuntu/vedic-mastery-study-backups/YYYY-MM-DD-HH-MM/`).
3.  **Delete Corrupted Repository**:
    ```bash
    # WARNING: This is a destructive command. Ensure you have a valid backup.
    rm -rf /home/ubuntu/vedic-mastery-study
    ```
4.  **Restore from Backup**:
    ```bash
    # Copy the entire backup directory back to the original location
    cp -r /path/to/your/backup/vedic-mastery-study /home/ubuntu/vedic-mastery-study
    ```
5.  **Validate Rollback**:
    -   Check that the old directory structure is restored.
    -   Check that a sample of files exists in their original locations.
    -   Run `git status` to ensure the repository is clean.
6.  **Log and Report**: Document the rollback and inform the user.

---

## 5. PROCEDURE: ROLLBACK GIT SUBMODULE INTEGRATION

**When to use**: If the git submodules (Phase 6) cause repository corruption or unmanageable conflicts.

### **Steps**:

1.  **De-initialize the Submodule**:
    ```bash
    # Example for DharmicData
    git submodule deinit -f 02_EXTERNAL_SOURCES/DharmicData
    ```
2.  **Remove the Submodule Directory**:
    ```bash
    rm -rf .git/modules/02_EXTERNAL_SOURCES/DharmicData
    git rm -f 02_EXTERNAL_SOURCES/DharmicData
    ```
3.  **Remove from `.gitmodules`**:
    -   Manually edit the `.gitmodules` file to remove the entry for the submodule.
4.  **Commit the Removal**:
    ```bash
    git commit -m "Rollback: Remove DharmicData submodule"
    ```
5.  **Repeat for all submodules**.
6.  **Validate, Log, and Report**.

---

## 6. PROCEDURE: ROLLBACK DATA IMPORTS

**When to use**: If a data import (Phases 7-11) introduces significant data corruption that cannot be fixed.

### **Steps**:

1.  **Identify the Scope**: Determine which `external_source_id` and `text_id`(s) were affected by the bad import.
2.  **Execute Deletion Scripts**:
    ```sql
    -- Example: Delete all verses and related data for a specific text_id from a bad import
    DELETE FROM verse_analysis WHERE verse_id IN (SELECT verse_id FROM verses WHERE text_id = <bad_text_id>);
    DELETE FROM verse_classification WHERE verse_id IN (SELECT verse_id FROM verses WHERE text_id = <bad_text_id>);
    DELETE FROM commentaries WHERE verse_id IN (SELECT verse_id FROM verses WHERE text_id = <bad_text_id>);
    DELETE FROM cross_references WHERE source_verse_id IN (SELECT verse_id FROM verses WHERE text_id = <bad_text_id>) OR target_verse_id IN (SELECT verse_id FROM verses WHERE text_id = <bad_text_id>);
    DELETE FROM reading_progress WHERE text_id = <bad_text_id>;
    DELETE FROM verses WHERE text_id = <bad_text_id>;
    DELETE FROM source_texts WHERE text_id = <bad_text_id>;
    DELETE FROM import_decisions WHERE source_file LIKE 
    '%<name_of_bad_import_file>%
    ';
    ```
3.  **Update Tracking Tables**:
    -   Recalculate depth scores using `depth_tracker.py`.
    -   Remove the text from the `deepening_queue`.
4.  **Validate, Log, and Report**.
