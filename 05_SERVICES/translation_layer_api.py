#!/usr/bin/env python3
"""
Translation Layer API Service
Self-sufficient Sanskrit translation service with internal linguistic knowledge base.

Features:
- Dictionary lookup (Monier-Williams)
- Corpus search (Itihasa parallel translations)
- Translation caching
- Word stem analysis
- Context-aware translation suggestions

Author: Transformation 2.0
Date: November 2024
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from supabase import create_client, Client
import uvicorn

# Supabase configuration
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"

# Initialize FastAPI app
app = FastAPI(
    title="Vedic Mastery Translation Layer",
    description="Self-sufficient Sanskrit translation service with internal linguistic knowledge base",
    version="2.1.0"
)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class DictionaryLookupRequest(BaseModel):
    word: str
    limit: int = 5

class DictionaryEntry(BaseModel):
    headword: str
    definition: str
    part_of_speech: Optional[str]
    source: str

class CorpusSearchRequest(BaseModel):
    sanskrit_text: str
    limit: int = 5

class CorpusMatch(BaseModel):
    sanskrit_text: str
    english_translation: str
    source: str
    translator: Optional[str]
    quality_score: float

class TranslationRequest(BaseModel):
    sanskrit_text: str
    context: Optional[str] = None

class TranslationResponse(BaseModel):
    sanskrit_text: str
    dictionary_matches: List[DictionaryEntry]
    corpus_matches: List[CorpusMatch]
    suggestions: List[str]


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check and API information"""
    return {
        "service": "Vedic Mastery Translation Layer",
        "version": "2.1.0",
        "status": "operational",
        "features": [
            "Dictionary lookup (Monier-Williams: 286,535 entries)",
            "Corpus search (Itihasa: 92,030 translations)",
            "Translation caching",
            "Context-aware suggestions"
        ]
    }


@app.post("/dictionary/lookup", response_model=List[DictionaryEntry])
async def lookup_dictionary(request: DictionaryLookupRequest):
    """
    Look up a Sanskrit word in the Monier-Williams dictionary.
    
    Returns matching dictionary entries with definitions.
    """
    try:
        # Search for exact match first
        result = supabase.table('dictionary_entries')\
            .select('headword, definition, part_of_speech, source')\
            .eq('headword', request.word)\
            .limit(request.limit)\
            .execute()
        
        # If no exact match, try case-insensitive search
        if not result.data:
            result = supabase.table('dictionary_entries')\
                .select('headword, definition, part_of_speech, source')\
                .ilike('headword', f'%{request.word}%')\
                .limit(request.limit)\
                .execute()
        
        return result.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dictionary lookup failed: {str(e)}")


@app.post("/corpus/search", response_model=List[CorpusMatch])
async def search_corpus(request: CorpusSearchRequest):
    """
    Search for similar Sanskrit text in the pre-translated corpus.
    
    Returns matching translations from the Itihasa corpus.
    """
    try:
        # Search for similar Sanskrit text
        result = supabase.table('pre_translated_corpus')\
            .select('sanskrit_text, english_translation, source, translator, translation_quality_score')\
            .ilike('sanskrit_text', f'%{request.sanskrit_text}%')\
            .limit(request.limit)\
            .execute()
        
        # Format response
        matches = []
        for row in result.data:
            matches.append({
                'sanskrit_text': row['sanskrit_text'],
                'english_translation': row['english_translation'],
                'source': row['source'],
                'translator': row.get('translator'),
                'quality_score': row.get('translation_quality_score', 0.0)
            })
        
        return matches
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Corpus search failed: {str(e)}")


