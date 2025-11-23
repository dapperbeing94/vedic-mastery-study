> **Vedic Mastery Study - Supabase Administration Protocol v1.0**

This protocol governs the administration, maintenance, and security of the project's Supabase instance.

1.  **Access Control**: User is the sole owner. Agent access is granted via temporary API keys.
2.  **Schema Changes**: All schema changes must follow the `SELF_EVOLVING_DATABASE_PROTOCOL`.
3.  **Backups**: Automated daily backups configured in Supabase, with weekly backups downloaded to the GitHub repository's `04_ARCHIVES/database_backups/` directory.
4.  **Monitoring**: Regularly monitor resource usage (CPU, memory, storage) via the Supabase dashboard.
