# Health Monitoring Protocol

**Version:** 1.0  
**Created:** November 23, 2024 (Transformation 2.1)  
**Status:** Partially Active (Basic checks in 2.1, Auto-repair in 3.0)  
**Owner:** Solution Architect Persona

---

## Purpose

This protocol defines the **system health monitoring framework** that continuously checks the integrity, performance, and consistency of the Vedic Mastery Study system. It detects issues proactively and, in Transformation 3.0, will automatically repair common problems.

---

## Health Check Categories

### **1. Database Health**
- Connectivity and availability
- Orphaned records
- Missing foreign key relationships
- Index health and fragmentation
- Table statistics accuracy

### **2. Data Integrity**
- Missing required embeddings
- Null values in required fields
- Constraint violations
- Referential integrity

### **3. API Health**
- Endpoint availability
- Response time performance
- Error rates
- Rate limiting status

### **4. Service Health**
- Translation Layer availability
- Model provider connectivity
- Cache hit rates
- Queue depths

### **5. System Performance**
- Query performance
- API latency
- Memory usage
- Disk space

---

## Health Check Definitions

### **Database Connectivity Check**

```python
def check_database_connectivity() -> HealthCheckResult:
    """Verify database is accessible"""
    
    try:
        db.execute("SELECT 1")
        return HealthCheckResult(
            check="database_connectivity",
            status="healthy",
            message="Database connection successful"
        )
    except Exception as e:
        return HealthCheckResult(
            check="database_connectivity",
            status="unhealthy",
            message=f"Database connection failed: {str(e)}",
            severity="critical"
        )
```

### **Orphaned Records Check**

```python
def check_orphaned_records() -> HealthCheckResult:
    """Detect records with missing foreign key references"""
    
    orphaned = []
    
    # Check verses with missing text_id
    orphaned_verses = db.query(Verse).filter(
        ~Verse.text_id.in_(db.query(Text.id))
    ).count()
    
    if orphaned_verses > 0:
        orphaned.append(f"{orphaned_verses} verses with invalid text_id")
    
    # Check commentaries with missing verse_id
    orphaned_commentaries = db.query(Commentary).filter(
        ~Commentary.verse_id.in_(db.query(Verse.id))
    ).count()
    
    if orphaned_commentaries > 0:
        orphaned.append(f"{orphaned_commentaries} commentaries with invalid verse_id")
    
    if orphaned:
        return HealthCheckResult(
            check="orphaned_records",
            status="unhealthy",
            message=f"Found orphaned records: {', '.join(orphaned)}",
            severity="medium",
            auto_repair_available=True
        )
    else:
        return HealthCheckResult(
            check="orphaned_records",
            status="healthy",
            message="No orphaned records found"
        )
```

### **Missing Embeddings Check**

```python
def check_missing_embeddings() -> HealthCheckResult:
    """Check for verses missing embeddings (after 3.0)"""
    
    total_verses = db.query(Verse).count()
    verses_with_embeddings = db.query(Verse).filter(
        Verse.embedding_vector.isnot(None)
    ).count()
    
    missing = total_verses - verses_with_embeddings
    percentage = (missing / total_verses * 100) if total_verses > 0 else 0
    
    if percentage > 10:  # More than 10% missing
        return HealthCheckResult(
            check="missing_embeddings",
            status="unhealthy",
            message=f"{missing} verses ({percentage:.1f}%) missing embeddings",
            severity="medium",
            auto_repair_available=True
        )
    elif percentage > 0:
        return HealthCheckResult(
            check="missing_embeddings",
            status="degraded",
            message=f"{missing} verses ({percentage:.1f}%) missing embeddings",
            severity="low",
            auto_repair_available=True
        )
    else:
        return HealthCheckResult(
            check="missing_embeddings",
            status="healthy",
            message="All verses have embeddings"
        )
```

### **API Endpoint Health Check**

```python
def check_api_endpoints() -> HealthCheckResult:
    """Check all API endpoints are responsive"""
    
    endpoints = [
        "/health",
        "/api/verses/1",
        "/api/dictionary/lookup?word=dharma",
        "/api/corpus/search?query=karma"
    ]
    
    failures = []
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code >= 500:
                failures.append(f"{endpoint}: {response.status_code}")
        except Exception as e:
            failures.append(f"{endpoint}: {str(e)}")
    
    if failures:
        return HealthCheckResult(
            check="api_endpoints",
            status="unhealthy",
            message=f"Failed endpoints: {', '.join(failures)}",
            severity="high"
        )
    else:
        return HealthCheckResult(
            check="api_endpoints",
            status="healthy",
            message="All API endpoints responsive"
        )
```

### **Query Performance Check**

