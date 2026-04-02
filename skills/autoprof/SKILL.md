---
name: autoprof
description: AutoProf non-parametric galaxy isophote fitting pipeline. Use when fitting galaxy surface brightness profiles with AutoProf's FFT-based method, benchmarking against photutils/GALFIT, or running AutoProf programmatically on FITS images.
---

# AutoProf

Non-parametric isophotal analysis pipeline for galaxy images (Stone et al. 2021).
Uses FFT-based fit-stabilization to robustly extract SB profiles ~2 mag/arcsec²
fainter than photutils on the same images.

- **Docs**: https://autoprof.readthedocs.io/en/latest/
- **Code**: https://github.com/Autostronomy/AutoProf
- **Paper**: https://arxiv.org/abs/2106.13809
- **Install**: `pip install autoprof` (v1.3.4)
- **Successor**: AstroPhot (parametric, multi-band) — use for PSF-limited or crowded fields

## Critical: Environment Isolation Required

AutoProf v1.2+ pins `photutils<=1.5.0`, which conflicts with modern environments.
**Always use a separate virtual environment:**

```bash
python3 -m venv /path/to/autoprof_venv
/path/to/autoprof_venv/bin/pip install autoprof==1.3.4
```

Call via `/path/to/autoprof_venv/bin/python script.py`.

Additional constraints:
- Input FITS must be **uncompressed** (`.fits`, not `.fits.fz`). Decompress first.
- AutoProf reads image from HDU 0 by default; use `ap_image_hdu` to change.

## Programmatic Usage

### Pipeline approach (recommended)

```python
from autoprof.Pipeline import Isophote_Pipeline

pipeline = Isophote_Pipeline(loggername="autoprof.log")
result = pipeline.Process_Image(options={
    "ap_image_file": "/path/to/galaxy.fits",  # uncompressed FITS
    "ap_mask_file": "/path/to/mask.fits",     # optional; 0=good, >0=bad
    "ap_mask_hdu": 0,
    "ap_name": "galaxy_name",
    "ap_pixscale": 0.262,       # arcsec/pixel (required)
    "ap_zeropoint": 22.5,       # nanomaggy zeropoint
    "ap_process_mode": "image",
    "ap_doplot": False,
    "ap_saveto": "/output/dir/",
    "ap_isoclip": True,         # sigma-clip along isophotes
})
# result is dict of step timings if success, or 1 if failure
```

### Direct function calls (bypass pipeline, access results in-memory)

```python
from autoprof.pipeline_steps import (
    Background_Mode, PSF_Assumed, Center_HillClimb,
    Isophote_Initialize, Isophote_Fit_FFT_Robust,
    Isophote_Extract, EllipseModel,
)

img = fits.getdata("galaxy.fits").astype(float)
options = {
    "ap_pixscale": 0.262, "ap_zeropoint": 22.5,
    "ap_name": "test", "ap_isoclip": True, "ap_doplot": False,
}
results = {}

for step in [Background_Mode, PSF_Assumed, Center_HillClimb,
             Isophote_Initialize, Isophote_Fit_FFT_Robust,
             Isophote_Extract]:
    img, res = step(img, results, options)
    results.update(res)

# Profile in results["prof data"]
# Model image via EllipseModel step
```

## Output Format

### Profile columns (`.prof` file, CSV)

The `.prof` file has two header lines: line 0 is `# units...` (comment), line 1 is
column names. Parse with: `np.genfromtxt(file, delimiter=",", names=True, skip_header=1)`

| Column | Unit | Description |
|--------|------|-------------|
| `R` | arcsec | Semi-major axis (in **arcsec**, not pixels) |
| `SB` | mag/arcsec² | Surface brightness (99.999 = invalid/below noise) |
| `SB_e` | mag/arcsec² | SB error |
| `totmag` | mag | Cumulative enclosed magnitude |
| `totmag_e` | mag | Enclosed magnitude error |
| `ellip` | — | Ellipticity (1 - b/a) |
| `ellip_e` | — | Ellipticity error |
| `pa` | deg | Position angle (**astronomical**: CCW from +y/North) |
| `pa_e` | deg | PA error |
| `pixels` | count | Pixels sampled |
| `maskedpixels` | count | Masked pixels |
| `totmag_direct` | mag | Direct-sum enclosed magnitude |

### Auxiliary file (`.aux`, YAML-like)

Contains: center (x, y), background level, PSF FWHM, initial geometry,
fit flags, processing time.

## Key Parameters

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `ap_pixscale` | (required) | Pixel scale (arcsec/pixel) |
| `ap_zeropoint` | 22.5 | Photometric zero point |
| `ap_isoclip` | False | Sigma-clip along isophotes |
| `ap_isoclip_nsigma` | 5 | Clipping threshold |
| `ap_fit_limit` | 2 | Stop at N × background noise |
| `ap_samplegeometricscale` | 0.1 | Radial spacing growth factor |
| `ap_isofit_iterlimitmax` | 300 | Max fitting iterations |
| `ap_isoaverage_method` | "median" | Averaging along isophotes |
| `ap_fluxunits` | "mag" | Output: "mag" or "intensity" |
| `ap_iso_measurecoefs` | None | Fourier modes to measure, e.g. `(3,4)` |
| `ap_isoinit_pa_set` | None | Override initial PA (deg, astro convention) |
| `ap_isoinit_ellip_set` | None | Override initial ellipticity |
| `ap_set_center` | None | Override center: `{"x": float, "y": float}` |

## Pipeline Steps

Default order: `background` → `psf` → `center` → `isophoteinit` →
`isophotefit` → `isophoteextract` → `checkfit` → `writeprof`

The core fitter is `Isophote_Fit_FFT_Robust` — FFT-based with regularization,
distinct from photutils' Jedrzejewski (1987) iterative method.

## Conventions

- **PA**: astronomical convention (CCW from +y/North), same as SGA
- **SMA**: output R is in **arcsec** (R_pixels × ap_pixscale)
- **SB**: already in mag/arcsec² (no conversion needed for comparison)
- **Mask**: 0 = good, nonzero = bad (same convention as our pipeline masks)
- **SB=99.999**: sentinel for invalid/below-noise isophotes — filter these out

## Comparison with photutils

| Feature | AutoProf | photutils |
|---------|----------|-----------|
| Algorithm | FFT-based + regularization | Jedrzejewski (1987) iterative |
| PA convention | Astronomical (CCW from +y) | Math (CCW from +x) |
| SMA output unit | arcsec | pixels |
| SB output | mag/arcsec² | raw intensity (nanomaggies/pixel) |
| Harmonics | via `ap_iso_measurecoefs` | always measured (a3/b3/a4/b4) |
| Center | Auto hill-climb or fixed | Via EllipseGeometry |
| Background | Auto-estimated | Not handled (user subtracts) |
| Model image | `EllipseModel` step | `build_ellipse_model()` |
| Env constraint | Needs isolated venv | Works with modern stack |
