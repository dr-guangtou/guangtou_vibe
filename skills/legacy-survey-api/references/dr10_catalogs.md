# DR10 Catalog Summary

Source: https://www.legacysurvey.org/dr10/catalogs/

## Main Catalog Types

- Tractor catalogs: model-fit source measurements at brick level.
- Sweep catalogs: merged/filterable subsets built for large-area queries.

## Commonly Used Field Groups

- Source identity and coordinates: object id, RA, DEC, brick metadata.
- Photometry: fluxes or magnitudes across g/r/z and related inverse variances.
- Quality and masking: maskbits, allmask_* flags, fit quality indicators.
- Morphology and model outputs: type and model parameters from Tractor fitting.

## Practical Use

- For quality-controlled samples, combine photometric cuts with maskbit and allmask filtering.
- Always document whether values are fluxes or transformed magnitudes in downstream outputs.
