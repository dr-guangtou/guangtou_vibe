---
name: spherex-irsa-access
description: Access and analyze SPHEREx spectrophotometric data from IRSA (NASA/IPAC Infrared Science Archive)
category: astronomy
tags: [spherex, irsa, spectroscopy, nasa, infrared, astroquery, tap]
author: Song Huang
date: 2026-03-30
version: 1.0.0
requirements:
  - astroquery>=0.4.7
  - pyvo>=1.5
  - astropy>=5.0
  - numpy
  - matplotlib
  - firefly-client (optional, for visualization)
---

# SPHEREx IRSA Data Access Skill

Access SPHEREx (Spectro-Photometer for the History of the Universe, Epoch of Reionization, and Ices Explorer) data hosted by the NASA/IPAC Infrared Science Archive (IRSA).

## Overview

SPHEREx is a NASA Astrophysics Medium Explorer mission launched in March 2025 that provides:
- **Wavelength coverage**: 0.75–5.0 µm near-infrared spectroscopy
- **Spectral resolution**: R ≈ 40–150 (varies by band)
- **Survey area**: All-sky with deeper data in SPHEREx Deep Fields
- **Data releases**: Weekly Quick Release (QR) products

### SPHEREx Detector Bands

| Band | Wavelength (µm) | Spectral Resolution (R) | Detector |
|------|-----------------|------------------------|----------|
| 1 | 0.75 – 1.09 | ~39 | Short-wavelength |
| 2 | 1.10 – 1.62 | ~41 | Short-wavelength |
| 3 | 1.63 – 2.41 | ~41 | Short-wavelength |
| 4 | 2.42 – 3.82 | ~35 | Long-wavelength |
| 5 | 3.83 – 4.41 | ~112 | Long-wavelength |
| 6 | 4.42 – 5.00 | ~128 | Long-wavelength |

## Data Products

### Main Product: Spectral Image MEF (Multi-Extension FITS)

Each Level 2 Spectral Image file contains:

| Extension | Name | Description |
|-----------|------|-------------|
| 0 | PRIMARY | Minimal metadata, no data |
| 1 | IMAGE | Calibrated flux in MJy/sr (2040×2040) |
| 2 | FLAGS | Per-pixel status/processing flags |
| 3 | VARIANCE | Per-pixel variance estimate |
| 4 | ZODI | Zodiacal dust background model (NOT subtracted) |
| 5 | PSF | 3D cube of Point Spread Functions |
| 6 | WCS-WAVE | Spectral WCS lookup table |

**Important Notes:**
- Zodiacal light model is provided but NOT subtracted from IMAGE
- PSF is oversampled by factor of 10 (101×101 pixels ≈ 10×10 SPHEREx pixels)
- Spectral WCS uses WAVE-TAB lookup table mechanism due to Linear Variable Filters

### Data Releases

- **QR2** (Quick Release 2): Current release with improved calibrations (October 2025+)
- **QR1**: Retired (July–October 2025)
- **DOI**: 10.26131/IRSA652 (cite this when using QR2 data)

## API Access Methods

### Method 1: SIA (Simple Image Access) via astroquery

Best for: Simple queries by position

```python
from astroquery.ipac.irsa import Irsa
from astropy.coordinates import SkyCoord
import astropy.units as u

# Define coordinates
coord = SkyCoord(ra=210.80227, dec=54.34895, unit='deg')
search_radius = 1 * u.arcsec

# Query for spectral images
results = Irsa.query_sia(
    pos=(coord, search_radius),
    collection='spherex_qr2'  # or 'spherex_qr2_deep' for Deep Survey
)

# Access URL for first result
url = results['access_url'][0]
```

**Available Collections:**
- `spherex_qr2`: Wide Survey spectral images
- `spherex_qr2_deep`: Deep Survey spectral images  
- `spherex_qr2_cal`: Calibration files

**Note:** SIA has ~1 day lag after weekly data ingestion.

### Method 2: TAP (Table Access Protocol) via pyvo

Best for: Immediate access to newly ingested data, complex queries

