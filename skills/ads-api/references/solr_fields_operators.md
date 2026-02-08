# ADS Solr Fields and Operators

## Source
- ADS Help: Comprehensive Solr term list
- URL: https://ui.adsabs.harvard.edu/help/search/comprehensive-solr-term-list

## Usage Model

- ADS search supports many indexed fields and parser operators.
- Always verify field names before production queries.
- Use fielded clauses to reduce ambiguity and improve precision.

## Frequently Used Retrieval Fields

Use these commonly in `q` and/or `fl` workflows:
- `bibcode`
- `title`
- `author`
- `year`
- `abstract`
- `doi`
- `identifier`
- `bibstem`
- `citation_count`
- `read_count`
- `property`

## Field Strategy

- Keep `fl` minimal to reduce payload size and parsing cost.
- Use sortable/quantitative fields (`year`, `citation_count`) for ranking and filtering.
- Use publication identity fields (`bibcode`, `doi`, `identifier`) for deduplication.

## Operator Guidance

- Use boolean operators (`AND`, `OR`, `NOT`) explicitly.
- Use range operators for date and numeric scoping.
- Use parser-specific functions only when base field logic is insufficient.

## Practical Pattern

1. Start with high-signal fields (`title`, `author`, `year`).
2. Add constraints (`bibstem`, `property`) to narrow corpus.
3. Add metadata fields to `fl` only if needed downstream.
