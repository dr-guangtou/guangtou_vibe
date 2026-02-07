# arXiv API Basics (Summary)

## Base Endpoint

- Legacy API endpoint: `http://export.arxiv.org/api/query`
- Use HTTP GET or POST with query parameters.

## Core Query Parameters

- `search_query`: Free-text search and fielded queries.
- `id_list`: Comma-separated arXiv identifiers.
- `start`: 0-based index of the first result.
- `max_results`: Maximum number of results to return.
- `sortBy`: Sorting field.
- `sortOrder`: Sorting order.

## Response Format

- Responses are Atom 1.0 feeds.
- Parse Atom with the arXiv namespace for arXiv-specific fields.
- Use OpenSearch elements (`totalResults`, `startIndex`, `itemsPerPage`) to manage paging.

## Example Request (URL-Encoded)

`http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=10`
