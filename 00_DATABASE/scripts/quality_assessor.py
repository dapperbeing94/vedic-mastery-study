#!/usr/bin/env python3
"""
Quality Assessor - Vedic Mastery Study v2.0
Assesses the quality and depth of analytical work using the Quality Assessment Protocol.
"""

import sqlite3
from typing import Dict, List, Tuple
from datetime import datetime

class QualityAssessor:
    def __init__(self, db_path: str = "../vedic_knowledge.db"):
        self.db_path = db_path
        self.conn = None
        
        # Quality metric weights (from Quality Assessment Protocol)
        self.weights = {
            'analysis_completeness': 0.30,
            'commentary_integration': 0.20,
            'cross_ref_density': 0.25,
            'conceptual_clarity': 0.15,
            'provenance': 0.10
        }
    
    def connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
    
    def assess_verse(self, verse_id: int) -> Dict[str, float]:
        """
        Assess the quality of a single verse's analytical work.
        
        Returns:
            Dict with individual metric scores and overall quality
        """
        metrics = {}
        
        # 1. Analysis Completeness (30%)
        metrics['analysis_completeness'] = self._assess_analysis_completeness(verse_id)
        
        # 2. Commentary Integration (20%)
        metrics['commentary_integration'] = self._assess_commentary_integration(verse_id)
        
        # 3. Cross-Reference Density (25%)
        metrics['cross_ref_density'] = self._assess_cross_ref_density(verse_id)
        
        # 4. Conceptual Clarity (15%)
        metrics['conceptual_clarity'] = self._assess_conceptual_clarity(verse_id)
        
        # 5. Provenance & Validation (10%)
        metrics['provenance'] = self._assess_provenance(verse_id)
        
        # Calculate overall quality score
        overall = sum(metrics[k] * self.weights[k] for k in metrics.keys())
        metrics['overall_quality'] = overall
        
        # Store in database
        self._store_quality_metrics(verse_id, metrics)
        
        return metrics
    
    def _assess_analysis_completeness(self, verse_id: int) -> float:
        """Assess the depth of verse analysis."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT literal_meaning, philosophical_implication, keywords
            FROM verse_analysis
            WHERE verse_id = ?
        """, (verse_id,))
        row = cursor.fetchone()
        
        if not row:
            return 0.0
        
        # Calculate score based on content length and presence
        score = 0.0
        
        if row['literal_meaning']:
            word_count = len(row['literal_meaning'].split())
            score += min(word_count / 100, 0.4)  # Max 0.4 for literal meaning
        
        if row['philosophical_implication']:
            word_count = len(row['philosophical_implication'].split())
            score += min(word_count / 150, 0.4)  # Max 0.4 for philosophical
        
        if row['keywords']:
            keyword_count = len(row['keywords'].split(','))
            score += min(keyword_count / 10, 0.2)  # Max 0.2 for keywords
        
        return min(score, 1.0)
    
    def _assess_commentary_integration(self, verse_id: int) -> float:
        """Assess how well commentaries are integrated."""
        cursor = self.conn.cursor()
        
        # Count original commentaries
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM commentaries 
            WHERE verse_id = ? AND is_original = TRUE
        """, (verse_id,))
        original_count = cursor.fetchone()['count']
        
        # Check for synthesized commentary
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM commentaries 
            WHERE verse_id = ? AND is_original = FALSE
        """, (verse_id,))
        synthesized_count = cursor.fetchone()['count']
        
        score = 0.0
        
        # Score based on original commentaries (max 0.5)
        score += min(original_count / 5, 0.5)
        
        # Score for synthesized commentary (max 0.5)
        if synthesized_count > 0:
            score += 0.5
        
        return min(score, 1.0)
    
    def _assess_cross_ref_density(self, verse_id: int) -> float:
        """Assess the richness of cross-references."""
        cursor = self.conn.cursor()
        
        # Count total cross-references
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM cross_references 
            WHERE source_verse_id = ? OR target_verse_id = ?
        """, (verse_id, verse_id))
        total_refs = cursor.fetchone()['count']
        
        # Count variety of relationship types
        cursor.execute("""
            SELECT COUNT(DISTINCT relationship_type) as count 
            FROM cross_references 
            WHERE source_verse_id = ? OR target_verse_id = ?
        """, (verse_id, verse_id))
        relationship_variety = cursor.fetchone()['count']
        
        # Count external category connections
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM cross_references cr
            JOIN verses v1 ON cr.source_verse_id = v1.id
            JOIN verses v2 ON cr.target_verse_id = v2.id
            JOIN texts t1 ON v1.text_id = t1.id
            JOIN texts t2 ON v2.text_id = t2.id
            WHERE (cr.source_verse_id = ? OR cr.target_verse_id = ?)
            AND t1.category != t2.category
        """, (verse_id, verse_id))
        external_refs = cursor.fetchone()['count']
        
        score = 0.0
        score += min(total_refs / 10, 0.5)  # Max 0.5 for quantity
        score += min(relationship_variety / 5, 0.25)  # Max 0.25 for variety
        score += min(external_refs / 3, 0.25)  # Max 0.25 for external connections
        
        return min(score, 1.0)
    
    def _assess_conceptual_clarity(self, verse_id: int) -> float:
        """Assess conceptual tagging quality."""
        cursor = self.conn.cursor()
        
        # Count tagged concepts
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM verse_concepts 
            WHERE verse_id = ?
        """, (verse_id,))
        concept_count = cursor.fetchone()['count']
        
        # Check relevance scores
        cursor.execute("""
            SELECT AVG(relevance_score) as avg_relevance 
            FROM verse_concepts 
            WHERE verse_id = ?
        """, (verse_id,))
        avg_relevance = cursor.fetchone()['avg_relevance'] or 0.0
        
        score = 0.0
        score += min(concept_count / 5, 0.5)  # Max 0.5 for quantity
        score += avg_relevance * 0.5  # Max 0.5 for relevance
        
        return min(score, 1.0)
    
    def _assess_provenance(self, verse_id: int) -> float:
        """Assess data provenance and validation."""
        cursor = self.conn.cursor()
        
        # Check for valid source_text link
        cursor.execute("""
            SELECT source_text_id 
            FROM verses 
            WHERE id = ?
        """, (verse_id,))
        row = cursor.fetchone()
        
        if not row or not row['source_text_id']:
            return 0.0
        
        return 1.0  # Full score if provenance is valid
    
    def _store_quality_metrics(self, verse_id: int, metrics: Dict[str, float]):
        """Store quality metrics in the database."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO quality_metrics 
            (verse_id, analysis_completeness, commentary_integration, 
             cross_ref_density, conceptual_clarity, provenance, 
             overall_quality, assessment_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, (verse_id, metrics['analysis_completeness'], 
              metrics['commentary_integration'], metrics['cross_ref_density'],
              metrics['conceptual_clarity'], metrics['provenance'], 
              metrics['overall_quality']))
        
        self.conn.commit()
    
    def assess_text(self, text_id: int) -> Dict:
        """
        Assess the overall quality of all verses in a text.
        
        Returns:
            Dict with text-level statistics and depth score
        """
        cursor = self.conn.cursor()
        
        # Get all verses for this text
        cursor.execute("SELECT id FROM verses WHERE text_id = ?", (text_id,))
        verse_ids = [row['id'] for row in cursor.fetchall()]
        
        if not verse_ids:
            return {'depth_score': 0.0, 'verses_assessed': 0}
        
        # Assess each verse
        total_quality = 0.0
        for verse_id in verse_ids:
            metrics = self.assess_verse(verse_id)
            total_quality += metrics['overall_quality']
        
        # Calculate average depth score
        depth_score = total_quality / len(verse_ids)
        
        return {
            'depth_score': depth_score,
            'verses_assessed': len(verse_ids),
            'text_id': text_id
        }

def main():
    """Example usage."""
    assessor = QualityAssessor()
    assessor.connect()
    
    # Example: Assess a specific verse
    verse_id = 1
    metrics = assessor.assess_verse(verse_id)
    
    print(f"Quality Metrics for Verse {verse_id}:")
    for key, value in metrics.items():
        print(f"  {key}: {value:.2f}")
    
    assessor.close()

if __name__ == "__main__":
    main()
