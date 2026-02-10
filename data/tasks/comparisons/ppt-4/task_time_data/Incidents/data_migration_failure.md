# Incident Report: Data Migration Script Failure

**Incident ID:** INC-2025-1105  
**Severity:** P1 - High (Potential P0 if undetected)  
**Status:** Resolved  
**Discovery:** QA Testing  

---

## Executive Summary

During QA testing on November 5th, a data migration script designed to convert legacy data formats to the new multi-tenant schema was discovered to be silently failing on records containing special characters (Unicode, accented letters, certain punctuation). The failure mode was silent data truncation, which could have resulted in data loss in production.

**Key Facts:**
- No actual data loss occurred (caught in QA)
- Affected ~3% of test records
- Root cause: Character encoding mismatch
- Fix deployed within 5 days

---

## Timeline

| Date | Event |
|------|-------|
| 2025-11-01 | Migration script deployed to QA environment |
| 2025-11-05 | QA tester (Jennifer) notices truncated customer names |
| 2025-11-05 | Initial investigation - pattern identified: special characters |
| 2025-11-06 | Sarah Kim assigned for deep investigation |
| 2025-11-07 | Root cause confirmed: UTF-8 vs Latin-1 encoding issue |
| 2025-11-08 | Fix developed and tested in isolation |
| 2025-11-09 | Fix verified in QA environment |
| 2025-11-10 | Migration script re-run successfully - all data intact |

---

## Technical Details

### The Problem

The data migration script was reading legacy data files exported from TechCorp's existing system. These files contained mixed character encodings due to years of data entry from different systems.

```
Expected: UTF-8 encoding throughout
Actual: Mix of UTF-8, Latin-1 (ISO-8859-1), and Windows-1252

Examples of affected data:
- Customer names: "Müller" → "M" (truncated at ü)
- Addresses: "123 Café Street" → "123 Caf" (truncated at é)
- Notes: "€500 payment" → "" (entire field lost due to € symbol)
```

### Why It Was Silent

The migration script used a legacy database driver that was configured with:
- `errors='ignore'` - silently drop characters that can't be encoded
- No validation step comparing input vs output record counts
- No character-level integrity check

### Impact Assessment

| Category | Count | Percentage |
|----------|-------|------------|
| Total records migrated | 847 (test set) | 100% |
| Records with special characters | 127 | 15% |
| Records with data truncation | 26 | 3% |
| Records with complete field loss | 4 | 0.5% |

**If this had reached production:**
- ~25,000 records estimated to have special characters
- ~5,000 records would have experienced truncation
- ~400 records would have lost entire fields
- Customer names, addresses, and notes most affected

---

## Root Cause Analysis

### Technical Root Cause
1. Legacy export tool output files with inconsistent encoding
2. Migration script assumed UTF-8 throughout
3. Database driver configured to silently ignore encoding errors
4. No data integrity validation after migration

### Process Root Cause
1. Migration script was developed against sanitized test data
2. Test data did not include international characters
3. No code review specifically for encoding handling
4. QA test cases didn't include special character validation until Jennifer's ad-hoc testing

### Why It Wasn't Caught Earlier
- Development environment used clean test data
- Integration tests used ASCII-only fixtures
- The "happy path" worked perfectly
- No explicit encoding test cases

---

## Resolution

### Code Fix
```python
# Before (problematic)
with open(file_path, 'r') as f:
    data = f.read()

# After (robust)
import chardet

def read_with_encoding_detection(file_path):
    # Detect the actual encoding
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding'] or 'utf-8'
    
    # Read with detected encoding, replacing errors
    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
        data = f.read()
    
    # Log any replacement characters for review
    if '\ufffd' in data:
        logger.warning(f"Encoding issues detected in {file_path}")
    
    return data
```

### Validation Added
1. Record count comparison (before vs after)
2. Field-level hash validation for critical fields
3. Special character presence check
4. Automated report of any data transformations

### Process Improvements
1. Test data now includes international character set
2. Encoding handling added to code review checklist
3. Data migration validation step added to QA process

---

## Lessons Learned

### What Went Well
- QA caught the issue before production
- Root cause identification was quick (2 days)
- Fix was straightforward once root cause understood
- Team response was collaborative, not blame-focused

### What Went Wrong
- Test data wasn't representative of production
- Silent failure mode masked the problem
- Encoding handling wasn't considered in design
- Migration validation was assumed, not verified

### What Was Lucky
- Jennifer happened to notice truncated names
- The issue was caught with time to fix before launch
- No real customer data was affected

---

## Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Add international character test fixtures | Sarah Kim | 2025-11-12 | Complete |
| Implement migration validation framework | David Park | 2025-11-15 | Complete |
| Update code review checklist for encoding | Maria Santos | 2025-11-12 | Complete |
| Create encoding handling guidelines doc | Sarah Kim | 2025-11-18 | Complete |
| Add pre-migration data profiling step | DevOps | 2025-11-20 | Complete |

---

## Quotes from Team Discussion

> "This is exactly the kind of bug that causes post-launch nightmares. We got lucky." - David Park

> "The test data problem is systemic. If our test data doesn't look like production data, we're not really testing." - Sarah Kim

> "Silent failures are the worst kind. We should never configure anything to silently ignore errors." - Maria Santos

> "Jennifer saved us here. Good instinct to investigate those truncated names." - James Chen

---

## Sign-off

**Prepared by:** Sarah Kim (Database Lead)  
**Reviewed by:** David Park (Engineering Lead)  
**Approved by:** James Chen (Project Manager)  
**Date:** November 12, 2025

---

*Classification: Internal - Post-Mortem Documentation*
