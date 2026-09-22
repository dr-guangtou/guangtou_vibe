---
name: spherex-irsa-access
description: Use when working with SPHEREx data at IRSA - finding exposures, downloading spectral-image cutouts, reading the Level 2 MEF (IMAGE/FLAGS/VARIANCE/ZODI/PSF or EPSF/WCS-WAVE), assigning per-pixel wavelengths, choosing a PSF zone, masking flags, subtracting zodiacal light, or extracting a spectrum for a point source or galaxy. Also use when a script written for QR2 breaks on QR3 files.
category: astronomy
tags: [spherex, irsa, spectroscopy, nasa, infrared, astroquery, pyvo, tap, sia, tractor]
author: Song Huang
date: 2026-09-22
version: 2.0.0
requirements:
  - astroquery>=0.4.11
  - pyvo>=1.9
  - astropy>=7.0
  - numpy
  - photutils (for ePSF handling and aperture photometry)
---

# SPHEREx IRSA data access

Verified against the live IRSA archive on 2026-09-22. SPHEREx facts change every few
months (new releases, new pipeline versions, new products); re-check the QR overview page
and the Explanatory Supplement before trusting any number here:
`https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html`,
`https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp_QR.pdf` (v2.0, 2026-08-25).

## Overview

SPHEREx delivers Level 2 "spectral images": one 2040x2040 frame per detector per
pointing, 6.15 arcsec pixels, in MJy/sr, where every pixel has its own wavelength set by a
linear variable filter (0.75-5.0 um, R ~ 39-41 in bands 1-3, 35 in band 4, 112 and 128
in bands 5-6). A spectrum of a sky position is built from many pointings. The images are
NOT zodiacal-light subtracted.

## State of the archive (2026-09-22)

| Release | Pipeline | Collections | DOI | Status |
|---|---|---|---|---|
| QR1 | 6.2-6.3 | - | 10.26131/IRSA629 | retired Feb 2026 |
| QR2 | 6.4-6.5.7 | `spherex_qr2`, `spherex_qr2_deep` | 10.26131/IRSA652 | 2025-04-24 to 2026-07-20 |
| QR3 | 7.0.x (R7) | `spherex_qr3`, `spherex_qr3_deep` | 10.26131/IRSA662 | from 2026-07-20, ingested Sept 2026 |
| DR1 | R7 | - | - | Year 1 reprocessing, late fall 2026, adds catalogs and all-sky cubes |

Do not mix QR1/QR2; use `l3_flux_corrections` when mixing QR2 and QR3 photometry.

## Quick start

```python
import pyvo, astropy.units as u
from astropy.io import fits
from astropy.utils.data import conf
conf.remote_timeout = 120

service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")
ra, dec, size = 210.80227, 54.34895, 0.05
query = f"""
SELECT 'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size}' AS uri,
       p.time_bounds_lower, p.energy_bandpassname, p.provenance_version, o.collection
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
JOIN spherex.observation o ON o.obsid = p.obsid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
  AND p.energy_bandpassname = 'SPHEREx-D3'
ORDER BY p.time_bounds_lower"""
exposures = service.search(query).to_table()
hdulist = fits.open(exposures["uri"][0], cache=False)
```

TAP sees new data immediately; SIA (`Irsa.query_sia(pos=(coord, r), collection='spherex_qr3')`)
lags by about a day. Constrain TAP queries spatially; whole-table `ORDER BY`/`GROUP BY`
on `spherex.obscore` take minutes.

## The MEF, per release

| HDU | QR2 (VERSION 6.x) | QR3 (VERSION 7.x) |
|---|---|---|
| IMAGE | MJy/sr; WCS + SIP; alt WCS `A` (pixel offsets CRPIX1A/2A) and `W` (wavelength) | same |
| FLAGS | int32; bit names in header as `MP_<NAME>` | int32; names as `MSKN####`/`MSKM####` (unused planes omitted) |
| VARIANCE | (MJy/sr)^2 | same |
| ZODI | model, not subtracted | same (ZODIMDL = KEL98_WAVESCL_V1) |
| PSF | cube (121, 101, 101), 10x oversampled, zones XCTR_i/YCTR_i; header-order bug unless VERSION >= 6.5.6 or `+psffix1` | absent |
| EPSF | absent | BinTable, 441 rows (451 for D3), 33x33 stamps at 5x, cols BINX BINY XCENTER YCENTER NEFF_MEAN CWAVE CBAND EPSF |
| WCS-WAVE | WAVE-TAB lookup, visualization grade | same |

