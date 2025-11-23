> **Vedic Mastery Study - Read-Only Knowledge Base Protocol v2.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol defines the rules and procedures for interacting with the Vedic Mastery Study knowledge base in a **read-only** capacity. Its purpose is to allow for safe, non-destructive querying, exploration, and synthesis of the existing knowledge without any risk of modifying the underlying data.

**This protocol is intended for tasks that require drawing conclusions from the existing knowledge base, not for adding new knowledge.**

---

## 2. SCOPE

This protocol is activated when the user asks a question or requests a task that can be fulfilled by querying the database, such as:
-   "What are the main themes of the Brihadaranyaka Upanishad?"
-   "Show me all verses that discuss the concept of Atman."
-   "Compare the concept of Dharma in the Ramayana and the Mahabharata."
-   "Create a summary of Shankara's commentary on Bhagavad Gita Chapter 2."

---

## 3. CORE PRINCIPLES (v2.0 Architecture)

### 3.1. Strict Read-Only Operations

-   Under this protocol, only `SELECT` SQL queries are permitted.
-   `INSERT`, `UPDATE`, `DELETE`, and `ALTER` commands are strictly forbidden.

### 3.2. Acknowledge the Two Layers

-   When presenting information, it is crucial to distinguish between the **Source Layer** and the **Analytical Layer**.
-   **Source Layer data** (the raw verse text, original translations) should be clearly attributed to its external source (e.g., "From DharmicData, based on the BORI Critical Edition").
-   **Analytical Layer data** (our analysis, synthesized commentaries, cross-references) should be presented as the project's own intellectual output (e.g., "Our analysis highlights the following key points...").

### 3.3. Utilize the Full Schema

-   Queries should leverage the full richness of the 34-table schema.
-   Instead of simple keyword searches, queries should use the structured relationships in the database:
    -   Use the `taxonomy` table to query entire branches of knowledge (e.g., all Upanishads).
    -   Use the `cross_references` table to trace arguments and themes across texts.
    -   Use the `verse_concepts` and `concept_relationships` tables to explore the conceptual ontology.

---

## 4. STANDARD QUERY WORKFLOW

When a user prompt activates this protocol:

1.  **Deconstruct the Request**: Break down the user's query into a set of questions that can be answered by the database.
    -   *Example*: "Compare Dharma in the Ramayana and Mahabharata" becomes:
        -   Find all verses in the Ramayana tagged with the `Dharma` concept.
        -   Find all verses in the Mahabharata tagged with the `Dharma` concept.
        -   Retrieve our `verse_analysis` for those verses.
        -   Identify cross-references between these two sets of verses.

2.  **Formulate SQL Queries**: Construct the necessary `SELECT` queries with appropriate `JOIN`s to retrieve the data from both the Source and Analytical Layers.

3.  **Execute Queries**: Run the queries against the `vedic_knowledge.db` database.

4.  **Synthesize the Response**: This is the most critical step. Do not simply dump the raw query results. Synthesize the retrieved data into a coherent, well-structured, and insightful response.
    -   Start with a high-level summary.
    -   Use tables to compare and contrast key points.
    -   Quote key verses (from the Source Layer) to support the analysis.
    -   Reference our own interpretations (from the Analytical Layer).
    -   Clearly distinguish between source material and our analysis.

5.  **Present the Response**: Deliver the synthesized response to the user in a clear, readable format, following the project's standard formatting guidelines.

---

## 5. FORBIDDEN ACTIONS

Under this protocol, the following actions are strictly forbidden:

-   **Modifying the Database**: No `INSERT`, `UPDATE`, or `DELETE` operations.
-   **Adding New Knowledge**: If the answer is not in the database, this protocol does not permit adding it. The correct procedure is to flag it as a knowledge gap and add the relevant text to the `deepening_queue` for the Vedic Sage persona to handle later.
-   **Modifying Files**: This protocol does not permit editing any project files.

---

## 6. EXITING THE PROTOCOL

This protocol is automatically exited upon the successful delivery of the synthesized response to the user. If the user's follow-up prompt requires adding new knowledge or modifying the system, the agent will switch to the appropriate protocol (e.g., `VEDIC_SAGE_KNOWLEDGE_ACQUISITION_PROTOCOL`).