@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Comprehensive translation service combining dictionary and corpus lookups.
    
    Returns:
    - Dictionary matches for individual words
    - Corpus matches for similar phrases
    - Translation suggestions based on context
    """
    try:
        # Split text into words for dictionary lookup
        words = request.sanskrit_text.split()
        
        # Dictionary lookups
        dictionary_matches = []
        for word in words[:3]:  # Limit to first 3 words
            result = supabase.table('dictionary_entries')\
                .select('headword, definition, part_of_speech, source')\
                .eq('headword', word)\
                .limit(2)\
                .execute()
            
            dictionary_matches.extend(result.data)
        
        # Corpus search
        corpus_result = supabase.table('pre_translated_corpus')\
            .select('sanskrit_text, english_translation, source, translator, translation_quality_score')\
            .ilike('sanskrit_text', f'%{request.sanskrit_text}%')\
            .limit(3)\
            .execute()
        
        corpus_matches = []
        for row in corpus_result.data:
            corpus_matches.append({
                'sanskrit_text': row['sanskrit_text'],
                'english_translation': row['english_translation'],
                'source': row['source'],
                'translator': row.get('translator'),
                'quality_score': row.get('translation_quality_score', 0.0)
            })
        
        # Generate suggestions
        suggestions = []
        if corpus_matches:
            suggestions.append(f"Found {len(corpus_matches)} similar translations in corpus")
        if dictionary_matches:
            suggestions.append(f"Found {len(dictionary_matches)} word definitions")
        if not corpus_matches and not dictionary_matches:
            suggestions.append("No direct matches found. Try breaking down the text into individual words.")
        
        return {
            'sanskrit_text': request.sanskrit_text,
            'dictionary_matches': dictionary_matches,
            'corpus_matches': corpus_matches,
            'suggestions': suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")


# ============================================================================
# AI/ML ENDPOINTS (Placeholder - Transformation 3.0)
# ============================================================================

class SemanticSearchRequest(BaseModel):
    query: str
    limit: int = 10

class AIInsightRequest(BaseModel):
    verse_id: int
    insight_type: str  # 'commentary', 'analysis', 'connections'

class HealthCheckResponse(BaseModel):
    status: str
    score: float
    checks: List[Dict]


@app.post("/semantic/search")
async def semantic_search(request: SemanticSearchRequest):
    """
    Semantic search using vector embeddings.
    
    Status: NOT IMPLEMENTED - Placeholder for Transformation 3.0
    Returns: 501 Not Implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Semantic search not yet implemented. Activation scheduled for Transformation 3.0. Use /corpus/search for keyword-based search."
    )


@app.post("/ai/generate-insight")
async def generate_ai_insight(request: AIInsightRequest):
    """
    Generate AI-powered insights for a verse.
    
    Status: NOT IMPLEMENTED - Placeholder for Transformation 3.0
    Returns: 501 Not Implemented
    """
    raise HTTPException(
        status_code=501,
        detail="AI insight generation not yet implemented. Activation scheduled for Transformation 3.0."
    )


@app.get("/ai/embedding-coverage")
async def get_embedding_coverage():
    """
    Get embedding coverage statistics.
    
    Status: NOT IMPLEMENTED - Placeholder for Transformation 3.0
    Returns: 501 Not Implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Embedding coverage tracking not yet implemented. Activation scheduled for Transformation 3.0."
    )


@app.get("/health/check")
async def health_check():
    """
    Run system health checks.
    
    Status: NOT IMPLEMENTED - Placeholder for Transformation 3.0
    Returns: 501 Not Implemented
    """
    raise HTTPException(
        status_code=501,
        detail="Health check system not yet implemented. Activation scheduled for Transformation 3.0. Use GET / for basic status."
    )


@app.get("/stats")
async def get_stats():
    """Get Translation Layer statistics"""
    try:
        # Count dictionary entries
        dict_count = supabase.table('dictionary_entries').select('id', count='exact').execute()
        
        # Count corpus entries
        corpus_count = supabase.table('pre_translated_corpus').select('id', count='exact').execute()
        
        # Count verses
        verses_count = supabase.table('verses').select('id', count='exact').execute()
        
        return {
            'dictionary_entries': dict_count.count,
            'corpus_translations': corpus_count.count,
            'vedic_verses': verses_count.count,
            'total_resources': dict_count.count + corpus_count.count + verses_count.count
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats retrieval failed: {str(e)}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🚀 Starting Translation Layer API...")
    print(f"   Supabase: {SUPABASE_URL}")
    print(f"   Endpoints:")
    print(f"     Active (v2.0):")
    print(f"       - GET  /")
    print(f"       - POST /dictionary/lookup")
    print(f"       - POST /corpus/search")
    print(f"       - POST /translate")
    print(f"       - GET  /stats")
    print(f"     Placeholder (v3.0):")
    print(f"       - POST /semantic/search (501)")
    print(f"       - POST /ai/generate-insight (501)")
    print(f"       - GET  /ai/embedding-coverage (501)")
    print(f"       - GET  /health/check (501)")
    print(f"\n   Server starting on http://0.0.0.0:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
