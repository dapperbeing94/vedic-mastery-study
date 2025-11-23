# Model Provider Protocol

**Version:** 1.0  
**Created:** November 23, 2024 (Transformation 2.1)  
**Status:** Foundation Established (Activation: Transformation 3.0)  
**Owner:** Solution Architect Persona

---

## Purpose

This protocol defines standards and procedures for integrating AI/ML model providers (OpenAI, Anthropic, Perplexity, etc.) into the Vedic Mastery Study system. It ensures consistent, cost-effective, and reliable use of AI models across all system components.

---

## Scope

This protocol covers:

- Model provider integration and authentication
- API usage patterns and best practices
- Cost management and optimization
- Error handling and retry logic
- Rate limiting and throttling
- Model selection and routing
- Prompt engineering standards
- Response validation and quality control

---

## Supported Model Providers

### **Primary Providers**

#### **1. OpenAI**

**Models:**
- `gpt-4-turbo` - Primary model for AI-generated insights
- `gpt-3.5-turbo` - Cost-effective alternative
- `text-embedding-3-large` - Embedding generation (1536 dimensions)
- `text-embedding-3-small` - Cost-effective embeddings (512 dimensions)

**Use Cases:**
- AI-generated commentary and insights
- Semantic embedding generation
- Translation quality improvement
- Fine-tuning for Sanskrit translation

**Cost Structure:**
- GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
- GPT-3.5 Turbo: $0.0005/1K input tokens, $0.0015/1K output tokens
- Embedding Large: $0.00013/1K tokens
- Embedding Small: $0.00002/1K tokens

**Authentication:**
- API Key stored in environment variable: `OPENAI_API_KEY`
- Organization ID (if applicable): `OPENAI_ORG_ID`

#### **2. Anthropic (Claude)**

**Models:**
- `claude-3-opus` - Highest capability, most expensive
- `claude-3-sonnet` - Balanced performance and cost
- `claude-3-haiku` - Fast and cost-effective

**Use Cases:**
- Alternative to GPT-4 for insights
- Cross-validation of AI-generated content
- Long-context analysis (200K tokens)

**Cost Structure:**
- Opus: $0.015/1K input tokens, $0.075/1K output tokens
- Sonnet: $0.003/1K input tokens, $0.015/1K output tokens
- Haiku: $0.00025/1K input tokens, $0.00125/1K output tokens

**Authentication:**
- API Key stored in environment variable: `ANTHROPIC_API_KEY`

#### **3. Perplexity**

**Models:**
- `pplx-7b-online` - Real-time web search integration
- `pplx-70b-online` - More capable, higher cost

**Use Cases:**
- Research and fact-checking
- Finding external sources
- Validating historical/cultural context

**Cost Structure:**
- TBD (check current pricing)

**Authentication:**
- API Key stored in environment variable: `PERPLEXITY_API_KEY`

### **Future Providers (Planned)**

- **Sentence Transformers** - Open-source embeddings
- **Hugging Face** - Custom model hosting
- **Cohere** - Alternative embeddings and generation

---

## Model Provider Abstraction

### **Interface Design**

All model providers must implement a common interface:

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ModelRequest(BaseModel):
    """Standard request format for all providers"""
    prompt: str
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    system_prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class ModelResponse(BaseModel):
    """Standard response format from all providers"""
    content: str
    model: str
    provider: str
    tokens_used: int
    cost: float
    metadata: Dict[str, Any]