```python
import pyvo
from astropy.coordinates import SkyCoord
import astropy.units as u

# Define TAP service
service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")

# Define coordinates and cutout parameters
ra = 210.80227 * u.degree
dec = 54.34895 * u.degree
size = 0.1 * u.degree
bandpass = 'SPHEREx-D2'

# Build TAP query
query = f"""
SELECT
    'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra.value},{dec.value}d&size={size.value}' AS uri,
    p.time_bounds_lower
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
WHERE 1 = CONTAINS(POINT('ICRS', {ra.value}, {dec.value}), p.poly)
        AND p.energy_bandpassname = '{bandpass}'
ORDER BY p.time_bounds_lower
"""

# Execute query
results = service.search(query)
```

### Method 3: Direct Cutout URL

Best for: Direct file access when you have the base URL

```python
import requests

# Append cutout parameters to base URL
cutout_url = (
    "https://irsa.ipac.caltech.edu/ibe/data/spherex/qr/level2/.../image.fits"
    "?center=156.09328159,-41.64466331&size=0.1"
)

response = requests.get(cutout_url)
with open('cutout.fits', 'wb') as f:
    f.write(response.content)
```

## Working with SPHEREx Data in Python

### Reading MEF Files

```python
from astropy.io import fits
from astropy.wcs import WCS
import time
import urllib.error
import http.client

# Increase timeout for large files
from astropy.utils.data import conf
conf.remote_timeout = 120

# Load with retry logic for transient errors
max_retries = 3
for attempt in range(max_retries):
    try:
        hdulist = fits.open(url)
        break
    except (TimeoutError, urllib.error.HTTPError, http.client.IncompleteRead):
        if attempt == max_retries - 1:
            raise
        time.sleep(10 * (attempt + 1))

# Examine structure
hdulist.info()
```

### Working with Spatial WCS

```python
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord

# Load spatial WCS from IMAGE header
header = hdulist['IMAGE'].header
spatial_wcs = WCS(header)

# Convert world to pixel coordinates
coord = SkyCoord(ra=210.80227, dec=54.34895, unit='deg')
x, y = spatial_wcs.world_to_pixel(coord)

# Convert pixel to world
ra, dec = spatial_wcs.pixel_to_world(x, y)
```

### Working with Spectral WCS

```python
# Load spectral WCS (requires full HDUList for lookup table)
spectral_wcs = WCS(header, fobj=hdulist, key='W')

# Disable SIP for spectral WCS (not applicable)
spectral_wcs.sip = None

# Get wavelength and bandwidth at pixel coordinates
wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
print(f"Wavelength: {wavelength.to(u.micrometer):.4f}")
print(f"Bandwidth: {bandwidth.to(u.micrometer):.4f}")
```

### Working with PSF Extensions

```python
import numpy as np

# Load PSF cube
psf_cube = hdulist['PSF'].data  # Shape: (121, 101, 101) for QR2
psf_header = hdulist['PSF'].header

# PSF is oversampled by 10x
oversampling = psf_header['OVERSAMP']  # = 10

# Find appropriate PSF zone for given coordinates
# QR2 uses 11x11 grid (121 zones total)
# Zone centers: XCTR_i, YCTR_i where i=1 to 121
# Zone widths: XWID_i, YWID_i

# Get zone indices from spatial WCS
x_idx = int(x / (2040 / 11))  # Approximate
y_idx = int(y / (2040 / 11))
zone_index = y_idx * 11 + x_idx

# Extract PSF for this zone
psf = psf_cube[zone_index]
```

**⚠️ Important PSF Header Note (versions ≤ 6.5.5):**
Earlier versions had incorrect PSF zone indexing. Check version:
```python
from packaging.version import Version
version = Version(hdulist[0].header['VERSION'])
if version <= Version('6.5.5') and 'psffix1' not in str(version.local):
    # Need header fix - see references/spherex_psf_header_fix.py
    pass
```

### Creating and Packaging Cutouts

