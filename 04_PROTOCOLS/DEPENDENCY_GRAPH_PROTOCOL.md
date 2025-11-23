# Dependency Graph Protocol

**Version:** 1.0  
**Created:** November 23, 2024 (Transformation 2.1)  
**Status:** Foundation Established (Activation: Transformation 3.0)  
**Owner:** Solution Architect Persona

---

## Purpose

This protocol defines the **dependency relationships** between all components of the Vedic Mastery Study system and establishes rules for **cascading updates** when components change. It ensures that when one component evolves, all dependent components are automatically identified and updated to maintain system coherence.

---

## Scope

This protocol covers dependencies between:

- Database schema (tables, columns, indexes)
- API endpoints and models
- Service layer logic
- Protocols and documentation
- Test suites
- ML pipelines and models
- Vector databases and embeddings

---

## Dependency Graph Definition

### **Component Types**

1. **Database Schema** (`database.*`)
2. **API Endpoints** (`api.*`)
3. **Service Logic** (`service.*`)
4. **Protocols** (`protocol.*`)
5. **Tests** (`test.*`)
6. **ML Pipelines** (`ml.*`)
7. **Vector Database** (`vector.*`)

### **Dependency Relationships**

#### **Database Schema Dependencies**

```python
DEPENDENCY_GRAPH = {
    "database.verses": {
        "triggers": [
            "api.models.Verse",
            "api.endpoints.get_verse",
            "service.verse_service",
            "test.test_verse_api",
            "protocol.ARCHITECTURE_DOCUMENTATION",
            "protocol.SUPABASE_ADMINISTRATION_PROTOCOL",
            "ml.embedding_pipeline"
        ],
        "description": "Verses table schema"
    },
    
    "database.dictionary_entries": {
        "triggers": [
            "api.models.DictionaryEntry",
            "api.endpoints.dictionary_lookup",
            "service.translation_service",
            "test.test_dictionary_api",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL"
        ],
        "description": "Monier-Williams dictionary entries"
    },
    
    "database.pre_translated_corpus": {
        "triggers": [
            "api.models.CorpusEntry",
            "api.endpoints.corpus_search",
            "service.translation_service",
            "test.test_corpus_api",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL",
            "ml.embedding_pipeline"
        ],
        "description": "Itihasa translation corpus"
    },
    
    "database.ai_generated_insights": {
        "triggers": [
            "api.models.AIInsight",
            "api.endpoints.ai_insights",
            "service.ai_insight_service",
            "test.test_ai_insights_api",
            "protocol.MODEL_PROVIDER_PROTOCOL",
            "ml.insight_generation_pipeline"
        ],
        "description": "AI-generated commentary and insights"
    },
    
    "database.translation_cache": {
        "triggers": [
            "api.models.TranslationCache",
            "service.translation_service",
            "test.test_translation_cache",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL"
        ],
        "description": "Cached translations"
    },
    
    "database.knowledge_evolution_log": {
        "triggers": [
            "api.models.EvolutionLog",
            "service.evolution_logger",
            "test.test_evolution_logging",
            "protocol.SYSTEM_EVOLUTION_PROTOCOL"
        ],
        "description": "Knowledge evolution tracking"
    },
    
    "database.ai_interaction_log": {
        "triggers": [
            "api.models.AIInteraction",
            "service.ai_service",
            "test.test_ai_logging",
            "protocol.MODEL_PROVIDER_PROTOCOL"
        ],
        "description": "AI model interaction logging"
    }
}
```

#### **API Endpoint Dependencies**

