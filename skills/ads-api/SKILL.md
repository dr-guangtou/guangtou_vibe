---
name: ads-api
description: NASA ADS literature search and API execution guidance for publication/citation retrieval. Use when building ADS queries, translating research questions into ADS search syntax, selecting Solr fields/operators, calling ADS API endpoints (search, metrics, export, libraries, visualizations), or troubleshooting ADS API authentication/query issues.
---

# ADS API

## Quick Start

1. Define the retrieval goal (discovery, citation tracing, metrics, export, library workflows).
2. Build and validate the ADS query syntax.
3. Select minimal output fields (`fl`) needed for the task.
4. Execute ADS API requests with token authentication.
5. Check pagination, rate-limit behavior, and response completeness before concluding.

## Build Queries

Use these core syntax rules first:
- Use uppercase `AND`, `OR`, `NOT` for explicit boolean logic.
- Use `+term` for required terms and `-term` for excluded terms.
- Use quoted phrases for exact matching, for example `"dark matter"`.
- Use fielded terms such as `author:"Doe, J"`, `year:2024`, `bibstem:ApJ`.
- Use ranges such as `year:[2018 TO 2024]`.
- Use grouped clauses with parentheses for precedence control.

Read `/Users/mac/Documents/yuzhe/skills/ads-api/references/search_syntax.md` for canonical syntax patterns and edge-case behavior.
Read `/Users/mac/Documents/yuzhe/skills/ads-api/references/search_parser.md` when parser behavior or advanced operators become relevant.

## Use API Endpoints

- Base API host: `https://api.adsabs.harvard.edu`.
- Send token in `Authorization: Bearer <ADS_API_TOKEN>`.
- Start with `GET /v1/search/query` for most workflows.
- Add `fl` and `rows` explicitly; avoid overfetching fields.
- Use deterministic sorting when reproducibility matters.

Use endpoint-specific guidance:
- `/Users/mac/Documents/yuzhe/skills/ads-api/references/api_basics.md`
- `/Users/mac/Documents/yuzhe/skills/ads-api/references/api_endpoints.md`
- `/Users/mac/Documents/yuzhe/skills/ads-api/references/api_examples.md`

## Field Selection

Before running large queries, confirm field names and semantics in:
- `/Users/mac/Documents/yuzhe/skills/ads-api/references/solr_fields_operators.md`

For speed and reliability, request only required fields in `fl` (for example `bibcode,title,author,year,citation_count`).

## Validation Checklist

- Confirm query parses and returns expected document class.
- Confirm filters and ranges are correctly scoped.
- Confirm pagination (`rows`, `start`) covers requested result volume.
- Confirm no silent truncation in returned fields.
- Confirm HTTP status; handle `429` and `5xx` with retry/backoff.

## Reference Index

Use `/Users/mac/Documents/yuzhe/skills/ads-api/references/index.md` to locate the right reference file quickly.
