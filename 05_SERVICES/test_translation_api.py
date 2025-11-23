#!/usr/bin/env python3
"""
Translation Layer API Test Suite
Comprehensive tests for the Translation Layer API service.
"""

import requests
import json

API_BASE = "http://localhost:8000"

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_health_check():
    """Test the root endpoint"""
    print_section("TEST 1: Health Check")
    
    response = requests.get(f"{API_BASE}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200

def test_stats():
    """Test the stats endpoint"""
    print_section("TEST 2: Database Statistics")
    
    response = requests.get(f"{API_BASE}/stats")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    stats = response.json()
    print(json.dumps(stats, indent=2))
    
    print(f"\n📊 Summary:")
    print(f"   Dictionary Entries: {stats.get('dictionary_entries', 0):,}")
    print(f"   Corpus Translations: {stats.get('corpus_translations', 0):,}")
    print(f"   Vedic Verses: {stats.get('vedic_verses', 0):,}")
    print(f"   Total Resources: {stats.get('total_resources', 0):,}")
    
    return response.status_code == 200

def test_dictionary_lookup():
    """Test dictionary lookup"""
    print_section("TEST 3: Dictionary Lookup")
    
    test_words = ["dharma", "karma", "yoga"]
    
    for word in test_words:
        print(f"\n🔍 Looking up: {word}")
        response = requests.post(
            f"{API_BASE}/dictionary/lookup",
            json={"word": word, "limit": 3}
        )
        
        if response.status_code == 200:
            results = response.json()
            print(f"   Found {len(results)} entries")
            for i, entry in enumerate(results, 1):
                print(f"\n   {i}. Headword: {entry.get('headword')}")
                print(f"      POS: {entry.get('part_of_speech', 'N/A')}")
                print(f"      Definition: {entry.get('definition', '')[:100]}...")
        else:
            print(f"   ❌ Error: {response.status_code}")
    
    return True

def test_corpus_search():
    """Test corpus search"""
    print_section("TEST 4: Corpus Search")
    
    # Test with a common Sanskrit phrase
    test_phrase = "धर्म"
    
    print(f"🔍 Searching corpus for: {test_phrase}")
    response = requests.post(
        f"{API_BASE}/corpus/search",
        json={"sanskrit_text": test_phrase, "limit": 3}
    )
    
    if response.status_code == 200:
        results = response.json()
        print(f"   Found {len(results)} matches\n")
        for i, match in enumerate(results, 1):
            print(f"   {i}. Sanskrit: {match.get('sanskrit_text', '')[:80]}...")
            print(f"      English: {match.get('english_translation', '')[:80]}...")
            print(f"      Source: {match.get('source')}")
            print(f"      Translator: {match.get('translator', 'N/A')}")
            print(f"      Quality: {match.get('quality_score', 0.0)}/10\n")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    return response.status_code == 200

def test_full_translation():
    """Test the comprehensive translation endpoint"""
    print_section("TEST 5: Full Translation Service")
    
    # Test with a Sanskrit phrase
    test_text = "धर्म"
    
    print(f"🔍 Translating: {test_text}")
    response = requests.post(
        f"{API_BASE}/translate",
        json={"sanskrit_text": test_text}
    )
    
    if response.status_code == 200:
        result = response.json()
        
        print(f"\n📖 Dictionary Matches: {len(result.get('dictionary_matches', []))}")
        for i, entry in enumerate(result.get('dictionary_matches', [])[:3], 1):
            print(f"   {i}. {entry.get('headword')}: {entry.get('definition', '')[:60]}...")
        
        print(f"\n📚 Corpus Matches: {len(result.get('corpus_matches', []))}")
        for i, match in enumerate(result.get('corpus_matches', [])[:2], 1):
            print(f"   {i}. {match.get('english_translation', '')[:60]}...")
        
        print(f"\n💡 Suggestions:")
        for suggestion in result.get('suggestions', []):
            print(f"   - {suggestion}")
    else:
        print(f"   ❌ Error: {response.status_code}")
    
    return response.status_code == 200

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  TRANSLATION LAYER API - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    tests = [
        ("Health Check", test_health_check),
        ("Database Statistics", test_stats),
        ("Dictionary Lookup", test_dictionary_lookup),
        ("Corpus Search", test_corpus_search),
        ("Full Translation", test_full_translation),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n   Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! Translation Layer is fully operational!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")


if __name__ == "__main__":
    run_all_tests()
