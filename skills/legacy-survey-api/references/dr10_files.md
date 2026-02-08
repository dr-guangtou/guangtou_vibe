# DR10 File Structure

Source: https://www.legacysurvey.org/dr10/files/

## Core Layout Concepts

- Data are partitioned by bricks and grouped by product type.
- Catalog files include brick-level Tractor outputs and larger sweep subsets.
- Image products include coadds and derivative maps (for example depth or mask-related planes).

## Practical Pathing Rules

- Resolve a coordinate to a brick first when you need brick files.
- Use sweep files for broad cuts; confirm region and object type constraints.
- Keep a mapping table in your task output that records: object identifier, brick, and source file URL.

## Operational Checklist

1. Determine whether request is image-cutout or catalog extraction.
2. Resolve brick and product family.
3. Construct URL from `viewer_api_urls.md` pattern.
4. Record exact URL used for reproducibility.