```python
API_DEPENDENCIES = {
    "api.endpoints.get_verse": {
        "depends_on": [
            "database.verses",
            "service.verse_service"
        ],
        "triggers": [
            "test.test_verse_api",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL"
        ]
    },
    
    "api.endpoints.dictionary_lookup": {
        "depends_on": [
            "database.dictionary_entries",
            "service.translation_service"
        ],
        "triggers": [
            "test.test_dictionary_api",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL"
        ]
    },
    
    "api.endpoints.corpus_search": {
        "depends_on": [
            "database.pre_translated_corpus",
            "service.translation_service"
        ],
        "triggers": [
            "test.test_corpus_api",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL"
        ]
    },
    
    "api.endpoints.semantic_search": {
        "depends_on": [
            "database.verses.embedding_vector",
            "vector.pgvector_index",
            "service.semantic_search_service"
        ],
        "triggers": [
            "test.test_semantic_search_api",
            "protocol.SEMANTIC_SEARCH_PROTOCOL"
        ],
        "status": "placeholder (3.0)"
    },
    
    "api.endpoints.ai_insights": {
        "depends_on": [
            "database.ai_generated_insights",
            "service.ai_insight_service",
            "ml.insight_generation_pipeline"
        ],
        "triggers": [
            "test.test_ai_insights_api",
            "protocol.MODEL_PROVIDER_PROTOCOL"
        ],
        "status": "placeholder (3.0)"
    },
    
    "api.endpoints.generate_embedding": {
        "depends_on": [
            "ml.embedding_pipeline",
            "service.embedding_service"
        ],
        "triggers": [
            "test.test_embedding_generation",
            "protocol.EMBEDDING_GENERATION_PROTOCOL"
        ],
        "status": "placeholder (3.0)"
    }
}
```

#### **Protocol Dependencies**

```python
PROTOCOL_DEPENDENCIES = {
    "protocol.SOUL_TRANSMIGRATION_PROTOCOL": {
        "depends_on": [
            "protocol.SYSTEM_EVOLUTION_PROTOCOL",
            "protocol.SUPABASE_ADMINISTRATION_PROTOCOL",
            "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL",
            "protocol.SOLUTION_ARCHITECT_PERSONA_PROTOCOL"
        ],
        "description": "Master protocol for context transfer"
    },
    
    "protocol.SYSTEM_EVOLUTION_PROTOCOL": {
        "depends_on": [
            "protocol.DEPENDENCY_GRAPH_PROTOCOL"
        ],
        "triggers": [
            "protocol.SOUL_TRANSMIGRATION_PROTOCOL"
        ],
        "description": "Defines how system evolves"
    },
    
    "protocol.SUPABASE_ADMINISTRATION_PROTOCOL": {
        "depends_on": [
            "database.*"
        ],
        "triggers": [
            "protocol.SOUL_TRANSMIGRATION_PROTOCOL",
            "protocol.ARCHITECTURE_DOCUMENTATION"
        ],
        "description": "Database administration procedures"
    },
    
    "protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL": {
        "depends_on": [
            "database.dictionary_entries",
            "database.pre_translated_corpus",
            "database.translation_cache",
            "api.endpoints.dictionary_lookup",
            "api.endpoints.corpus_search"
        ],
        "triggers": [
            "protocol.SOUL_TRANSMIGRATION_PROTOCOL"
        ],
        "description": "Translation Layer operations"
    }
}
```

#### **ML Pipeline Dependencies**

```python
ML_DEPENDENCIES = {
    "ml.embedding_pipeline": {
        "depends_on": [
            "database.verses",
            "database.pre_translated_corpus",
            "service.model_provider"
        ],
        "triggers": [
            "database.verses.embedding_vector",
            "database.pre_translated_corpus.embedding_vector",
            "vector.pgvector_index"
        ],
        "status": "foundation (3.0)"
    },
    
    "ml.insight_generation_pipeline": {
        "depends_on": [
            "database.verses",
            "database.commentaries",
            "service.model_provider"
        ],
        "triggers": [
            "database.ai_generated_insights",
            "database.ai_interaction_log"
        ],
        "status": "foundation (3.0)"
    },
    
    "ml.fine_tuning_pipeline": {
        "depends_on": [
            "database.pre_translated_corpus",
            "service.model_provider"
        ],
        "triggers": [
            "service.fine_tuned_translator"
        ],
        "status": "foundation (3.0)"
    }
}
```

---

## Cascading Update Rules

### **Rule 1: Schema Change Propagation**

When a database schema changes:

1. **Identify Impacted Components**
   - Query dependency graph for all components that depend on changed schema
   - Include both direct and transitive dependencies

