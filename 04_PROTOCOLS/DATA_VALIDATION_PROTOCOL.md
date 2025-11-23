# Data Validation Protocol

**Version:** 1.0  
**Created:** November 23, 2024 (Transformation 2.1)  
**Status:** Foundation Established (Activation: Transformation 3.0)  
**Owner:** Solution Architect Persona

---

## Purpose

This protocol defines the **5-stage data validation pipeline** that ensures all knowledge entering the Vedic Mastery Study database meets quality standards. It prevents duplicates, detects contradictions, validates authenticity, and maintains data integrity.

---

## Validation Pipeline Overview

```
Input Data
    ↓
Stage 1: Format Validation
    ↓
Stage 2: Duplicate Detection
    ↓
Stage 3: Contradiction Checking
    ↓
Stage 4: Quality Scoring
    ↓
Stage 5: Authenticity Verification
    ↓
Validated Data → Database
    ↓
Rejected Data → Review Queue
```

---

## Stage 1: Format Validation

**Purpose:** Ensure data conforms to expected schema and format

**Validation Rules:**

```python
def validate_format(data: Dict[str, Any], schema: str) -> ValidationResult:
    """Validate data format against schema"""
    
    checks = []
    
    # Required fields present
    required_fields = get_required_fields(schema)
    for field in required_fields:
        if field not in data or data[field] is None:
            checks.append(ValidationCheck(
                stage="format",
                check="required_field",
                field=field,
                passed=False,
                message=f"Missing required field: {field}"
            ))
    
    # Data types correct
    for field, expected_type in get_field_types(schema).items():
        if field in data and not isinstance(data[field], expected_type):
            checks.append(ValidationCheck(
                stage="format",
                check="data_type",
                field=field,
                passed=False,
                message=f"Invalid type for {field}: expected {expected_type}"
            ))
    
    # Field constraints met
    for field, constraints in get_field_constraints(schema).items():
        if field in data:
            if not validate_constraints(data[field], constraints):
                checks.append(ValidationCheck(
                    stage="format",
                    check="constraints",
                    field=field,
                    passed=False,
                    message=f"Constraint violation for {field}"
                ))
    
    return ValidationResult(stage="format", checks=checks)
```

**Example: Verse Validation**

```python
VERSE_SCHEMA = {
    "required_fields": ["text_id", "chapter", "verse_number", "sanskrit_text"],
    "optional_fields": ["english_translation", "commentary"],
    "field_types": {
        "text_id": int,
        "chapter": int,
        "verse_number": int,
        "sanskrit_text": str,
        "english_translation": str
    },
    "constraints": {
        "sanskrit_text": {"min_length": 1, "max_length": 5000},
        "chapter": {"min": 1},
        "verse_number": {"min": 1}
    }
}
```

---

## Stage 2: Duplicate Detection

**Purpose:** Prevent duplicate entries in the knowledge base

**Detection Methods:**

### **2.1 Exact Duplicate Detection**

```python
def detect_exact_duplicate(data: Dict[str, Any], table: str) -> bool:
    """Check for exact duplicates based on unique keys"""
    
    unique_keys = get_unique_keys(table)
    
    query = db.query(table)
    for key in unique_keys:
        query = query.filter(getattr(table, key) == data[key])
    
    return query.first() is not None
```

### **2.2 Fuzzy Duplicate Detection**

```python
from fuzzywuzzy import fuzz

def detect_fuzzy_duplicate(data: Dict[str, Any], table: str, threshold: int = 90) -> List[Dict]:
    """Detect similar but not identical entries"""
    
    comparison_field = get_comparison_field(table)  # e.g., "sanskrit_text"
    
    existing_entries = db.query(table).all()
    
    duplicates = []
    for entry in existing_entries:
        similarity = fuzz.ratio(
            data[comparison_field],
            getattr(entry, comparison_field)
        )
        
        if similarity >= threshold:
            duplicates.append({
                "id": entry.id,
                "similarity": similarity,
                "entry": entry
            })
    
    return duplicates
```

### **2.3 Semantic Duplicate Detection (3.0)**

```python
def detect_semantic_duplicate(data: Dict[str, Any], table: str, threshold: float = 0.95) -> List[Dict]:
    """Detect semantically similar entries using embeddings"""
    
    # Generate embedding for new data
    embedding = generate_embedding(data["content"])
    
    # Find similar embeddings in database
    similar = db.query(table).filter(
        cosine_similarity(table.embedding_vector, embedding) > threshold
    ).all()
    
    return similar
```

---

## Stage 3: Contradiction Checking

**Purpose:** Detect contradictory information in the knowledge base

**Detection Methods:**

### **3.1 Direct Contradiction Detection**

