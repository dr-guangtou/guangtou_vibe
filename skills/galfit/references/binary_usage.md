# Running the GALFIT Binary

## Invocation

```bash
galfit [OPTIONS] <feedme-file>
```

On this machine the binary is installed at
`/Users/shuang/code/galfit/galfit` (GALFIT 3.0.7, August 2017).

## Important Flags

| Flag | Effect |
|---|---|
| `-i` | Interactive mode. Press `q` to start fitting. |
| `-imax <n>` | Cap iterations at n. Good for sanity checks; set to ~50-100 for real fits. |
| `-noskyest` | Skip internal sky estimation. Use when you supply a sigma image or your sky is already zero. |
| `-skyped <n>` | Force sky pedestal to `n`. |
| `-skyrms <n>` | Force sky RMS to `n`. |
| `-o1` | Make model only (do not fit). Writes `model.fits`. |
| `-o2` | Make imgblock only (data+model+residual cube). Does not fit. |
| `-o3` | Make subcomponents file (`subcomps.fits`, one HDU per component). |
| `-outsig` | Write the internal sigma image to `sigma.fits`. |
| `-help` | Dump the full help and FLAGS catalog. |

## Required FITS Header Keywords on the Input Image

GALFIT reads four keywords from the data image header:

- `EXPTIME` - exposure time in seconds. If missing, defaults to 1.0.
- `GAIN` (or `ATODGAIN`) - e-/ADU. Default 7.
- `NCOMBINE` - number of combined exposures. Default 1.
- `RDNOISE` - read noise in e-. Default 5.2 (but unused since 3.0.1).

Without correct `GAIN`, GALFIT's internally generated sigma image will be
wrong. Supply a sigma image (`C)` in the header) when in doubt.

## Header Items (A-P)

These live inside the `.galfit` / `.feedme` file, not on the command line.
See `profile_schemas.md` and the bundled parser for the full surface.

Key to remember:

- `P) 0` - normal optimization run (default).
- `P) 1` - make model, quit. No fit.
- `P) 2` - make imgblock, quit.
- `P) 3` - also write `subcomps.fits`.

## Exit Codes

- `0` - solution produced (reliability not guaranteed; check `FLAGS`).
- `1` - aborted without producing a solution.

## FLAGS Header Keyword

After a run, `imgblock.fits[2]`'s header carries `FLAGS` listing every
warning raised during iteration. Example: `FLAGS = "1 A-4 A-5 A-6"`.

Most-actionable flags:

- `1` - the fit never converged.
- `2` - hit the `-imax` iteration ceiling.
- `A-*` - astrometry/FITS-related.

Run `galfit -help` to dump the full flag catalog.

## After a Run - the Output Files

Every successful run produces:

1. `galfit.NN` - restart file (NN starts at 01 and monotonically increases
   across all runs in the cwd). Parse this with
   `galfit_io.read_galfit(path)` to get the structured best-fit parameters
   with uncertainties.
2. `fit.log` - human-readable log, appended across runs.
3. `imgblock.fits` - 3-layer cube: data / model / residual.
4. `subcomps.fits` - only with `-o3` or `P) 3`.

## Recipe: Small Sanity Check

```bash
# Start from a parser-written feedme; cap iterations; generate everything.
galfit -imax 10 my.feedme
ls -lt galfit.* imgblock.fits subcomps.fits 2>/dev/null
```

## Recipe: Production Fit

```bash
galfit -imax 100 -noskyest my.feedme
# Verify it converged
python -c "
from astropy.io import fits
flags = fits.getheader('imgblock.fits', 2).get('FLAGS', '')
print('FLAGS:', flags)
"
# Parse the structured result
python -c "
import sys; sys.path.insert(0, '<skill-dir>/scripts')
import galfit_io
gf = galfit_io.read_galfit(sorted(__import__('glob').glob('galfit.*'))[-1])
for c in gf.components:
    print(type(c).__name__, c.x.value, c.y.value)
"
```

## Common Pitfalls

- **The binary runs interactively unless given a feedme file.** If it
  hangs, you probably forgot the filename.
- **`galfit.NN` numbering continues from the last run.** Delete old
  `galfit.*` files or run in a clean directory to avoid confusion.
- **The input-image filename is resolved relative to the cwd**, not the
  feedme location. Run from the directory that holds the feedme.
- **Filenames with whitespace are unsupported.** GALFIT's tokenizer splits
  on any whitespace.
- **Missing `EXPTIME`/`GAIN`** silently propagates to a wrong sigma image.
  Always verify these are present (or supply your own sigma via `C)`).
