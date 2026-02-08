---
name: legacy-survey-api
description: "Guidance for using the Legacy Survey DR10 data (images and catalogs) through viewer URL APIs and release file structure, with local cache refresh workflows, maskbits interpretation, and known-issues checks. Use when tasks involve cutouts, tractor/sweep catalogs, bricks, or quality masking for Legacy Survey data products."
---

# Legacy Survey API

Use this skill for DR10 image/catalog access and interpretation while keeping context usage small.

## Workflow

1. Confirm the target data product: image cutout, brick-level tractor catalog, or sweep catalog query.
2. Refresh local references before analysis:
   - `python3 scripts/refresh_legacysurvey_cache.py --output-dir references/cache`
   - For no-network environments, use `--dry-run` and rely on bundled references.
3. Load only the minimum reference files from `references/index.md` needed for the task.
4. Build API URLs using `references/viewer_api_urls.md` patterns.
5. Validate mask flags and caveats using `references/dr10_bitmasks.md` and `references/dr10_issues.md` before final conclusions.

## Keep Context Lean

- Do not load all reference files at once.
- Start from `references/index.md`, then open only relevant files.
- Prefer catalog-specific references for catalog tasks and image-specific references for cutout tasks.

## References

- `references/index.md`
- `references/dr10_status.md`
- `references/dr10_description.md`
- `references/dr10_files.md`
- `references/dr10_catalogs.md`
- `references/dr10_bitmasks.md`
- `references/dr10_issues.md`
- `references/viewer_api_urls.md`