```python
def detect_direct_contradiction(data: Dict[str, Any]) -> List[Contradiction]:
    """Detect direct contradictions (e.g., different translations for same verse)"""
    
    contradictions = []
    
    # Example: Check if new translation contradicts existing
    if data["type"] == "translation":
        existing = get_existing_translations(data["verse_id"])
        
        for translation in existing:
            if are_contradictory(data["translation"], translation):
                contradictions.append(Contradiction(
                    type="translation_mismatch",
                    existing_id=translation.id,
                    new_data=data,
                    confidence=0.8
                ))
    
    return contradictions
```

### **3.2 AI-Powered Contradiction Detection (3.0)**

```python
def detect_ai_contradiction(data: Dict[str, Any]) -> List[Contradiction]:
    """Use AI to detect subtle contradictions"""
    
    # Get related knowledge
    related = find_related_knowledge(data)
    
    # Use AI to check for contradictions
    prompt = f"""
    Check if the following new information contradicts any existing knowledge:
    
    New: {data["content"]}
    
    Existing:
    {format_related_knowledge(related)}
    
    Return JSON with contradictions found.
    """
    
    response = ai_provider.generate(prompt)
    contradictions = parse_contradictions(response)
    
    return contradictions
```

---

## Stage 4: Quality Scoring

**Purpose:** Assign quality scores to all data

**Scoring Dimensions:**

```python
class QualityScore(BaseModel):
    completeness: float  # 0-1: Are all expected fields populated?
    accuracy: float      # 0-1: Is the data accurate? (requires validation)
    consistency: float   # 0-1: Is it consistent with existing data?
    source_authority: float  # 0-1: How authoritative is the source?
    overall: float       # 0-1: Weighted average

def calculate_quality_score(data: Dict[str, Any]) -> QualityScore:
    """Calculate comprehensive quality score"""
    
    # Completeness: percentage of optional fields populated
    completeness = calculate_completeness(data)
    
    # Accuracy: based on source and validation
    accuracy = calculate_accuracy(data)
    
    # Consistency: how well it fits with existing knowledge
    consistency = calculate_consistency(data)
    
    # Source authority: credibility of source
    source_authority = get_source_authority(data.get("source"))
    
    # Overall: weighted average
    overall = (
        completeness * 0.2 +
        accuracy * 0.4 +
        consistency * 0.2 +
        source_authority * 0.2
    )
    
    return QualityScore(
        completeness=completeness,
        accuracy=accuracy,
        consistency=consistency,
        source_authority=source_authority,
        overall=overall
    )
```

**Quality Thresholds:**

- **High Quality:** overall >= 0.8 → Auto-approve
- **Medium Quality:** 0.5 <= overall < 0.8 → Human review
- **Low Quality:** overall < 0.5 → Auto-reject or flag

---

## Stage 5: Authenticity Verification

**Purpose:** Verify data comes from authentic, trusted sources

**Verification Methods:**

### **5.1 Source Verification**

```python
TRUSTED_SOURCES = {
    "monier_williams": {"authority": 0.95, "type": "dictionary"},
    "itihasa_corpus": {"authority": 0.85, "type": "translation"},
    "gita_press": {"authority": 0.90, "type": "publisher"},
    "ramakrishna_mission": {"authority": 0.90, "type": "publisher"}
}

def verify_source(data: Dict[str, Any]) -> SourceVerification:
    """Verify data source is authentic"""
    
    source = data.get("source")
    
    if source in TRUSTED_SOURCES:
        return SourceVerification(
            verified=True,
            authority=TRUSTED_SOURCES[source]["authority"],
            source_type=TRUSTED_SOURCES[source]["type"]
        )
    else:
        return SourceVerification(
            verified=False,
            authority=0.5,  # Default for unknown sources
            source_type="unknown",
            requires_review=True
        )
```

### **5.2 OCR Error Detection**

```python
def detect_ocr_errors(text: str) -> List[str]:
    """Detect common OCR errors in text"""
    
    errors = []
    
    # Check for common OCR mistakes
    ocr_patterns = [
        (r'\bl\b', '1'),  # lowercase L mistaken for 1
        (r'\bO\b', '0'),  # uppercase O mistaken for 0
        (r'rn', 'm'),     # rn mistaken for m
        # ... more patterns
    ]
    
    for pattern, likely_error in ocr_patterns:
        if re.search(pattern, text):
            errors.append(f"Possible OCR error: '{pattern}' might be '{likely_error}'")
    
    return errors
```

### **5.3 AI-Generated Content Detection (3.0)**

```python
def detect_ai_generated(text: str) -> float:
    """Detect if content is AI-generated (requires validation)"""
    
    # Use AI detection model or heuristics
    # Return confidence score (0-1)
    
    indicators = [
        "As an AI",
        "I don't have access to",
        "I cannot provide",
        # ... more indicators
    ]
    
    score = 0.0
    for indicator in indicators:
        if indicator in text:
            score += 0.2
    
    return min(score, 1.0)
```

---

