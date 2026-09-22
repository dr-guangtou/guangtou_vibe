---
name: sdss-iv-spectra
title: SDSS-I–IV Optical Spectra (Legacy / BOSS / eBOSS)
description: Use when working with SDSS spectra (Legacy, BOSS, eBOSS).
version: 1.0.0
author: Song Huang
license: MIT
tags: [astronomy, sdss, spectroscopy, fits, boss, eboss, legacy, astroquery, dr17]
metadata:
  hermes:
    tags: [astronomy, sdss, spectroscopy, fits, boss, eboss, legacy, astroquery, dr17]
    related_skills: [hsc-survey-data]
---

# SDSS-I–IV Optical Spectra (Legacy / BOSS / eBOSS)

## When to Use

Use this skill whenever a task involves SDSS-I to IV single-fiber optical spectra (Legacy, SEGUE, BOSS, eBOSS/SEQUELS/TDSS/SPIDERS): understanding survey context, locating and downloading FITS spectra from the SAS, reading the files, applying quality cuts, or checking known caveats. **Not** for MaNGA (IFU), APOGEE (NIR), or MaStar.

Single-fiber optical spectra from the Sloan Digital Sky Survey: **Legacy (SDSS-I/II), SEGUE, BOSS (SDSS-III), and eBOSS/SEQUELS/TDSS/SPIDERS (SDSS-IV)** — i.e. the two fiber spectrographs at APO. **Not** MaNGA (IFU), APOGEE (NIR), or MaStar. **DR17 is the final release** of SDSS-IV (data through Jan 2021; cumulative, includes all prior releases). Citation: Abdurro'uf et al. 2022, ApJS, 259, 35.

## 1. Survey context

- **SDSS spectrograph** (SDSS-I/II, DR1–8): Legacy + SEGUE-1/2. 640 fibers/plate, 3″ fibers, 3800–9200 Å, R ≈ 1500–2500, log10 pixel spacing 0.0001 dex.
- **BOSS spectrograph** (SDSS-III/IV, DR9+): BOSS + eBOSS + SEQUELS/TDSS/SPIDERS. 1000 fibers/plate, 2″ fibers, 3650–10,400 Å, R ≈ 1560–2270.
- Flux units: **10⁻¹⁷ erg s⁻¹ cm⁻² Å⁻¹**. Wavelengths are **vacuum**, heliocentric, corrected to the barycenter at exposure midpoint.
- **Plate geometry:** plates are 1.49° radius; min fiber separation 55″ (SDSS) / 62″ (BOSS); nothing closer than 100″ to plate center.
- **Plate-number ranges:** Legacy/SEGUE-1 = 266–2974 (SDSS spectrograph), SEGUE-2 = 3000–3509, BOSS/eBOSS = 3510+ (eBOSS plates mostly ≥ 10000).
- **DR17 scope (verified stats):** 5,789,200 total spectra; 4,846,156 useful; 2,863,635 galaxies; 960,678 quasars; 1,021,843 stars; 475,531 sky. BOSS/eBOSS: 3,946 plates (3,803 unique), 3,946,000 spectra (3,518,265 unique) — CMASS 980,922, LOWZ 374,913, eBOSS LRG 298,762, eBOSS ELG 269,889, quasars 1,032,126. SEGUE: 229 plates, 155,520 spectra (138,099 unique objects).

## 2. Identifiers (memorize these)

A spectrum is uniquely identified by **(plate, MJD, fiberID)**:
- `plate` = plug plate number; `MJD` = Modified Julian Date of the night (plates re-observed get new MJDs); `fiberID` = 1–640 (SDSS) or 1–1000 (BOSS).
- `specObjID` = 64-bit hash of (plate, MJD, fiberID, run2d) — the join key in SkyServer/CAS tables.
- `run2d` = reduction version: **26** (Legacy/SEGUE-1), **103** (stellar-cluster plates), **104** (SEGUE-2), **v5_13_2** (all BOSS/eBOSS in DR17; v5_13_0 = DR16, v5_10_0 = DR14, v5_5_12 = DR10, v5_4_45 = DR9).
- `survey`/`programname` tags select subsamples: `sdss`, `segue1`, `segue2`, `boss`, `eboss` (e.g. eBOSS LSS data = survey `eboss`, program `eboss`).

## 3. Data access

