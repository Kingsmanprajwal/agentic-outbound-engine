# n8n workflows

| File | What it does |
|---|---|
| `01-source-and-dedupe.json` | Pulls companies from Apollo, cleans the domains, skips any already in Salesforce, and creates the new ones as Accounts |

## 01 Source and dedupe accounts

```
Start → Search settings → Apollo company search → Normalise companies
      → Existing Salesforce websites → Keep only new accounts → Create Salesforce account
```

### Credentials it needs (created in n8n, never in this repo)

| Node | n8n credential type | Values |
|---|---|---|
| Apollo company search | **Header Auth** | Name `x-api-key`, Value: your Apollo API key |
| Existing Salesforce websites, Create Salesforce account | **Salesforce OAuth2 API** | Client ID and Client Secret from a Salesforce External Client App |

### Salesforce External Client App settings

- Callback URL: `http://localhost:5678/rest/oauth2-credential/callback`
- OAuth scopes: **Full access (full)** and **Perform requests at any time (refresh_token, offline_access)**
- Require PKCE: **on** (n8n uses the PKCE grant)

### Notes

- Each run uses 1 Apollo credit per page (25 companies by default). Change the filters in the **Search settings** node.
- If Apollo's API is locked on your plan, the Apollo node returns 403. The CSV fallback comes next.
- Create Salesforce account continues on error, so one rejected company (for example, blocked by the duplicate rule) doesn't stop the rest. Check its output for errors after each run.
