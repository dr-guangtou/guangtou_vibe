# SPHEREx IRSA Data Access - Quick Reference

## Quick Commands

### Query by Position (SIA - Simplest)
```python
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

coord = SkyCoord(ra=210.8, dec=54.3, unit='deg')
results = Irsa.query_sia(pos=(coord, 1*u.arcsec), collection='spherex_qr2')
url = results['access_url'][0]
```

### Query Cutouts (TAP - No Lag)
```python
import pyvo
service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")

query = f"""
SELECT 'https://irsa.ipac.caltech.edu/' || a.uri || 
       '?center={ra},{dec}d&size={size}' AS uri
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
  AND p.energy_bandpassname = 'SPHEREx-D2'
ORDER BY p.time_bounds_lower
"""
results = service.search(query)
```

### Read MEF with Retry
```python
from astropy.io import fits
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        hdulist = fits.open(url)
        break
    except (TimeoutError, urllib.error.HTTPError):
        if attempt == max_retries - 1:
            raise
        time.sleep(10 * (attempt + 1))
```

### Get Wavelength at Position
```python
from astropy.wcs import WCS
import astropy.units as u

# Spatial WCS
spatial_wcs = WCS(hdulist['IMAGE'].header)
x, y = spatial_wcs.world_to_pixel(coord)

# Spectral WCS
spectral_wcs = WCS(hdulist['IMAGE'].header, fobj=hdulist, key='W')
spectral_wcs.sip = None
wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
print(f"λ = {wavelength.to(u.um):.4f}")
```

## SPHEREx Detector Bands

| Band | λ (µm) | R | Query String |
|------|--------|---|--------------|
| D1 | 0.75–1.09 | ~39 | `SPHEREx-D1` |
| D2 | 1.10–1.62 | ~41 | `SPHEREx-D2` |
| D3 | 1.63–2.41 | ~41 | `SPHEREx-D3` |
| D4 | 2.42–3.82 | ~35 | `SPHEREx-D4` |
| D5 | 3.83–4.41 | ~112 | `SPHEREx-D5` |
| D6 | 4.42–5.00 | ~128 | `SPHEREx-D6` |

## MEF Structure

```
HDU 0: PRIMARY    - Metadata only
HDU 1: IMAGE      - Flux in MJy/sr (2040×2040)
HDU 2: FLAGS      - Per-pixel flags
HDU 3: VARIANCE   - Variance estimate
HDU 4: ZODI       - Zodiacal model (NOT subtracted)
HDU 5: PSF        - 3D cube, oversampled 10×
HDU 6: WCS-WAVE   - Spectral WCS lookup table
```

## Collections

| Collection | Description |
|------------|-------------|
| `spherex_qr2` | Wide Survey (current) |
| `spherex_qr2_deep` | Deep Survey |
| `spherex_qr2_cal` | Calibration files |

## Direct Cutout URL Format

```
https://irsa.ipac.caltech.edu/ibe/data/spherex/qr/level2/...
    /image.fits?center=RA,DEC&size=DEGREES
```

## Important Notes

- **Zodi NOT subtracted**: IMAGE extension contains un-subtracted zodiacal light
- **SIA lag**: ~1 day after weekly ingestion; use TAP for immediate access
- **Timeout**: Increase to 120s: `astropy.utils.data.conf.remote_timeout = 120`
- **PSF zones**: QR2 uses 11×11 grid (121 zones), each 101×101 pixels
- **Versions**: Check `hdulist[0].header['VERSION']` for PSF header fixes needed

## Citation

```
This publication makes use of data products from the 
Spectro-Photometer for the History of the Universe, 
Epoch of Reionization and Ices Explorer (SPHEREx), 
which is a joint project of the Jet Propulsion 
Laboratory and the California Institute of Technology, 
and is funded by the National Aeronautics and Space 
Administration.
```

**DOI**: 10.26131/IRSA652 (QR2)

## Links

- **Data Explorer**: https://irsa.ipac.caltech.edu/applications/spherex
- **Tutorials**: https://caltech-ipac.github.io/irsa-tutorials/spherex/
- **Documentation**: https://caltech-ipac.github.io/spherex-archive-documentation/