**Portals**
- SkyServer (CAS SQL): https://skyserver.sdss.org/dr17/ — `specObj` view / `specObjAll` table, Quick Look, Explore.
- CasJobs: https://skyserver.sdss.org/casjobs/ (bulk SQL; choose DR17 context; use for big queries — SkyServer SQL search has a ~4 MB response limit).
- Interactive webapp: https://dr17.sdss.org/optical/plate/search and /optical/spectrum/search (view + wget/rsync download).
- **Data model:** https://data.sdss.org/datamodel/ (file schemas; e.g. `files/SPECTRO_REDUX/RUN2D/spectra/PLATE4/spec.html`).
- **FITS tree:** https://data.sdss.org/sas/dr17/

**SAS catalog files** (in `/sas/dr17/sdss/spectro/redux/`)
- `specObj-dr17.fits` (6.7 GB; redshifts+classifications of all spectra; BOSS-only and SDSS-only splits also available), `plates-dr17.fits` (3.7 MB), `photoPlate-dr17.fits` / `photoPosPlate-dr17.fits` (photometric matches, 17.5 GB each).
- Per-reduction: `spAll-v5_13_2.fits` (16 GB, BOSS/eBOSS all-spectra params), `platelist.fits`, `platequality.txt`, `spAllLine-v5_13_2.fits`.

