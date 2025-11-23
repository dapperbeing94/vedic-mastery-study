> **Vedic Mastery Study - Data Integrity Protocol v1.0**

This protocol ensures the integrity and consistency of the data in the Supabase database.

1.  **Validation Scripts**: Python scripts will be created to:
    -   Check for orphaned records (e.g., verses without a text).
    -   Validate foreign key relationships.
    -   Check for duplicate entries.
2.  **Regular Audits**: The validation scripts will be run weekly as a scheduled task.
3.  **Conflict Resolution**: Any integrity issues will be logged in a `data_integrity_issues` table for manual review.
