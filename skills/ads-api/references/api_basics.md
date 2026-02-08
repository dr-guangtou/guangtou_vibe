# ADS API Basics

## Sources
- ADS API README: https://github.com/adsabs/adsabs-dev-api/blob/master/README.md
- ADS API overview links: https://ui.adsabs.harvard.edu/help/api/

## Authentication

- API host: `https://api.adsabs.harvard.edu`
- Provide token in header:
  - `Authorization: Bearer <ADS_API_TOKEN>`
- Obtain token from ADS account settings.

## Core Search Endpoint

- Endpoint: `GET /v1/search/query`
- Common query params:
  - `q`: ADS query string
  - `fl`: comma-separated returned fields
  - `rows`: page size
  - `start`: offset for pagination
  - `sort`: deterministic ordering when needed

## Minimal cURL Pattern

```bash
curl -s "https://api.adsabs.harvard.edu/v1/search/query?q=star&fl=title,bibcode&rows=5" \
  -H "Authorization: Bearer $ADS_API_TOKEN"
```

## Reliability Notes

- Handle HTTP `429` with retry/backoff.
- Handle `5xx` with bounded retries.
- Log full request parameters for reproducibility.
