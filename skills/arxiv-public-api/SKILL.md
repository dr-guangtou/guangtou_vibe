---
name: arxiv-public-api
description: "Guidance for safe, compliant use of arXiv public APIs (legacy arXiv API, OAI-PMH, RSS) including query construction, paging, Atom feed parsing, and strict rate-limit/timeout compliance (one request every three seconds, single connection)."
---

# arXiv Public API

## Safety and Compliance First

- Read and follow `references/terms_of_use.md` before making requests.
- Enforce the legacy API rate limits across all machines you control: one request every three seconds and a single connection at a time.
- Do not parallelize requests or attempt to circumvent rate limits.
- Use OAI-PMH for bulk metadata harvesting and large result sets.

## Workflow

1. Confirm the goal and expected volume. If the task implies bulk harvesting, switch to OAI-PMH.
2. Build the API request using `search_query` or `id_list` and optional `start`, `max_results`, `sortBy`, and `sortOrder`.
3. Page results using 0-based `start` and `max_results`. Keep slices small and respect the 3-second delay between calls.
4. Parse the Atom 1.0 response and handle errors returned as Atom feeds.
5. Cache results and avoid repeated calls for identical queries within the same day.

## References

- `references/terms_of_use.md`
- `references/api_basics.md`
- `references/user_manual.md`
