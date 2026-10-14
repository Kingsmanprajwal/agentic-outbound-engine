# Agentic Outbound Engine: Build Guide

A step-by-step guide to building the project and having proof of it at the end. Plan for about 10 days at 2 to 3 hours a day.

Free tiers and limits change, so check each tool's current plan before you rely on it.

## The stack

| Job | Tool | Cost | Why this one |
|-----|------|------|--------------|
| CRM | Salesforce Developer Edition | Free | You already know Salesforce, and it's a real CRM |
| Account sourcing | Apollo (free plan) | Free | Company search and basic enrichment. API access can be limited on free plans, so have a CSV fallback |
| Hiring-signal scraping | Firecrawl | Free credits | Turns careers pages into clean text |
| Workflow orchestration | n8n (self-hosted with Docker, or the cloud trial) | Free / trial | You've used it, and it's the closest match to Clay-style workflows |
| AI research and drafting | Claude API (Anthropic Console) | Pay as you go, a few dollars | Use a smaller model for bulk research and a larger one for drafting |
| MCP server | Python, the official `mcp` SDK, `simple-salesforce`, `pydantic` | Free | Python is quick to write, and pydantic gives you strict output validation |
| Email drafts | Gmail (n8n Gmail node) | Free | Saves drafts so nothing sends on its own |
| Code and docs | GitHub | Free | Your proof of work |
| Demo video | Loom or OBS | Free | A 2 to 3 minute walkthrough |
| Diagram | Mermaid (in the README) or draw.io | Free | Renders directly on GitHub |

## Ground rules

- **Keep secrets out of Git.** Put API keys in a `.env` file, add `.env` to `.gitignore`, and commit a `.env.example` with blank values.
- **Use a sandbox.** Salesforce Developer Edition only. Never point this at your employer's org.
- **Nothing sends automatically.** Drafts only, with a human approval step. This is also the right answer on GDPR and PECR, since you're working with UK and EU contacts.
- **Use company-level data.** Skip personal data about individuals for the demo, and don't store anything you wouldn't want in a public repo.

## Repo structure

```
agentic-outbound-engine/
  README.md
  .env.example
  .gitignore
  docs/
    01-scope-and-signals.md
    02-build-guide.md
    architecture.md
    accuracy-audit.md
  config/
    scoring_weights.json
  n8n/
    workflows/          (exported workflow JSON files)
  mcp_server/
    server.py
    tools/
    schemas.py
  data/
    sample_accounts.csv
  demo/
    screenshots/
```

## Phase 1: Foundations (day 1)

1. Create the GitHub repo and clone it locally. Add the folder structure above and push the first commit.
2. Sign up for a Salesforce Developer Edition org, Apollo, Firecrawl, and the Anthropic Console.
3. Install Docker and start n8n with the official Docker image. Open it in your browser and confirm it runs.
4. Create `.env` and `.gitignore` before you add any keys.

**Proof to capture:** a screenshot of the empty repo structure, and one of n8n running.

## Phase 2: Salesforce setup (day 1 to 2)

1. On Account, add custom fields: `ICP_Score__c`, `Signal_Summary__c`, `AI_Research_JSON__c`, `Confidence__c`, `Approval_Status__c` (Pending, Approved, Rejected), `Draft_Email__c`.
2. Add a validation rule so `ICP_Score__c` stays between 0 and 100.
3. Turn on a duplicate rule and matching rule on Account (by name and website).
4. Create a connected app or use a security token with the `simple-salesforce` library, and store the credentials in `.env`.
5. Create a list view called "Pending Review".

**Proof to capture:** screenshots of the custom fields, the validation rule and the Pending Review list view.

## Phase 3: Source accounts (day 2)

1. In Apollo, filter for companies in the UK and the EU countries you chose, with 50 to 500 employees, in IT services, professional services or SaaS.
2. Export 50 to 100 companies. If the API isn't available on your plan, export a CSV and read it in n8n.
3. Save the raw file in `data/` as `sample_accounts.csv`. Keep only company-level fields: name, domain, headcount, country, industry.

**Proof to capture:** the CSV (company data only), and a note on how many accounts you pulled.

## Phase 4: Enrichment and dedupe in n8n (day 3 to 4)

Build one workflow with these stages:

1. **Ingest:** read the CSV or call the Apollo API.
2. **Normalise:** lowercase domains, strip `www.` and trailing slashes, trim company names.
3. **Dedupe:** query Salesforce by domain. If the account exists, skip it or update it. If not, continue.
4. **Waterfall enrichment:** try Apollo first. If a field comes back empty, try a second source, for example scraping the company site with Firecrawl. Stop at the first value you find.
5. **Hiring signal:** use Firecrawl on the careers page and keep the text of any IT admin, sysadmin or helpdesk roles.
6. **Error handling:** add an error workflow that logs failures, with a retry on rate limits. Use the Error Trigger node.

