# Valuebound: Ideal Customer Profile (ICP)

Written from the point of view of a GTM engineer at Valuebound: **who should Valuebound sell to, and how do we find them automatically?**

Based on Valuebound's public website, scraped with Firecrawl on 5 November 2026 (homepage, services, case studies, careers, contact). Anything not stated on the site is marked **(assumption)**. Check those with the sales team before building on them.

## 1. What Valuebound sells

| Offer | What the buyer gets | Evidence |
|---|---|---|
| **Drupal migration and upgrades** | Move off an old Drupal version, or onto Drupal from another CMS, without breaking the business | Services page; case studies on Drupal 8 and Drupal 9 migrations |
| **Custom Drupal builds and integrations** | Websites, portals and commerce, connected to CRM, ERP, identity, search and analytics | Services page FAQ |
| **Drupal support, security and performance** | Ongoing maintenance, security updates, Core Web Vitals, accessibility | Services page |
| **Pharma MarTech** | HCP (doctor) engagement, CLM and eDetailing, compliance workflows, rural reach | Site metadata; 4 pharma case studies |
| **Intranets, LMS and employee experience** | Internal portals and learning platforms for large companies | Blog focus April to June 2026; intranet redesign testimonial from an IT Director |

**Core strength:** 15+ years of enterprise Drupal (they wrote a Drupal 8 book) and 60+ engagements, delivered from an offshore team in India at a lower cost than US or EU agencies **(assumption: lower cost isn't stated on the site, but it's typical for this delivery model)**.

## 2. The ICP in one sentence

> **Organisations with 500+ employees (assumption) in higher education, pharma and life sciences, publishing and media, or hi-tech that run a business-critical website or portal on Drupal (especially an outdated version) and need to migrate, integrate or stabilise it without a large in-house web team.**

## 3. Segments, in priority order

### Segment A: Enterprises on outdated Drupal (main segment)
- **Who:** any industry, but strongest in **publishing and media** (TIME Inc, Farm Journal Media, American Heritage) and **hi-tech** (VMware, Cypress Semiconductor, Mindtickle, Airmeet).
- **Trigger:** the site runs Drupal 7, 8 or 9, all now past end of life, or is behind on major upgrades. Drupal 7 support ended in January 2025, so every Drupal 7 site still live is overdue.
- **Pain:** security risk, broken modules, slow site, editors stuck with old workflows, and an upgrade that's too big for the internal team.
- **Why Valuebound wins:** a structured migration plan covering architecture, content migration, redirects, testing and release controls (services page), plus case studies proving it.

### Segment B: Higher education in the US
- **Who:** universities and colleges, plus education publishers and ed-tech firms.
- **Evidence:** 5 blog posts in May 2025 aimed at US higher ed (one names Pennsylvania); case studies on a 22,000-product higher-ed commerce platform and an LMS for live classrooms.
- **Pain:** the website is "the front door" for student recruitment; many sites, many editors, accessibility rules, and an LMS that has to integrate with other systems.
- **Why now:** higher-ed IT teams are stretched, and Drupal is very common in universities **(assumption, widely reported)**.

### Segment C: Pharma and life sciences
- **Two sub-segments:**
  1. **Global pharma** that needs one governed Drupal platform across many countries. One case study covers 80+ countries and 40% faster launches.
  2. **Indian pharma** that needs HCP engagement, CLM and eDetailing, and rural reach. There are 3 case studies for top Indian pharma brands, plus Eversana and Dr. Reddy's.
- **Pain:** compliance review slows every launch, regional sites drift apart, and field and digital channels are disconnected.

