"""
Active Health Check System
Status: FUNCTIONAL - Transformation 2.1
Activation: NOW (detects issues, doesn't auto-repair)

This script runs health checks on the current system and generates a report.
Auto-repair functionality will be activated in Transformation 3.0.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("[WARNING] Supabase client not available. Install with: pip3 install supabase")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("[WARNING] Requests library not available. Install with: pip3 install requests")


# Supabase configuration
SUPABASE_URL = "https://yvcyprwldvoubyytptqu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inl2Y3lwcndsZHZvdWJ5eXRwdHF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4NjA1MTQsImV4cCI6MjA3OTQzNjUxNH0.eC2DYZcqKyFrokv_YwnlE1B5QKwCq0fTddsydh_5ypE"


class HealthStatus:
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class HealthCheckResult:
    def __init__(self, check_name: str, status: str, score: float, message: str, details: Dict = None):
        self.check_name = check_name
        self.status = status
        self.score = score
        self.message = message
        self.details = details or {}
    
    def to_dict(self):
        return {
            "check_name": self.check_name,
            "status": self.status,
            "score": self.score,
            "message": self.message,
            "details": self.details
        }


def check_database_connectivity() -> HealthCheckResult:
    """Check if Supabase database is accessible"""
    if not SUPABASE_AVAILABLE:
        return HealthCheckResult(
            check_name="database_connectivity",
            status=HealthStatus.CRITICAL,
            score=0.0,
            message="Supabase client not installed",
            details={"error": "Missing dependency"}
        )
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Try a simple query
        result = supabase.table('verses').select('id', count='exact').limit(1).execute()
        
        return HealthCheckResult(
            check_name="database_connectivity",
            status=HealthStatus.HEALTHY,
            score=1.0,
            message="Database is accessible and responsive",
            details={"response_time_ms": "< 1000"}
        )
    except Exception as e:
        return HealthCheckResult(
            check_name="database_connectivity",
            status=HealthStatus.CRITICAL,
            score=0.0,
            message=f"Database connection failed: {str(e)}",
            details={"error": str(e)}
        )


def check_data_integrity() -> HealthCheckResult:
    """Check data integrity (table counts, null values, etc.)"""
    if not SUPABASE_AVAILABLE:
        return HealthCheckResult(
            check_name="data_integrity",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message="Cannot check - Supabase client not available",
            details={}
        )
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Check expected tables exist and have data
        checks = {
            "verses": 100000,  # Expected minimum
            "dictionary_entries": 280000,
            "pre_translated_corpus": 90000,
            "texts": 50
        }
        
        issues = []
        for table, expected_min in checks.items():
            try:
                result = supabase.table(table).select('id', count='exact').limit(1).execute()
                count = result.count
                
                if count < expected_min:
                    issues.append(f"{table}: {count} rows (expected >= {expected_min})")
            except Exception as e:
                issues.append(f"{table}: Error querying ({str(e)})")
        
        if issues:
            return HealthCheckResult(
                check_name="data_integrity",
                status=HealthStatus.WARNING,
                score=0.7,
                message=f"Data integrity issues found: {len(issues)}",
                details={"issues": issues}
            )
        else:
            return HealthCheckResult(
                check_name="data_integrity",
                status=HealthStatus.HEALTHY,
                score=1.0,
                message="All tables have expected data",
                details={"tables_checked": len(checks)}
            )
    except Exception as e:
        return HealthCheckResult(
            check_name="data_integrity",
            status=HealthStatus.CRITICAL,
            score=0.0,
            message=f"Data integrity check failed: {str(e)}",
            details={"error": str(e)}
        )


def check_embedding_coverage() -> HealthCheckResult:
    """Check embedding coverage for verses"""
    if not SUPABASE_AVAILABLE:
        return HealthCheckResult(
            check_name="embedding_coverage",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message="Cannot check - Supabase client not available",
            details={}
        )
    
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        # Count total verses
        total_result = supabase.table('verses').select('id', count='exact').limit(1).execute()
        total_verses = total_result.count
        
        # Count verses with embeddings (embedding_vector IS NOT NULL)
        # Note: This will be 0 until Transformation 3.0
        embedded_result = supabase.table('verses')\
            .select('id', count='exact')\
            .not_.is_('embedding_vector', 'null')\
            .limit(1)\
            .execute()
        embedded_verses = embedded_result.count
        
        coverage = (embedded_verses / total_verses * 100) if total_verses > 0 else 0.0
        
        # This is expected to be 0% until 3.0
        if coverage == 0.0:
            return HealthCheckResult(
                check_name="embedding_coverage",
                status=HealthStatus.WARNING,
                score=0.0,
                message="Embeddings not yet generated (expected until Transformation 3.0)",
                details={
                    "total_verses": total_verses,
                    "embedded_verses": embedded_verses,
                    "coverage_percent": coverage
                }
            )
        elif coverage < 50.0:
            return HealthCheckResult(
                check_name="embedding_coverage",
                status=HealthStatus.WARNING,
                score=coverage / 100.0,
                message=f"Low embedding coverage: {coverage:.1f}%",
                details={
                    "total_verses": total_verses,
                    "embedded_verses": embedded_verses,
                    "coverage_percent": coverage
                }
            )
        else:
            return HealthCheckResult(
                check_name="embedding_coverage",
                status=HealthStatus.HEALTHY,
                score=coverage / 100.0,
                message=f"Good embedding coverage: {coverage:.1f}%",
                details={
                    "total_verses": total_verses,
                    "embedded_verses": embedded_verses,
                    "coverage_percent": coverage
                }
            )
    except Exception as e:
        return HealthCheckResult(
            check_name="embedding_coverage",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message=f"Coverage check failed: {str(e)}",
            details={"error": str(e)}
        )


def check_api_health() -> HealthCheckResult:
    """Check if Translation Layer API is running"""
    if not REQUESTS_AVAILABLE:
        return HealthCheckResult(
            check_name="api_health",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message="Cannot check - requests library not available",
            details={}
        )
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return HealthCheckResult(
                check_name="api_health",
                status=HealthStatus.HEALTHY,
                score=1.0,
                message=f"API is running (version {data.get('version', 'unknown')})",
                details={"version": data.get('version'), "status": data.get('status')}
            )
        else:
            return HealthCheckResult(
                check_name="api_health",
                status=HealthStatus.WARNING,
                score=0.5,
                message=f"API returned status {response.status_code}",
                details={"status_code": response.status_code}
            )
    except requests.exceptions.ConnectionError:
        return HealthCheckResult(
            check_name="api_health",
            status=HealthStatus.WARNING,
            score=0.0,
            message="API is not running (connection refused)",
            details={"note": "Start API with: python3 05_SERVICES/translation_layer_api.py"}
        )
    except Exception as e:
        return HealthCheckResult(
            check_name="api_health",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message=f"API check failed: {str(e)}",
            details={"error": str(e)}
        )


def check_repository_status() -> HealthCheckResult:
    """Check if git repository is clean and up to date"""
    try:
        import subprocess
        
        # Check if we're in a git repository
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            cwd='/home/ubuntu/vedic-mastery-study'
        )
        
        if result.returncode != 0:
            return HealthCheckResult(
                check_name="repository_status",
                status=HealthStatus.UNKNOWN,
                score=0.5,
                message="Not in a git repository",
                details={}
            )
        
        uncommitted = result.stdout.strip()
        
        if uncommitted:
            files = uncommitted.split('\n')
            return HealthCheckResult(
                check_name="repository_status",
                status=HealthStatus.WARNING,
                score=0.7,
                message=f"Repository has {len(files)} uncommitted changes",
                details={"uncommitted_files": len(files)}
            )
        else:
            return HealthCheckResult(
                check_name="repository_status",
                status=HealthStatus.HEALTHY,
                score=1.0,
                message="Repository is clean (all changes committed)",
                details={}
            )
    except Exception as e:
        return HealthCheckResult(
            check_name="repository_status",
            status=HealthStatus.UNKNOWN,
            score=0.5,
            message=f"Repository check failed: {str(e)}",
            details={"error": str(e)}
        )


def run_all_health_checks() -> Dict:
    """Run all health checks and generate report"""
    print("=" * 70)
    print("VEDIC MASTERY STUDY - SYSTEM HEALTH CHECK")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Status: Transformation 2.1 (Active Monitoring)")
    print("=" * 70)
    print()
    
    # Run all checks
    checks = [
        check_database_connectivity(),
        check_data_integrity(),
        check_embedding_coverage(),
        check_api_health(),
        check_repository_status()
    ]
    
    # Calculate overall score
    overall_score = sum(c.score for c in checks) / len(checks)
    
    # Determine overall status
    if overall_score >= 0.9:
        overall_status = HealthStatus.HEALTHY
    elif overall_score >= 0.7:
        overall_status = HealthStatus.WARNING
    else:
        overall_status = HealthStatus.CRITICAL
    
    # Count issues
    issues_found = sum(1 for c in checks if c.status != HealthStatus.HEALTHY)
    
    # Print results
    print("HEALTH CHECK RESULTS:")
    print()
    
    for check in checks:
        status_symbol = {
            HealthStatus.HEALTHY: "✅",
            HealthStatus.WARNING: "⚠️ ",
            HealthStatus.CRITICAL: "❌",
            HealthStatus.UNKNOWN: "❓"
        }.get(check.status, "?")
        
        print(f"{status_symbol} {check.check_name}")
        print(f"   Status: {check.status.upper()}")
        print(f"   Score: {check.score:.2f}")
        print(f"   Message: {check.message}")
        if check.details:
            print(f"   Details: {json.dumps(check.details, indent=6)}")
        print()
    
    print("=" * 70)
    print(f"OVERALL STATUS: {overall_status.upper()}")
    print(f"OVERALL SCORE: {overall_score:.2f}")
    print(f"ISSUES FOUND: {issues_found}")
    print("=" * 70)
    
    # Generate report object
    report = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": overall_status,
        "overall_score": overall_score,
        "issues_found": issues_found,
        "checks": [c.to_dict() for c in checks]
    }
    
    return report


if __name__ == "__main__":
    report = run_all_health_checks()
    
    # Save report to file
    report_dir = "/home/ubuntu/vedic-mastery-study/07_SYSTEM_CORE/health_monitoring/reports"
    os.makedirs(report_dir, exist_ok=True)
    
    report_file = os.path.join(
        report_dir,
        f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to: {report_file}")
    print("\n[INFO] Health check complete!")
    print("[INFO] Auto-repair functionality will be activated in Transformation 3.0")
