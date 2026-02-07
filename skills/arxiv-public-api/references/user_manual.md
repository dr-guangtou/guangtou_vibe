# arXiv API User Manual (Summary)

## Query Parameters and Logic

- `search_query` and `id_list` can be used independently or together.
- If only `search_query` is provided, results match the query.
- If only `id_list` is provided, results return for those IDs.
- If both are provided, results are the intersection of `id_list` and `search_query`.

## Paging and Result Size

- `start` is 0-based and selects the first returned result.
- `max_results` controls the number of results returned.
- When paging, increment `start` by `max_results`.
- For multiple calls, include a 3-second delay between requests.
- `max_results` is limited to 30000 in slices of at most 2000.
- Requests with `max_results` > 30000 return HTTP 400.
- For queries returning more than 1,000 results, refine the query or request smaller slices.
- Use OAI-PMH for bulk metadata harvesting or large result sets.

## Sorting

- `sortBy` values: `relevance`, `lastUpdatedDate`, `submittedDate`.
- `sortOrder` values: `ascending`, `descending`.

## Atom Response and Errors

- Responses are Atom 1.0 feeds, including errors.
- The OpenSearch elements `totalResults`, `startIndex`, and `itemsPerPage` are useful for paging.
- Errors are returned as Atom feeds with a single `<entry>` and an error message in `<summary>`.

## Update Cadence and Caching

- Search results do not change more than once per day due to the 24-hour submission cycle.
- Do not call the API more than once per day for the same query; cache results.
