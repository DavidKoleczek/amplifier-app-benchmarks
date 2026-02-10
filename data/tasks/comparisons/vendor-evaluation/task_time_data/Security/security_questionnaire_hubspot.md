# Security Questionnaire - HubSpot
## Vendor Response

**Completed by:** HubSpot Security Team  
**Date:** December 12, 2025  
**Version:** Q4-2025

---

## 1. Security Certifications & Compliance

| Certification | Status | Valid Through | Notes |
|---------------|--------|---------------|-------|
| SOC 2 Type II | ✓ Current | Nov 2026 | Annual audit |
| SOC 3 | ✓ Current | Nov 2026 | Public report |
| ISO 27001 | ✓ Current | Aug 2027 | |
| CSA STAR Level 1 | ✓ Current | Self-assessment |
| GDPR | ✓ Compliant | N/A | EU operations |
| CCPA | ✓ Compliant | N/A | CA operations |
| Privacy Shield | ✓ Certified | N/A | US-EU transfers |
| FedRAMP | ✗ Not Available | N/A | Not on roadmap |
| HIPAA | ✗ Not Certified | N/A | See notes below |
| PCI DSS | ✓ Level 1 | Payments only |

**HIPAA Note:** HubSpot is not HIPAA certified and does not sign BAAs. While HubSpot implements security controls that align with HIPAA requirements, customers with strict HIPAA obligations should evaluate if HubSpot meets their specific compliance needs. We recommend consulting your compliance officer.

**Audit Reports:** SOC 2 Type II and SOC 3 reports available to customers under NDA.

---

## 2. Data Security

### 2.1 Encryption

| Data State | Method | Key Management |
|------------|--------|----------------|
| At Rest | AES-256 | HubSpot managed |
| In Transit | TLS 1.2+ | HubSpot managed |
| Database | AES-256 | AWS KMS |
| Backups | AES-256 | AWS KMS |

**Customer-Managed Keys:** Not currently available. On roadmap for 2026.

**Field-Level Encryption:** Not available. All data encrypted at rest with same key hierarchy.

### 2.2 Data Residency

| Region | Data Centers | Availability |
|--------|--------------|--------------|
| United States | AWS US East (Virginia) | ✓ Default |
| European Union | AWS EU (Frankfurt) | ✓ Available |
| Other Regions | Not available | Planned |

**EU Data Hosting:** Available for Professional and Enterprise tiers. Must be selected at account creation.

### 2.3 Data Isolation

- Multi-tenant SaaS architecture
- Logical separation by Hub ID
- Database-level access controls
- Regular penetration testing validates isolation
- No cross-tenant access possible

---

## 3. Access Controls

### 3.1 Authentication

| Method | Supported |
|--------|-----------|
| Username/Password | ✓ |
| SAML 2.0 SSO | ✓ (Professional+) |
| OAuth 2.0 | ✓ |
| Google Sign-In | ✓ |
| MFA - App-based | ✓ |
| MFA - SMS | ✓ |
| Security Keys (FIDO2) | ✗ Not yet |

**MFA:** Can be enforced at organization level. Recommended for all users.

### 3.2 Authorization

| Feature | Capability |
|---------|------------|
| User Roles | Yes - predefined roles |
| Custom Permissions | Yes - granular |
| Team-based Access | Yes - partitioning |
| Object Permissions | Yes - CRM records |
| Field Permissions | Limited - not field-level |
| Record-Level Access | Yes - ownership model |

**Note:** HubSpot's permission model is simpler than enterprise CRMs. Very granular permissions may require workarounds.

### 3.3 Password Policies

Standard policies:
- Minimum 8 characters
- Complexity requirements available
- 90-day expiration (optional)
- Lockout after failed attempts
- Password history: 4 passwords

**Advanced password policies (custom expiration, longer history) available on Enterprise tier only.**

---

## 4. Infrastructure Security

### 4.1 Physical Security

HubSpot uses AWS infrastructure:
- SOC 2 certified data centers
- 24/7 physical security
- Biometric access controls
- Video surveillance
- Environmental controls

### 4.2 Network Security

| Control | Implementation |
|---------|----------------|
| Firewalls | AWS VPC + WAF |
| IDS/IPS | AWS GuardDuty |
| DDoS Protection | AWS Shield |
| WAF | AWS WAF + custom rules |
| Network Segmentation | VPC isolation |

### 4.3 Application Infrastructure

- Containerized microservices
- Automated scaling
- Blue-green deployments
- Infrastructure as code
- Immutable infrastructure