### Segment D: Large companies needing an intranet or LMS (emerging)
- **Who:** companies with thousands of staff across locations (assumption based on the blog's "5,000 employees across time zones" example).
- **Evidence:** blog posts from April to June 2026 on intranets and LMS; an intranet redesign testimonial.
- **Status:** a newer offer with less proof. Test it in small batches before scaling outreach.

## 4. Firmographics

| Attribute | Fit | Notes |
|---|---|---|
| **Employees** | 500 to 10,000+ (assumption) | The site says "enterprise" throughout. Smaller firms rarely have a Drupal estate worth migrating. |
| **Regions** | 1. **USA** 2. **India** 3. UK, EU and Middle East (secondary) | New York office and US higher-ed content; Indian pharma case studies; Landmark Group (Middle East) and Travelopia (UK) as logos |
| **Industries** | Higher ed, pharma and life sciences, publishing and media, hi-tech and SaaS, financial services | From the case-study filters: Software & Hi-Tech, Pharma Research, Ed-Tech, Software Utility, Financial Services |
| **Tech** | Runs Drupal, or plans to replatform onto it | Drupal is the centre of every service page |

## 5. Buyer personas (roles, not named people)

| Role | Cares about | Typical message angle |
|---|---|---|
| **CTO / VP Engineering** | Risk, security, team capacity | "Your Drupal 7 site is past end of life. Here's a migration plan that doesn't stop releases." |
| **Director of Digital / Head of Web** | Site speed, editor workflows, launch speed | "40% faster regional launches for a global pharma brand" |
| **CMO / Head of Digital Marketing** | Leads, SEO, campaign speed | Core Web Vitals and conversion |
| **CIO (higher ed)** | Accessibility, many sites, tight budget | Higher-ed migration case study |
| **Head of Digital / Commercial Excellence (pharma)** | HCP engagement, compliant launches | HCP omnichannel case studies |
| **IT Director / Head of Internal Comms** | Intranet adoption, onboarding | Intranet redesign testimonial |

## 6. Buying signals for the outbound engine

These replace the IT-management signals in `config/signals.yaml` if the engine is pointed at Valuebound's market. Every signal has an automatable source, as Step 2 requires.

| # | Signal | Source | Rule | First-guess weight |
|---|---|---|---|---|
| V1 | **Site runs Drupal** | Firecrawl: the page's `generator` meta tag (this is how we saw Valuebound's own site runs Drupal 11). Apollo technology data as backup. | Generator contains "Drupal" | **30** |
| V2 | **Outdated Drupal version** | Same generator tag | Drupal 7, 8 or 9 | **25** |
| V3 | **Hiring Drupal or web developers** | Apollo job postings, careers page via Firecrawl | Open role with "Drupal", "PHP", "web developer" or "CMS" in the title or description, in the last 60 days | **20** |
| V4 | **Slow or failing website** | Google PageSpeed Insights API (free) | Mobile performance score below 50 | **15** |
| V5 | **New digital leader** | Apollo people data (job title and start date only, no personal contact details stored) | New CTO, CDO, CIO or Head of Digital in the last 6 months | **10** |
| | **Total** | | | **100** |

**Filters (no points, in or out):**
- Industry is one of the five listed in section 4.
- 500+ employees (assumption; tune once real data comes in).
- Region: USA or India first, then UK, EU and the Middle East.

**Why V1 and V2 carry the most weight:** they come straight from the prospect's own website, so they're the most reliable signals and the easiest to check by hand in the 30-account audit. A site on Drupal 7 has a deadline that's already passed. That's the strongest "why now" Valuebound has.

## 7. Who is not a fit

- **Small businesses** (under about 100 staff) with simple marketing sites: deals are too small.
- **Other Drupal agencies**: they're competitors, not buyers.
- **Companies on a hosted website builder** (Wix, Squarespace) with no integration needs.
- **Companies that just finished a full replatform** in the last 12 months (assumption): no need for at least a year.

## 8. Open questions for the Valuebound sales team

1. What's the smallest deal size worth pursuing? This sets the real employee filter.
2. Which region closes best today: the USA or India?
3. Is the pharma MarTech offer sold only in India, or globally too?
4. Do non-Drupal migrations (for example WordPress or Sitecore to Drupal) close as well as Drupal upgrades?
5. Which past clients would agree to be referenced in outbound emails?

## 9. Sources

| Page | What it gave |
|---|---|
| https://www.valuebound.com/ | Services, industries, client logos, stats, Drupal 11 generator tag |
| https://www.valuebound.com/services (redirects to /services/drupal) | Full Drupal offer, integrations, FAQ |
| https://www.valuebound.com/case-study | Case-study industries; pharma case studies |
| https://www.valuebound.com/career | Delivery team, remote culture |
| https://www.valuebound.com/contact-us | Offices: New York, Bangalore, Indore |
