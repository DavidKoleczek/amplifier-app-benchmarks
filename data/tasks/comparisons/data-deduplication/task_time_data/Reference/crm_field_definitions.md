# CRM Field Definitions - Customer Data Dictionary

**Document Version:** 2.1  
**Last Updated:** 2025-11-01  
**Owner:** Data Operations Team

---

## Overview

This document defines the standard field schema for customer records in our CRM system. All data imports, exports, and merges should conform to these definitions.

---

## Core Customer Fields

### customer_id
- **Type:** String
- **Format:** `CRM-XXX` (CRM prefix + 3-digit sequential number)
- **Required:** Yes
- **Description:** Unique identifier for each customer record
- **Notes:** Auto-generated on record creation. Never reuse IDs from deleted records.

### company_name
- **Type:** String
- **Max Length:** 255 characters
- **Required:** Yes
- **Description:** Legal or commonly used business name
- **Standardization Rules:**
  - Use title case (e.g., "Acme Corporation" not "ACME CORPORATION")
  - Include legal suffix (Inc, LLC, Co, Corp) when known
  - Avoid abbreviations unless part of official name
  - See `company_name_standardization.xlsx` for approved variations

### contact_name
- **Type:** String
- **Max Length:** 100 characters
- **Required:** Yes
- **Description:** Full name of primary contact
- **Format:** "First Last" or "Title First Last" (e.g., "Dr. Emily Watson")

### contact_email
- **Type:** String (Email)
- **Max Length:** 254 characters
- **Required:** Yes
- **Validation:** Must be valid email format, must not be on bounce list
- **Description:** Primary email for customer communications
- **Notes:** Prefer work email over personal

### phone
- **Type:** String
- **Format:** `XXX-XXXX` (standardized to hyphenated format)
- **Required:** No
- **Description:** Primary phone number
- **Standardization:** Strip all formatting on import, store as `XXX-XXXX`

### industry
- **Type:** String (Enum)
- **Required:** Yes
- **Valid Values:**
  - Agriculture
  - Automotive
  - Construction
  - Education
  - Energy
  - Financial Services
  - Forestry
  - Healthcare
  - Hospitality
  - Insurance
  - Logistics
  - Manufacturing
  - Real Estate
  - Retail
  - Technology
  - Other

### annual_revenue
- **Type:** Decimal
- **Required:** No
- **Description:** Estimated annual revenue in USD
- **Notes:** Update annually; flag if data is >2 years old

### last_contact_date
- **Type:** Date
- **Format:** `YYYY-MM-DD`
- **Required:** Yes
- **Description:** Date of most recent meaningful interaction
- **Staleness Rule:** Records with last_contact_date > 180 days are flagged as "potentially stale"

### lead_source
- **Type:** String (Enum)
- **Required:** Yes
- **Valid Values:**
  - Cold Call
  - Conference
  - Partner
  - Referral
  - Trade Show
  - Website
  - Other

### status
- **Type:** String (Enum)
- **Required:** Yes
- **Valid Values:**
  - Active - Current customer with recent engagement
  - Inactive - No engagement >180 days, may require re-qualification
  - Churned - Former customer, lost to competitor or business closure
  - Prospect - Not yet converted to customer
- **Business Rules:**
  - Auto-transition Active → Inactive after 180 days no contact
  - Manual review required for Inactive → Churned

### address
- **Type:** String
- **Max Length:** 500 characters
- **Required:** No
- **Format:** "Street, City, State ZIP"
- **Description:** Primary business address

---

## Data Quality Rules

### Duplicate Detection
Records are considered potential duplicates if ANY of:
1. Exact email match (case-insensitive)
2. Company name fuzzy match (>85% similarity) AND same industry
3. Phone number exact match (after normalization)

### Merge Priority
When merging duplicates, prefer data from:
1. Most recent `last_contact_date`
2. CRM system over legacy Salesforce
3. Direct entry over imported records

### Stale Record Criteria
A record is flagged as "stale" if:
- `last_contact_date` > 180 days ago AND status = "Active"
- Email has bounced (hard bounce)
- Phone number disconnected (if verified)

---

## Import/Export Specifications

### Required Fields for Import
- company_name
- contact_name  
- contact_email
- industry
- status

### Auto-Generated Fields (Do Not Import)
- customer_id
- created_date
- modified_date

### Date Formats Accepted on Import
- `YYYY-MM-DD` (preferred)
- `MM/DD/YYYY`
- `DD-Mon-YYYY`

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 2.1 | 2025-11-01 | Data Ops | Added staleness rules |
| 2.0 | 2025-06-15 | Data Ops | Added industry enum values |
| 1.0 | 2024-01-10 | Data Ops | Initial version |