```python
def check_query_performance() -> HealthCheckResult:
    """Check database query performance"""
    
    slow_queries = []
    
    # Test common queries
    queries = {
        "get_verse": lambda: db.query(Verse).filter(Verse.id == 1).first(),
        "search_dictionary": lambda: db.query(DictionaryEntry).filter(
            DictionaryEntry.headword.like("%dharma%")
        ).limit(10).all(),
        "list_texts": lambda: db.query(Text).all()
    }
    
    for name, query_func in queries.items():
        start = time.time()
        query_func()
        duration = time.time() - start
        
        if duration > 1.0:  # Slower than 1 second
            slow_queries.append(f"{name}: {duration:.2f}s")
    
    if slow_queries:
        return HealthCheckResult(
            check="query_performance",
            status="degraded",
            message=f"Slow queries detected: {', '.join(slow_queries)}",
            severity="medium"
        )
    else:
        return HealthCheckResult(
            check="query_performance",
            status="healthy",
            message="All queries performing well"
        )
```

---

## Health Check Execution

### **Manual Health Check**

```python
def run_health_check() -> HealthReport:
    """Run all health checks and generate report"""
    
    report = HealthReport(timestamp=datetime.now())
    
    # Database checks
    report.add_check(check_database_connectivity())
    report.add_check(check_orphaned_records())
    report.add_check(check_missing_embeddings())
    
    # API checks
    report.add_check(check_api_endpoints())
    
    # Performance checks
    report.add_check(check_query_performance())
    
    # Calculate overall health score
    report.calculate_health_score()
    
    return report
```

### **Automated Health Check (3.0)**

```python
from apscheduler.schedulers.background import BackgroundScheduler

def schedule_health_checks():
    """Schedule automated health checks"""
    
    scheduler = BackgroundScheduler()
    
    # Run full health check every hour
    scheduler.add_job(
        run_health_check_and_log,
        'interval',
        hours=1,
        id='hourly_health_check'
    )
    
    # Run critical checks every 5 minutes
    scheduler.add_job(
        run_critical_health_checks,
        'interval',
        minutes=5,
        id='critical_health_check'
    )
    
    scheduler.start()

def run_health_check_and_log():
    """Run health check and log results"""
    
    report = run_health_check()
    
    # Log to database
    log_health_report(report)
    
    # Alert if unhealthy
    if report.health_score < 0.8:
        send_alert(report)
    
    # Auto-repair if enabled
    if AUTO_REPAIR_ENABLED:
        auto_repair(report)
```

---

## Auto-Repair System (3.0)

### **Auto-Repair Rules**

```python
AUTO_REPAIR_RULES = {
    "orphaned_records": {
        "enabled": True,
        "action": delete_orphaned_records,
        "requires_approval": False
    },
    "missing_embeddings": {
        "enabled": True,
        "action": generate_missing_embeddings,
        "requires_approval": False
    },
    "stale_cache": {
        "enabled": True,
        "action": clear_stale_cache,
        "requires_approval": False
    },
    "fragmented_indexes": {
        "enabled": True,
        "action": rebuild_indexes,
        "requires_approval": True  # Requires human approval
    }
}

def auto_repair(report: HealthReport):
    """Automatically repair issues found in health check"""
    
    for check in report.checks:
        if check.status != "healthy" and check.auto_repair_available:
            rule = AUTO_REPAIR_RULES.get(check.check)
            
            if rule and rule["enabled"]:
                if rule["requires_approval"]:
                    # Queue for human approval
                    queue_repair_for_approval(check, rule["action"])
                else:
                    # Auto-repair immediately
                    try:
                        rule["action"](check)
                        log_repair(check, "success")
                    except Exception as e:
                        log_repair(check, "failed", str(e))
```

### **Repair Actions**

```python
def delete_orphaned_records(check: HealthCheckResult):
    """Delete orphaned records"""
    
    # Delete orphaned verses
    db.query(Verse).filter(
        ~Verse.text_id.in_(db.query(Text.id))
    ).delete(synchronize_session=False)
    
    # Delete orphaned commentaries
    db.query(Commentary).filter(
        ~Commentary.verse_id.in_(db.query(Verse.id))
    ).delete(synchronize_session=False)
    
    db.commit()

def generate_missing_embeddings(check: HealthCheckResult):
    """Generate embeddings for verses that are missing them"""
    
    verses_without_embeddings = db.query(Verse).filter(
        Verse.embedding_vector.is_(None)
    ).limit(100).all()  # Process in batches
    
    for verse in verses_without_embeddings:
        embedding = generate_embedding(verse.sanskrit_text + " " + verse.english_translation)
        verse.embedding_vector = embedding
        verse.embedding_model = "text-embedding-3-large"
        verse.embedding_generated_at = datetime.now()
    
    db.commit()

def clear_stale_cache(check: HealthCheckResult):
    """Clear cache entries older than 30 days"""
    
    cutoff = datetime.now() - timedelta(days=30)
    
    db.query(TranslationCache).filter(
        TranslationCache.created_at < cutoff
    ).delete()
    
    db.commit()
```

