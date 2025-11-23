#!/usr/bin/env python3
"""
Vedic Mastery Study - Continuity and Thoroughness Protocol
Automated tracking system for breadth and depth across the Vedic framework

Usage:
    python3 vedic_tracker.py --status          # Show current status
    python3 vedic_tracker.py --recommend       # Get top 5 recommendations
    python3 vedic_tracker.py --update          # Recalculate all scores
    python3 vedic_tracker.py --dashboard       # Generate full dashboard
"""

import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path

# Database path
DB_PATH = "/home/ubuntu/vedic-mastery-study/00_DATABASE/vedic_knowledge.db"
STUDY_DOCS_PATH = "/home/ubuntu/vedic-mastery-study/01_STUDY_DOCUMENTS"

class VedicTracker:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()
    
    # ========== DEPTH SCORING ==========
    
    def calculate_depth_score(self, text_id):
        """
        Calculate depth score (0-10) for a text based on:
        - Study documents existence
        - File size and structure
        - Depth criteria met
        """
        cursor = self.conn.cursor()
        
        # Get text info
        cursor.execute("SELECT * FROM texts WHERE id = ?", (text_id,))
        text = cursor.fetchone()
        
        if not text:
            return 0
        
        score = 0
        
        # Level 1: Text identified (always true if in database)
        score += 1
        
        # Level 2-3: Study status
        if text['study_status'] == 'completed':
            score += 2
        elif text['study_status'] == 'in_progress':
            score += 1
        
        # Level 4-5: File existence and size
        if text['file_path']:
            file_path = Path(text['file_path'])
            if file_path.exists():
                file_size = file_path.stat().st_size
                if file_size > 5000:  # >5KB
                    score += 1
                if file_size > 15000:  # >15KB
                    score += 1
        
        # Level 6-9: Depth criteria
        cursor.execute("""
            SELECT COUNT(*) as met_count 
            FROM depth_criteria 
            WHERE text_id = ? AND criterion_met = 1
        """, (text_id,))
        met_count = cursor.fetchone()['met_count']
        score += min(4, met_count)  # Up to 4 points for criteria
        
        return min(10, score)
    
    def calculate_category_breadth_score(self, category_id):
        """
        Calculate breadth score (0-10) for a category based on:
        - Percentage of expected texts covered
        """
        cursor = self.conn.cursor()
        
        # Count texts in this category with study_status = 'completed'
        cursor.execute("""
            SELECT COUNT(*) as completed_count
            FROM texts
            WHERE category = (SELECT name FROM categories WHERE id = ?)
            AND study_status = 'completed'
        """, (category_id,))
        completed_count = cursor.fetchone()['completed_count']
        
        # Get total expected texts (from subcategories or estimate)
        cursor.execute("""
            SELECT SUM(expected_text_count) as total_expected
            FROM subcategories
            WHERE category_id = ?
        """, (category_id,))
        result = cursor.fetchone()
        total_expected = result['total_expected'] if result['total_expected'] else 10
        
        # Calculate percentage
        if total_expected == 0:
            return 0
        
        percentage = (completed_count / total_expected) * 100
        
        # Convert to 0-10 scale
        if percentage >= 80:
            return 10
        elif percentage >= 60:
            return 8
        elif percentage >= 40:
            return 6
        elif percentage >= 20:
            return 4
        elif percentage > 0:
            return 2
        else:
            return 0
    
    def calculate_category_depth_score(self, category_id):
        """
        Calculate average depth score for all texts in a category
        """
        cursor = self.conn.cursor()
        
        # Get all texts in this category
        cursor.execute("""
            SELECT id FROM texts
            WHERE category = (SELECT name FROM categories WHERE id = ?)
            AND study_status = 'completed'
        """, (category_id,))
        texts = cursor.fetchall()
        
        if not texts:
            return 0
        
        total_depth = sum(self.calculate_depth_score(text['id']) for text in texts)
        return round(total_depth / len(texts), 1)
    
    def calculate_combined_score(self, breadth, depth):
        """
        Combined score = (Breadth × 0.3) + (Depth × 0.7)
        """
        return round((breadth * 0.3) + (depth * 0.7), 1)
    
    # ========== GAP ANALYSIS ==========
    
    def identify_gaps(self):
        """
        Identify all gaps (breadth and depth) across categories
        """
        cursor = self.conn.cursor()
        
        # Clear existing gaps
        cursor.execute("DELETE FROM gap_analysis WHERE resolved = 0")
        
        # Get all categories with their progress
        cursor.execute("""
            SELECT 
                c.*,
                COALESCE(p.breadth_score, 0) as breadth,
                COALESCE(p.depth_score, 0) as depth,
                COALESCE(p.combined_score, 0) as combined
            FROM categories c
            LEFT JOIN progress_tracking p ON c.id = p.category_id
            WHERE c.level = 1
            ORDER BY c.display_order
        """)
        categories = cursor.fetchall()
        
        gaps = []
        
        for category in categories:
            breadth = category['breadth']
            depth = category['depth']
            combined = category['combined']
            
            # Identify breadth gaps
            if breadth < category['target_breadth_score']:
                gap_size = category['target_breadth_score'] - breadth
                priority = self.calculate_priority(category, gap_size, 'breadth')
                
                cursor.execute("""
                    INSERT INTO gap_analysis (category_id, gap_type, priority_score, recommendation)
                    VALUES (?, ?, ?, ?)
                """, (
                    category['id'],
                    'breadth',
                    priority,
                    f"Increase breadth coverage in {category['name']} (current: {breadth}/10, target: {category['target_breadth_score']}/10)"
                ))
                gaps.append({
                    'category': category['name'],
                    'type': 'breadth',
                    'priority': priority,
                    'current': breadth,
                    'target': category['target_breadth_score']
                })
            
            # Identify depth gaps
            if depth < category['target_depth_score']:
                gap_size = category['target_depth_score'] - depth
                priority = self.calculate_priority(category, gap_size, 'depth')
                
                cursor.execute("""
                    INSERT INTO gap_analysis (category_id, gap_type, priority_score, recommendation)
                    VALUES (?, ?, ?, ?)
                """, (
                    category['id'],
                    'depth',
                    priority,
                    f"Increase depth in {category['name']} (current: {depth}/10, target: {category['target_depth_score']}/10)"
                ))
                gaps.append({
                    'category': category['name'],
                    'type': 'depth',
                    'priority': priority,
                    'current': depth,
                    'target': category['target_depth_score']
                })
        
        self.conn.commit()
        return gaps
    
    def calculate_priority(self, category, gap_size, gap_type):
        """
        Priority = (Importance × Gap Size × Type Factor)
        
        Importance based on category:
        - Core Vedic Foundation: 10
        - Upanishads: 10
        - Darsanas: 9
        - Smriti: 8
        - Others: 6-7
        
        Type Factor:
        - Depth gaps: 1.5 (prioritize depth for Blue Belt)
        - Breadth gaps: 1.0
        """
        importance_map = {
            'Core Vedic Foundation': 10,
            'Smriti Texts': 8,
            'Darsanas': 9,
            'Tantra and Agamas': 6,
            'Yogic Corpus': 7,
            'Sciences and Knowledge Systems': 5,
            'Commentarial Traditions': 7,
            'Regional Canonical Texts': 4,
            'Modern Synthesizers': 3,
            'Synthesis Work': 9
        }
        
        importance = importance_map.get(category['name'], 5)
        type_factor = 1.5 if gap_type == 'depth' else 1.0
        
        return round(importance * gap_size * type_factor, 2)
    
    # ========== RECOMMENDATIONS ==========
    
    def get_recommendations(self, n=5):
        """
        Get top N recommendations based on priority scores
        """
        cursor = self.conn.cursor()
        
        # First, update gaps
        self.identify_gaps()
        
        # Get top recommendations
        cursor.execute("""
            SELECT 
                c.name as category,
                g.gap_type,
                g.priority_score,
                g.recommendation
            FROM gap_analysis g
            JOIN categories c ON g.category_id = c.id
            WHERE g.resolved = 0
            ORDER BY g.priority_score DESC
            LIMIT ?
        """, (n,))
        
        return cursor.fetchall()
    
    # ========== STATUS AND DASHBOARD ==========
    
    def get_overall_status(self):
        """
        Get overall progress status
        """
        cursor = self.conn.cursor()
        
        # Get all main categories with their progress
        cursor.execute("""
            SELECT 
                c.id,
                c.name,
                c.target_breadth_score,
                c.target_depth_score,
                COALESCE(p.breadth_score, 0) as breadth,
                COALESCE(p.depth_score, 0) as depth,
                COALESCE(p.combined_score, 0) as combined
            FROM categories c
            LEFT JOIN progress_tracking p ON c.id = p.category_id
            WHERE c.level = 1
            ORDER BY c.display_order
        """)
        categories = cursor.fetchall()
        
        status = {
            'overall_breadth': 0,
            'overall_depth': 0,
            'overall_combined': 0,
            'categories': []
        }
        
        total_breadth = 0
        total_depth = 0
        
        for category in categories:
            status['categories'].append({
                'name': category['name'],
                'breadth': category['breadth'],
                'depth': category['depth'],
                'combined': category['combined'],
                'target_breadth': category['target_breadth_score'],
                'target_depth': category['target_depth_score']
            })
            
            total_breadth += category['breadth']
            total_depth += category['depth']
        
        # Calculate averages
        n = len(categories)
        status['overall_breadth'] = round(total_breadth / n, 1) if n > 0 else 0
        status['overall_depth'] = round(total_depth / n, 1) if n > 0 else 0
        status['overall_combined'] = self.calculate_combined_score(
            status['overall_breadth'],
            status['overall_depth']
        )
        
        return status
    
    def generate_dashboard(self):
        """
        Generate a comprehensive dashboard
        """
        status = self.get_overall_status()
        recommendations = self.get_recommendations(5)
        
        print("\n" + "="*80)
        print("VEDIC MASTERY STUDY - CONTINUITY & THOROUGHNESS DASHBOARD")
        print("="*80)
        print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "-"*80)
        print("OVERALL PROGRESS")
        print("-"*80)
        print(f"Overall Breadth Score: {status['overall_breadth']}/10")
        print(f"Overall Depth Score:   {status['overall_depth']}/10")
        print(f"Overall Combined:      {status['overall_combined']}/10")
        
        print("\n" + "-"*80)
        print("CATEGORY BREAKDOWN")
        print("-"*80)
        print(f"{'Category':<35} {'Breadth':<10} {'Depth':<10} {'Combined':<10}")
        print("-"*80)
        
        for cat in status['categories']:
            print(f"{cat['name']:<35} {cat['breadth']:<10} {cat['depth']:<10} {cat['combined']:<10}")
        
        print("\n" + "-"*80)
        print("TOP 5 PRIORITIES")
        print("-"*80)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['gap_type'].upper()}] {rec['category']}")
            print(f"   Priority Score: {rec['priority_score']}")
            print(f"   Recommendation: {rec['recommendation']}")
        
        print("\n" + "="*80)
    
    def update_all_scores(self):
        """
        Recalculate and update all scores in the database
        """
        cursor = self.conn.cursor()
        
        print("Updating all scores...")
        
        # Clear existing progress tracking
        cursor.execute("DELETE FROM progress_tracking")
        
        # Get all categories
        cursor.execute("SELECT * FROM categories WHERE level = 1")
        categories = cursor.fetchall()
        
        for category in categories:
            breadth = self.calculate_category_breadth_score(category['id'])
            depth = self.calculate_category_depth_score(category['id'])
            combined = self.calculate_combined_score(breadth, depth)
            
            cursor.execute("""
                INSERT INTO progress_tracking (category_id, breadth_score, depth_score, combined_score)
                VALUES (?, ?, ?, ?)
            """, (category['id'], breadth, depth, combined))
        
        self.conn.commit()
        print("All scores updated successfully!")

def main():
    import sys
    
    tracker = VedicTracker()
    
    if len(sys.argv) < 2:
        print("Usage: python3 vedic_tracker.py [--status|--recommend|--update|--dashboard]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--status":
        status = tracker.get_overall_status()
        print(f"\nOverall Breadth: {status['overall_breadth']}/10")
        print(f"Overall Depth: {status['overall_depth']}/10")
        print(f"Overall Combined: {status['overall_combined']}/10")
    
    elif command == "--recommend":
        recommendations = tracker.get_recommendations(5)
        print("\nTop 5 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec['gap_type'].upper()}] {rec['category']}")
            print(f"   Priority: {rec['priority_score']}")
            print(f"   {rec['recommendation']}")
    
    elif command == "--update":
        tracker.update_all_scores()
    
    elif command == "--dashboard":
        tracker.generate_dashboard()
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
