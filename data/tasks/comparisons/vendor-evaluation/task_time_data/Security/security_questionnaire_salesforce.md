# Security Questionnaire - Salesforce
## Vendor Response

**Completed by:** Salesforce Trust & Security Team  
**Date:** December 10, 2025  
**Version:** 2025.Q4

---

## 1. Security Certifications & Compliance

| Certification | Status | Valid Through | Notes |
|---------------|--------|---------------|-------|
| SOC 1 Type II | ✓ Current | Dec 2026 | Annual audit |
| SOC 2 Type II | ✓ Current | Dec 2026 | Annual audit |
| ISO 27001 | ✓ Current | Mar 2027 | 3-year cycle |
| ISO 27017 | ✓ Current | Mar 2027 | Cloud security |
| ISO 27018 | ✓ Current | Mar 2027 | Cloud privacy |
| CSA STAR Level 2 | ✓ Current | Jun 2026 | |
| FedRAMP High | ✓ Current | Sep 2026 | Government Cloud only |
| HIPAA | ✓ Available | N/A | BAA available |
| PCI DSS Level 1 | ✓ Current | Mar 2026 | Commerce Cloud |
| GDPR | ✓ Compliant | N/A | EU operations |
| CCPA | ✓ Compliant | N/A | CA operations |

**Audit Reports Available:** SOC 1, SOC 2, ISO certificates available under NDA via Trust Portal.

---

## 2. Data Security

### 2.1 Encryption

| Data State | Method | Key Management |
|------------|--------|----------------|
| At Rest | AES-256 | Salesforce managed |
| In Transit | TLS 1.2/1.3 | Certificate pinning |
| Database | AES-256 | HSM-backed |
| Backups | AES-256 | Separate key hierarchy |

**Shield Platform Encryption (Optional Add-On):**
- Customer-managed encryption keys
- Field-level encryption
- Deterministic vs probabilistic options
- Bring Your Own Key (BYOK) supported

### 2.2 Data Residency

| Region | Data Centers | Availability |
|--------|--------------|--------------|
| North America | Virginia, Oregon, Chicago | ✓ |
| Europe | Frankfurt, London, Paris | ✓ |
| Asia Pacific | Tokyo, Sydney, Singapore | ✓ |
| Canada | Toronto | ✓ |
| Government | FedRAMP regions | ✓ (Gov Cloud) |

**Hyperforce:** New architecture enabling additional data residency options. Currently in rollout.

### 2.3 Data Isolation

- Multi-tenant architecture with logical data separation
- Organization ID (OrgID) enforced at database level
- No cross-tenant data access possible
- Regular penetration testing validates isolation

---

## 3. Access Controls

### 3.1 Authentication

| Method | Supported |
|--------|-----------|
| Username/Password | ✓ |
| SAML 2.0 SSO | ✓ |
| OAuth 2.0 | ✓ |
| MFA - App-based | ✓ |
| MFA - SMS | ✓ |
| MFA - Security Key (FIDO2) | ✓ |
| Social Login | ✓ (Optional) |
| Certificate-based | ✓ |

**MFA Enforcement:** Can be required for all users, specific profiles, or specific permission sets.

### 3.2 Authorization

| Feature | Capability |
|---------|------------|
| Profiles | Yes - control object CRUD |
| Permission Sets | Yes - additive permissions |
| Permission Set Groups | Yes - bundle permissions |
| Field-Level Security | Yes - per profile/permission set |
| Record-Level Security | Yes - OWD, sharing rules, manual |
| Territory Management | Yes - hierarchy-based |
| Role Hierarchy | Yes - data visibility |
| Session Policies | Yes - IP, time, device |

### 3.3 Password Policies

Configurable per organization:
- Minimum length: 8-128 characters
- Complexity requirements
- Expiration periods
- History enforcement (up to 24 passwords)
- Lockout thresholds
- Password reset flows

---

## 4. Infrastructure Security

### 4.1 Physical Security

- Tier III+ data centers
- 24/7 security personnel
- Biometric access controls
- Video surveillance
- Visitor logging
- Caged equipment areas

### 4.2 Network Security

