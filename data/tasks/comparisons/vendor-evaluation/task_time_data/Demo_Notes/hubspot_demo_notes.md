# HubSpot Demo Notes
## Combined Team Feedback

**Date:** December 5, 2025  
**Attendees:** Amanda Foster (HS AE), James Park (HS SE), Sarah Chen, Mike Torres, Lisa Park (Marketing), Jennifer Park  
**Duration:** 90 minutes

---

## Overall Team Reactions

| Person | Role | Rating | One-Line Take |
|--------|------|--------|---------------|
| Sarah Chen | IT Director | 7/10 | "Surprisingly capable, some security gaps" |
| Mike Torres | VP Sales | 8/10 | "My team would actually use this" |
| Lisa Park | Marketing Director | 9/10 | "Finally, marketing and sales in one place" |
| Jennifer Park | Sales Manager | 8/10 | "Clean interface, easy pipeline" |

---

## Demo Flow

### 1. Platform Overview (15 min)
- Unified platform pitch - one database, multiple "Hubs"
- Free CRM base with paid Hubs for additional features
- Showed the contact record as "single source of truth"

**Impression:** Clean, modern, well-designed. Everything connects.

### 2. Sales Hub Deep Dive (30 min)

**Pipeline Management**
- Board view is DEFAULT (huge plus for Mike)
- Drag-and-drop deal stages
- Deal properties customizable without admin
- Inline editing - change value without opening deal
- Forecasting built into pipeline view

**Quote from Mike:** "This is what I wanted Salesforce to feel like"

**Activity Tracking**
- Email integration showed every email auto-logged
- Meeting scheduler (like Calendly, built-in)
- Call recording and transcription (with consent)
- Tasks sync with Google/Outlook calendar

**Sequences (Automated Outreach)**
- Multi-step email sequences for prospecting
- A/B testing built-in
- Automatic unenroll when reply received
- This replaces our need for Outreach.io potentially

**Mobile App**
- Fast, clean mobile experience
- Business card scanner
- One-tap calling with logging
- Offline mode available

### 3. Marketing Hub (20 min)

Lisa was extremely engaged during this section.

**Email Marketing**
- Professional email builder (drag-and-drop)
- Personalization tokens from CRM data
- Send time optimization
- A/B testing

**Automation**
- Visual workflow builder (vs. Pardot's clunky interface per Lisa)
- Lead nurturing sequences
- Lifecycle stage progression
- Internal notifications

**Lead Scoring**
- Engagement-based scoring
- Fit scoring based on properties
- Score thresholds trigger notifications

**Lisa's take:** "This is better than Mailchimp AND integrates with sales. We could consolidate tools."

### 4. Reporting (15 min)

**Standard Reports**
- Pre-built reports for common metrics
- Clean visualizations
- Attribution reporting for marketing

**Custom Reports**
- Report builder less complex than Salesforce
- Some limitations on cross-object reporting (needed Operations Hub)
- Dashboards are customizable and shareable

### 5. Service Hub Quick Look (10 min)

- Ticketing system shown briefly
- Knowledge base capabilities
- Customer portal
- Not as deep as dedicated support tools but "good enough" for our needs

---

## Technical Assessment (Sarah's Section)

### Security & Compliance

**Have:**
- SOC 2 Type II ✓
- ISO 27001 ✓
- GDPR compliant ✓
- SSO (SAML) ✓
- 2FA ✓
- Audit logs ✓

**Don't Have:**
- HIPAA certification ✗ (concerning for healthcare clients)
- FedRAMP ✗
- Field-level encryption (only at-rest and in-transit)

**Assessment:** Security is "good enough" for most business use but falls short if we have regulated clients.

### Integration

- Native integrations list is shorter than Salesforce but covers our needs
- Zapier fills gaps
- API is clean and well-documented
- Data sync (Operations Hub) is bidirectional with many tools

### Administration

- Self-service administration is MUCH easier
- Most changes don't require admin training
- Settings are logically organized
- Sandbox/test environment is available (Enterprise tier)

**Admin burden estimate:** 0.25 FTE vs. 0.5+ FTE for Salesforce

---

## Concerns Raised

### 1. Customization Limits
**Q (Sarah):** Can we create custom objects with complex relationships?
**A:** Yes, but there are some limits on relationships. Custom objects are relatively new (2023). Not as flexible as Salesforce.

### 2. Enterprise Scalability
**Q (Sarah):** How does performance hold at 500+ users?
**A:** "Most of our customers are under 500 users. We have larger customers but that's not our sweet spot." 

*Honest answer - appreciated but noted.*

### 3. Security Certifications
**Q (Sarah):** Timeline for HIPAA/healthcare compliance?
**A:** "It's on the roadmap but no committed date. We recommend a BAA with us and careful data handling for PHI."

*Not great. We have some healthcare clients.*

### 4. Reporting Depth
**Q (Mike):** Can I build complex sales activity reports?
**A:** Showed what's possible, but some advanced cross-object reports need Operations Hub Pro.

---

## Standout Positives

1. **Marketing + Sales alignment** - This is genuinely unified, not bolted together
2. **User experience** - Modern, intuitive, well-designed
3. **Sequences** - Could eliminate need for separate sales engagement tool
4. **Time-to-value** - They claim 6-8 weeks, seemed realistic based on demo complexity
5. **Transparent pricing** - What you see is what you get (mostly)

---

## Standout Concerns

1. **Security gaps** - No HIPAA is a real issue for us
2. **Enterprise maturity** - Platform is newer, still evolving
3. **Custom object limits** - May hit walls with complex data models
4. **"Growing pains" risk** - If we scale significantly, may outgrow

---

## Marketing Team Specific Feedback (Lisa)

"I've used Marketo, Pardot, and Mailchimp. HubSpot's Marketing Hub is the best user experience I've seen. The fact that it connects directly to sales pipeline with no integration needed is huge.

Current state: Marketing → Mailchimp → Manual handoff → Spreadsheet → Sales
HubSpot state: Marketing → Sales (same system)

**My vote is strongly for HubSpot.** The marketing capabilities alone would save us $15K/year in other tools plus countless hours of manual handoff."

---

## Sales Team Specific Feedback (Mike)

"This is the first CRM demo where I didn't immediately think 'my reps will hate this.' The mobile app is fast. The pipeline is visual. Email logging is automatic. 

My only concern is it might be TOO simple - we'll need to test whether it handles our specific workflow needs. But for adoption, this is a winner."

---

## Vendor Team Assessment

Amanda (AE) - Professional, not pushy. Asked good discovery questions. Felt like she actually wanted to fit our needs vs. just closing a deal.

James (SE) - Very knowledgeable. Answered technical questions honestly, including acknowledging limitations. Didn't try to spin weaknesses.

**Good vendor relationship experience.**

---

## Next Steps

- [ ] Security questionnaire (sent, awaiting response)
- [ ] Reference call with similar company (ideally with healthcare clients)
- [ ] Trial access for Mike's team to test actual workflows
- [ ] Marketing integration POC with Lisa
- [ ] Operations Hub demo for advanced reporting

---

*Compiled by Sarah Chen from team feedback*
