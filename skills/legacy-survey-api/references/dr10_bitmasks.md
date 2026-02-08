# DR10 Bitmasks and Flags

Source: https://www.legacysurvey.org/dr10/bitmasks/

## Flags to Check Before Science Use

- `maskbits`: pixel-level or region-level mask conditions.
- `allmask_g`, `allmask_r`, `allmask_z`: per-band contamination/masking indicators.
- `fitbits`: fit diagnostics and model-behavior flags.

## Interpretation Workflow

1. Define a baseline clean-sample policy (for example reject severe masking flags).
2. Apply per-band `allmask_*` constraints consistent with your band usage.
3. Add fit-quality filtering with `fitbits` when model reliability matters.
4. Record exact bit conditions in output metadata for reproducibility.

## Notes

- Bit definitions can evolve by release; keep this skill scoped to DR10 unless explicitly switched.
- Validate bit usage against `dr10_issues.md` for known problematic cases.
