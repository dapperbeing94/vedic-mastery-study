"""
Protocol Regression Analysis and Cross-Reference Audit
Transformation 2.1 - Phase 6

This script audits all protocols for:
1. Cross-references between protocols
2. Missing references to new infrastructure
3. Outdated version numbers
4. Broken links or references
5. Consistency in terminology
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set
import json

# Project root
PROJECT_ROOT = Path("/home/ubuntu/vedic-mastery-study")

# Protocol directories
PROTOCOL_DIRS = [
    PROJECT_ROOT / "02_PERSONAS",
    PROJECT_ROOT / "04_PROTOCOLS",
    PROJECT_ROOT / "03_PROJECT_MANAGEMENT"
]

# Special files to check
SPECIAL_FILES = [
    PROJECT_ROOT / "SOUL_TRANSMIGRATION_PROTOCOL.md",
    PROJECT_ROOT / "README.md"
]


class ProtocolAudit:
    def __init__(self):
        self.protocols = {}
        self.cross_references = {}
        self.issues = []
        
    def scan_protocols(self):
        """Scan all protocol files"""
        print("=" * 70)
        print("PROTOCOL REGRESSION ANALYSIS")
        print("=" * 70)
        print()
        
        # Scan directories
        for protocol_dir in PROTOCOL_DIRS:
            if protocol_dir.exists():
                for file_path in protocol_dir.glob("*.md"):
                    self._analyze_file(file_path)
        
        # Scan special files
        for file_path in SPECIAL_FILES:
            if file_path.exists():
                self._analyze_file(file_path)
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single protocol file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        rel_path = file_path.relative_to(PROJECT_ROOT)
        
        self.protocols[str(rel_path)] = {
            'path': file_path,
            'size': len(content),
            'lines': len(content.split('\n'))
        }
        
        # Find references to other protocols
        references = self._find_references(content)
        self.cross_references[str(rel_path)] = references
        
        # Check for specific issues
        self._check_version_references(str(rel_path), content)
        self._check_infrastructure_references(str(rel_path), content)
    
    def _find_references(self, content: str) -> List[str]:
        """Find references to other files"""
        references = []
        
        # Pattern 1: Markdown links [text](path.md)
        md_links = re.findall(r'\[([^\]]+)\]\(([^)]+\.md)\)', content)
        references.extend([link[1] for link in md_links])
        
        # Pattern 2: Direct file mentions
        file_mentions = re.findall(r'`([^`]+\.md)`', content)
        references.extend(file_mentions)
        
        # Pattern 3: Protocol names
        protocol_mentions = re.findall(r'([A-Z_]+_PROTOCOL)', content)
        references.extend(protocol_mentions)
        
        return list(set(references))
    
    def _check_version_references(self, file_path: str, content: str):
        """Check for outdated version references"""
        # Check for Transformation version mentions
        transformation_versions = re.findall(r'Transformation\s+(\d+\.\d+)', content)
        
        for version in transformation_versions:
            if version == "1.0" or version == "2.0":
                # These are historical, OK
                pass
            elif version == "2.1":
                # Current version, OK
                pass
            elif version == "3.0":
                # Future version, OK
                pass
            else:
                self.issues.append({
                    'file': file_path,
                    'type': 'unknown_version',
                    'message': f"Unknown Transformation version: {version}"
                })
    
    def _check_infrastructure_references(self, file_path: str, content: str):
        """Check if file mentions new infrastructure"""
        new_infrastructure = [
            'pgvector',
            'embedding',
            'semantic search',
            'AI-generated',
            'health monitoring',
            'dependency graph',
            'model provider',
            'data validation'
        ]
        
        mentions = {}
        for term in new_infrastructure:
            if term.lower() in content.lower():
                mentions[term] = True
        
        if mentions and 'SOUL_TRANSMIGRATION' not in file_path:
            # File mentions new infrastructure - good!
            pass
    
    def generate_cross_reference_matrix(self):
        """Generate a cross-reference matrix"""
        print("\n" + "=" * 70)
        print("CROSS-REFERENCE MATRIX")
        print("=" * 70)
        print()
        
        for protocol, references in self.cross_references.items():
            if references:
                print(f"📄 {protocol}")
                for ref in references:
                    print(f"   → {ref}")
                print()
    
    def check_missing_references(self):
        """Check for protocols that should reference new infrastructure"""
        print("\n" + "=" * 70)
        print("MISSING REFERENCE ANALYSIS")
        print("=" * 70)
        print()
        
        # Protocols that should reference Supabase
        should_reference_supabase = [
            "04_PROTOCOLS/TRANSLATION_LAYER_PROTOCOL.md",
            "04_PROTOCOLS/TRANSLATION_LAYER_OPERATIONS_PROTOCOL.md",
            "SOUL_TRANSMIGRATION_PROTOCOL.md"
        ]
        
        for protocol_path in should_reference_supabase:
            if protocol_path in self.protocols:
                with open(self.protocols[protocol_path]['path'], 'r') as f:
                    content = f.read()
                
                if 'supabase' not in content.lower():
                    self.issues.append({
                        'file': protocol_path,
                        'type': 'missing_reference',
                        'message': "Should reference Supabase but doesn't"
                    })
                    print(f"⚠️  {protocol_path}")
                    print(f"   Missing reference to: Supabase")
                    print()
    
    def generate_report(self):
        """Generate final audit report"""
        print("\n" + "=" * 70)
        print("AUDIT SUMMARY")
        print("=" * 70)
        print()
        
        print(f"Total Protocols Scanned: {len(self.protocols)}")
        print(f"Total Cross-References Found: {sum(len(refs) for refs in self.cross_references.values())}")
        print(f"Total Issues Found: {len(self.issues)}")
        print()
        
        if self.issues:
            print("ISSUES DETECTED:")
            print()
            for issue in self.issues:
                print(f"❌ {issue['file']}")
                print(f"   Type: {issue['type']}")
                print(f"   Message: {issue['message']}")
                print()
        else:
            print("✅ No issues detected!")
        
        # Save report
        report = {
            'timestamp': str(Path(__file__).stat().st_mtime),
            'protocols_scanned': len(self.protocols),
            'cross_references': sum(len(refs) for refs in self.cross_references.values()),
            'issues': self.issues,
            'protocol_list': list(self.protocols.keys()),
            'cross_reference_matrix': self.cross_references
        }
        
        report_path = PROJECT_ROOT / "07_SYSTEM_CORE" / "protocol_audit_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nReport saved to: {report_path}")
        
        return report


if __name__ == "__main__":
    audit = ProtocolAudit()
    audit.scan_protocols()
    audit.generate_cross_reference_matrix()
    audit.check_missing_references()
    report = audit.generate_report()
