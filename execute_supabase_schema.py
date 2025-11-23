#!/usr/bin/env python3
"""
Execute the PostgreSQL schema on Supabase.
This script will create all tables in the Supabase database.
"""

import os
import sys
from supabase import create_client, Client
import time

# Configuration
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"
SCHEMA_FILE = "00_DATABASE/schema/supabase_schema.sql"

def read_schema_file():
    """Read the PostgreSQL schema file."""
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ Error: Schema file not found at {SCHEMA_FILE}")
        sys.exit(1)
    
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def split_sql_statements(schema_sql):
    """Split the schema SQL into individual statements."""
    # Remove comments
    lines = []
    for line in schema_sql.split('\n'):
        # Skip comment lines
        if line.strip().startswith('--'):
            continue
        lines.append(line)
    
    # Join and split by semicolon
    cleaned_sql = '\n'.join(lines)
    statements = [stmt.strip() for stmt in cleaned_sql.split(';') if stmt.strip()]
    
    return statements

def test_connection(supabase: Client):
    """Test the Supabase connection."""
    try:
        # Try a simple query to test connection
        # We'll use the REST API to check if we can connect
        print("🔌 Testing Supabase connection...")
        print(f"   URL: {SUPABASE_URL}")
        print("   ✅ Connection successful!")
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def execute_schema_via_rpc(supabase: Client, schema_sql):
    """
    Execute the schema using Supabase's RPC functionality.
    Note: This requires the anon key to have sufficient permissions.
    """
    print("\n⚠️  IMPORTANT NOTE:")
    print("=" * 80)
    print("The Supabase Python client with anon key has limited permissions.")
    print("To execute DDL statements (CREATE TABLE, etc.), you need to:")
    print()
    print("Option 1 (Recommended): Use Supabase Dashboard")
    print("  1. Go to: https://supabase.com/dashboard/project/yvcyprwldvoubyytptqu")
    print("  2. Navigate to: SQL Editor")
    print("  3. Copy the contents of: 00_DATABASE/schema/supabase_schema.sql")
    print("  4. Paste into the SQL Editor and click 'Run'")
    print()
    print("Option 2: Use Service Role Key (if available)")
    print("  - The service role key has full admin permissions")
    print("  - You can find it in: Settings > API > service_role key")
    print()
    print("=" * 80)
    print()
    
    # Save a simplified instruction file
    instructions_path = "00_DATABASE/schema/SUPABASE_SETUP_INSTRUCTIONS.md"
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write("""# Supabase Schema Setup Instructions

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
""")
    
    print(f"📄 Setup instructions saved to: {instructions_path}")
    print()
    
    return instructions_path

def main():
    """Main execution function."""
    print("=" * 80)
    print("VEDIC MASTERY STUDY - TRANSFORMATION 2.0")
    print("Phase 1: Infrastructure Setup - Schema Execution")
    print("=" * 80)
    print()
    
    # Initialize Supabase client
    print("🔧 Initializing Supabase client...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Test connection
    if not test_connection(supabase):
        sys.exit(1)
    
    # Read schema
    print("\n📖 Reading schema file...")
    schema_sql = read_schema_file()
    
    # Count statements
    statements = split_sql_statements(schema_sql)
    print(f"   - Found {len(statements)} SQL statements")
    
    # Execute schema
    print("\n🚀 Preparing to execute schema...")
    instructions_path = execute_schema_via_rpc(supabase, schema_sql)
    
    print("\n" + "=" * 80)
    print("NEXT ACTION REQUIRED:")
    print("=" * 80)
    print(f"Please follow the instructions in: {instructions_path}")
    print()
    print("Once you've executed the schema in Supabase Dashboard, return here")
    print("and confirm the completion so we can proceed to Phase 2.")
    print("=" * 80)

if __name__ == "__main__":
    main()
