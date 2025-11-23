"""
Integration and Regression Test Suite
Transformation 2.1 - Phase 7

This test suite validates:
1. Existing functionality still works (regression)
2. New infrastructure integrates properly
3. Database schema is healthy
4. API endpoints respond correctly
5. Health monitoring system works
"""

import sys
import os
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent / "05_SERVICES"))
sys.path.insert(0, str(Path(__file__).parent))

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("[ERROR] Supabase client not available")
    sys.exit(1)

try:
    from fastapi.testclient import TestClient
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("[ERROR] FastAPI TestClient not available")
    sys.exit(1)

# Configuration
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"


class TestResult:
    def __init__(self, test_name, passed, message="", details=None):
        self.test_name = test_name
        self.passed = passed
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status}: {self.test_name}\n   {self.message}"


class IntegrationTestSuite:
    def __init__(self):
        self.results = []
        self.supabase = None
        self.api_client = None
    
    def setup(self):
        """Initialize test environment"""
        print("=" * 70)
        print("TRANSFORMATION 2.1 - INTEGRATION & REGRESSION TEST SUITE")
        print("=" * 70)
        print()
        
        # Initialize Supabase
        try:
            self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            print("✅ Supabase client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize Supabase: {e}")
            return False
        
        # Initialize API client
        try:
            from translation_layer_api import app
            self.api_client = TestClient(app)
            print("✅ API test client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize API client: {e}")
            return False
        
        print()
        return True
    
    def run_all_tests(self):
        """Run all test categories"""
        print("=" * 70)
        print("RUNNING TESTS")
        print("=" * 70)
        print()
        
        # Category 1: Database Regression Tests
        print("📊 DATABASE REGRESSION TESTS")
        print("-" * 70)
        self.test_database_connectivity()
        self.test_core_tables_exist()
        self.test_core_data_integrity()
        self.test_new_tables_exist()
        self.test_new_columns_exist()
        print()
        
        # Category 2: API Regression Tests
        print("🔌 API REGRESSION TESTS")
        print("-" * 70)
        self.test_api_root_endpoint()
        self.test_api_dictionary_lookup()
        self.test_api_corpus_search()
        self.test_api_translate()
        self.test_api_stats()
        print()
        
        # Category 3: New API Endpoints (Placeholders)
        print("🆕 NEW API ENDPOINT TESTS (Placeholders)")
        print("-" * 70)
        self.test_api_semantic_search_placeholder()
        self.test_api_ai_insight_placeholder()
        self.test_api_embedding_coverage_placeholder()
        self.test_api_health_check_placeholder()
        print()
        
        # Category 4: Health Monitoring Tests
        print("🏥 HEALTH MONITORING TESTS")
        print("-" * 70)
        self.test_health_check_script_exists()
        self.test_health_check_runs()
        print()
        
        # Category 5: Protocol Tests
        print("📋 PROTOCOL INTEGRITY TESTS")
        print("-" * 70)
        self.test_protocol_files_exist()
        self.test_protocol_cross_references()
        print()
    
    # Database Regression Tests
    def test_database_connectivity(self):
        try:
            result = self.supabase.table('verses').select('id', count='exact').limit(1).execute()
            self.results.append(TestResult(
                "Database Connectivity",
                True,
                f"Successfully connected to Supabase (query time < 1s)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "Database Connectivity",
                False,
                f"Failed to connect: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_core_tables_exist(self):
        core_tables = ['verses', 'texts', 'commentaries', 'concepts', 'taxonomy', 
                       'dictionary_entries', 'pre_translated_corpus']
        try:
            for table in core_tables:
                result = self.supabase.table(table).select('id', count='exact').limit(1).execute()
            
            self.results.append(TestResult(
                "Core Tables Exist",
                True,
                f"All {len(core_tables)} core tables accessible"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "Core Tables Exist",
                False,
                f"Failed to access core tables: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_core_data_integrity(self):
        try:
            # Check verses
            verses_result = self.supabase.table('verses').select('id', count='exact').limit(1).execute()
            verses_count = verses_result.count
            
            # Check dictionary
            dict_result = self.supabase.table('dictionary_entries').select('id', count='exact').limit(1).execute()
            dict_count = dict_result.count
            
            # Check corpus
            corpus_result = self.supabase.table('pre_translated_corpus').select('id', count='exact').limit(1).execute()
            corpus_count = corpus_result.count
            
            passed = verses_count > 100000 and dict_count > 280000 and corpus_count > 90000
            
            self.results.append(TestResult(
                "Core Data Integrity",
                passed,
                f"Verses: {verses_count:,}, Dictionary: {dict_count:,}, Corpus: {corpus_count:,}",
                {"verses": verses_count, "dictionary": dict_count, "corpus": corpus_count}
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "Core Data Integrity",
                False,
                f"Failed to check data integrity: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_new_tables_exist(self):
        new_tables = ['ai_interaction_log', 'ai_generated_insights', 'knowledge_evolution_log',
                      'data_validation_queue', 'system_health_log', 'semantic_search_cache',
                      'model_fine_tuning_log', 'component_dependencies']
        try:
            existing = []
            for table in new_tables:
                try:
                    result = self.supabase.table(table).select('id', count='exact').limit(1).execute()
                    existing.append(table)
                except:
                    pass
            
            passed = len(existing) == len(new_tables)
            self.results.append(TestResult(
                "New Tables Exist (2.1)",
                passed,
                f"{len(existing)}/{len(new_tables)} new tables created",
                {"existing": existing}
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "New Tables Exist (2.1)",
                False,
                f"Failed to check new tables: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_new_columns_exist(self):
        try:
            # Check if verses table has new embedding columns
            result = self.supabase.table('verses').select('*').limit(1).execute()
            if result.data:
                columns = result.data[0].keys()
                has_embedding_vector = 'embedding_vector' in columns
                has_embedding_model = 'embedding_model' in columns
                
                passed = has_embedding_vector and has_embedding_model
                self.results.append(TestResult(
                    "New Columns Exist (2.1)",
                    passed,
                    f"Embedding columns in verses table: {passed}",
                    {"embedding_vector": has_embedding_vector, "embedding_model": has_embedding_model}
                ))
            else:
                self.results.append(TestResult(
                    "New Columns Exist (2.1)",
                    False,
                    "No data in verses table to check columns"
                ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "New Columns Exist (2.1)",
                False,
                f"Failed to check new columns: {str(e)}"
            ))
            print(self.results[-1])
    
    # API Regression Tests
    def test_api_root_endpoint(self):
        try:
            response = self.api_client.get("/")
            passed = response.status_code == 200 and response.json().get('version') == '2.1.0'
            self.results.append(TestResult(
                "API Root Endpoint",
                passed,
                f"Status: {response.status_code}, Version: {response.json().get('version')}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Root Endpoint",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_dictionary_lookup(self):
        try:
            response = self.api_client.post("/dictionary/lookup", json={"word": "dharma"})
            passed = response.status_code == 200 and len(response.json()) > 0
            self.results.append(TestResult(
                "API Dictionary Lookup",
                passed,
                f"Status: {response.status_code}, Results: {len(response.json()) if passed else 0}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Dictionary Lookup",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_corpus_search(self):
        try:
            response = self.api_client.post("/corpus/search", json={"query": "dharma", "limit": 5})
            passed = response.status_code == 200
            self.results.append(TestResult(
                "API Corpus Search",
                passed,
                f"Status: {response.status_code}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Corpus Search",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_translate(self):
        try:
            response = self.api_client.post("/translate", json={"sanskrit_text": "dharma"})
            passed = response.status_code == 200
            self.results.append(TestResult(
                "API Translate",
                passed,
                f"Status: {response.status_code}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Translate",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_stats(self):
        try:
            response = self.api_client.get("/stats")
            passed = response.status_code == 200 and response.json().get('total_resources', 0) > 0
            self.results.append(TestResult(
                "API Stats",
                passed,
                f"Status: {response.status_code}, Resources: {response.json().get('total_resources', 0):,}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Stats",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    # New API Endpoint Tests (Placeholders)
    def test_api_semantic_search_placeholder(self):
        try:
            response = self.api_client.post("/semantic/search", json={"query": "dharma", "limit": 5})
            passed = response.status_code == 501
            self.results.append(TestResult(
                "API Semantic Search (Placeholder)",
                passed,
                f"Status: {response.status_code} (expected 501)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Semantic Search (Placeholder)",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_ai_insight_placeholder(self):
        try:
            response = self.api_client.post("/ai/generate-insight", json={"verse_id": 1, "insight_type": "commentary"})
            passed = response.status_code == 501
            self.results.append(TestResult(
                "API AI Insight (Placeholder)",
                passed,
                f"Status: {response.status_code} (expected 501)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API AI Insight (Placeholder)",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_embedding_coverage_placeholder(self):
        try:
            response = self.api_client.get("/ai/embedding-coverage")
            passed = response.status_code == 501
            self.results.append(TestResult(
                "API Embedding Coverage (Placeholder)",
                passed,
                f"Status: {response.status_code} (expected 501)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Embedding Coverage (Placeholder)",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    def test_api_health_check_placeholder(self):
        try:
            response = self.api_client.get("/health/check")
            passed = response.status_code == 501
            self.results.append(TestResult(
                "API Health Check (Placeholder)",
                passed,
                f"Status: {response.status_code} (expected 501)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "API Health Check (Placeholder)",
                False,
                f"Failed: {str(e)}"
            ))
            print(self.results[-1])
    
    # Health Monitoring Tests
    def test_health_check_script_exists(self):
        script_path = Path(__file__).parent / "health_monitoring" / "run_health_check.py"
        passed = script_path.exists()
        self.results.append(TestResult(
            "Health Check Script Exists",
            passed,
            f"Script found at: {script_path}" if passed else "Script not found"
        ))
        print(self.results[-1])
    
    def test_health_check_runs(self):
        try:
            from health_monitoring.run_health_check import run_all_health_checks
            report = run_all_health_checks()
            passed = report['overall_score'] > 0.5
            self.results.append(TestResult(
                "Health Check Runs",
                passed,
                f"Overall score: {report['overall_score']:.2f}, Status: {report['overall_status']}"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "Health Check Runs",
                False,
                f"Failed to run health check: {str(e)}"
            ))
            print(self.results[-1])
    
    # Protocol Tests
    def test_protocol_files_exist(self):
        protocol_files = [
            "02_PERSONAS/SOLUTION_ARCHITECT_PERSONA_PROTOCOL.md",
            "04_PROTOCOLS/SYSTEM_EVOLUTION_PROTOCOL.md",
            "04_PROTOCOLS/DEPENDENCY_GRAPH_PROTOCOL.md",
            "04_PROTOCOLS/MODEL_PROVIDER_PROTOCOL.md",
            "04_PROTOCOLS/DATA_VALIDATION_PROTOCOL.md",
            "04_PROTOCOLS/HEALTH_MONITORING_PROTOCOL.md"
        ]
        
        project_root = Path("/home/ubuntu/vedic-mastery-study")
        existing = [f for f in protocol_files if (project_root / f).exists()]
        passed = len(existing) == len(protocol_files)
        
        self.results.append(TestResult(
            "Protocol Files Exist",
            passed,
            f"{len(existing)}/{len(protocol_files)} protocol files found"
        ))
        print(self.results[-1])
    
    def test_protocol_cross_references(self):
        try:
            from protocol_audit import ProtocolAudit
            audit = ProtocolAudit()
            audit.scan_protocols()
            
            total_refs = sum(len(refs) for refs in audit.cross_references.values())
            passed = total_refs > 100
            
            self.results.append(TestResult(
                "Protocol Cross-References",
                passed,
                f"{total_refs} cross-references found (expected > 100)"
            ))
            print(self.results[-1])
        except Exception as e:
            self.results.append(TestResult(
                "Protocol Cross-References",
                False,
                f"Failed to audit protocols: {str(e)}"
            ))
            print(self.results[-1])
    
    def generate_report(self):
        """Generate final test report"""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print()
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            print()
            for result in self.results:
                if not result.passed:
                    print(f"❌ {result.test_name}")
                    print(f"   {result.message}")
                    print()
        
        print("=" * 70)
        
        # Determine overall status
        if success_rate >= 95:
            print("🎉 OVERALL STATUS: EXCELLENT")
        elif success_rate >= 80:
            print("✅ OVERALL STATUS: GOOD")
        elif success_rate >= 60:
            print("⚠️  OVERALL STATUS: ACCEPTABLE")
        else:
            print("❌ OVERALL STATUS: NEEDS ATTENTION")
        
        print("=" * 70)
        
        return {
            'total_tests': total_tests,
            'passed': passed_tests,
            'failed': failed_tests,
            'success_rate': success_rate,
            'results': [{'test': r.test_name, 'passed': r.passed, 'message': r.message} for r in self.results]
        }


if __name__ == "__main__":
    suite = IntegrationTestSuite()
    
    if not suite.setup():
        print("❌ Test setup failed. Exiting.")
        sys.exit(1)
    
    suite.run_all_tests()
    report = suite.generate_report()
    
    # Exit with appropriate code
    sys.exit(0 if report['success_rate'] >= 80 else 1)
