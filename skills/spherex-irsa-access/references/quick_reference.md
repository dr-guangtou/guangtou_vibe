# SPHEREx IRSA quick reference (verified 2026-09-22)

## Releases and collections

| Release | Pipeline VERSION | Observation IDs served | SIA/TAP collections | S3 prefix | DOI |
|---|---|---|---|---|---|
| QR1 | 6.2.1-6.3.0 | retired February 2026 | - | - | 10.26131/IRSA629 |
| QR2 | 6.4.0-6.5.7 | 2025W17_4B (MJD 60789.75) to 2026W29_2A (MJD 61241.0) | spherex_qr2, spherex_qr2_deep | qr2/ | 10.26131/IRSA652 |
| QR3 | 7.0.5 (R7) | 2026W30_1B (2026-07-20) onward; ingested 2026-09-15 | spherex_qr3, spherex_qr3_deep | qr3/ | 10.26131/IRSA662 |
| DR1 | R7.0-7.2 | Year 1 reprocessing, late fall 2026 | - | - | - |

Survey 3/4 data from 2026-05-16 to 2026-07-19 sit in spherex_qr2 (VERSION 6.5.7) until DR1.
Warnings from the project: do not combine QR1 and QR2; caution combining QR2 and QR3 (gain
change; use `l3_flux_corrections_D<n>`). QR2 files with VERSION 6.4-6.5.5 and no `+psffix1`
suffix have the PSF cube plane order bug (up to +/-5% photometry in two corners).

## Bands

| Band | um | R | Notes |
|---|---|---|---|
| 1 | 0.75-1.09 | 39 | He 1.083 um airglow in every exposure |
| 2 | 1.10-1.62 | 41 | He leak features near 1.25 and 1.49 um |
| 3 | 1.63-2.41 | 41 | long edge squeezed by the 2.42 um dichroic, DICHROIC flag |
| 4 | 2.42-3.82 | 35 | short edge squeezed; shuttle glow near 3.0 um |
| 5 | 3.83-4.41 | 112 | shuttle glow near 4.5 um (band 5/6) |
| 6 | 4.42-5.00 | 128 | |

Pixel 6.15 arcsec; XPOSURE 113.5826 s; TELAPSE 118.1873 s; 17 nominal channels per band
(102 total); per-exposure 5 sigma depth ~19.5 AB (0.75-3.8 um), ~17.5-18.5 AB (3.8-5 um).

## TAP (https://irsa.ipac.caltech.edu/TAP)

Tables: `spherex.observation` (obsid, collection, observationid), `spherex.plane`
(planeid, obsid, productid D1-D6, energy_bandpassname 'SPHEREx-D1'..'SPHEREx-D6', poly,
time_bounds_lower/upper MJD, provenance_version, quality_flag, metrics_maglimit,
position_resolution, energy_resolvingpower), `spherex.artifact` (planeid, uri),
`spherex.obscore` (obs_collection, obs_id, s_ra, s_dec, s_region, t_min, t_max),
`spherex.splices` (SPLICES ice-target catalog, DOI 10.26131/IRSA554).

```sql
SELECT 'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size}' AS uri,
       p.time_bounds_lower, p.energy_bandpassname, p.provenance_version, o.collection
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
JOIN spherex.observation o ON o.obsid = p.obsid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
  AND o.collection = 'spherex_qr3'
ORDER BY p.time_bounds_lower
```

## SIA2

`https://irsa.ipac.caltech.edu/SIA?COLLECTION=spherex_qr3&POS=circle+RA+DEC+RADIUS`;
`Irsa.list_collections(servicetype='SIA', filter='spherex')`; result has `access_url`
and `cloud_access` (JSON with bucket and key). About one day behind ingestion.

## Files, cutouts, cloud

- IBE: `https://irsa.ipac.caltech.edu/ibe/data/spherex/<qr2|qr3>/level2/<PlanningPeriod>/l2b-v<ver>-<yyyy>-<doy>/<det>/level2_<obsid>D<det>_spx_l2b-v<ver>-<yyyy>-<doy>.fits`
- Cutout: append `?center=RA,DEC&size=SIZE_DEG` (the notebooks write `RA,DECd`).
- S3: `s3://nasa-irsa-spherex/` (us-east-1, anonymous); `fits.open('s3://...', fsspec_kwargs={'anon': True})`.
  Prefixes: qr2/{abs_gain_matrix, average_psf, dark, dichroic, gain_factors, level2, nonfunc,
  nonlinear_pars, readnoise_pars, sip, solid_angle_pixel_map, spectral_channels, spectral_wcs};
  qr3/ adds aurora_template, epsf, he_template, l3_flux_corrections, nonfunc_v2,
  shuttle_glow_template, xtalk_class1, xtalk_class2, zodi_scaling_v2 (no average_psf).
- ePSF calibration files: `qr3/epsf/cal-epsf-v1-2026-191/<det>/epsf_D<det>_spx_cal-epsf-v1-2026-191.fits` (v2 for D3).

## MEF layout

QR2: PRIMARY(VERSION) / IMAGE / FLAGS / VARIANCE / ZODI / PSF (121,101,101; OVERSAMP=10;
XCTR_i, YCTR_i for i=1..121 in 0-based parent pixels; plane index i-1) / WCS-WAVE.
QR3: PRIMARY(VERSION 7.x) / IMAGE / FLAGS / VARIANCE / ZODI / EPSF (BinTable: BINX, BINY,
XCENTER, YCENTER, XWIDTH, YWIDTH, NSTAR, NEFF_MEAN, CWAVE, CBAND, EPSF 33x33; OVSMPX =
OVSMPY = 5; 21x21 zones, 11x41 for D3; ORDERING 'x-fast then y') / WCS-WAVE.

