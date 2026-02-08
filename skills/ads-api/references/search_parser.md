# ADS Search Parser (Advanced)

## Source
- ADS Help: Search parser
- URL: https://ui.adsabs.harvard.edu/help/search/search-parser

## Purpose

Use parser-level syntax when standard boolean/fielded query patterns are not enough.

## Advanced Use Cases

- Complex nested expressions with strict precedence.
- Parser-specific function usage for citation/reference relationships.
- Mixed free-text and structured metadata clauses.

## Operational Guidance

- Validate parser behavior on small test queries before scaling up.
- Isolate parser-heavy clauses in parentheses for readability and debugging.
- Prefer incremental construction:
  1. Start with a minimal working clause.
  2. Add one advanced component at a time.
  3. Re-run and verify each change.

## Debugging Pattern

- If result volume is unexpectedly high/low, simplify to one clause and reintroduce conditions iteratively.
- Confirm each parser-specific operator against the official parser help before automating.