Export the workflow JSON into `n8n/workflows/`.

**Proof to capture:** a screenshot of the workflow canvas, a run with a deliberate failure and the retry, and the exported JSON in the repo.

## Phase 5: Research with Claude (day 4 to 5)

1. Send each account's scraped context to the Claude API with a system prompt that asks for JSON only.
2. Define the output schema in `mcp_server/schemas.py` using pydantic: `what_they_do`, `tech_stack`, `hiring_signals`, `pain_point_hypothesis`, `confidence` (0 to 1).
3. Validate every response against the schema. If it fails validation, retry once. If it still fails, mark the row "needs review" and do not write it to Salesforce.
4. Route anything with confidence below your threshold (start with 0.6) to the Pending Review view instead of auto-writing.
5. Use a smaller model for this bulk step to keep costs down, and record the cost per account.

**Proof to capture:** the schema file, a valid response, a rejected response, and a cost-per-account figure.

## Phase 6: Score and prioritise (day 5)

1. Put your weights from Step 1 in `config/scoring_weights.json`.
2. Write a small function that reads each signal, applies the weights and returns a score from 0 to 100, plus a one-line reason for each point contribution.
3. Write the score and reason back to Salesforce.
4. Sort the accounts and look at the top 10 yourself. If the ranking feels wrong, change the weights in the config file, not in code.

**Proof to capture:** the weights file, a ranked list, and one example of the reasons behind a single score.

## Phase 7: Draft outreach (day 6)

1. For the top accounts, call Claude with the research JSON and ask for a short email (under 100 words) that refers to one specific signal.
2. Save the result in `Draft_Email__c` and as a Gmail draft through the n8n Gmail node.
3. Set `Approval_Status__c` to Pending. Nothing moves forward until you change it by hand.

**Proof to capture:** 3 sample drafts and the Pending status in Salesforce.

## Phase 8: The MCP server (day 6 to 8)

1. Install the `mcp` Python SDK and write `mcp_server/server.py`.
2. Add **read** tools: `search_accounts`, `get_account_context`, `score_account`.
3. Add **write** tools: `draft_outreach` and `push_to_crm`. `push_to_crm` must refuse to run unless the account's approval status is Approved.
4. Keep responses small. Return only the fields Claude needs (name, domain, score, top signals), not the whole record. Note the token difference in the README.
5. Connect the server to Claude (Claude Desktop or Claude Code) through its MCP configuration and test a single prompt such as "Find the top 5 pending accounts and draft outreach for the first one."
6. Add a simple audit log: every tool call writes a line with the time, tool name and account id.

**Proof to capture:** the tool list, a screenshot of the single-prompt run, the approval gate refusing a write, and a sample of the audit log.

## Phase 9: Measure it (day 9)

1. Pick 30 accounts at random.
2. For each, check the system's output against what you find by hand: headcount, tech stack, hiring signal, pain point. Mark each field right or wrong.
3. Calculate field-level accuracy and put the table in `docs/accuracy-audit.md`.
4. Record these numbers: time per account before and after, the share of rows sent to review, cost per account.
5. Compare against your goal from Step 1. If you missed it, say so and write down why. A missed target explained honestly is worth more than a number that looks too good.

**Proof to capture:** the audit table and the before-and-after numbers.

## Phase 10: Package it (day 10)

1. Write the README: one paragraph on what it does, the architecture diagram (Mermaid), the setup steps, and the results from Phase 9.
2. Add a "Limitations" section: no Marketo or Gong Engage, a sandbox only, and drafts only.
3. Record a 2 to 3 minute demo: the problem, the n8n flow, the MCP run, the approval gate, the numbers.
4. Pin the repo on your GitHub profile and link it from your resume and portfolio.
5. Only add resume bullets for things you built, with numbers you measured.

## Quick checklist

- [ ] Repo created, `.env` ignored
- [ ] Salesforce fields, validation rule and duplicate rule in place
- [ ] 50 to 100 accounts sourced
- [ ] n8n workflow exported with error handling
- [ ] Claude research returns validated JSON
- [ ] Scoring weights in config, reasons attached
- [ ] Draft emails saved, nothing sent
- [ ] MCP server with read and write tools and an approval gate
- [ ] 30-account audit completed
- [ ] README, diagram and demo video done