class ModelProvider(ABC):
    """Abstract base class for all model providers"""
    
    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate text completion"""
        pass
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding vector"""
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """Validate API key is configured and working"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, request: ModelRequest) -> float:
        """Estimate cost before making request"""
        pass
```

### **Implementation Example: OpenAI Provider**

```python
import openai
from typing import List

class OpenAIProvider(ModelProvider):
    """OpenAI model provider implementation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key
        self.client = openai.OpenAI()
    
    def generate(self, request: ModelRequest) -> ModelResponse:
        """Generate text using OpenAI GPT models"""
        
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        response = self.client.chat.completions.create(
            model=request.metadata.get("model", "gpt-4-turbo"),
            messages=messages,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        tokens_used = response.usage.total_tokens
        cost = self._calculate_cost(tokens_used, request.metadata.get("model"))
        
        return ModelResponse(
            content=response.choices[0].message.content,
            model=response.model,
            provider="openai",
            tokens_used=tokens_used,
            cost=cost,
            metadata={"finish_reason": response.choices[0].finish_reason}
        )
    
    def embed(self, text: str, model: str = "text-embedding-3-large") -> List[float]:
        """Generate embedding using OpenAI embedding models"""
        
        response = self.client.embeddings.create(
            model=model,
            input=text
        )
        
        return response.data[0].embedding
    
    def validate_api_key(self) -> bool:
        """Validate OpenAI API key"""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False
    
    def _calculate_cost(self, tokens: int, model: str) -> float:
        """Calculate cost based on tokens and model"""
        # Cost calculation logic
        pass
```

---

## Usage Patterns

### **Pattern 1: AI-Generated Insights**

**Use Case:** Generate commentary for a Vedic verse

**Model Selection:**
- Primary: GPT-4 Turbo (highest quality)
- Fallback: Claude 3 Sonnet (if OpenAI unavailable)
- Budget: GPT-3.5 Turbo (if cost is concern)

**Prompt Template:**

```python
INSIGHT_GENERATION_PROMPT = """
You are a scholar of Vedic philosophy and Sanskrit literature. Generate insightful commentary on the following verse.

Verse (Sanskrit): {sanskrit_text}
Verse (English): {english_translation}
Text: {text_name}
Context: {context}

Provide:
1. Philosophical interpretation
2. Practical application
3. Related concepts
4. Historical/cultural context

Be scholarly but accessible. Cite relevant sources when possible.
"""

def generate_insight(verse_id: int) -> str:
    verse = get_verse(verse_id)
    
    request = ModelRequest(
        prompt=INSIGHT_GENERATION_PROMPT.format(
            sanskrit_text=verse.sanskrit_text,
            english_translation=verse.english_translation,
            text_name=verse.text_name,
            context=verse.context
        ),
        max_tokens=1500,
        temperature=0.7,
        system_prompt="You are a Vedic philosophy expert.",
        metadata={"model": "gpt-4-turbo", "verse_id": verse_id}
    )
    
    provider = get_provider("openai")
    response = provider.generate(request)
    
    # Log interaction
    log_ai_interaction(verse_id, request, response)
    
    return response.content
```

### **Pattern 2: Semantic Embedding Generation**

**Use Case:** Generate embeddings for all verses

**Model Selection:**
- Primary: text-embedding-3-large (best quality)
- Budget: text-embedding-3-small (10x cheaper)

**Batch Processing:**

```python
def generate_embeddings_batch(verses: List[Verse], batch_size: int = 100):
    """Generate embeddings for verses in batches"""
    
    provider = get_provider("openai")
    
    for i in range(0, len(verses), batch_size):
        batch = verses[i:i+batch_size]
        
        for verse in batch:
            # Combine Sanskrit and English for richer embedding
            text = f"{verse.sanskrit_text} {verse.english_translation}"
            
            embedding = provider.embed(text, model="text-embedding-3-large")
            
            # Store in database
            update_verse_embedding(verse.id, embedding, "text-embedding-3-large")
        
        # Rate limiting
        time.sleep(1)
```

### **Pattern 3: Translation Quality Validation**

**Use Case:** Validate AI-generated translations

**Model Selection:**
- Primary: Claude 3 Sonnet (good at analysis)
- Cross-check: GPT-4 Turbo

**Validation Prompt:**

```python
VALIDATION_PROMPT = """
Evaluate the quality of this Sanskrit-to-English translation.

Sanskrit: {sanskrit}
English Translation: {translation}
Reference Translation: {reference}

Rate the translation on:
1. Accuracy (1-10)
2. Fluency (1-10)
3. Completeness (1-10)

Provide:
- Overall score (1-10)
- Strengths
- Weaknesses
- Suggested improvements

Format as JSON.
"""
```

---

## Cost Management

### **Cost Tracking**

**Log Every API Call:**

```python
class AIInteractionLog(BaseModel):
    id: int
    timestamp: datetime
    provider: str
    model: str
    operation: str  # "generate", "embed", "validate"
    tokens_used: int
    cost: float
    verse_id: Optional[int]
    metadata: Dict[str, Any]

def log_ai_interaction(verse_id, request, response):
    """Log AI interaction for cost tracking"""
    
    log = AIInteractionLog(
        timestamp=datetime.now(),
        provider=response.provider,
        model=response.model,
        operation="generate",
        tokens_used=response.tokens_used,
        cost=response.cost,
        verse_id=verse_id,
        metadata=request.metadata
    )
    
    db.add(log)
    db.commit()
```

**Cost Monitoring:**

```python
def get_monthly_cost() -> float:
    """Get total AI cost for current month"""
    
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
    
    total = db.query(func.sum(AIInteractionLog.cost))\
        .filter(AIInteractionLog.timestamp >= start_of_month)\
        .scalar()
    
    return total or 0.0

def get_cost_by_provider() -> Dict[str, float]:
    """Get cost breakdown by provider"""
    
    results = db.query(
        AIInteractionLog.provider,
        func.sum(AIInteractionLog.cost)
    ).group_by(AIInteractionLog.provider).all()
    
    return {provider: cost for provider, cost in results}
```

### **Cost Optimization Strategies**

1. **Caching**
   - Cache AI responses to avoid duplicate requests
   - Use `translation_cache` table
   - Check cache before making API call

2. **Batch Processing**
   - Process multiple items in single request when possible
   - Use batch embedding endpoints
   - Reduce API overhead

3. **Model Selection**
   - Use cheaper models for simple tasks
   - Reserve GPT-4 for complex analysis
   - Use GPT-3.5 for routine operations

4. **Prompt Optimization**
   - Keep prompts concise
   - Reduce unnecessary context
   - Use system prompts effectively

5. **Rate Limiting**
   - Implement request throttling
   - Avoid hitting rate limits (which waste retries)
   - Spread requests over time

---

## Error Handling

### **Retry Logic**

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def generate_with_retry(provider, request):
    """Generate with automatic retry on failure"""
    try:
        return provider.generate(request)
    except RateLimitError:
        # Wait and retry
        raise
    except APIError as e:
        # Log error and retry
        log_error(e)
        raise
    except Exception as e:
        # Log and fail
        log_error(e)
        raise
```

### **Fallback Providers**

```python
def generate_with_fallback(request: ModelRequest) -> ModelResponse:
    """Try primary provider, fall back to secondary if fails"""
    
    providers = [
        ("openai", "gpt-4-turbo"),
        ("anthropic", "claude-3-sonnet"),
        ("openai", "gpt-3.5-turbo")
    ]
    
    for provider_name, model in providers:
        try:
            provider = get_provider(provider_name)
            request.metadata["model"] = model
            return provider.generate(request)
        except Exception as e:
            log_error(f"{provider_name} failed: {e}")
            continue
    
    raise Exception("All providers failed")
```

---

## Rate Limiting

### **Provider Rate Limits**

**OpenAI:**
- GPT-4: 10,000 tokens/min (Tier 1)
- GPT-3.5: 90,000 tokens/min (Tier 1)
- Embeddings: 1,000,000 tokens/min

**Anthropic:**
- Claude 3: 50,000 tokens/min (Tier 1)

**Implementation:**

```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)  # 10 calls per minute
def rate_limited_generate(provider, request):
    """Rate-limited generation"""
    return provider.generate(request)
```

---

## Prompt Engineering Standards

### **Prompt Structure**

**Good Prompt:**
```
You are a {role}.

Task: {clear_task_description}

Input:
{structured_input}

Output Format:
{expected_format}

Constraints:
- {constraint_1}
- {constraint_2}

Examples:
{few_shot_examples}
```

**Bad Prompt:**
```
Tell me about this verse: {verse_text}
```

### **Prompt Templates**

Store reusable prompts:

```python
PROMPT_TEMPLATES = {
    "insight_generation": """...""",
    "translation_validation": """...""",
    "concept_extraction": """...""",
    "relationship_discovery": """..."""
}

def get_prompt_template(name: str) -> str:
    return PROMPT_TEMPLATES.get(name, "")
```

---

## Response Validation

### **Validation Rules**

```python
def validate_ai_response(response: ModelResponse, expected_format: str) -> bool:
    """Validate AI response meets expectations"""
    
    # Check for empty response
    if not response.content or len(response.content.strip()) == 0:
        return False
    
    # Check for expected format
    if expected_format == "json":
        try:
            json.loads(response.content)
        except:
            return False
    
    # Check for minimum length
    if len(response.content) < 50:
        return False
    
    # Check for hallucination indicators
    hallucination_phrases = [
        "I don't have access to",
        "I cannot provide",
        "As an AI"
    ]
    if any(phrase in response.content for phrase in hallucination_phrases):
        return False
    
    return True
```

---

## Evolution Rules

### **When This Protocol Changes**

**Triggers:**
- Update SYSTEM_EVOLUTION_PROTOCOL.md
- Update SOUL_TRANSMIGRATION_PROTOCOL.md
- Update SOLUTION_ARCHITECT_PERSONA_PROTOCOL.md
- Update implementation in `05_SERVICES/model_providers/`

**Validation:**
- Test all provider integrations
- Verify cost tracking still works
- Validate error handling

### **When New Provider Added**

**Triggers:**
- Update this protocol with provider details
- Implement provider class
- Add provider to factory
- Update tests
- Update cost tracking

---

## Implementation Status

### **Transformation 2.1 (Current)**

**Status:** Foundation Established

**Deliverables:**
- ✅ Protocol documented
- ✅ Interface design defined
- ✅ Usage patterns documented
- ⏳ Provider implementations (3.0)
- ⏳ Cost tracking (3.0)
- ⏳ Rate limiting (3.0)

### **Transformation 3.0 (Planned)**

**Planned Implementation:**
- Implement OpenAI provider
- Implement Anthropic provider
- Implement Perplexity provider
- Build cost tracking system
- Add rate limiting
- Create prompt template library

---

## Related Protocols

- **DEPENDENCY_GRAPH_PROTOCOL.md** - Model provider dependencies
- **SYSTEM_EVOLUTION_PROTOCOL.md** - How this protocol evolves
- **DATA_VALIDATION_PROTOCOL.md** - Validating AI-generated content
- **HEALTH_MONITORING_PROTOCOL.md** - Monitoring AI service health
- **SOUL_TRANSMIGRATION_PROTOCOL.md** - Context transfer includes AI state

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
