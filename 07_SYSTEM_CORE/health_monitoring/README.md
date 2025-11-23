# Health Monitoring System

**Status:** ACTIVE (Transformation 2.1)  
**Auto-Repair:** Coming in Transformation 3.0

## Overview

The health monitoring system provides automated checks for the Vedic Mastery Study infrastructure. It detects issues and generates detailed reports, with auto-repair functionality planned for Transformation 3.0.

## Quick Start

### Run Health Check

```bash
cd /home/ubuntu/vedic-mastery-study
python3 07_SYSTEM_CORE/health_monitoring/run_health_check.py
```

### Output

The health check will:
1. Test all system components
2. Generate a detailed console report
3. Save a JSON report to `reports/` directory
4. Provide an overall health score (0.0 to 1.0)

## Health Checks Performed

### 1. Database Connectivity
- **Tests:** Supabase connection and query execution
- **Healthy:** Database responds within 1 second
- **Critical:** Cannot connect to database

### 2. Data Integrity
- **Tests:** Table existence and row counts
- **Healthy:** All tables have expected minimum data
- **Warning:** Some tables have less data than expected
- **Critical:** Tables missing or query errors

### 3. Embedding Coverage
- **Tests:** Percentage of verses with embeddings
- **Healthy:** > 90% coverage
- **Warning:** 0-90% coverage
- **Note:** Expected to be 0% until Transformation 3.0

### 4. API Health
- **Tests:** Translation Layer API responsiveness
- **Healthy:** API returns 200 status
- **Warning:** API not running or returns errors

### 5. Repository Status
- **Tests:** Git repository cleanliness
- **Healthy:** No uncommitted changes
- **Warning:** Uncommitted files present

## Health Status Levels

| Status | Score Range | Meaning |
|--------|-------------|---------|
| ✅ HEALTHY | 0.90 - 1.00 | All systems operational |
| ⚠️  WARNING | 0.70 - 0.89 | Minor issues detected |
| ❌ CRITICAL | 0.00 - 0.69 | Major issues require attention |
| ❓ UNKNOWN | N/A | Unable to determine status |

## Report Files

Health check reports are saved to:
```
07_SYSTEM_CORE/health_monitoring/reports/health_report_YYYYMMDD_HHMMSS.json
```

### Report Structure

```json
{
  "timestamp": "2025-11-23T16:56:33",
  "overall_status": "warning",
  "overall_score": 0.74,
  "issues_found": 2,
  "checks": [
    {
      "check_name": "database_connectivity",
      "status": "healthy",
      "score": 1.0,
      "message": "Database is accessible and responsive",
      "details": {...}
    },
    ...
  ]
}
```

## Automation (Coming in 3.0)

### Scheduled Health Checks
Health checks can be scheduled to run automatically:
- Hourly: Quick checks
- Daily: Full system scan
- Weekly: Deep analysis with trend reports

### Auto-Repair
Transformation 3.0 will add automatic repair for common issues:
- Regenerate missing embeddings
- Fix broken foreign key relationships
- Restart failed services
- Clear cache when needed

### Alerting
Future alerting options:
- Email notifications for critical issues
- Slack/Discord webhooks
- Dashboard integration

## Troubleshooting

### "Supabase client not available"
```bash
pip3 install supabase
```

### "Requests library not available"
```bash
pip3 install requests
```

### API Health Check Fails
Start the Translation Layer API:
```bash
cd /home/ubuntu/vedic-mastery-study
python3 05_SERVICES/translation_layer_api.py
```

## Integration

### Use in Scripts

```python
from health_monitoring.run_health_check import run_all_health_checks

report = run_all_health_checks()

if report['overall_status'] == 'critical':
    # Handle critical issues
    send_alert(report)
```

### Use in CI/CD

```yaml
# .github/workflows/health-check.yml
- name: Run Health Check
  run: python3 07_SYSTEM_CORE/health_monitoring/run_health_check.py
- name: Check Status
  run: |
    if [ $? -ne 0 ]; then
      echo "Health check failed!"
      exit 1
    fi
```

## Roadmap

### Transformation 2.1 (Current)
- ✅ Active health checks
- ✅ Detailed reporting
- ✅ JSON report export

### Transformation 3.0 (Planned)
- ⏳ Auto-repair system
- ⏳ Scheduled monitoring
- ⏳ Alert notifications
- ⏳ Trend analysis
- ⏳ Dashboard visualization

## Related Protocols

- `04_PROTOCOLS/HEALTH_MONITORING_PROTOCOL.md` - Complete protocol specification
- `04_PROTOCOLS/SYSTEM_EVOLUTION_PROTOCOL.md` - Self-healing architecture
- `03_PROJECT_MANAGEMENT/TRANSFORMATION_3.0_ROADMAP.md` - Future enhancements

## Support

For issues or questions:
1. Review the Health Monitoring Protocol
2. Check the health report JSON for detailed error messages
3. Consult the Transformation 2.1 documentation
