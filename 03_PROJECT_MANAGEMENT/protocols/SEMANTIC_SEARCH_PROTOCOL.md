> **Vedic Mastery Study - Semantic Search Protocol v1.0**

This protocol governs the creation and use of vector embeddings for semantic search.

1.  **Embedding Model**: Use a sentence-transformer model (e.g., `all-MiniLM-L6-v2`) for generating embeddings.
2.  **Embedding Pipeline**: A Python script (`embedding_pipeline.py`) will be created to:
    -   Read new verses from the `verses` table.
    -   Generate embeddings for the `devanagari` and `source_translation` fields.
    -   Store the embeddings in a dedicated `verse_embeddings` table with a `vector` column.
3.  **Search Function**: A Supabase edge function will be created to perform vector similarity searches.