**Individual spectra — verified URL patterns (DR17):**
```
Legacy/SEGUE:  https://data.sdss.org/sas/dr17/sdss/spectro/redux/{run2d}/spectra/{plate:04d}/spec-{plate}-{mjd}-{fiber:04d}.fits
  e.g. https://data.sdss.org/sas/dr17/sdss/spectro/redux/26/spectra/0266/spec-0266-51602-0001.fits   (708 KB)

BOSS/eBOSS lite: https://data.sdss.org/sas/dr17/eboss/spectro/redux/v5_13_2/spectra/lite/{plate}/spec-{plate}-{mjd}-{fiber:04d}.fits
BOSS/eBOSS full: https://data.sdss.org/sas/dr17/eboss/spectro/redux/v5_13_2/spectra/full/{plate}/spec-{plate}-{mjd}-{fiber:04d}.fits
  e.g. https://data.sdss.org/sas/dr17/eboss/spectro/redux/v5_13_2/spectra/lite/4055/spec-4055-55359-0001.fits   (213 KB)
       https://data.sdss.org/sas/dr17/eboss/spectro/redux/v5_13_2/spectra/full/4055/spec-4055-55359-0001.fits  (1.4 MB)
```
- Legacy dirs/filenames zero-pad the plate to 4 digits (e.g. `0266`); BOSS/eBOSS use the plain plate number, fiber always 4-digit padded.
- **lite = recommended default** (coadded spectrum + catalog row; ~0.2 MB); **full** adds all individual-exposure frames (~1.5 MB).
- The same `v5_13_2` tree is mirrored under `/sas/dr17/sdss/spectro/redux/v5_13_2/`.
- Older releases: DR16 eBOSS used `.../eboss/spectro/redux/final/spectra/...`; earlier DRs used `spectra/{plate4}/{plate}/` (plate4 = plate//1000*1000) — check the release's own tree.
- spPlate coadd files: `redux/{run2d}/{plate}/spPlate-{plate}-{mjd}.fits` (~60 MB; all 640/1000 fibers of one plate-MJD in one file).
- Checksums: `{dir}/**/*.sha1sum` files next to the data (e.g. `eboss_spectro_redux_v5_13_2.sha1sum`).

**astroquery** (docs: https://astroquery.readthedocs.io/en/latest/sdss/sdss.html)
```python
from astroquery.sdss import SDSS
from astropy.coordinates import SkyCoord

pos = SkyCoord('0h8m05.63s +14d50m23.3s', frame='icrs')
xid = SDSS.query_region(pos, radius='5 arcsec', spectro=True)   # cone (radius ≤ 3 arcmin) or box (width/height)
sp  = SDSS.get_spectra(plate=4055, mjd=55359, fiber=1)          # or matches=xid, or via coordinates
tpl = SDSS.get_spectral_template('galaxy')                      # DR7-era templates only!
```
- astroquery defaults to DR17; `SDSS.clear_cache()` fixes stale results. Needs a consistent astropy/pyvo environment (system Python 3.9 here has a pyvo↔astropy conflict — use a proper research env or the direct-URL method below).

## 4. FITS structure (verified on real DR17 files)

**Individual spec file** (DR17, both Legacy and BOSS — binary-table format):
- HDU0: primary header (MJD, FIBERID, RA, DEC, RUN2D, ...; observing metadata).
- HDU1 `COADD`: coadded spectrum as a **binary table** — columns `flux, loglam, ivar, and_mask, or_mask, wdisp, sky, model` (n ≈ 3835 px Legacy, 4608 px BOSS).
- HDU2 `SPALL` (BOSS) / `SPECOBJ` (Legacy): the full spAll row — class, z, zErr, zWarning, snMedian, targets, etc.
- HDU3 `SPZLINE`: emission/absorption line fits (LINENAME, LINEWAVE, LINEZ, LINEZ_ERR, LINESIGMA, ...).
- HDU4+: per-exposure cframe tables (`B1-*`, `R1-*`) — **full files only**; each has flux, loglam, ivar, mask, wdisp, sky, calib.

**spPlate coadd file** (image format, all fibers): HDU0 flux image (NPIX × nfibers), HDU1 ivar, HDU2 andmask (int32), HDU3 ormask, HDU4 wdisp, HDU5 plug-map table (OBJID, RA, DEC, MAG, FIBERID, PRIMTARGET, ...), HDU6 sky.

**Older format caveat:** DR7-era spSpec files and pre-DR16 BOSS spec files used separate image HDUs (`FLUX, LOGLAM, IVAR, ANDMASK, ORMASK` [+SKY, MODEL]) with wavelengths from `COEFF0`/`COEFF1` header keywords (λ = 10^(COEFF0 + COEFF1·i)). Write readers that branch on HDU type.

```python
from astropy.io import fits
hdu = fits.open('spec-4055-55359-0001.fits')
tab = hdu['COADD'].data                     # or hdu[1].data
wave = 10 ** tab['loglam']                  # vacuum, heliocentric
flux = tab['flux'] * 1e-17                  # erg/s/cm2/A
ivar = tab['ivar']                          # 1/sigma^2; 0 = masked pixel
mask = tab['and_mask']                      # SPPIXMASK; use AND mask
row  = hdu['SPALL'].data                    # z, class, zWarning, targets...
```

## 5. Catalog selection & quality cuts

Use the `specObj` view / `specObjAll` table (CAS) or `spAll` (SAS). Key columns: `plate, mjd, fiberid, specobjid, ra, dec, class, subclass, z, zErr, zWarning, snMedian, sciencePrimary, velDisp` (+ `*_NOQSO` variants for BOSS).

- **Unique objects:** `sciencePrimary = 1` (best of repeated observations, 2″ grouping). Subset flags: `sdssPrimary, legacyPrimary, bossPrimary, seguePrimary, segue1Primary, segue2Primary`.
- **Good redshifts:** `zWarning = 0` or `= 16` (16 = MANY_OUTLIERS, benign — commonly set on high-S/N stars and broad-line AGN). Any other bit → treat classification/redshift with care.
- **BOSS galaxy targets:** trust `Z_NOQSO / Z_ERR_NOQSO / ZWARNING_NOQSO / CLASS_NOQSO` (avoids spurious QSO-template fits). Best classification for BOSS galaxies: `CLASS_NOQSO`.
- **Plate quality:** `platequality` = good/marginal/bad; `isPrimary` / `isBest` per plate-MJD; avoid "bad" plates unless necessary (some good redshifts exist there).
- **eBOSS:** pipeline z ≠ final LSS redshifts — use the DR16/DR17 clustering catalogs for cosmology samples (https://www.sdss4.org/dr17/spectro/lss/).
- CLASS values: `GALAXY` (subclasses STARFORMING, STARBURST, AGN, BROADLINE), `QSO`, `STAR` (O…M/T subclasses, Carbon, CV, etc.).
- Sky/standard fibers are present in all files (class `SKY`, `STD`) — exclude via `specClass`/`class`.

**Galaxy value-added catalogs (https://www.sdss4.org/dr17/spectro/galaxy/):** Portsmouth SED-fit stellar masses + kinematics/emission lines (GANDALF/pPXF), Wisconsin PCA masses + velocity dispersions, Granada FSPS masses, MPA-JHU (DR8 only, deprecated), eBOSS FIREFLY VAC (DR16 eBOSS). Standard galaxy sample cut: `CLASS_NOQSO='galaxy' AND ZWARNING_NOQSO=0 AND (Z_NOQSO > Z_ERR_NOQSO > 0)`.

## 6. Bitmasks (official DR17 values)

**ZWARNING** (spectrum-level; value = 2^bit):
| Bit | Value | Meaning |
|---|---|---|
| 0 | 1 | SKY (sky fiber) |
| 1 | 2 | LITTLE_COVERAGE (wavelength coverage < 0.18) |
| 2 | 4 | SMALL_DELTA_CHI2 (best fit too close to 2nd) |
| 3 | 8 | NEGATIVE_MODEL (stars/QSOs only) |
| 4 | 16 | MANY_OUTLIERS (benign; >5% of pixels >5σ) |
| 5 | 32 | Z_FITLIMIT (Z_ERR = -1) |
| 6 | 64 | NEGATIVE_EMISSION (QSO lines) |
| 7 | 128 | UNPLUGGED |
| 8 | 256 | BAD_TARGET |
| 9 | 512 | NODATA |

**SPPIXMASK** (pixel-level; use the AND mask): common bits — 0 NOPLUG, 2 BADFLAT, 3 BADARC, 7 BADSKYFIBER, 9 WHOPPER (bright-star crosstalk), 14 SATURATION, 15 BADPIX, 16 COSMIC, 18 FULLREJECT (ivar=0), 19 PARTIALREJECT, 21 CROSSTALK, 22 NOSKY (ivar=0), 23 BRIGHTSKY, 25 COMBINEREJ, 26 BADFLUXFACTOR. Full tables: https://www.sdss4.org/dr17/algorithms/bitmasks/

## 7. Known issues / caveats (digest of https://www.sdss4.org/dr17/spectro/caveats/)

**All spectra:** spectra are NOT corrected for Galactic extinction (apply SFD E(B-V) yourself); night-sky emission lines + imperfect sky subtraction (mask via ivar/NOSKY/BRIGHTSKY); coadd errors are approximate; σ_* only reliable above ~70 km/s; some lines clipped at the chip gap; spectrophotometric calibration can imprint artificial Balmer lines; a few missing/corrupted files on SAS (list on the caveats page).

**BOSS/eBOSS:** galaxy targets fitted to QSO templates with unphysical parameters (→ use NOQSO values); QSO flux calibration wrong for DR12 and earlier; a bad CCD column produced bogus z>5 QSOs; BPT classes in `emissionLinesPort` can be wrong for some objects; artificial 6000 Å features from bright-star crosstalk; QSO fibers with washers (ZOFFSET records intended, not actual, offset — check `washers.par`); one eFEDS plate missing in DR17; bad plates in eFEDS.

**Specific plates:** 6138/56598 had corrupt header (delete `EXPID` on read; fixed DR16); 389 & 2338 lost second-night data (spPlate duplicates); 3770/55234 bad sky for fibers ≤ 500.

**SEGUE:** duplicates, quality cuts, and observational biases documented on the caveats page.

**DR16-era spec-file quirks (fixed in DR17):** `flux`/`ivar` columns uppercase in some plates, lowercase in others; full-dir files lost per-exposure HDU headers (recover from spCFrame).

## 8. Pitfalls checklist

- Zero-padding: legacy `0266` vs BOSS `4055`; fiber always 4-digit (`0001`).
- `run2d` must match the file's reduction (26/103/104 vs v5_13_2) — never mix.
- Wavelengths are **vacuum** — convert to air to compare with lab line lists: AIR = VAC / (1 + 5.792105e-2/(238.0185 - (1e4/VAC)²) + 1.67917e-3/(57.362 - (1e4/VAC)²)).
- Fluxes are per-fiber aperture (3″/2″), not total; `fiber2`/`fiberMag` corrections for totals.
- Repeated observations: same plate, different MJD → different fiber layouts; dedupe with sciencePrimary.
- Fiber collisions mean you cannot get spectra of close pairs (55″/62″).
- Sky and standard-star fibers are interleaved — filter them out of samples.

## 9. References

- DR17 home: https://www.sdss4.org/dr17/ · Spectro overview: https://www.sdss4.org/dr17/spectro/
- Basics: https://www.sdss4.org/dr17/spectro/spectro_basics/ · Access: https://www.sdss4.org/dr17/spectro/spectro_access/
- Catalogs: https://www.sdss4.org/dr17/spectro/catalogs/ · Caveats: https://www.sdss4.org/dr17/spectro/caveats/
- Galaxy VACs: https://www.sdss4.org/dr17/spectro/galaxy/ · Pipeline: https://www.sdss4.org/dr17/spectro/pipeline/
- Bitmasks: https://www.sdss4.org/dr17/algorithms/bitmasks/ · LSS/clustering: https://www.sdss4.org/dr17/spectro/lss/
- Data model: https://data.sdss.org/datamodel/ · SAS tree: https://data.sdss.org/sas/dr17/
- astroquery SDSS: https://astroquery.readthedocs.io/en/latest/sdss/sdss.html
- DR17 paper: Abdurro'uf et al. 2022, ApJS, 259, 35 · Bolton et al. 2012 (BOSS pipeline), AJ, 144, 144
