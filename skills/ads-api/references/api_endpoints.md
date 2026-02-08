# ADS API Endpoints and Scope

## Sources
- ADS API docs entrypoint: https://ui.adsabs.harvard.edu/help/api/api-docs.html
- ADS API OpenAPI announcement: https://blog.adsabs.harvard.edu/2018/06/21/ads-api-now-with-openapi-docs/
- ADS API overview page: https://ui.adsabs.harvard.edu/help/api/

## Major Endpoint Families

The ADS API documentation and OpenAPI materials organize functionality around:
- Search: `/v1/search/query`
- Metrics: `/v1/metrics`
- Export formats: `/v1/export`
- Visualizations: `/v1/vis`
- ORCID affiliation workflows: `/v1/orcid`
- User libraries/bibliographic collections: `/v1/biblib`

## Endpoint Selection Heuristics

- Use `search/query` for discovery and record retrieval.
- Use `metrics` for citation/read statistics aggregates.
- Use `export` when output format (BibTeX, RIS, etc.) is the main deliverable.
- Use `biblib` endpoints for saved library operations.

## Production Tips

- Confirm endpoint parameters in latest docs before final execution.
- Keep endpoint-specific payload examples near the calling code.
- Enforce auth header on every request (including helper scripts).