---

## 5. Application Security

### 5.1 Secure Development

| Practice | Implemented |
|----------|-------------|
| Secure SDLC | Yes |
| Code Review | Yes - mandatory |
| Static Analysis (SAST) | Yes |
| Dynamic Analysis (DAST) | Yes |
| Dependency Scanning | Yes |
| Penetration Testing | Yes - annual + quarterly |
| Bug Bounty | Yes - private program |

### 5.2 Vulnerability Management

- Continuous automated scanning
- Weekly security reviews
- Critical: 24-48 hours
- High: 7 days
- Medium: 30 days
- Customer communication for impactful issues

---

## 6. Incident Response

### 6.1 Capabilities

| Capability | Details |
|------------|---------|
| Security Team | Dedicated security org |
| 24/7 Monitoring | Yes - automated alerts |
| Incident Response | Documented IRP |
| Mean Time to Detect | Generally < 4 hours |
| Mean Time to Respond | Generally < 24 hours |
| Communication | Email + in-app + status page |

### 6.2 Customer Notification

- Security incidents: 72 hours (or as legally required)
- Privacy incidents: As required by law
- Service incidents: status.hubspot.com

---

## 7. Business Continuity

### 7.1 Availability

| Metric | Target | Historical |
|--------|--------|------------|
| Uptime SLA | 99.95% | 99.98% (2024) |
| RPO | 24 hours | Typically < 4 hours |
| RTO | 24 hours | Typically < 8 hours |

### 7.2 Disaster Recovery

- Multi-AZ deployment
- Automated failover
- Regular DR testing
- Geographic redundancy (same region)

**Note:** Cross-region DR is available but not default. Discuss requirements.

### 7.3 Backup

- Daily automated backups
- 30-day retention
- Customer data export available
- Point-in-time recovery: Not available

---

## 8. Audit & Monitoring

### 8.1 Logging

| Log Type | Retention | Access |
|----------|-----------|--------|
| Login Activity | 90 days | Admin portal |
| Security Activity | 90 days | Admin portal |
| CRM Activity | Varies | CRM records |
| API Activity | 30 days | Developer portal |

### 8.2 Audit Logs

Available audit events:
- User logins/logouts
- Permission changes
- Data exports
- Integration changes
- Security setting changes

**Limitations:** Less granular than Salesforce. No field-level audit trail.

### 8.3 SIEM Integration

- No native SIEM connectors
- API-based log export possible
- Webhook integrations available
- Third-party apps for Splunk/Sentinel exist

---

## 9. Vendor Management

| Question | Response |
|----------|----------|
| Sub-processors | List available in DPA |
| Background checks | Yes - all employees |
| Security training | Annual required |
| Third-party audits | Covered by SOC 2 |
| Sub-processor notification | 30 days via email |

---

## 10. Contractual

| Item | Available |
|------|-----------|
| Data Processing Agreement | Yes - standard |
| Business Associate Agreement | No - not HIPAA certified |
| SLA | Yes - 99.95% uptime |
| Security Addendum | Yes - DPA covers |
| Insurance | Yes - cyber liability |

---

## Gaps & Considerations

### Security Gaps Identified

| Gap | Risk Level | Notes |
|-----|------------|-------|
| No HIPAA BAA | HIGH | Cannot store PHI |
| No FedRAMP | MEDIUM | No government compliance |
| No customer-managed keys | MEDIUM | Limited key control |
| Limited audit granularity | LOW | Less detail than enterprise |
| No FIDO2/security keys | LOW | Coming soon |

### Mitigation Recommendations

1. **HIPAA:** Do not store protected health information in HubSpot. Use for non-PHI business data only.

2. **Enhanced Monitoring:** Implement third-party security monitoring via API if detailed audit required.

3. **SSO Enforcement:** Enable SAML SSO and MFA for all users.

4. **Data Classification:** Implement policies to prevent sensitive data entry.

---

## Summary Assessment

**Security Posture: GOOD (with caveats)**

HubSpot demonstrates solid security practices for a B2B SaaS platform:
- SOC 2 Type II certified
- ISO 27001 certified
- Strong encryption in transit and at rest
- Modern infrastructure (AWS)
- Active security program

**Concerns for Meridian:**
- No HIPAA certification (relevant for healthcare clients)
- Less granular audit/permissions than enterprise CRM
- No customer-controlled encryption keys
- Limited data residency options

**Recommendation:** Approved for business data. NOT approved for PHI or highly regulated data.

---

*For additional information, visit trust.hubspot.com*
