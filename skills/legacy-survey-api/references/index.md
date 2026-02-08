# Legacy Survey DR10 Reference Index

Use this index to load only what you need.

## File Map

- `dr10_status.md`: Survey progress, imaging area, and release scope.
- `dr10_description.md`: DR10 content summary and processing context.
- `dr10_files.md`: Directory and filename conventions for DR10 products.
- `dr10_catalogs.md`: Tractor/sweep schema summary and usage notes.
- `dr10_bitmasks.md`: Maskbits, allmask, and fitbits interpretation.
- `dr10_issues.md`: Known caveats and mitigation checks.
- `viewer_api_urls.md`: URL patterns for cutouts and catalog retrieval.

## Quick Search Patterns

- Image cutouts: `jpeg-cutout`, `fits-cutout`, `layer=`, `pixscale=`
- Catalog retrieval: `tractor`, `sweep`, `bricks`, `fits`
- Quality flags: `maskbits`, `allmask_g`, `allmask_r`, `allmask_z`, `fitbits`
- Caveats: `known issue`, `artifact`, `depth`, `calibration`

## Suggested Loading Strategy

1. Start with `viewer_api_urls.md` for endpoint construction.
2. Open `dr10_files.md` for exact file paths.
3. Open `dr10_catalogs.md` for column semantics.
4. Open `dr10_bitmasks.md` and `dr10_issues.md` before final filtering or scientific interpretation.
