# Agentic Outbound Engine

An outbound research engine for IT-managed SMBs and MSPs in the UK and EU. It collects buying signals for each account, scores them, and drafts outreach that waits for a person to approve it before anything is sent.

**Goal:** cut manual research per account from 3 hours to under 2 minutes, with at least 90% field-level accuracy on a 30-account manual audit.

## Planning documents

| Step | Document | Status |
|---|---|---|
| 1. Scope and signals | [docs/01-scope-and-signals.md](docs/01-scope-and-signals.md) | Draft |
| 2. Build guide | [docs/02-build-guide.md](docs/02-build-guide.md) | Reference |
| 3. Signals and weights | [docs/03-signals-and-weights.md](docs/03-signals-and-weights.md) | Draft |

## Build progress

Follows the 10 phases in the [build guide](docs/02-build-guide.md).

| Phase | What | Status |
|---|---|---|
| 1 | Foundations: repo, sign-ups, n8n running, `.env` | In progress |
| 2 | Salesforce setup | Not started |
| 3 | Source accounts | Not started |
| 4 | Enrichment and dedupe in n8n | Not started |
| 5 | Research with Claude | Not started |
| 6 | Score and prioritise | Not started |
| 7 | Draft outreach | Not started |
| 8 | MCP server | Not started |
| 9 | Measure it | Not started |
| 10 | Package it | Not started |

## Ground rules

- API keys live in `.env`, which Git ignores. Copy `.env.example` to `.env` to start.
- Salesforce Developer Edition only, never an employer org.
- Nothing sends automatically. Every email is a draft that waits for human approval.
- Company-level data only.