2. **Update API Models**
   - Update Pydantic models to match new schema
   - Add/remove fields as needed
   - Update field types and validators

3. **Update Service Logic**
   - Modify service layer to handle schema changes
   - Update queries and data transformations
   - Add error handling for new constraints

4. **Update Tests**
   - Modify test fixtures to match new schema
   - Update test assertions
   - Add tests for new fields/constraints

5. **Update Documentation**
   - Update ARCHITECTURE_DOCUMENTATION.md
   - Update SUPABASE_ADMINISTRATION_PROTOCOL.md
   - Update API documentation
   - Update relevant operational protocols

6. **Update ML Pipelines (if applicable)**
   - Modify embedding generation if schema affects embedded content
   - Update data extraction logic
   - Regenerate embeddings if needed

### **Rule 2: API Change Propagation**

When an API endpoint changes:

1. **Update API Documentation**
   - Document new request/response formats
   - Update examples
   - Note breaking changes

2. **Update Tests**
   - Modify integration tests
   - Update API contract tests
   - Add tests for new functionality

3. **Update Protocols**
   - Update TRANSLATION_LAYER_OPERATIONS_PROTOCOL.md
   - Update usage examples in protocols
   - Document new workflows

4. **Update Client Code (if exists)**
   - Modify any client libraries
   - Update SDK documentation

### **Rule 3: Protocol Change Propagation**

When a protocol changes:

1. **Update Dependent Protocols**
   - Identify protocols that reference changed protocol
   - Update cross-references
   - Ensure consistency

2. **Update SOUL_TRANSMIGRATION_PROTOCOL**
   - Always update master protocol
   - Ensure context transfer includes new protocol
   - Update version number

3. **Update Implementation**
   - Modify code to match new protocol
   - Update tests to validate protocol compliance

### **Rule 4: ML Pipeline Change Propagation**

When an ML pipeline changes:

1. **Update Database Schema (if needed)**
   - Add new columns for pipeline outputs
   - Update indexes

2. **Update API Endpoints**
   - Expose new ML capabilities
   - Update request/response models

3. **Update Protocols**
   - Document new ML workflows
   - Update MODEL_PROVIDER_PROTOCOL.md
   - Update operational procedures

4. **Update Tests**
   - Add tests for new pipeline
   - Validate outputs
   - Test error handling

---

## Dependency Validation

### **Validation Checklist**

After any component change, validate:

- [ ] All dependent components identified
- [ ] All dependent components updated
- [ ] All tests passing
- [ ] All documentation updated
- [ ] Cross-references validated
- [ ] No broken links in protocols
- [ ] SOUL_TRANSMIGRATION_PROTOCOL updated
- [ ] Changes committed to repository

### **Automated Validation (Future)**

In Transformation 3.0, implement automated validation:

```python
def validate_dependencies(changed_component):
    """
    Validate all dependencies after a component change.
    
    Args:
        changed_component: Component that was changed
        
    Returns:
        ValidationReport with status and issues
    """
    report = ValidationReport()
    
    # Get all dependent components
    dependents = get_dependents(changed_component)
    
    # Check each dependent
    for dependent in dependents:
        if not is_updated(dependent, changed_component):
            report.add_issue(f"{dependent} not updated after {changed_component} change")
    
    # Check tests
    if not all_tests_passing():
        report.add_issue("Tests failing after change")
    
    # Check documentation
    if not documentation_updated(changed_component):
        report.add_issue("Documentation not updated")
    
    return report
```

---

## Dependency Visualization

### **Graph Representation (Future)**

In Transformation 3.0, create visual dependency graph:

```
database.verses
    ├── api.models.Verse
    ├── api.endpoints.get_verse
    │   ├── test.test_verse_api
    │   └── protocol.TRANSLATION_LAYER_OPERATIONS_PROTOCOL
    ├── service.verse_service
    ├── ml.embedding_pipeline
    │   └── database.verses.embedding_vector
    │       └── vector.pgvector_index
    │           └── api.endpoints.semantic_search
    └── protocol.ARCHITECTURE_DOCUMENTATION
```

---

## Evolution Rules

### **When This Protocol Changes**