## Validation Workflow

### **Complete Validation Pipeline**

```python
def validate_data(data: Dict[str, Any], schema: str) -> ValidationReport:
    """Run complete validation pipeline"""
    
    report = ValidationReport(data=data, schema=schema)
    
    # Stage 1: Format Validation
    format_result = validate_format(data, schema)
    report.add_stage(format_result)
    if not format_result.passed:
        report.status = "rejected"
        report.reason = "Format validation failed"
        return report
    
    # Stage 2: Duplicate Detection
    exact_dup = detect_exact_duplicate(data, schema)
    fuzzy_dups = detect_fuzzy_duplicate(data, schema)
    if exact_dup:
        report.status = "rejected"
        report.reason = "Exact duplicate found"
        return report
    if fuzzy_dups:
        report.add_warning(f"Found {len(fuzzy_dups)} similar entries")
        report.requires_review = True
    
    # Stage 3: Contradiction Checking
    contradictions = detect_direct_contradiction(data)
    if contradictions:
        report.add_warning(f"Found {len(contradictions)} potential contradictions")
        report.requires_review = True
    
    # Stage 4: Quality Scoring
    quality = calculate_quality_score(data)
    report.quality_score = quality
    if quality.overall < 0.5:
        report.status = "rejected"
        report.reason = "Quality score too low"
        return report
    elif quality.overall < 0.8:
        report.requires_review = True
    
    # Stage 5: Authenticity Verification
    source_verification = verify_source(data)
    report.source_verification = source_verification
    if not source_verification.verified:
        report.requires_review = True
    
    # Final decision
    if report.requires_review:
        report.status = "review"
    else:
        report.status = "approved"
    
    return report
```

---

## Human Review Queue

### **Review Queue Management**

```python
class ReviewQueue(BaseModel):
    id: int
    data: Dict[str, Any]
    validation_report: ValidationReport
    priority: int  # 1-10, higher = more urgent
    status: str  # "pending", "approved", "rejected"
    reviewer: Optional[str]
    review_notes: Optional[str]
    created_at: datetime
    reviewed_at: Optional[datetime]

def add_to_review_queue(data: Dict[str, Any], report: ValidationReport):
    """Add data to human review queue"""
    
    priority = calculate_priority(report)
    
    queue_item = ReviewQueue(
        data=data,
        validation_report=report,
        priority=priority,
        status="pending",
        created_at=datetime.now()
    )
    
    db.add(queue_item)
    db.commit()
```

### **Review Interface (Future)**

```python
def get_review_queue(limit: int = 10) -> List[ReviewQueue]:
    """Get items from review queue, ordered by priority"""
    
    return db.query(ReviewQueue)\
        .filter(ReviewQueue.status == "pending")\
        .order_by(ReviewQueue.priority.desc())\
        .limit(limit)\
        .all()

def approve_review_item(item_id: int, reviewer: str, notes: str):
    """Approve a review queue item"""
    
    item = db.query(ReviewQueue).get(item_id)
    item.status = "approved"
    item.reviewer = reviewer
    item.review_notes = notes
    item.reviewed_at = datetime.now()
    
    # Insert data into database
    insert_validated_data(item.data)
    
    db.commit()
```

---

## Evolution Rules

### **When This Protocol Changes**

**Triggers:**
- Update SYSTEM_EVOLUTION_PROTOCOL.md
- Update SOUL_TRANSMIGRATION_PROTOCOL.md
- Update implementation in `08_DATA_QUALITY/validation_pipeline.py`
- Update tests

**Validation:**
- Test all validation stages
- Verify thresholds still appropriate
- Check false positive/negative rates

---

## Implementation Status

### **Transformation 2.1 (Current)**

**Status:** Foundation Established

**Deliverables:**
- ✅ 5-stage pipeline documented
- ✅ Validation logic defined
- ✅ Quality scoring framework
- ⏳ Implementation (3.0)
- ⏳ AI-powered validation (3.0)
- ⏳ Review queue interface (3.0)

### **Transformation 3.0 (Planned)**

**Planned Implementation:**
- Implement all 5 validation stages
- Build review queue system
- Add AI-powered contradiction detection
- Create review interface
- Integrate with data ingestion pipeline

---

## Related Protocols

- **SYSTEM_EVOLUTION_PROTOCOL.md** - How this protocol evolves
- **MODEL_PROVIDER_PROTOCOL.md** - AI-powered validation
- **DEPENDENCY_GRAPH_PROTOCOL.md** - Validation dependencies
- **HEALTH_MONITORING_PROTOCOL.md** - Monitor validation metrics

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-23 | Initial creation | Solution Architect Persona |

---

**Prepared by:** Solution Architect Persona  
**Date:** November 23, 2024  
**Transformation:** 2.1 - Phase 1, Turn 1.1  
**Status:** Foundation Established (Activation: 3.0)