---

## Health Metrics

### **Health Score Calculation**

```python
def calculate_health_score(checks: List[HealthCheckResult]) -> float:
    """Calculate overall system health score (0-1)"""
    
    weights = {
        "healthy": 1.0,
        "degraded": 0.7,
        "unhealthy": 0.3
    }
    
    severity_multipliers = {
        "critical": 2.0,
        "high": 1.5,
        "medium": 1.0,
        "low": 0.5
    }
    
    total_weight = 0
    weighted_score = 0
    
    for check in checks:
        weight = weights.get(check.status, 0.5)
        multiplier = severity_multipliers.get(check.severity, 1.0)
        
        total_weight += multiplier
        weighted_score += weight * multiplier
    
    return weighted_score / total_weight if total_weight > 0 else 0.0
```

### **Health Trends**

```python
def get_health_trend(days: int = 7) -> List[HealthReport]:
    """Get health check history for trend analysis"""
    
    cutoff = datetime.now() - timedelta(days=days)
    
    reports = db.query(HealthReport).filter(
        HealthReport.timestamp >= cutoff
    ).order_by(HealthReport.timestamp.asc()).all()
    
    return reports

def analyze_health_trend(reports: List[HealthReport]) -> TrendAnalysis:
    """Analyze health trend over time"""
    
    scores = [r.health_score for r in reports]
    
    # Calculate trend
    if len(scores) > 1:
        trend = (scores[-1] - scores[0]) / len(scores)
    else:
        trend = 0.0
    
    return TrendAnalysis(
        current_score=scores[-1] if scores else 0.0,
        average_score=sum(scores) / len(scores) if scores else 0.0,
        trend=trend,
        trend_direction="improving" if trend > 0 else "degrading" if trend < 0 else "stable"
    )
```

---

## Alerting

### **Alert Rules**

```python
ALERT_RULES = {
    "critical_health": {
        "condition": lambda report: report.health_score < 0.5,
        "channels": ["email", "slack"],
        "message": "CRITICAL: System health score below 50%"
    },
    "degraded_health": {
        "condition": lambda report: report.health_score < 0.8,
        "channels": ["email"],
        "message": "WARNING: System health score below 80%"
    },
    "api_down": {
        "condition": lambda report: any(c.check == "api_endpoints" and c.status == "unhealthy" for c in report.checks),
        "channels": ["email", "slack", "sms"],
        "message": "CRITICAL: API endpoints are down"
    }
}

def send_alert(report: HealthReport):
    """Send alerts based on health report"""
    
    for rule_name, rule in ALERT_RULES.items():
        if rule["condition"](report):
            for channel in rule["channels"]:
                send_alert_via_channel(channel, rule["message"], report)
```

---

## Evolution Rules

### **When This Protocol Changes**

**Triggers:**
- Update SYSTEM_EVOLUTION_PROTOCOL.md
- Update SOUL_TRANSMIGRATION_PROTOCOL.md
- Update implementation in `07_SYSTEM_CORE/self_healing.py`
- Update health check definitions

**Validation:**
- Test all health checks
- Verify auto-repair logic
- Check alert rules

---

## Implementation Status

### **Transformation 2.1 (Current)**

**Status:** Partially Active

**Deliverables:**
- ✅ Protocol documented
- ✅ Health check definitions
- ✅ Manual health check script
- ⏳ Automated scheduling (3.0)
- ⏳ Auto-repair system (3.0)
- ⏳ Alerting (3.0)

### **Transformation 3.0 (Planned)**

**Planned Implementation:**
- Implement all health checks
- Schedule automated checks
- Build auto-repair system
- Set up alerting
- Create health dashboard

---

## Related Protocols

- **SYSTEM_EVOLUTION_PROTOCOL.md** - How this protocol evolves
- **DEPENDENCY_GRAPH_PROTOCOL.md** - Health check dependencies
- **DATA_VALIDATION_PROTOCOL.md** - Data integrity checks
- **SUPABASE_ADMINISTRATION_PROTOCOL.md** - Database health

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2024-11-23 | Initial creation | Solution Architect Persona |

---

**Prepared by:** Solution Architect Persona  
**Date:** November 23, 2024  
**Transformation:** 2.1 - Phase 1, Turn 1.1  
**Status:** Partially Active (Full activation: 3.0)
