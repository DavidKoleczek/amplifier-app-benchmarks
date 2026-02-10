# Pipedrive Demo Notes
## Team Feedback

**Date:** December 8, 2025  
**Attendees:** Alex Rivera (Pipedrive AM), Sarah Chen, Mike Torres, Jennifer Park  
**Duration:** 60 minutes

---

## Overall Impressions

| Person | Role | Rating | One-Line Take |
|--------|------|--------|---------------|
| Sarah Chen | IT Director | 5/10 | "Too lightweight for our needs" |
| Mike Torres | VP Sales | 9/10 | "THIS is what a CRM should feel like" |
| Jennifer Park | Sales Manager | 8/10 | "Love the simplicity, worried about scale" |

**The divergence in ratings is notable.** Sales loves it, IT is concerned.

---

## Demo Highlights

### Pipeline Management (Mike's Focus)

**What we saw:**
- Visual pipeline as THE primary interface
- Drag-and-drop deals between stages
- Deal rotting indicators (shows deals going stale)
- Quick edit everything inline
- Multiple pipelines supported

**Mike's reaction:** "This is exactly how I think about sales. Visual. Simple. Fast."

**Time test:** Mike asked to update a deal stage. Took 2 seconds (literally drag-and-drop). Same action in Salesforce demo was 15+ seconds.

### Contact Management

- Clean contact cards with full history
- Timeline shows all interactions
- Smart data enrichment (pulls LinkedIn, company info)
- Duplicate detection works well
- Contact import was demonstrated - straightforward

### Email Integration

- Full two-way sync demonstrated (Gmail)
- Every email auto-logged to contact
- Email tracking (opens, clicks)
- Templates available
- One caveat: Bulk email limit is 250/day

### Activity Management

- Activities tied to deals and contacts
- Reminder system is simple but effective
- Calendar integration (Google, Outlook)
- No native call recording (would need add-on)

### Mobile App

- **Lightning fast** - noticeably quicker than both Salesforce and HubSpot
- Clean interface matches desktop
- Offline mode genuinely works
- Call logging in 2 taps

**Jennifer's comment:** "My reps would actually pull this out after a meeting."

### Reporting

- Basic pipeline reports look good
- Forecast view is simple but functional
- Activity reports available
- Custom reports... limited

**Here's the gap:** When Sarah asked about complex reporting (multi-dimensional, cross-pipeline analysis), Alex was honest that Pipedrive isn't built for that.

---

## Technical Assessment (Sarah)

### The Good

- Cloud-native, modern architecture
- API is clean and well-documented
- Uptime has been solid historically
- GDPR compliant
- Data export is straightforward

### The Concerning

**Security Certifications:**
- SOC 2 Type II: "In progress" (expected Q2 2026)
- ISO 27001: "Planned for 2026"
- HIPAA: Not available, no BAA
- FedRAMP: No

**This is a significant gap.** For a company our size with some enterprise clients, the lack of SOC 2 today is concerning.

**SSO/Enterprise:**
- SAML SSO only on Enterprise tier
- Audit logs only on Enterprise tier
- No field-level permissions (all or nothing)
- No sandbox environment

**Integration Limits:**
- API rate limits (200 calls/sec)
- Native integrations: 400 vs. 3000+ for Salesforce
- No native marketing automation
- No native service/ticketing

### My IT Perspective

Pipedrive is a great sales tool. But it's ONLY a sales tool. We'd need:
- Separate marketing platform (keeping Mailchimp)
- Separate service desk (if we need ticketing)
- Third-party tools for advanced reporting
- Accept security gaps until certifications complete

**TCO may not be as low as it appears** when you add these tools back.

---

## Sales Team Assessment (Mike)

### Why I Like It

1. **Speed:** Everything is fast
2. **Visual:** Pipeline-centric design is how salespeople think
3. **Low friction:** Updating deals is instant
4. **Mobile:** Best mobile experience we've seen
5. **Adoption:** My team would use this (seriously)

### Why I'm Hesitant

1. **No marketing integration:** Lisa won't be able to see lead sources
2. **Basic reporting:** I'll still need spreadsheets for complex analysis
3. **Perceived as "small business":** Optics with board?
4. **Scale uncertainty:** What happens at 300, 500 users?

### My Honest Take

If I could only buy Pipedrive and knew we'd stay at 150 users, I'd pick it in a heartbeat. The user experience is simply better.

But we're a growing company. And when Sarah says we need SOC 2 for enterprise deals... I have to listen. 

**Pipedrive is my heart choice. Not sure if it's my head choice.**

---

## Limitations Acknowledged by Vendor

Credit to Alex for being honest:

1. "We're not trying to be Salesforce. We do pipeline management extremely well."
2. "If you need deep marketing automation, you'll need another tool."
3. "Our security certifications are coming but we don't have them today."
4. "For complex enterprises, we may not be the right fit."

This transparency is refreshing but confirms our concerns.

---

## Feature Gap Analysis

| Requirement | Pipedrive | Notes |
|-------------|-----------|-------|
| Pipeline management | ✓ Excellent | Best in class |
| Contact management | ✓ Good | Clean and simple |
| Email integration | ✓ Good | Bulk limits exist |
| Forecasting | ✓ Basic | Functional |
| Mobile CRM | ✓ Excellent | Best we've seen |
| Marketing automation | ✗ Basic only | Need separate tool |
| Service/support | ✗ No | Need separate tool |
| Advanced reporting | ✗ Limited | Gap |
| Security certs | ✗ In progress | Gap |
| Enterprise controls | △ Enterprise tier only | Extra cost |
| API/Integrations | △ Adequate | Not as robust |

---

## Cost Reality Check

**What Pipedrive quoted:** ~$95K Year 1

**What we'd actually need:**
- Pipedrive Professional: $90,370
- Upgrade to Enterprise (for SSO, audit): +$44,450
- Mailchimp Pro (marketing): +$15,000
- Help Scout (if we need ticketing): +$8,000
- Estimated integration work: +$5,000

**Realistic Total:** ~$163,000

Still cheaper than Salesforce, but not the "fraction of the cost" it appears at first glance.

---

## Questions We Asked

**Q:** When will SOC 2 be complete?
**A:** "Q2 2026 is the target. We're in the audit process now."

**Q:** Can we get it in writing that SOC 2 is coming?
**A:** "I can provide a letter from our security team with timeline."

**Q:** What's your largest customer (user count)?
**A:** "We have customers over 1,000 users but our sweet spot is 50-300."

**Q:** If we outgrow Pipedrive, how hard is data export?
**A:** "Full data export available. We don't lock you in."

---

## Recommendation Summary

**For sales team adoption:** Pipedrive is #1
**For IT/security requirements:** Pipedrive is #3
**For marketing integration:** Pipedrive is #3

**Overall position:** Great sales tool, not yet an enterprise platform.

---

## Next Steps

- [ ] Request SOC 2 timeline letter
- [ ] Reference call with 150+ user customer
- [ ] Price out realistic TCO with additional tools
- [ ] Trial access for sales team
- [ ] Decision: Is simplicity worth the gaps?

---

*Notes compiled by Sarah Chen*
