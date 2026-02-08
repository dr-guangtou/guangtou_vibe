# Viewer URL API Guide (DR10)

Sources:
- https://www.legacysurvey.org/viewer/urls
- https://www.legacysurvey.org/viewer

## Core Endpoints

- JPEG cutout:
  - `https://www.legacysurvey.org/viewer/jpeg-cutout?ra=<ra>&dec=<dec>&pixscale=<arcsec_per_pixel>&layer=ls-dr10`
- FITS cutout:
  - `https://www.legacysurvey.org/viewer/fits-cutout?ra=<ra>&dec=<dec>&pixscale=<arcsec_per_pixel>&size=<pixels>&layer=ls-dr10`
- Viewer landing at coordinate:
  - `https://www.legacysurvey.org/viewer?ra=<ra>&dec=<dec>&layer=ls-dr10&zoom=<zoom>`

## Useful Parameters

- `ra`, `dec`: ICRS coordinates in degrees.
- `layer`: set to DR10 layer (`ls-dr10`) unless task requires a different layer.
- `pixscale`: cutout resolution in arcsec/pixel.
- `size`: output image size in pixels (for FITS cutout requests).
- `bands`: optional band selection when supported by endpoint.

## Catalog/File URL Patterns (Workflow)

1. Resolve brick and product class from DR10 file docs.
2. Build file URL using DR10 directory conventions from `dr10_files.md`.
3. Keep a per-request log: coordinate, brick, endpoint, and final URL.

## Minimal Construction Recipe

1. Confirm coordinate and requested product (image or catalog).
2. Start from endpoint template above.
3. Set `layer=ls-dr10` and tune `pixscale`/`size`.
4. Fetch and inspect.
5. Apply `dr10_bitmasks.md` and `dr10_issues.md` checks before interpreting results.
