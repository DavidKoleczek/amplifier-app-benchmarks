# Security Questionnaire - Pipedrive
## Vendor Response

**Completed by:** Pipedrive Security Team  
**Date:** December 14, 2025  
**Version:** 2025.4

---

## 1. Security Certifications & Compliance

| Certification | Status | Expected | Notes |
|---------------|--------|----------|-------|
| SOC 2 Type II | ⏳ In Progress | Q2 2026 | Currently in audit |
| SOC 1 | ✗ Not planned | N/A | |
| ISO 27001 | ⏳ Planned | 2026 | Post-SOC 2 |
| CSA STAR | ✗ Not yet | TBD | |
| GDPR | ✓ Compliant | N/A | EU company origin |
| CCPA | ✓ Compliant | N/A | |
| Privacy Shield | ✓ Certified | N/A | |
| FedRAMP | ✗ Not available | N/A | Not planned |
| HIPAA | ✗ Not available | N/A | No BAA |
| PCI DSS | ✓ Via Stripe | N/A | Payment processing |

**Important Note:** SOC 2 Type II certification is in progress. We can provide a bridge letter from our auditors confirming the audit timeline. Expected completion: Q2 2026.

**Audit Reports:** SOC 2 report will be available upon completion. Currently can provide security assessment documentation.

---

## 2. Data Security

### 2.1 Encryption

| Data State | Method | Key Management |
|------------|--------|----------------|
| At Rest | AES-256 | Pipedrive managed (AWS KMS) |
| In Transit | TLS 1.2+ | Pipedrive managed |
| Database | AES-256 | AWS RDS encryption |
| Backups | AES-256 | AWS S3 encryption |

**Customer-Managed Keys:** Not available. Not on current roadmap.

**Field-Level Encryption:** Not available.

### 2.2 Data Residency

| Region | Data Centers | Availability |
|--------|--------------|--------------|
| United States | AWS US East | ✓ Default |
| European Union | AWS Frankfurt | ✓ Available |

**Data residency selection:** Available during initial setup. Transfer between regions requires support assistance and may involve service interruption.

### 2.3 Data Isolation

- Multi-tenant cloud architecture
- Logical separation by company ID
- Database-level row security
- Application-level access controls
- Annual penetration testing

---

## 3. Access Controls

### 3.1 Authentication

| Method | Supported |
|--------|-----------|
| Username/Password | ✓ |
| Google SSO | ✓ All plans |
| SAML 2.0 SSO | ✓ Enterprise only |
| OAuth 2.0 | ✓ For integrations |
| MFA - App-based | ✓ |
| MFA - SMS | ✓ |
| Security Keys (FIDO2) | ✗ |

**SSO Limitation:** SAML SSO is only available on Enterprise plan ($74.90/user/month vs $49.90 Professional).

### 3.2 Authorization

| Feature | Capability |
|---------|------------|
| Permission Sets | Yes - predefined (3 levels) |
| Custom Permissions | Limited |
| Visibility Groups | Enterprise only |
| Field Permissions | No - all or nothing |
| Record-Level Access | Basic - owner/shared |

**Permission Model:** Pipedrive uses a simpler permission model than enterprise CRMs:
- Admin: Full access
- Manager: Team oversight
- User: Own data + shared

**Custom Roles:** Not available. Must work within predefined permission levels.

### 3.3 Password Policies

| Policy | Available |
|--------|-----------|
| Minimum length | Yes - 8 chars |
| Complexity | Yes - basic |
| Expiration | No |
| History | No |
| Lockout | Yes - after 5 failures |

**Note:** Password policies are limited compared to enterprise platforms. Recommend enforcing SSO for stronger authentication.

---

## 4. Infrastructure Security

### 4.1 Physical Security

Pipedrive uses AWS infrastructure:
- AWS SOC 2 certified data centers
- 24/7 physical security
- Access controls and monitoring
- Environmental controls

### 4.2 Network Security

| Control | Implementation |
|---------|----------------|
| Firewalls | AWS Security Groups |
| DDoS Protection | AWS Shield Standard |
| WAF | AWS WAF |
| Network Monitoring | Internal monitoring |
| VPN | Not available |

### 4.3 Application Infrastructure

- Cloud-native on AWS
- Auto-scaling groups
- Load-balanced architecture
- Regular security updates

---

## 5. Application Security

### 5.1 Secure Development

| Practice | Implemented |
|----------|-------------|
| Secure SDLC | Yes |
| Code Review | Yes |
| Static Analysis (SAST) | Yes |
| Dynamic Analysis (DAST) | Limited |
| Dependency Scanning | Yes |
| Penetration Testing | Yes - annual |
| Bug Bounty | Yes - via Bugcrowd |

