> **Vedic Mastery Study v2.0 - Quality Assessment Protocol v2.0**
> **Last Updated**: November 23, 2025
> **Status**: ACTIVE

---

## 1. PURPOSE

This protocol defines the framework and metrics for assessing the quality and depth of the analytical work performed by the Vedic Sage persona. Its purpose is to move beyond simple word counts and establish a robust, quantitative measure of knowledge depth, ensuring that our work is consistently thorough and insightful.

---

## 2. SCOPE

This protocol is applied during Phase 6 of the `VEDIC_SAGE_KNOWLEDGE_ACQUISITION_PROTOCOL`. It is executed by the `quality_assessor.py` script.

---

## 3. QUALITY METRICS

For each verse that has been analyzed, the following metrics are calculated and stored in the `quality_metrics` table. Each metric is scored on a scale of 0.0 to 1.0.

### 3.1. Analysis Completeness (Weight: 30%)

-   **Description**: Measures the depth and thoroughness of the interpretation in the `verse_analysis` table.
-   **Calculation**:
    -   Word count of the analysis text.
    -   Presence and quality of keywords.
    -   Linguistic complexity and richness of the vocabulary used.
    -   (Future) Semantic analysis to check for superficial vs. deep interpretation.

### 3.2. Commentary Integration (Weight: 20%)

-   **Description**: Measures how well traditional commentaries have been integrated.
-   **Calculation**:
    -   Presence of a synthesized commentary entry (where `is_original` = `FALSE`).
    -   Number of original source commentaries (`is_original` = `TRUE`) that were referenced.
    -   Identification of agreements and disagreements among commentators.

### 3.3. Cross-Reference Density (Weight: 25%)

-   **Description**: Measures the richness of the verse's connections to the rest of the knowledge base.
-   **Calculation**:
    -   Total number of entries in `cross_references` where this verse is the source or target.
    -   Variety of `relationship_type`s used (not just `related_to`).
    -   Number of connections to texts outside of its own category (e.g., an Upanishad verse linked to a Purana).

### 3.4. Conceptual Clarity (Weight: 15%)

-   **Description**: Measures how well the verse is mapped to our conceptual ontology.
-   **Calculation**:
    -   Number of concepts tagged in the `verse_concepts` table.
    -   Relevance scores of the tagged concepts.
    -   Clarity and completeness of the descriptions for the tagged concepts in the main `concepts` table.

### 3.5. Provenance & Validation (Weight: 10%)

-   **Description**: A foundational check to ensure all data is traceable and validated.
-   **Calculation**:
    -   `1.0` if the verse has a valid link to a `source_texts` entry.
    -   `1.0` if all cross-references have been marked as `validated`.
    -   `0.0` otherwise.

---

## 4. OVERALL QUALITY SCORE

### 4.1. Verse-Level Score

The `overall_quality` score for a single verse is the weighted average of the five metrics above.

```
overall_quality = (analysis_completeness * 0.30) + 
                  (commentary_integration * 0.20) + 
                  (cross_ref_density * 0.25) + 
                  (conceptual_clarity * 0.15) + 
                  (provenance * 0.10)
```

### 4.2. Text-Level Depth Score

The final `depth_score` for an entire text (which is stored in the `progress_tracking` table) is the average `overall_quality` score of all its verses.

---

## 5. QUALITY ASSESSMENT WORKFLOW

1.  **Invocation**: The `quality_assessor.py` script is called at the end of the deepening workflow for a specific text.
2.  **Calculation**: The script iterates through every verse of the text, calculates the five metrics, and computes the `overall_quality` score for each.
3.  **Storage**: The results are stored in the `quality_metrics` table.
4.  **Aggregation**: The script then calculates the average score for the entire text.
5.  **Comparison**: It compares the calculated text-level depth score against the `target_depth_score` for that text in the `deepening_queue`.
6.  **Gap Analysis**: If the score is below the target, the script identifies which specific metrics are weakest (e.g., "Low Cross-Reference Density in Chapter 3"). This gap analysis is presented to the Vedic Sage persona.
7.  **Decision**: Based on the gap analysis, a decision is made:
    -   **If Score >= Target**: The quality is sufficient. Proceed to final synthesis.
    -   **If Score < Target**: The quality is insufficient. Loop back to the relevant phase(s) of the deepening workflow to address the identified gaps.

---

## 6. CONTINUOUS IMPROVEMENT

This protocol is designed to be self-improving. The metrics and weights can be adjusted over time as we gain a better understanding of what constitutes true knowledge depth. Any changes to the metrics themselves will be managed by the `SELF_EVOLVING_DATABASE_PROTOCOL`.
