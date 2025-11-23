#!/usr/bin/env python3
"""
Generate comprehensive study documents for all 12 remaining principal Upanishads
based on the parallel research data.
"""

import json
import os

def generate_upanishad_documents():
    # Load the parallel research data
    with open('/home/ubuntu/upanishad_comprehensive_research.json', 'r') as f:
        data = json.load(f)
    
    # Create the output directory
    output_dir = "01_STUDY_DOCUMENTS/02_Upanishads"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 80)
    print("GENERATING COMPREHENSIVE UPANISHAD STUDY DOCUMENTS")
    print("=" * 80)
    print()
    
    for item in data['results']:
        upanishad_data = item['output']
        name = upanishad_data['upanishad_name']
        
        print(f"Generating document for {name}...")
        
        # Create the markdown content
        content = f"""# {name} - Comprehensive Study

**Date**: November 22, 2024  
**Status**: ✅ Comprehensive Overview Complete  
**Category**: Principal Upanishads (Mukhya Upanishads)

---

## 📖 Introduction

{name} is one of the principal Upanishads of the Hindu tradition, representing a profound exploration of the ultimate reality (Brahman) and the nature of the Self (Atman). This document provides a comprehensive overview based on traditional commentaries and scholarly research.

---

## 🏛️ Structure and Organization

{upanishad_data['structure']}

---

## 📜 Historical Context

{upanishad_data['historical_context']}

---

## 🔑 Core Teachings and Philosophy

{upanishad_data['core_teachings']}

---

## 📿 Key Verses and Analysis

{upanishad_data['key_verses']}

---

## 💭 Major Commentaries

{upanishad_data['commentaries']}

---

## 🙏 Practical Applications

{upanishad_data['practical_applications']}

---

## 🔗 Cross-References and Connections

{upanishad_data['cross_references']}

---

## 📚 Authoritative Sources

{upanishad_data['sources']}

---

## 🎯 Summary and Significance

The {name} stands as a testament to the profound philosophical inquiry of the ancient Vedic tradition. Its teachings on the nature of Brahman, the Self, and the path to liberation continue to guide spiritual seekers in their journey toward ultimate truth.

**Key Takeaways:**
- The relationship between Atman (individual Self) and Brahman (universal reality)
- The method of inquiry and realization
- The practical path to spiritual liberation
- The integration of knowledge into daily life

---

**Om Shanti Shanti Shanti** 🙏

*This document is part of the Vedic Mastery Study - Blue Belt Progression*
"""
        
        # Sanitize filename
        filename = name.replace(" ", "_").replace("(", "").replace(")", "") + "_Comprehensive.md"
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"  - Created {file_path}")
    
    print("\n✅ All Upanishad study documents generated successfully!")
    print(f"Total documents created: {len(data['results'])}")

if __name__ == "__main__":
    generate_upanishad_documents()
