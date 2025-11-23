# Supabase Schema Setup Instructions

## Phase 1: Infrastructure Setup - Execute Schema

### Step 1: Access Supabase SQL Editor

1. Go to your Supabase project dashboard:
   - URL: https://supabase.com/dashboard/project/yvcyprwldvoubyytptqu

2. Navigate to the **SQL Editor** (in the left sidebar)

### Step 2: Execute the Schema

1. Open the schema file: `00_DATABASE/schema/supabase_schema.sql`

2. Copy the entire contents of the file

3. Paste into the Supabase SQL Editor

4. Click the **"Run"** button (or press Ctrl+Enter)

5. Wait for the execution to complete (should take 10-30 seconds)

### Step 3: Verify the Schema

After execution, verify that all tables were created:

1. Navigate to **Table Editor** in the Supabase dashboard

2. You should see approximately 42 tables, including:
   - Core tables: `texts`, `verses`, `commentaries`, `concepts`, etc.
   - Translation Layer tables: `dictionary_entries`, `pre_translated_corpus`, etc.
   - Taxonomy tables: `taxonomy`, `verse_classification`, etc.
   - Quality & Progress tables: `quality_metrics`, `reading_progress`, etc.

### Expected Table Count

- **Total Tables**: 42
  - 34 tables from existing SQLite schema
  - 5 new Translation Layer tables
  - 3 supporting tables

### Troubleshooting

If you encounter errors:

1. **Foreign Key Errors**: These are expected if tables are created out of order. The script handles this by disabling FK checks temporarily.

2. **Permission Errors**: Ensure you're logged in with the correct account that has admin access to this project.

3. **Syntax Errors**: Check that the entire SQL file was copied correctly without truncation.

### Next Steps

Once the schema is successfully created, return to the chat and confirm:
- "Schema executed successfully"
- Report any errors encountered

The agent will then proceed to Phase 2: Linguistic Resource Import.
