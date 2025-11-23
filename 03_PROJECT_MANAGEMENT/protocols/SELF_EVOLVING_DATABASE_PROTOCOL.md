> **Vedic Mastery Study v2.0 - Self-Evolving Database Protocol v2.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol governs the evolution of the Supabase (PostgreSQL) database schema and taxonomy, ensuring that the knowledge base can grow and adapt to new discoveries without compromising its structural integrity. It provides a systematic, safe, and audited process for modifying the core classification system.

---

## 2. SCOPE

This protocol applies to any proposed changes to:
-   The `taxonomy` table (our "Dewey Decimal System").
-   The database schema itself (adding/modifying tables or columns).

---

## 3. CORE WORKFLOW: TAXONOMY EVOLUTION

This workflow is triggered when content is discovered that cannot be accurately classified under the existing taxonomy.

### 3.1. Step 1: Conflict Detection

-   During the import process, the `taxonomy_manager.py` script will attempt to classify each verse.
-   If a verse cannot be classified with high confidence (e.g., no match, multiple ambiguous matches, or it represents a hybrid concept), it is flagged.
-   The conflict is logged in the `classification_conflicts` table with the verse ID and the nature of the conflict.

### 3.2. Step 2: Pattern Analysis

-   On a regular basis (or when a critical mass of conflicts is reached), a process will analyze the `classification_conflicts` table for patterns.
-   **Example**: If 20 verses from a new text are all flagged as a hybrid of "Yoga" and "Vedanta", this indicates a need for a new taxonomy branch.

### 3.3. Step 3: Proposal Generation

-   Based on the pattern analysis, the system will automatically generate a formal proposal for a taxonomy evolution.
-   The proposal is stored in the `taxonomy_proposals` table and includes:
    -   **`proposal_type`**: e.g., `new_branch`, `hybrid_category`, `restructure`.
    -   **`proposed_code`**: The new classification code (e.g., `8.350`).
    -   **`proposed_name`**: The name for the new category (e.g., "Yoga-Vedanta Synthesis").
    -   **`justification`**: The reasoning, supported by the conflict data.
    -   **`affected_verses`**: The number of verses that would be re-classified under this new category.

### 3.4. Step 4: Impact Analysis

-   Before presenting the proposal to the user, the system runs an impact analysis:
    -   What other parts of the taxonomy are affected?
    -   Are there any downstream effects on cross-references or concepts?
    -   What is the estimated effort to implement this change?

### 3.5. Step 5: User Approval (Critical Gate)

-   The complete proposal, including the justification and impact analysis, is presented to the user.
-   The user must provide explicit approval to proceed.

### 3.6. Step 6: Migration Execution

-   If approved, the `schema_migrator.py` script is invoked.
-   It performs the following actions in a single transaction:
    1.  **Generates Migration & Rollback SQL**: Creates the specific SQL scripts to apply and revert the change.
    2.  **Logs Scripts**: Stores the migration and rollback scripts in the `taxonomy_migrations` table.
    3.  **Applies Migration**: Executes the SQL to modify the `taxonomy` table.
    4.  **Updates Version**: Creates a new entry in `taxonomy_versions` with a snapshot of the new taxonomy.
    5.  **Re-classifies Verses**: Updates the `verse_classification` for all affected verses.
    6.  **Resolves Conflicts**: Marks the original conflicts in `classification_conflicts` as resolved.

### 3.7. Step 7: Validation

-   The system validates that the new taxonomy branch exists, the verses have been re-classified, and no data was lost.

---

## 4. SCHEMA MIGRATION

Any changes to the database schema (adding tables/columns) must follow a similar, rigorous process:

1.  **Proposal**: A detailed proposal outlining the change, the reason, and the impact.
2.  **User Approval**.
3.  **Script Generation**: Creation of a migration script and a corresponding rollback script.
4.  **Backup**: A full database backup is taken immediately before migration.
5.  **Execution**: The migration script is run.
6.  **Validation**: The new schema is validated.
7.  **Logging**: The migration is logged in the `taxonomy_migrations` table.

---

## 5. GOVERNANCE PRINCIPLES

-   **Immutability of History**: The `taxonomy_migrations` and `taxonomy_versions` tables are append-only. We never delete the history of how the system evolved.
-   **Safety First**: Every migration must have a corresponding, tested rollback script.
-   **Atomicity**: All migration steps are performed within a single database transaction to ensure that the system is never left in a partially migrated state.
-   **Human Oversight**: All significant structural changes require explicit user approval.
