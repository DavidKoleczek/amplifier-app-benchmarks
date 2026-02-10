# VelocityRM - Complete Product Documentation

**Version:** 4.2.1  
**Last Updated:** January 8, 2026  
**Classification:** Internal Use Only

---

## Table of Contents

1. [Product Overview](#product-overview)
2. [Technical Architecture](#technical-architecture)
3. [Feature Specifications](#feature-specifications)
4. [API Reference](#api-reference)
5. [Security & Compliance](#security--compliance)
6. [Integration Capabilities](#integration-capabilities)
7. [Known Limitations](#known-limitations)

---

## Product Overview

VelocityRM is an enterprise revenue management platform that combines CRM capabilities with advanced analytics and workflow automation. Designed for B2B sales organizations with complex deal cycles, VelocityRM provides end-to-end visibility from lead to cash.

### Target Market

- Mid-market and enterprise B2B companies
- Sales organizations with 10+ representatives
- Industries: Technology, Manufacturing, Financial Services, Professional Services
- Companies with deal cycles exceeding 30 days

### Core Value Proposition

VelocityRM addresses three fundamental challenges in B2B revenue operations:

1. **Pipeline Opacity** - Traditional CRMs rely on rep self-reporting. VelocityRM uses activity signals to automatically score deal health.

2. **Forecast Inaccuracy** - Most organizations achieve only 60-70% forecast accuracy. VelocityRM's ML models consistently deliver 85%+ accuracy.

3. **Process Fragmentation** - Revenue teams use 12+ tools on average. VelocityRM consolidates core workflows into a single platform.

---

## Technical Architecture

### System Components

VelocityRM operates as a cloud-native SaaS platform with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                    VelocityRM Platform                       │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Web Client    │   Mobile Apps   │   API Gateway           │
│   (React 18)    │   (React Native)│   (Kong)                │
├─────────────────┴─────────────────┴─────────────────────────┤
│                    Application Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ Deal Engine │ │ Analytics   │ │ Workflow Orchestrator   ││
│  │             │ │ Service     │ │                         ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    Data Layer                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ PostgreSQL  │ │ Redis       │ │ Elasticsearch           ││
│  │ (Primary)   │ │ (Cache)     │ │ (Search/Analytics)      ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│                    ML Infrastructure                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ Forecast    │ │ Deal Score  │ │ Activity Classification ││
│  │ Models      │ │ Models      │ │ Models                  ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

1. **Inbound Data**: Activity signals from email, calendar, call logs, and manual entry flow through the API Gateway
2. **Processing**: Real-time event processing enriches and normalizes data
3. **ML Scoring**: Asynchronous jobs score deals and generate forecasts (runs every 4 hours)
4. **Storage**: Primary data in PostgreSQL, derived analytics in Elasticsearch
5. **Caching**: Hot data cached in Redis with 15-minute TTL

### Infrastructure Specifications

| Component | Specification | Notes |
|-----------|--------------|-------|
| Compute | AWS EKS (Kubernetes) | Multi-AZ deployment |
| Database | PostgreSQL 15 (RDS) | Read replicas in each AZ |
| Cache | Redis 7.0 (ElastiCache) | Cluster mode enabled |
| Search | Elasticsearch 8.x | 3-node cluster |
| CDN | CloudFront | Global edge locations |
| WAF | AWS WAF | OWASP rule sets |

---

## Feature Specifications

### 1. Deal Management

#### 1.1 Deal Records
- **Field Types Supported**: Text, Number, Currency, Date, Picklist, Multi-select, Lookup, Formula
- **Custom Fields**: Up to 200 per object (Starter), 500 (Professional), Unlimited (Enterprise)
- **Record History**: 2 years (Starter), 5 years (Professional), Unlimited (Enterprise)

#### 1.2 Deal Stages
- Configurable stage definitions with entry/exit criteria
- Automatic stage progression based on activity signals
- Stage duration tracking and alerts
- Win probability mapping per stage

#### 1.3 Deal Scoring (AI-Powered)

The proprietary VelocityScore algorithm analyzes 47 signals across four categories:

| Category | Signals | Weight |
|----------|---------|--------|
| Engagement | Email opens, response rates, meeting frequency | 35% |
| Momentum | Stage velocity, activity trends, stakeholder additions | 25% |
| Fit | Company size, industry, tech stack match | 20% |
| Timing | Budget cycle alignment, urgency indicators | 20% |

**Technical Details:**
- Model type: Gradient Boosted Decision Trees (XGBoost)
- Training data: 2.3M historical deals across 450 customers
- Refresh frequency: Quarterly model retraining
- Accuracy metrics: 85% precision at 70% recall threshold

### 2. Pipeline Analytics

#### 2.1 Standard Reports
- Pipeline by Stage
- Pipeline by Rep
- Pipeline by Region/Segment
- Pipeline Movement (additions, progressions, removals)
- Coverage Analysis (pipeline vs. quota)

#### 2.2 Advanced Analytics (Professional & Enterprise)
- Cohort analysis
- Time-series forecasting
- Conversion funnel analysis
- Rep performance benchmarking
- Custom calculated metrics

#### 2.3 Forecasting Engine

**Methodology:**
1. Bottom-up rollup of deal-level forecasts
2. ML adjustment based on historical patterns
3. Manager override capability with audit trail
4. Confidence intervals at 80% and 95% levels

**Forecast Categories:**
- Commit: Deals with >90% close probability
- Best Case: Deals with >60% close probability
- Pipeline: All open deals weighted by probability

### 3. Workflow Automation

#### 3.1 Trigger Types
- Record creation
- Field change
- Stage change
- Time-based (scheduled)
- External webhook

#### 3.2 Action Types
- Create/Update records
- Send email (template-based)
- Send Slack/Teams notification
- Create task/reminder
- Call external API
- Route to queue

#### 3.3 Automation Limits

| Tier | Active Workflows | Actions/Day |
|------|-----------------|-------------|
| Starter | 10 | 5,000 |
| Professional | 50 | 50,000 |
| Enterprise | Unlimited | Unlimited |

### 4. Email & Calendar Integration

#### 4.1 Supported Providers
- Microsoft 365 (Exchange Online)
- Google Workspace
- Microsoft Exchange Server 2016+ (on-premise)

#### 4.2 Sync Capabilities
- Bi-directional email logging
- Calendar event sync
- Contact sync
- Activity timeline generation

#### 4.3 Email Tracking
- Open tracking (pixel-based)
- Link click tracking
- Attachment download tracking
- Reply detection

**Privacy Note:** Email tracking can be disabled at account or user level for GDPR compliance.

### 5. Integrations

#### 5.1 Native Integrations
| System | Capabilities | Sync Frequency |
|--------|--------------|----------------|
| Salesforce | Bi-directional sync | Real-time |
| HubSpot | Bi-directional sync | Real-time |
| Slack | Notifications, commands | Real-time |
| Microsoft Teams | Notifications, tabs | Real-time |
| Zoom | Meeting auto-log | Real-time |
| Gong | Conversation intelligence | Hourly |
| LinkedIn Sales Navigator | Contact enrichment | Daily |
| ZoomInfo | Company enrichment | On-demand |

#### 5.2 API Access

**REST API Specifications:**
- Base URL: `https://api.velocityrm.io/v2`
- Authentication: OAuth 2.0 (Bearer token)
- Rate Limits: 
  - Starter: 100 requests/minute
  - Professional: 500 requests/minute
  - Enterprise: 2,000 requests/minute
- Pagination: Cursor-based, 100 records default, 500 max

**Webhook Specifications:**
- Payload format: JSON
- Retry policy: 3 attempts with exponential backoff
- HMAC signature verification: SHA-256

---

## Security & Compliance

### Data Encryption
- At rest: AES-256
- In transit: TLS 1.3
- Database: Transparent Data Encryption (TDE)

### Access Controls
- SAML 2.0 SSO
- SCIM provisioning
- Role-based access control (RBAC)
- Field-level security
- IP allowlisting (Enterprise)

### Compliance Certifications
- SOC 2 Type II (annual audit)
- ISO 27001 (certified)
- GDPR compliant
- CCPA compliant
- HIPAA available (Enterprise, requires BAA)

### Data Residency
- US (N. Virginia, Oregon)
- EU (Ireland, Frankfurt)
- APAC (Singapore, Sydney)

---

## API Reference

### Authentication

```bash
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id={id}&client_secret={secret}
```

### Common Endpoints

#### List Deals
```bash
GET /v2/deals
Authorization: Bearer {token}

Query Parameters:
- stage: Filter by stage ID
- owner: Filter by owner ID
- updated_since: ISO 8601 timestamp
- limit: 1-500 (default 100)
- cursor: Pagination cursor
```

#### Create Deal
```bash
POST /v2/deals
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Acme Corp - Enterprise",
  "amount": 150000,
  "stage_id": "stage_003",
  "expected_close": "2026-03-31",
  "owner_id": "user_abc123",
  "custom_fields": {
    "product_interest": ["Core Platform", "Analytics Add-on"]
  }
}
```

#### Update Deal
```bash
PATCH /v2/deals/{deal_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "stage_id": "stage_004",
  "amount": 175000
}
```

### Webhook Payload Example

```json
{
  "event": "deal.stage_changed",
  "timestamp": "2026-01-14T10:30:00Z",
  "data": {
    "deal_id": "deal_xyz789",
    "previous_stage": "stage_003",
    "new_stage": "stage_004",
    "changed_by": "user_abc123"
  },
  "signature": "sha256=abc123..."
}
```

---

## Known Limitations

### Current Limitations (v4.2.1)

1. **Mobile App**
   - Offline mode limited to read-only (write sync planned Q2 2026)
   - Push notifications delayed up to 5 minutes

2. **Reporting**
   - Maximum 50 columns in custom reports
   - Dashboard auto-refresh interval minimum 5 minutes
   - Export limited to 100,000 rows per report

3. **Integrations**
   - Salesforce sync excludes custom objects with >50 fields
   - Google Calendar sync may have 1-2 minute delay
   - Gong integration requires Gong Enterprise tier

4. **Performance**
   - Bulk API limited to 10,000 records per request
   - Complex forecast calculations may take up to 30 seconds
   - Search index updates have 5-minute lag

### Upcoming Improvements (See Roadmap)

- Q1 2026: Mobile offline write support
- Q2 2026: Real-time dashboard refresh
- Q3 2026: Custom object sync for Salesforce
- Q4 2026: Advanced predictive analytics

---

## Appendix: Glossary

| Term | Definition |
|------|------------|
| Deal | A potential sale being tracked through the pipeline |
| Stage | A defined phase in the sales process |
| VelocityScore | Proprietary AI-generated deal health score (0-100) |
| Coverage | Ratio of pipeline value to quota |
| Commit | Deals expected to close with high confidence |
| MEDDIC | Sales methodology (Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion) |

---

*Document maintained by Product Engineering. For questions, contact product-docs@velocityrm.io*