### 5.2 Vulnerability Management

- Quarterly vulnerability scans
- Risk-based prioritization
- Critical: ASAP
- High: 30 days
- Medium: 90 days

---

## 6. Incident Response

### 6.1 Capabilities

| Capability | Details |
|------------|---------|
| Security Team | Yes - dedicated |
| 24/7 Monitoring | Automated monitoring |
| Incident Response | Documented process |
| Response Time | Best effort |
| Communication | Email notification |

### 6.2 Customer Notification

- Security incidents: 72 hours
- Privacy incidents: Per GDPR requirements
- Service incidents: status.pipedrive.com

---

## 7. Business Continuity

### 7.1 Availability

| Metric | Target | Historical |
|--------|--------|------------|
| Uptime SLA | 99.9% | ~99.95% |
| RPO | 24 hours | Best effort |
| RTO | Not specified | Best effort |

**Note:** SLA commitments are less detailed than enterprise vendors. "Best effort" recovery.

### 7.2 Disaster Recovery

- AWS multi-AZ deployment
- Automated failover within region
- No cross-region failover

### 7.3 Backup

- Daily backups
- 14-day retention
- Customer export available
- Point-in-time recovery: Not available

---

## 8. Audit & Monitoring

### 8.1 Logging

| Log Type | Retention | Access |
|----------|-----------|--------|
| Login Activity | 30 days | Admin portal |
| Data Changes | In-app history | Record level |
| Security Events | Limited | Enterprise only |

### 8.2 Audit Logs

**Enterprise Plan Only:**
- User login/logout
- Permission changes
- Data exports
- Integration activity

**Professional Plan:** Limited audit visibility.

### 8.3 SIEM Integration

- No native SIEM connectors
- API available for custom integration
- Webhook support
- No real-time streaming

---

## 9. Vendor Management

| Question | Response |
|----------|----------|
| Sub-processors | List in Privacy Policy |
| Background checks | Yes - key personnel |
| Security training | Annual |
| Third-party audits | SOC 2 in progress |

---

## 10. Contractual

| Item | Available |
|------|-----------|
| Data Processing Agreement | Yes |
| Business Associate Agreement | No |
| SLA | Yes - 99.9% uptime |
| Security Addendum | Limited |
| Insurance | Yes - basic coverage |

---

## Gaps & Risks Assessment

### Critical Gaps

| Gap | Risk | Impact |
|-----|------|--------|
| No SOC 2 (yet) | HIGH | Cannot demonstrate compliance |
| No HIPAA/BAA | HIGH | Cannot handle PHI |
| No SAML (Professional) | MEDIUM | SSO requires Enterprise upgrade |
| Limited audit logs | MEDIUM | Compliance challenges |
| No password expiration | MEDIUM | Weaker credential hygiene |
| Basic permissions | MEDIUM | Limited access control |

### Timeline for Improvements

| Item | Expected Date |
|------|---------------|
| SOC 2 Type II | Q2 2026 |
| ISO 27001 | H2 2026 |
| Enhanced audit logs | 2026 |
| SAML on lower tiers | No commitment |

---

## Vendor Statement

*"Pipedrive is committed to security and is actively investing in our compliance program. We acknowledge that our certification portfolio is still developing. We're happy to provide a letter from our SOC 2 auditors confirming our audit timeline, and to schedule a call with our security team to address specific concerns."*

---

## Summary Assessment

**Security Posture: DEVELOPING**

Pipedrive shows commitment to security but currently lacks enterprise-grade certifications:

**Positives:**
- Encryption at rest and in transit
- Bug bounty program active
- GDPR compliant (EU origin)
- AWS infrastructure foundation
- SOC 2 actively in progress

**Concerns:**
- No SOC 2 today (expected Q2 2026)
- No ISO 27001 certification
- No HIPAA capability
- Limited audit/logging on lower tiers
- Basic permission model
- SAML requires Enterprise upgrade

**Risk Assessment:** 

For a company requiring SOC 2 compliance today or handling regulated data (HIPAA, FedRAMP), Pipedrive does NOT currently meet requirements.

For companies that can:
1. Accept pending SOC 2 certification
2. Upgrade to Enterprise tier
3. Avoid regulated data

Pipedrive may be acceptable with documented risk acceptance.

**Recommendation:** CONDITIONAL approval pending:
- SOC 2 bridge letter
- Enterprise tier (for SSO and audit)
- Written policy: No PHI or regulated data
- Re-evaluation upon SOC 2 completion

---

*For questions, contact security@pipedrive.com*
