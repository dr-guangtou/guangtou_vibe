# GALFIT Output-File Decorations

The `galfit.NN` restart file and `fit.log` carry extra annotations that do
not appear in user-written input files. The parser captures all four on
`FittedValue` and strips them by default on write.

## The Four Decorations

| Syntax | Meaning | Source |
|---|---|---|
| `val` | Free, fitted value | Normal fit result |
| `[val]` | Held fixed in input (fit flag was 0) | README Section 10 |
| `{val}` | Pinned by an active constraint | README Section 10 |
| `*val*` | Numerically suspicious (3.0.1+) | README Section 10, TOP10 rule 8 |
| `(err)` | 1-sigma uncertainty, separate token | appears after value on same line |

## Composition

Envelopes can stack in any order; the parser peels layers iteratively. The
typical nesting is brackets/braces outermost and stars innermost, but this
is convention, not grammar:

- `[*0.15*]` - held fixed AND numerically suspicious.
- `*[0.15]*` - suspicious AND held fixed (equivalent under the parser).
- `{*1.24*}` - constrained AND suspicious.

`FittedValue` has three independent boolean flags (`fixed_in_output`,
`constrained_in_output`, `suspicious`) so any combination round-trips.

## Uncertainty column

Output files append uncertainties as a parenthesized tuple on the same
line, positioned between the values and the fit flags. The number of
values inside the parens matches the number of values on the line:

```
# Single-value row
 3) 20.0890   (0.0123)    1    # integrated magnitude (err = 0.0123)

# Two-value row (position)
 1) 48.5180 51.2800 (0.0042 0.0039)  1 1

# Two-value Fourier mode with uncertainties
F1) 0.0721 30.0150 (0.0015 2.3100)  1 1
```

The parser stores `FittedValue.uncertainty` per value.

## Asterisks - convergence warnings

Values wrapped in `*...*` mean GALFIT's covariance matrix signaled an
unreliable result for that parameter. Common triggers (TOP10 rule 8):

- r_eff < 0.5 pixels.
- Axis ratio q < 0.1.
- Nuker alpha or similar sharpness parameter driven to a pathological
  value.
- Strong parameter degeneracies (covariance near singular).

**A solution with any asterisked parameter should never be trusted.**
Refit with that parameter held fixed or with better initial guesses.

## The FLAGS FITS keyword

After a fit, `imgblock.fits[2]`'s FITS header carries a `FLAGS` keyword
listing every warning tripped during iteration:

```python
from astropy.io import fits
with fits.open("imgblock.fits") as hdul:
    flags = hdul[2].header.get("FLAGS", "")
    # e.g. "1 A-4 A-5 A-6"
```

Run `galfit -help` or consult README Section 10 for flag meanings. The
most actionable are `1` (diverged), `2` (maxed out iterations), and any
`A-` flag (astrometry / FITS-related).

## Round-Trip Posture

The parser's default write behavior strips all four decorations (produces
a clean input file usable as the next run's `.feedme`). To keep them for
diagnostic dumps:

```python
galfit_io.write_galfit(gf, "dump.galfit", preserve_decorations=True)
```

`to_yaml` and `to_json` always preserve decorations because YAML/JSON is
the round-trippable archival form, not a runnable GALFIT input.

## `fit.log`

The accumulated log is appended on every run (never rewritten). It
contains:

- Reduced chi^2, chi^2, NDoF per iteration.
- Best-fit parameters with 1-sigma errorbars.
- Square brackets / curly braces / asterisks with the same meaning as in
  `galfit.NN`.

`fit.log` is human-readable rather than strictly structured; the parser
targets `galfit.NN` because the grammar is stable.

## `imgblock.fits` Layers

The FITS cube has three or four layers:

- `[0]` - empty PrimaryHDU.
- `[1]` - input data.
- `[2]` - final model (header holds best-fit parameters too).
- `[3]` - residual (data - model).

With `P) 3` or `-o3`, GALFIT also writes `subcomps.fits` where each HDU
beyond index 0 is a single component's model image.