Useful IMAGE keywords: DETECTOR, OBSID, FINAST (0 = good), L2DQAFLG, PSF_FWHM (arcsec,
median; QR2 optical PSF and QR3 ePSF values differ), MJD-AVG, XPOSURE, `L2 N_<FLAG>`
counters, and in R7 only: HE_AIRGLOW_CONT, AURORA_CORR/AURORA_CONT,
SHUTTLE_GLOW_CORR/SHUTTLE_GLOW_CONT (threshold 0.2).

Cutout to parent pixel: `x_orig = 1 + x_cutout - CRPIX1A`, `y_orig = 1 + y_cutout - CRPIX2A`.

## FLAGS bits

0 TRANSIENT, 1 OVERFLOW, 2 SUR_ERROR, 4 PHANTOM (QR2 hdr), 5 REFERENCE (QR2 hdr),
6 NONFUNC, 7 DICHROIC, 9 MISSING_DATA, 10 HOT, 11 COLD, 12 FULLSAMPLE, 13 SUR_MISMATCH,
14 PHANMISS, 15 NONLINEAR, 16 VAR_UNDER, 17 PERSIST, 18 PERSIST_UNK, 19 OUTLIER,
20 CROSSTALK, 21 SOURCE, 22 GHOST, 23 GHOST_FPA (unused), 24 GHOST_EXT, 25 STREAK,
26 BLOOM, 27 SNOWBALL, 28 HALO, 29 SATELLITE_HALO; tool output only: 32 CONTAINS_BAD_PIXEL,
33 FIT_ERROR. Clean measurement: flags == 0 or == 2097152 (SOURCE only).

Official exclusion sets: photometry fit ignores SUR_ERROR NONFUNC MISSING_DATA HOT COLD
NONLINEAR PERSIST BLOOM SNOWBALL HALO SATELLITE_HALO; mosaic tool also drops TRANSIENT
DICHROIC PHANMISS CROSSTALK GHOST GHOST_FPA GHOST_EXT STREAK and propagates OVERFLOW
SOURCE OUTLIER.

## Backgrounds and systematics

- ZODI: modified Kelsall 1998 + Tsumura 2013 spectrum, rescaled per wavelength on
  |b| > 30 deg data (`zodi_scaling_v2`); not subtracted; dominant noise source.
- Airglow: He 1.083 um (3-30x the zodi), aurora N2 (bands 1-2), lines at 0.78, 0.84,
  0.93, 1.13, 1.81, 2.63, 2.75, 4.03, 4.64 um; shuttle glow 3.0/4.5 um (RAM < 70 deg
  now enforced); Earthshine ~40x below zodi at LZA 42 deg. Templates provided, not subtracted.
- Artifacts: frame-edge and linear ghosts, ~10 arcmin dichroic ghosts (bands 3-6, sources
  > 100-10000 Jy), 8 deg ghost from very bright stars, Moon edge glow (bands 1,4,5,6),
  snowballs/halos/blooms (masked only from 2025W51 in QR2), crosstalk (masked from R7),
  persistence, satellite streaks near the noise.
- Astrometry RMS < 0.3 arcsec (FINAST 0); corner distortion ~13 px (SIP in header).
- Absolute calibration < 1% vs CALSPEC per the Supplement; users adopt 3-5% (QR2 gain),
  3% visit-to-visit RMS in quadrature (also applied by Level 3), 8% floor (JWST check).

## Official tools

Spectrophotometry Tool (`/applications/spherex/tool-spectrophotometry`): Tractor forced
photometry; point or Sersic (n 0.5-6, b/a, PA east of north, Re 1-20 arcsec); local
background from a 15-pixel box with known sources masked, ZODI unused; outputs wavelength,
flux (uJy), flux_err, lambda_width, flags, fit_ql (mean |data-model|/sigma within 2.5 px),
flux_bkg, lvf_id, det_id, deep_flg, mjd, data_collection, x_image, y_image; 20 targets per
job, 2 jobs at once, run time ~1.67 s per image + 50 s; companions must be listed to be
deblended. Mosaic Tool (`/applications/spherex/tool-mosaic`): IMAGE - ZODI, flag mask,
17-channel template, binning reprojection; IMAGE/NHITS/FLAGS cubes of the 102 channels;
pixel >= 6.15 arcsec, field <= 5 deg, all-sky frames only. No API for either.

## Unit conversions

MJy/sr to mJy per pixel: `value * 23.5045 * pixscale_arcsec**2 / 1000` (constant pixel);
better: multiply by the Solid Angle Pixel Map (arcsec^2) after converting MJy/sr to
uJy/arcsec^2 with astropy units, as the official Source Discovery tool does.

## Citation

"This publication makes use of data products from the Spectro-Photometer for the History
of the Universe, Epoch of Reionization and Ices Explorer (SPHEREx), which is a joint
project of the Jet Propulsion Laboratory and the California Institute of Technology, and
is funded by the National Aeronautics and Space Administration." Cite the release DOI,
Bock et al. 2026 (ApJ 999, 139), Akeson et al. 2026 (ApJS 285, 67), Korngut et al. 2026
(arXiv:2603.29835), Cukierman et al. 2026 (ApJS 286, 22) for mosaics.

## Links

- Mission page: https://irsa.ipac.caltech.edu/Missions/spherex.html
- QR overview and DOIs: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html
- Explanatory Supplement: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp_QR.pdf
- PSF header erratum: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/psfhdrerr.html
- Archive guide: https://caltech-ipac.github.io/spherex-archive-documentation/
- Tutorials: https://caltech-ipac.github.io/irsa-tutorials/spherex/
- Tool help: https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/sp.html and .../mosaic.html
- Cloud: https://irsa.ipac.caltech.edu/cloud_access/#spherex
