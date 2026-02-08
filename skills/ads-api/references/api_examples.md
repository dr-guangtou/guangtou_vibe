# ADS API Examples and Notebook Map

## Sources
- ADS dev API repository: https://github.com/adsabs/adsabs-dev-api
- README notebook links under `API_documentation_Python` and `API_documentation_UNIXshell`

## Python Notebook Topics

Repository notebook set includes examples for:
- Search API
- Metrics API
- Export API
- Library API
- Visualizations API
- ORCID affiliation API

Path pattern:
- `API_documentation_Python/*.ipynb`

## UNIX Shell Notebook Topics

Equivalent shell-oriented examples are available for:
- Search API
- Metrics API
- Export API
- Library API
- Visualizations API
- ORCID affiliation API

Path pattern:
- `API_documentation_UNIXshell/*.ipynb`

## Reusable Example Pattern

1. Build `q` expression in ADS search syntax.
2. Request only required fields via `fl`.
3. Keep `rows` small for first validation run.
4. Paginate after schema/quality checks pass.
5. Persist query and endpoint metadata with results.
