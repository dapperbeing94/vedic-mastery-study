# TRANSFORMATION 2.0 EXECUTION PLAN (v2.0)

---

## 1.0 Objective

To execute a major architectural transformation of the Vedic Mastery project, migrating from a local SQLite database to a scalable, cloud-based Supabase (PostgreSQL) architecture. This transformation will also establish a self-sufficient Translation Layer and deeply integrate automated web scraping capabilities via Firecrawl.

## 2.0 Key Upgrades in v2.0

-   **Linguistic Knowledge Base**: Addition of a comprehensive internal dictionary and grammar database.
-   **Translation Layer**: New multi-tiered architecture for cost-effective and scholarly translations.
-   **Firecrawl Integration**: Automated text acquisition is now a core component of the data pipeline.

## 3.0 Execution Phases

| Phase | Title | Key Activities | Estimated Time | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Infrastructure Setup** | - Set up Supabase project & obtain credentials.<br>- Configure network access and security rules.<br>- Create the initial database schema (37 core tables). | 2-3 Hours | Not Started |
| **2** | **Linguistic Resource Import** | - **(2A)** Clone and parse the Monier-Williams dictionary (MWS) GitHub repo.<br>- **(2B)** Import MWS data into the `dictionary_entries` table.<br>- **(2C)** Clone and parse the Itihasa translation corpus.<br>- **(2D)** Import Itihasa data into the `pre_translated_corpus` table. | 7-12 Hours | Not Started |
| **3** | **Core Data Migration** | - Export all 100,729+ verses from the local `vedic_knowledge.db` (SQLite).<br>- Transform and clean the data for PostgreSQL compatibility.<br>- Bulk insert the core Vedic texts into the new Supabase tables. | 4-6 Hours | Not Started |
| **4** | **Service & Protocol Integration** | - Deploy the `Translation Layer` as a callable service.<br>- Update all Python scripts and personas to use the new Supabase database connection.<br>- Integrate `Firecrawl` calls into the Vedic Sage and Linguistics Expert workflows.<br>- Conduct end-to-end system tests. | 3-5 Hours | Not Started |

## 4.0 Pre-requisites

-   User has created a Supabase account.
-   User has provided the Supabase project URL and `anon` key.

## 5.0 Post-Transformation State

-   All Vedic data will reside in a scalable, cloud-hosted PostgreSQL database.
-   The system will possess a foundational, internal linguistic knowledge base, significantly reducing reliance on external translation APIs.
-   The project will have a robust, automated pipeline for acquiring new texts and commentaries from the web.
-   The `Vedic Sage` and `Linguistics Expert` personas will be fully operational within the new, integrated architecture.

---
**Status**: Plan updated to v2.0. Ready for execution pending user approval.
