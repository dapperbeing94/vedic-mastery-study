_# FIRECRAWL INTEGRATION PROTOCOL

---

## 1.0 Primary Directive

To automate the acquisition of Vedic texts and related scholarly materials from web sources, ensuring a continuous and scalable pipeline for populating the Vedic Mastery knowledge base. Firecrawl is the designated tool for all web scraping and crawling operations.

## 2.0 Core Use Cases

1.  **Bulk Text Acquisition**: Crawling and scraping entire websites containing Vedic texts (e.g., online libraries, digital archives).
2.  **Targeted Commentary Extraction**: Scraping specific webpages for scholarly commentaries, translations, and articles related to a verse or text.
3.  **Glossary & Dictionary Building**: Extracting definitions and terms from online Sanskrit dictionaries and glossaries to enrich the internal linguistic database.
4.  **Continuous Monitoring**: Setting up scheduled crawls to monitor key websites for new publications or updated content.

## 3.0 Standard Operating Procedure (SOP)

This workflow is triggered whenever a new digital text source is identified.

| Step | Action | Tool/Method | Description |
| :--- | :--- | :--- | :--- |
| 1 | **Identify Target URL** | Manual or Automated | A URL is identified for a new text, commentary, or resource to be added to the knowledge base. |
| 2 | **Initiate Scrape/Crawl** | `firecrawl` MCP | Execute a Firecrawl job via the MCP connector. Use `scrape` for single pages and `crawl` for entire websites. |
| 3 | **Specify Extraction Schema** | Firecrawl `pageOptions` | Define the specific data to be extracted, focusing on clean, structured content (e.g., `{ "mainContent": "article > div.content" }`). |
| 4 | **Process Raw Data** | Python Script | The raw Markdown/JSON output from Firecrawl is processed to clean HTML tags, normalize text, and structure it for database ingestion. |
| 5 | **Validate & Stage** | Manual Review | The cleaned data is staged for a brief manual review to ensure accuracy and integrity before it is committed to the database. |
| 6 | **Ingest into Database** | Python + Supabase Client | The validated text is inserted into the appropriate tables (`texts`, `commentaries`, `translations`, etc.) in the Supabase database. |
| 7 | **Update Roadmap** | `depth_tracker.py` | The project roadmap and depth tracker are updated to reflect the acquisition of the new text. |

## 4.0 Integration Points

Firecrawl is to be deeply threaded into the following project workflows:

-   **`TRANSFORMATION_2_EXECUTION_PLAN.md`**: Firecrawl is the primary tool for Phase 1 (Data Migration & Enrichment), responsible for acquiring any texts not available in the initial GitHub data dumps.
-   **`VEDIC_SAGE_HYBRID_PERSONA_PROTOCOL.md`**: When the Vedic Sage identifies a gap in commentaries or related texts during its analysis, it can trigger a Firecrawl job to search for and acquire the missing information from the web.
-   **`LINGUISTICS_EXPERT_PERSONA_PROTOCOL.md`**: When building the internal linguistic knowledge base, the Linguistics Expert can use Firecrawl to scrape online dictionaries and grammatical resources to populate the `dictionary_entries` and `grammatical_rules` tables.

## 5.0 Example Invocation (MCP CLI)

```bash
# Scrape a single commentary page
manus-mcp-cli tool call scrape --server firecrawl --input '{
  "url": "https://www.sacred-texts.com/hin/rigveda/rv01001.htm",
  "pageOptions": {
    "onlyMainContent": true
  }
}'

# Crawl an entire website for all Upanishads
manus-mcp-cli tool call crawl --server firecrawl --input '{
  "url": "https://www.upanishads.org/",
  "crawlerOptions": {
    "includes": ["/upanishads/*"],
    "excludes": ["/forums/", "/blog/"]
  }
}'
```

---
**Status**: Protocol defined. Ready for integration.
