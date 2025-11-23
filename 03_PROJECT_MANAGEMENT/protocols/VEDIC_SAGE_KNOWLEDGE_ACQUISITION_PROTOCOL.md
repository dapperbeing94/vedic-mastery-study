> **Vedic Mastery Study - Vedic Sage Knowledge Acquisition Protocol v1.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol defines the standard operating procedure for the **Vedic Sage persona** to systematically deepen the knowledge base. It provides a structured, source-agnostic workflow for moving a text from a raw, imported state to a deeply analyzed and cross-referenced state.

Its purpose is to ensure that our analytical work is thorough, consistent, and of high quality, transforming raw data into true wisdom.

---

## 2. SCOPE

This protocol is activated *after* the transformation is complete and the Source Layer has been populated. It governs the day-to-day work of the Vedic Sage persona.

---

## 3. THE 6-PHASE DEEPENING WORKFLOW

This workflow is applied to one text at a time, selected from the `deepening_queue` based on priority.

### 3.1. Phase 1: Foundational Reading & Comprehension

**Goal**: Achieve a complete, surface-level understanding of the text.

1.  **Select Text**: Choose the highest priority text from the `deepening_queue`.
2.  **Read All Verses**: Read every verse of the text from the `verses` table.
3.  **Update Status**: As each verse is read, update its status in the `reading_progress` table from `unread` to `read`.
4.  **Initial Synthesis**: After completing the reading, write a brief, initial synthesis of the text's main themes and structure. This is stored as a temporary document.

**Deliverable**: All verses for the text marked as `read`. An initial synthesis document.

### 3.2. Phase 2: Verse-Level Analysis

**Goal**: Perform a detailed, verse-by-verse interpretation.

1.  **Iterate Through Verses**: Go through the text again, verse by verse.
2.  **Write Analysis**: For each verse, write a detailed analysis in the `verse_analysis` table, covering:
    -   Its literal meaning.
    -   Its philosophical implication.
    -   Key concepts and keywords.
3.  **Update Status**: Update the `reading_progress` status from `read` to `analyzed`.

**Deliverable**: A complete set of entries in the `verse_analysis` table for the text.

### 3.3. Phase 3: Commentary Integration

**Goal**: Integrate traditional wisdom by analyzing commentaries.

1.  **Gather Commentaries**: Identify all available commentaries for the text from the `commentaries` table (where `is_original` = `TRUE`).
2.  **Synthesize Commentaries**: For each verse, read the associated commentaries and write a synthesized summary of the traditional interpretations. This is stored in the `commentaries` table with `is_original` set to `FALSE`.
3.  **Identify Disagreements**: Note any significant points of disagreement or different interpretations among commentators.

**Deliverable**: A synthesized commentary for each verse, stored in the `commentaries` table.

### 3.4. Phase 4: Cross-Reference Mapping

**Goal**: Weave the text into the broader fabric of Vedic knowledge.

1.  **Identify Internal Connections**: Find connections between verses *within* the same text.
2.  **Identify External Connections**: Use keyword and concept matching to find connections to verses in *other* texts across the entire database.
3.  **Create Links**: For each connection found, create an entry in the `cross_references` table, specifying:
    -   `source_verse_id` and `target_verse_id`.
    -   `relationship_type` (e.g., `quotes`, `clarifies`, `contradicts`, `expands_on`).
    -   `confidence_score`.

**Deliverable**: A rich network of entries in the `cross_references` table connected to the text.

### 3.5. Phase 5: Conceptual Tagging & Ontology

**Goal**: Map the text to our master conceptual framework.

1.  **Identify Concepts**: For each verse, identify the core philosophical concepts it discusses (e.g., Brahman, Atman, Karma).
2.  **Create Links**: Create entries in the `verse_concepts` table, linking the verse to the relevant entries in the `concepts` table.
3.  **Refine Ontology**: If the text introduces a new concept or a new relationship between concepts, trigger the `SELF_EVOLVING_DATABASE_PROTOCOL` to update the `concepts` and `concept_relationships` tables.

**Deliverable**: Comprehensive conceptual tagging for the text in the `verse_concepts` table.

### 3.6. Phase 6: Quality Assessment & Final Synthesis

**Goal**: Ensure high quality and produce the final, user-facing deep dive document.

1.  **Run Quality Assessment**: Invoke the `quality_assessor.py` script to score the completeness and depth of the work done in Phases 1-5. The results are stored in the `quality_metrics` table.
2.  **Address Gaps**: If the quality score is below the target, identify the gaps (e.g., missing cross-references, weak analysis) and loop back to the relevant phase to address them.
3.  **Write Deep Dive Document**: Once the quality target is met, generate the final, comprehensive deep dive Markdown document. This document programmatically pulls the data from all the different tables (`verses`, `verse_analysis`, `commentaries`, `cross_references`) to create a holistic view.
4.  **Update Final Status**: Mark the text as `complete` in the `deepening_queue` and update its final depth score in the `progress_tracking` table.

**Deliverable**: A final, high-quality deep dive document and updated project metrics.

---

## 4. ITERATIVE DEEPENING

This entire 6-phase process can be re-applied to the same text in the future. For example, if we import a new commentary for the Bhagavad Gita, we can re-run Phase 3 and Phase 6 for that text to integrate the new knowledge and update the final document, further increasing its depth score.