```python
from astropy.table import Table
import concurrent.futures

def process_cutout(row, ra, dec, cache=False):
    """Process a single cutout and extract wavelength."""
    from astropy.wcs import WCS
    from astropy.coordinates import SkyCoord
    
    with fits.open(row['uri'], cache=cache) as hdul:
        header = hdul['IMAGE'].header
        
        # Get pixel coordinates
        spatial_wcs = WCS(header)
        x, y = spatial_wcs.world_to_pixel(
            SkyCoord(ra=ra, dec=dec, unit='deg', frame='icrs')
        )
        
        # Get wavelength at position
        spectral_wcs = WCS(header, fobj=hdul, key='W')
        spectral_wcs.sip = None
        wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
        row['central_wavelength'] = wavelength.to(u.micrometer).value
        
        # Collect HDUs
        hdus = []
        for hdu in hdul[1:]:  # Skip primary
            hdu.header['EXTNAME'] = f"{hdu.header['EXTNAME']}{row['cutout_index']}"
            hdus.append(hdu.copy())
        row['hdus'] = hdus

# Serial processing
for row in results_table:
    process_cutout(row, ra, dec, cache=False)

# Parallel processing (faster)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(process_cutout, row, ra, dec, False)
        for row in results_table
    ]
    concurrent.futures.wait(futures)
```

### Writing Combined MEF

```python
# Create summary table
cols = fits.ColDefs([
    fits.Column(name='cutout_index', format='J', array=results_table['cutout_index']),
    fits.Column(name='observation_date', format='D', array=results_table['time_bounds_lower'], unit='d'),
    fits.Column(name='central_wavelength', format='D', array=results_table['central_wavelength'], unit='um'),
    fits.Column(name='access_url', format='A200', array=results_table['uri']),
])
table_hdu = fits.BinTableHDU.from_columns(cols)
table_hdu.header['EXTNAME'] = 'CUTOUT_INFO'

# Combine all HDUs
primary_hdu = fits.PrimaryHDU()
hdulist_list = [primary_hdu, table_hdu]
for fits_hdulist in results_table['hdus']:
    hdulist_list.extend(fits_hdulist)

combined_hdulist = fits.HDUList(hdulist_list)
combined_hdulist.writeto('spherex_cutouts.fits', overwrite=True)
```

## Visualization with Firefly

```python
from firefly_client import FireflyClient

# Initialize Firefly client
fc = FireflyClient.make_client(url='https://irsa.ipac.caltech.edu/irsaviewer')
fc.reinit_viewer()

# Display spectral image
fc.show_fits_image(
    file_input=url,
    plot_id='spectral_image',
    Title='SPHEREx Spectral Image'
)
```

Firefly understands SPHEREx alternative WCS coordinates, allowing you to see wavelength and bandwidth variations across pixels.

## Data Acknowledgment

When using SPHEREx QR data, include:

```
This publication makes use of data products from the Spectro-Photometer for 
the History of the Universe, Epoch of Reionization and Ices Explorer (SPHEREx), 
which is a joint project of the Jet Propulsion Laboratory and the California 
Institute of Technology, and is funded by the National Aeronautics and Space 
Administration.
```

**DOI**: 10.26131/IRSA652 (for QR2)

## Common Issues and Solutions

### Issue: Timeout errors
**Solution:** Increase astropy timeout and implement retry logic:
```python
from astropy.utils.data import conf
conf.remote_timeout = 120  # seconds
```

### Issue: SIA data not found (recent ingestion)
**Solution:** Use TAP queries instead - SIA has ~1 day lag:
```python
# Use pyvo TAP instead of SIA for latest data
service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")
```

### Issue: PSF zone mismatch (old data)
**Solution:** Check version and apply header fix if needed (see references/)

### Issue: Large cache files
**Solution:** Disable caching:
```python
fits.open(url, cache=False)
```

## External Resources

- **SPHEREx Mission**: https://spherex.caltech.edu/
- **IRSA SPHEREx**: https://irsa.ipac.caltech.edu/Missions/spherex.html
- **Data Explorer**: https://irsa.ipac.caltech.edu/applications/spherex
- **Tutorials**: https://caltech-ipac.github.io/irsa-tutorials/spherex/
- **Documentation**: https://caltech-ipac.github.io/spherex-archive-documentation/
- **Explanatory Supplement**: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/SPHEREx_Expsupp_QR.pdf

## References

- SPHEREx Explanatory Supplement (QR2)
- IRSA SPHEREx Archive User Guide
- IVOA SIA Protocol Specification
- FITS WCS Paper III (Spectral coordinates)