| Control | Implementation |
|---------|----------------|
| Firewalls | Multi-layer, next-gen |
| IDS/IPS | Real-time monitoring |
| DDoS Protection | Multiple providers |
| WAF | Application-layer protection |
| Network Segmentation | VLANs, microsegmentation |
| VPN | Site-to-site available |

### 4.3 Endpoint Security

- Server hardening (CIS benchmarks)
- Automated patching
- EDR on administrative systems
- Container security scanning
- Regular vulnerability assessments

---

## 5. Application Security

### 5.1 Secure Development

| Practice | Implemented |
|----------|-------------|
| Secure SDLC | Yes - formal process |
| Code Review | Yes - mandatory |
| Static Analysis (SAST) | Yes |
| Dynamic Analysis (DAST) | Yes |
| Dependency Scanning | Yes |
| Penetration Testing | Yes - annual + continuous |
| Bug Bounty | Yes - public program |

### 5.2 Vulnerability Management

- Continuous scanning
- Risk-based prioritization
- Critical: < 48 hours to patch
- High: < 7 days to patch
- Medium: < 30 days to patch
- Customer notification for critical issues

---

## 6. Incident Response

### 6.1 Capabilities

| Capability | Details |
|------------|---------|
| 24/7 SOC | Global security operations |
| Incident Response Team | Dedicated team |
| Mean Time to Detect | < 1 hour for critical |
| Mean Time to Respond | < 4 hours for critical |
| Communication | Status page, direct notification |
| Forensics | In-house capability |

### 6.2 Customer Notification

- Security incidents affecting customer data: 72 hours
- Privacy incidents: 72 hours (or as required by law)
- Service incidents: Real-time status page

---

## 7. Business Continuity

### 7.1 Availability

| Metric | Target | Historical |
|--------|--------|------------|
| Uptime SLA | 99.9% | 99.996% (2024) |
| RPO | 4 hours | Typically < 1 hour |
| RTO | 12 hours | Typically < 4 hours |

### 7.2 Disaster Recovery

- Geographically distributed data centers
- Real-time replication
- Automated failover capabilities
- Annual DR testing
- Multi-region active-active available

### 7.3 Backup

- Daily backups included
- Weekly export available
- 90-day retention (standard)
- Unlimited retention (Shield add-on)

---

## 8. Audit & Monitoring

### 8.1 Logging

| Log Type | Retention | Access |
|----------|-----------|--------|
| Login History | 6 months | User accessible |
| Setup Audit Trail | 180 days | Admin accessible |
| Field History | 18 months | Object accessible |
| Event Monitoring | 30 days | Shield add-on |

### 8.2 Real-time Monitoring (Shield)

- Login forensics
- API anomaly detection
- Report anomaly detection
- Data leakage detection

### 8.3 SIEM Integration

Native connectors for:
- Splunk
- Microsoft Sentinel
- IBM QRadar
- Sumo Logic
- Generic: Syslog, S3, Event Hubs

---

## 9. Vendor Management

| Question | Response |
|----------|----------|
| Sub-processors | List available in DPA |
| Background checks | Yes - all employees |
| Security training | Annual + role-based |
| Third-party audits | SOC 2 covers vendors |
| Sub-processor notification | 30 days notice |

---

## 10. Contractual

| Item | Available |
|------|-----------|
| Data Processing Agreement | Yes - standard or custom |
| Business Associate Agreement | Yes - HIPAA |
| SLA | Yes - 99.9% uptime |
| Security Addendum | Yes - on request |
| Insurance | Cyber liability coverage |

---

## Summary Assessment

**Security Posture: STRONG**

Salesforce demonstrates industry-leading security practices:
- Comprehensive certifications (SOC 2, ISO 27001, FedRAMP)
- Strong encryption (AES-256, with customer key option)
- Robust access controls
- Mature incident response
- Extensive audit capabilities

**Potential Concerns:**
- Advanced features (Shield, Event Monitoring) are add-on cost
- Multi-tenant architecture (addressed through logical isolation)

**Recommendation:** Approved for sensitive data with appropriate configuration.

---

*For additional security documentation, visit trust.salesforce.com*
