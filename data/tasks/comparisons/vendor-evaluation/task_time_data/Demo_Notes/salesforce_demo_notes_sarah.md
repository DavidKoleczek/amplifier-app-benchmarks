# Salesforce Demo Notes
## Sarah Chen - IT Director

**Date:** December 4, 2025  
**Attendees:** Marcus Thompson (SF AE), Diana Chen (SF SE), Sarah Chen, Mike Torres, Jennifer Park, David Kim  
**Duration:** 2 hours

---

## Overall Impression

Comprehensive and powerful, but complex. This is clearly enterprise-grade software with capabilities far beyond what we strictly need. The question is whether the additional capability justifies the cost and complexity.

**My rating: 7/10** (strong technical foundation, concerns about complexity)

---

## Technical Assessment

### Architecture & Infrastructure

**Positives:**
- Multi-tenant architecture is mature and proven
- 99.99% uptime SLA is industry-leading (they showed historical data)
- Multiple data center regions available
- Hyperforce migration path for future data residency needs
- API is robust - REST, SOAP, Bulk, Streaming options

**Concerns:**
- Complexity of the platform is significant
- Will need dedicated admin (at least 0.5 FTE) to manage properly
- Customizations in Apex require specialized skills
- Sandbox/deployment process adds overhead

### Security & Compliance

**Very Strong:**
- SOC 1, SOC 2, ISO 27001, 27017, 27018 - full suite
- HIPAA with BAA available (we may need this for healthcare clients)
- FedRAMP High on Government Cloud
- Shield encryption available for sensitive fields
- Comprehensive audit trail and event monitoring

**This is the clear leader on security certifications.** No other vendor in our evaluation comes close.

### Integration Capabilities

**Pros:**
- MuleSoft ownership means native integration platform
- 3,000+ AppExchange apps
- SSO options are comprehensive
- Good Microsoft 365 integration demonstrated

**Cons:**
- Some integrations are paid add-ons
- MuleSoft is powerful but adds another platform to manage
- ERP integration demo was conceptual, not actual

### Administration

**Showed us:**
- Permission sets and profiles (granular but complex)
- Delegated administration capabilities
- Sandbox management
- Change sets for deployment

**Concerns:**
- Admin console is overwhelming - many settings buried in unexpected places
- Permission model is powerful but has significant learning curve
- Quoted 40 hours admin training minimum

---

## Demo Feedback by Feature

### Sales Pipeline
- Visual pipeline needs customization to look good
- Kanban view available but not default
- Opportunity management is comprehensive
- Path feature (guided selling) is nice

### Reporting
- Report builder is powerful but not intuitive
- Dashboards look dated compared to modern tools
- Tableau CRM (Einstein Analytics) looks great but is extra cost
- Real-time wasn't really real-time (some delay noted)

### Mobile
- App is functional but heavy
- Offline support available but setup required
- Push notifications need configuration

### AI/Einstein
- Lead scoring demo was impressive
- Opportunity insights were helpful
- Einstein GPT mentioned but not demonstrated (still rolling out)

---

## Questions Raised

1. **Q:** What's the actual implementation timeline for a company our size?
   **A:** 16 weeks is "typical" but acknowledged 20+ weeks happens frequently with complex requirements.

2. **Q:** Can we start with Sales Cloud only and add other clouds later?
   **A:** Yes, but integration is better if planned together. Pricing is also better bundled.

3. **Q:** What happens if we exceed API limits?
   **A:** Calls get throttled, not blocked. Can purchase additional capacity.

4. **Q:** Data export options?
   **A:** Weekly data export included, real-time via API. Full data portability.

---

## Red Flags

1. **Implementation complexity** - Their 16-week timeline assumes a lot goes smoothly
2. **Hidden costs** - Several features we assumed included are add-ons (Shield, additional storage, some Einstein features)
3. **Admin burden** - Will need dedicated resource or risk underutilization
4. **User adoption risk** - Complex UI may face resistance from sales team

---

## IT Recommendation

From a pure IT/infrastructure perspective, Salesforce is the most robust option:
- Best security certifications
- Most mature platform
- Lowest technical risk

However, the total cost of ownership is concerning:
- License costs + implementation + ongoing admin + training
- May be overbuilt for our current needs (150 users)

**My recommendation:** Salesforce is the "safe" enterprise choice but we should seriously evaluate if we need this level of capability. If we're confident in significant growth, it makes sense. If we're optimizing for the next 2-3 years, it may be overkill.

---

## Follow-up Items

- [ ] Request reference call with similar-sized company (not enterprise)
- [ ] Get clarification on Shield encryption pricing
- [ ] Understand sandbox costs (are they included?)
- [ ] Request data migration sample with our actual data
- [ ] IT security questionnaire completion (sent, awaiting response)

---

*Notes by Sarah Chen, IT Director*
