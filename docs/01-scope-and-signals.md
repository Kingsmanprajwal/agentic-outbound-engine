# Agentic Outbound Engine: Step 1, Scope and Signals

Status: draft. Written before any build work starts.

## 1. Target market

**Region:** EMEA, starting with the UK and the EU.

**Who:** IT-managed SMBs and MSPs (managed service providers).

**Working definition:** Companies with 50 to 500 employees, based in the UK or an EU country, that either run a small in-house IT team or buy IT support from an MSP. MSPs themselves are in scope because they manage devices and access for many small clients at once.

**Why this segment:** Small IT teams carry a heavy load of device, identity and access management and rarely have tooling to match. A segment this narrow also means every account on the list can be explained, and the scoring has something concrete to test against.

**Note:** This is a segment I chose to demonstrate the pattern. It is not any employer's actual ICP.

## 2. Signals

A signal is a fact I can collect automatically that suggests an account needs IT management tooling now. Each one needs a named source, or it doesn't go in.

| # | Signal | Why it matters | Source | First-guess weight |
|---|--------|----------------|--------|--------------------|
| 1 | Headcount between 50 and 500 | Big enough to need tooling, small enough to lack a large IT team | Apollo | 20 |
| 2 | Hiring IT admin, sysadmin or helpdesk roles | Active IT growth or pain | Firecrawl on careers pages | 30 |
| 3 | Microsoft-heavy environment | Points to identity and device management needs | Job posts, Apollo tech data | 20 |
| 4 | Remote or multi-location workforce | Harder to manage devices and access | Careers pages, company site | 15 |
| 5 | Recent funding or headcount growth | Budget and a growing user base | Apollo | 15 |

Weights add up to 100. They are a first guess and will be revised in the scoring step once I can compare them against real accounts. Weights will live in a config file, not in code.

If a signal turns out to be unreliable to collect, it gets dropped rather than kept with a shaky value.

## 3. Goal

> Cut manual research per account from 3 hours to under 2 minutes, with at least 90% field-level accuracy on a 30-account manual audit.

**Baseline:** 3 hours of manual research per account, based on my own experience of doing this by hand.

## 4. Out of scope

- Sending emails automatically. Every message waits for human approval.
- Regions outside the UK and EU.
- Tools that need a paid licence I don't have, such as Marketo and Gong Engage.
- Replacing a full sales engagement platform.

## 5. Done when

- This page is complete, with the baseline filled in.
- The target market, signals and goal are agreed before any workflow is built.