**Triggers:**
- Update SYSTEM_EVOLUTION_PROTOCOL.md (dependency graph is core to evolution)
- Update SOUL_TRANSMIGRATION_PROTOCOL.md (include new dependencies)
- Update SOLUTION_ARCHITECT_PERSONA_PROTOCOL.md (update workflows)

**Validation:**
- Ensure all existing dependencies still valid
- Test cascading update logic
- Verify no circular dependencies

### **When Dependencies Change**

**Triggers:**
- Update this protocol with new dependency relationships
- Validate dependency graph consistency
- Update automated validation logic (when implemented)

---

## Implementation Status

### **Transformation 2.1 (Current)**

**Status:** Foundation Established

**Deliverables:**
- ✅ Dependency graph defined
- ✅ Cascading update rules documented
- ✅ Validation checklist created
- ⏳ Automated validation (planned for 3.0)
- ⏳ Visual graph (planned for 3.0)

### **Transformation 3.0 (Planned)**

**Planned Enhancements:**
- Implement automated dependency validation
- Create visual dependency graph
- Build dependency tracking into CI/CD
- Add dependency impact analysis tool

---

## Usage Examples

### **Example 1: Adding a Column to verses Table**

**Change:** Add `sentiment_score` column to `verses` table

**Cascading Updates:**

1. **Database Schema**
   ```sql
   ALTER TABLE verses ADD COLUMN sentiment_score FLOAT NULL;
   ```

2. **API Model**
   ```python
   class Verse(BaseModel):
       # ... existing fields ...
       sentiment_score: Optional[float] = None
   ```

3. **Service Logic**
   ```python
   def get_verse(verse_id):
       # Query now includes sentiment_score
       verse = db.query(Verse).filter(Verse.id == verse_id).first()
       return verse
   ```

4. **Tests**
   ```python
   def test_get_verse_includes_sentiment():
       verse = get_verse(1)
       assert hasattr(verse, 'sentiment_score')
   ```

5. **Documentation**
   - Update ARCHITECTURE_DOCUMENTATION.md (add sentiment_score to schema)
   - Update SUPABASE_ADMINISTRATION_PROTOCOL.md (document column purpose)
   - Update API docs (include sentiment_score in response)

### **Example 2: Adding New API Endpoint**

**Change:** Add `/api/semantic-search` endpoint

**Cascading Updates:**

1. **API Endpoint**
   ```python
   @app.post("/api/semantic-search")
   def semantic_search(query: str):
       # Implementation
       pass
   ```

2. **API Model**
   ```python
   class SemanticSearchRequest(BaseModel):
       query: str
       limit: int = 10
   
   class SemanticSearchResponse(BaseModel):
       results: List[Verse]
       scores: List[float]
   ```

3. **Service Logic**
   ```python
   class SemanticSearchService:
       def search(self, query, limit):
           # Implementation
           pass
   ```

4. **Tests**
   ```python
   def test_semantic_search():
       response = client.post("/api/semantic-search", json={"query": "dharma"})
       assert response.status_code == 200
   ```

5. **Documentation**
   - Update TRANSLATION_LAYER_OPERATIONS_PROTOCOL.md (add semantic search workflow)
   - Update API documentation (document new endpoint)
   - Add usage examples

---

## Related Protocols

- **SYSTEM_EVOLUTION_PROTOCOL.md** - Uses this dependency graph for evolution
- **SOLUTION_ARCHITECT_PERSONA_PROTOCOL.md** - Implements dependency-aware workflows
- **SUPABASE_ADMINISTRATION_PROTOCOL.md** - Database schema dependencies
- **TRANSLATION_LAYER_OPERATIONS_PROTOCOL.md** - API and service dependencies
- **SOUL_TRANSMIGRATION_PROTOCOL.md** - Ensures dependencies tracked across sessions

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-23 | Initial creation with complete dependency graph | Solution Architect Persona |

---

**Prepared by:** Solution Architect Persona  
**Date:** November 23, 2024  
**Transformation:** 2.1 - Phase 1, Turn 1.1  
**Status:** Foundation Established (Activation: 3.0)