Branch on `hdulist[0].header['VERSION']`. Use `references/spherex_flags.py` for the
canonical flag table (do not parse names from headers). Prefer the QR3 ePSF calibration
files (`s3://nasa-irsa-spherex/qr3/epsf/...`) even for QR2 images, as the official
tutorial recommends; `scripts/select_epsf.py` picks the zone.

## Wavelengths

Science wavelengths come from the per-pixel `CWAVE`/`CBAND` maps in the Spectral WCS
calibration product (`<release>/spectral_wcs/`). The in-file `W` WCS is a ~1 nm
approximation: `WCS(header, fobj=hdulist, key='W'); wcs.sip = None;
wavelength, bandwidth = wcs.pixel_to_world(x, y)`. Standard grid: the 102 nominal channels
in `<release>/spectral_channels/`. Drop the band 3/4 dichroic-edge channels and the
He 1.083 um airglow channels unless needed.

## Backgrounds

ZODI is the dominant background and is not subtracted. Official practice: the
Spectrophotometry Tool ignores ZODI and fits a local background in a 15-pixel box; the
Mosaic Tool subtracts IMAGE - ZODI. Airglow (He 1.083 um, aurora, shuttle glow at 3.0 and
4.5 um) is never subtracted; R7 headers carry `HE_AIRGLOW_CONT`, `AURORA_CONT`,
`SHUTTLE_GLOW_CONT`. Screen exposures with FINAST = 0 and L2DQAFLG = Pass.

## Official tools (GUI only, no API)

- Spectrophotometry Tool: Tractor forced photometry, point source or Sersic (Re 1-20
  arcsec), 20 targets per job, two concurrent jobs; returns wavelength, flux (uJy),
  flux_err, flags (bit 32 = CONTAINS_BAD_PIXEL, 33 = FIT_ERROR), fit_ql, flux_bkg.
- Mosaic Tool: 102-channel cube, >= 6.15 arcsec pixels, <= 5x5 deg, all-sky frames only;
  not for precision photometry.
- Cutouts: append `?center=RA,DEC&size=DEG` to an IBE URL; all HDUs kept, PSF/EPSF
  copied whole.

## Common mistakes

| Mistake | Fix |
|---|---|
| Treating IMAGE as sky-subtracted | subtract ZODI and fit a local background |
| Parsing flag names from `MP_*` on QR3 | use the hard-coded table |
| Reading `hdulist['PSF']` on QR3 | read `EPSF` table; branch on VERSION |
| Zone lookup with cutout pixel coords | convert with `x_orig = 1 + x_cut - CRPIX1A` |
| Passing an oversampled ePSF to Tractor | shift, integrate to native pixels, renormalize (`photutils.psf.ImagePSF`) |
| Using WCS-WAVE for science wavelengths | use CWAVE/CBAND |
| Same aperture in all bands | apply wavelength-dependent aperture corrections (N_eff grows with wavelength) |
| Trusting tool `flux_err` alone | add 3% visit-to-visit RMS in quadrature; absolute floor 3-8% |

## Files

- `references/quick_reference.md` - verified numbers, tables, flag bits, URLs, citation text.
- `references/spherex_flags.py` - canonical flag table and mask builder for QR2 and QR3.
- `references/spherex_psf_header_fix.py` - fix for pre-6.5.6 QR2 PSF cubes (legacy).
- `scripts/query_tap_cutouts.py`, `scripts/query_sia_basic.py`, `scripts/download_cutouts.py` - discovery and bulk cutouts.
- `scripts/read_mef.py` - inspect a QR2 or QR3 MEF; `scripts/select_epsf.py` - pick the ePSF zone for a sky position.
- `templates/example_notebook.py` - end-to-end example.

Detailed project notes (Explanatory Supplement, papers, tutorials) live in the
`spherex_psb` repo under `docs/spherex_data_guide.md` and `docs/reference_notes/`.
