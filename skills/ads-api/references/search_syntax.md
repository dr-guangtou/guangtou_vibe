# ADS Search Syntax Reference

## Source
- ADS Help: Search syntax
- URL: https://ui.adsabs.harvard.edu/help/search/search-syntax

## Core Query Grammar

- Default parsing supports Lucene/Solr-style terms and operators.
- Use explicit boolean operators in uppercase: `AND`, `OR`, `NOT`.
- Prefer grouping with parentheses to avoid precedence ambiguity.

## Required and Excluded Terms

- `+term` requires a token to be present.
- `-term` excludes a token.

## Phrases and Proximity

- Use quotes for exact phrases: `"gravitational lensing"`.
- Use proximity syntax on phrases when needed: `"stellar mass"~N`.

## Wildcards and Fuzzy Matching

- `*` and `?` support wildcard matching.
- `term~` supports fuzzy matching for spelling variants.
- Use wildcards conservatively to avoid very broad expansions.

## Range Syntax

- Inclusive range: `[lower TO upper]`.
- Exclusive range: `{lower TO upper}`.
- Common usage: `year:[2015 TO 2025]`.

## Fielded Query Patterns

- Use `field:value` for targeted matching.
- Combine multiple field clauses with boolean operators.
- Example pattern:
  - `(author:"Doe, J" AND bibstem:ApJ) AND year:[2020 TO 2025]`

## Quality Notes

- Start with strict clauses, then relax constraints incrementally.
- Prefer explicit fields over all-field free text for reproducibility.
- Record final query strings in outputs for auditability.
