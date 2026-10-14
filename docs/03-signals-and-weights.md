# Agentic Outbound Engine: Step 2, Signals and Weights

Status: draft. Replaces the first-guess signal table in [Step 1](01-scope-and-signals.md).

## 1. Rule for picking signals

A signal goes in only if it can be collected automatically from a named source, with a clear yes/no rule. If a signal can't be collected reliably, it makes the score look more precise than it is, so it gets dropped.

## 2. Decision

Four signals are scored. Headcount moves out of the score and becomes a filter.

| Signal | Decision | Why |
|---|---|---|
| Headcount band (50 to 500) | **Filter, not scored** | Every account on the list already passes it, because it defines the target market. Scoring it would add the same 20 points to every account and change no ranking. |
| Hiring IT admin, sysadmin or helpdesk roles | **Scored** | Strongest sign of current IT pain. Two sources that check each other. |
| Microsoft-heavy stack | **Scored** | Apollo technographics are collected automatically and backed up by job-post text. |
| Recent funding or headcount growth | **Scored** | Apollo has both. Many SMBs never raise funding, so headcount growth also counts. |
| Remote or multi-location workforce | **Scored, on probation** | Sources are weaker. It stays only if it passes the reliability test in section 5. |

## 3. Signal definitions

Every signal is binary: an account either gets the full points or none. That keeps every score explainable during the 30-account audit. Graded scoring can come in Step 6 if the data supports it.

### Filter: headcount band

- **Rule:** the account has 50 to 500 employees and its headquarters is in the UK or an EU country.
- **Source:** Apollo employee count and HQ location.
- **If missing:** the account is excluded, not guessed.

### S1. Hiring IT admin, sysadmin or helpdesk roles: 40 points

- **Rule:** at least one open role posted in the last 60 days with a title matching the IT role list, for example "IT administrator", "systems administrator", "sysadmin", "IT support", "helpdesk", "service desk", "desktop support", "IT manager" or "infrastructure engineer".
- **Primary source:** Apollo active job postings, filtered by job title.
- **Confirmation source:** Firecrawl scrape of the company careers page.
- **Note for MSPs:** helpdesk hiring at an MSP means its client base is growing, which still counts.

### S2. Microsoft-heavy stack: 25 points

- **Rule:** Apollo shows at least two Microsoft identity, device or workplace technologies, such as Microsoft 365, Azure, Entra ID / Azure AD, Intune or Microsoft Teams, **or** an open IT role mentions Microsoft 365, Azure AD / Entra, Intune or Active Directory.
- **Sources:** Apollo technology data, then job-post text from S1.

### S3. Recent funding or headcount growth: 20 points

- **Rule:** a funding round in the last 18 months, **or** headcount growth of at least 10% over the last 12 months.
- **Source:** Apollo funding data and headcount growth.

### S4. Remote or multi-location workforce: 15 points (on probation)

- **Rule:** open roles in two or more distinct locations, **or** roles marked remote or hybrid, **or** the company site lists two or more offices.
- **Sources:** Apollo job locations, then the careers page and company site via Firecrawl.

## 4. Weights

| Signal | Points | Reason for the rank |
|---|---|---|
| S1. Hiring IT roles | 40 | Most direct sign of pain right now, and the easiest to verify by hand |
| S2. Microsoft-heavy stack | 25 | Shows fit with identity and device management, but says nothing about timing |
| S3. Funding or growth | 20 | Shows budget and a growing user base, but is indirect |
| S4. Remote or multi-location | 15 | Real pain, but the weakest source |
| **Total** | **100** | |

These are first guesses. They get revised in Step 6, after the scores are compared against real accounts. The weights live in [`config/signals.yaml`](../config/signals.yaml) (moves to `config/scoring_weights.json` in Phase 6), not in code.

Changes from Step 1:
- Headcount went from 20 points to a filter.
- Those 20 points moved to IT hiring (+10), the Microsoft stack (+5) and funding or growth (+5).
- Remote or multi-location kept its 15 points but is on probation.

## 5. Reliability test

Run on the 30-account audit set before any scoring is trusted. For each signal:

- **Coverage:** the source returns a usable value for at least 80% of accounts.
- **Accuracy:** the automatic yes/no matches a manual check for at least 90% of accounts.

A signal that fails either test is dropped. Its points are spread across the remaining signals in proportion to their weights. S4 is the most likely to fail. If it does, the engine runs on three signals.

## 6. Done when

- The four signals, the headcount filter and the weights are agreed.
- `config/signals.yaml` matches this page.
- The reliability test is scheduled to run on the 30-account audit set.
