# A/B Test Results: Landing Page Variants

**Test Name:** Spring Launch Landing Page Optimization  
**Test Period:** April 7 - May 10, 2025  
**Test Owner:** Marcus Webb  
**Status:** COMPLETED - Results Disputed

---

## Test Overview

Tested two landing page variants to optimize form completion rate.

**Control (Version A):** Original design with feature-focused hero
**Treatment (Version B):** Redesigned with testimonial-led hero + simplified form

## Traffic Split

| Variant | Sessions | % Split |
|---------|----------|---------|
| Version A | 4,234 | 49.8% |
| Version B | 4,267 | 50.2% |
| **Total** | **8,501** | 100% |

**Note:** Targeting was 50/50 but slight imbalance due to caching issues in first 48 hours.

## Primary Metric: Form Completion Rate

| Variant | Form Starts | Completions | Rate |
|---------|-------------|-------------|------|
| Version A | 1,058 | 614 | 58.0% |
| Version B | 1,089 | 697 | 64.0% |
| **Difference** | | | **+6.0 pp** |

**Relative Lift:** +10.3%

## Statistical Significance

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| p-value | 0.087 | 0.05 | NOT SIGNIFICANT |
| Confidence | 91.3% | 95% | BELOW THRESHOLD |
| Sample Size | 8,501 | 12,000 (recommended) | UNDERPOWERED |

### ⚠️ IMPORTANT CAVEAT

**This test did NOT reach statistical significance.**

The 91.3% confidence level means there's an 8.7% chance the observed difference is due to random variation, not a true effect. Industry standard requires 95% confidence.

### Why Sample Size Was Limited

1. **GA Tracking Outage (April 11-24):** Lost ~14 days of data during outage
2. **Campaign Timeline:** Test had to conclude with campaign end
3. **Original Plan:** 6-week test, only got ~4 weeks of clean data

## Secondary Metrics

| Metric | Version A | Version B | Diff | Significant? |
|--------|-----------|-----------|------|--------------|
| Bounce Rate | 38.2% | 35.8% | -2.4pp | No (p=0.12) |
| Time on Page | 2:34 | 2:51 | +17s | Yes (p=0.03) |
| Scroll Depth | 62% | 71% | +9pp | Yes (p=0.02) |
| MQL to SQL Rate | 41% | 39% | -2pp | No (p=0.45) |

## Qualitative Observations

**Version B Strengths:**
- Users spent more time reading testimonials
- Higher scroll depth suggests more engagement
- Simpler form reduced abandonment

**Version B Concerns:**
- Slightly lower MQL-to-SQL rate (not significant, but worth monitoring)
- Sales team feedback: "Leads from new page seem less informed about features"

## Disputed Interpretation

### Marketing Team (Jennifer Chen, CMO) Position:
> "The 10% lift is meaningful even at 91% confidence. Combined with the significant improvements in time-on-page and scroll depth, we should roll out Version B. Waiting for 95% confidence is academic perfectionism."

### Data Team (Marcus Webb) Position:
> "We can't claim Version B is better with only 91% confidence. The MQL-to-SQL dip is concerning - we might be getting more form fills but lower quality leads. Recommend extending test or running follow-up."

### Finance Team (Tom Rodriguez, CFO) Position:
> "I need to know if we're making decisions based on real data or hope. What's the cost of being wrong here?"

## Recommendation

**For the campaign recap presentation:**

1. Present results with appropriate caveats
2. Note the test was underpowered due to tracking outage
3. Show directional findings but avoid claiming "Version B won"
4. Recommend follow-up test in next campaign with proper sample size

**Suggested language:**
> "A/B test showed promising results for Version B (+10.3% form completion), though the test was cut short by the tracking outage and did not reach statistical significance. Recommend continued testing."

---

## Appendix: Test Configuration

**Tool:** Optimizely  
**Allocation:** Cookie-based, 50/50  
**Exclusions:** Internal IPs, bot traffic  
**Goal:** Form submission event  

**Version A URL:** /spring-launch?v=a  
**Version B URL:** /spring-launch?v=b  

Screenshots available in Creative_Assets/landing_page_screenshots/
