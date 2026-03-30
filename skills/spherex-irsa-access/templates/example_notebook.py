"""
SPHEREx Data Access Example Notebook (Python script version)
============================================================

This script demonstrates common SPHEREx data access patterns.
Convert to Jupyter notebook with: jupytext --to notebook example_notebook.py

Requirements:
    pip install astroquery pyvo astropy matplotlib numpy
"""

# %% [markdown]
# # SPHEREx Data Access Tutorial
# 
# This notebook demonstrates how to:
# 1. Query SPHEREx spectral images using SIA and TAP
# 2. Download and read MEF files
# 3. Work with spatial and spectral WCS
# 4. Extract cutouts and package them
# 5. Work with PSF models

# %%
# Imports
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.table import Table
import astropy.units as u
from astroquery.ipac.irsa import Irsa
import pyvo

# Increase timeout for large files
from astropy.utils.data import conf
conf.remote_timeout = 120

# Suppress astropy warnings about alternative WCS
import logging
logging.getLogger('astropy').setLevel(logging.ERROR)

print("Imports complete!")

# %% [markdown]
# ## 1. Query SPHEREx Data with SIA (Simple Image Access)
# 
# SIA is the simplest method for querying by position.
# Note: SIA has ~1 day lag after weekly data ingestion.

# %%
# Define coordinates (example: M101 Pinwheel Galaxy)
ra = 210.80227
dec = 54.34895
coord = SkyCoord(ra=ra, dec=dec, unit='deg')
search_radius = 1 * u.arcsec

print(f"Querying position: RA={ra}, Dec={dec}")

# Query for wide survey data
results_sia = Irsa.query_sia(
    pos=(coord, search_radius),
    collection='spherex_qr2'
)

print(f"Found {len(results_sia)} images")
print(f"\nColumns: {results_sia.colnames}")

# %%
# Display first result
if len(results_sia) > 0:
    print("\nFirst result:")
    for col in ['access_url', 'obs_title', 'energy_bandpassname', 'time_bounds_lower']:
        if col in results_sia.colnames:
            print(f"  {col}: {results_sia[col][0]}")

# %% [markdown]
# ## 2. Query with TAP (Table Access Protocol)
# 
# TAP provides immediate access to newly ingested data (no SIA lag).
# It also allows more complex queries.

# %%
# Define TAP service
service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")

# Define cutout parameters
cutout_size = 0.1 * u.degree
bandpass = 'SPHEREx-D2'

# Build TAP query for cutouts
query = f"""
SELECT
    'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={cutout_size.value}' AS uri,
    p.time_bounds_lower,
    p.energy_bandpassname
FROM spherex.artifact a
JOIN spherex.plane p ON a.planeid = p.planeid
WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
        AND p.energy_bandpassname = '{bandpass}'
ORDER BY p.time_bounds_lower
"""

results_tap = service.search(query)
print(f"TAP query found {len(results_tap)} cutouts")

# %% [markdown]
# ## 3. Read and Inspect a SPHEREx MEF File

# %%
import time
import urllib.error
import http.client

# Get URL from SIA results
if len(results_sia) > 0:
    url = results_sia['access_url'][0]
    print(f"Loading: {url}")
    
    # Load with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            hdulist = fits.open(url)
            break
        except (TimeoutError, urllib.error.HTTPError, http.client.IncompleteRead):
            if attempt == max_retries - 1:
                raise
            time.sleep(10 * (attempt + 1))
    
    # Display structure
    print("\nFile structure:")
    hdulist.info()

# %% [markdown]
# ## 4. Work with WCS (World Coordinate System)

# %%
if len(results_sia) > 0:
    # Get IMAGE header
    image_header = hdulist['IMAGE'].header
    
    # Spatial WCS
    spatial_wcs = WCS(image_header)
    print("Spatial WCS:")
    print(spatial_wcs)
    
    # Convert world to pixel
    x, y = spatial_wcs.world_to_pixel(coord)
    print(f"\nPixel coordinates at ({ra}, {dec}): ({x:.2f}, {y:.2f})")
    
    # Spectral WCS
    spectral_wcs = WCS(image_header, fobj=hdulist, key='W')
    spectral_wcs.sip = None  # Disable SIP for spectral WCS
    
    # Get wavelength at position
    wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
    print(f"\nAt pixel ({x:.1f}, {y:.1f}):")
    print(f"  Wavelength: {wavelength.to(u.micrometer):.4f}")
    print(f"  Bandwidth: {bandwidth.to(u.micrometer):.4f}")

# %% [markdown]
# ## 5. Visualize Image Data

# %%
if len(results_sia) > 0:
    # Get image data
    image_data = hdulist['IMAGE'].data
    
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # Display image (using log scale)
    vmin, vmax = np.percentile(image_data, [1, 99])
    im = ax.imshow(image_data, origin='lower', vmin=vmin, vmax=vmax, cmap='viridis')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Surface Brightness (MJy/sr)')
    
    # Labels
    ax.set_xlabel('Pixel X')
    ax.set_ylabel('Pixel Y')
    ax.set_title(f'SPHEREx Spectral Image - Detector {image_header.get("DETECTOR", "Unknown")}')
    
    plt.tight_layout()
    plt.savefig('spherex_example_image.png', dpi=150)
    plt.show()
    print("Image saved to spherex_example_image.png")

# %% [markdown]
# ## 6. Work with PSF Cube

# %%
if len(results_sia) > 0 and 'PSF' in hdulist:
    psf_cube = hdulist['PSF'].data
    psf_header = hdulist['PSF'].header
    
    print(f"PSF cube shape: {psf_cube.shape}")
    print(f"Oversampling factor: {psf_header.get('OVERSAMP', 'N/A')}")
    
    # Find zone index for our position (approximate)
    n_zones = psf_cube.shape[0]
    grid_size = int(np.sqrt(n_zones))  # Usually 11 for QR2
    
    zone_x = int(x / (2040 / grid_size))
    zone_y = int(y / (2040 / grid_size))
    zone_index = zone_y * grid_size + zone_x
    zone_index = min(zone_index, n_zones - 1)  # Ensure valid index
    
    print(f"\nApproximate zone: ({zone_x}, {zone_y}) -> index {zone_index}")
    
    # Extract and plot PSF
    psf = psf_cube[zone_index]
    
    fig, ax = plt.subplots(1, 1, figsize=(6, 6))
    im = ax.imshow(psf, origin='lower', cmap='hot')
    ax.set_title(f'PSF for Zone {zone_index}')
    plt.colorbar(im, ax=ax)
    plt.tight_layout()
    plt.savefig('spherex_example_psf.png', dpi=150)
    plt.show()

# %% [markdown]
# ## 7. Extract a Spectrum from Cutouts
# 
# This example shows how to get multiple cutouts and extract a spectrum.

# %%
# Get cutout URLs from TAP results
if len(results_tap) > 0:
    n_cutouts = min(10, len(results_tap))  # Process first 10
    
    wavelengths = []
    fluxes = []
    
    print(f"Processing {n_cutouts} cutouts...")
    
    for i in range(n_cutouts):
        url = results_tap['uri'][i]
        
        try:
            with fits.open(url, cache=False) as cutout_hdul:
                # Get data
                image = cutout_hdul['IMAGE'].data
                header = cutout_hdul['IMAGE'].header
                
                # Get spatial and spectral WCS
                spatial_wcs = WCS(header)
                spectral_wcs = WCS(header, fobj=cutout_hdul, key='W')
                spectral_wcs.sip = None
                
                # Get pixel coordinates at center
                cx, cy = image.shape[1] / 2, image.shape[0] / 2
                
                # Get wavelength
                wavelength, _ = spectral_wcs.pixel_to_world(cx, cy)
                
                # Get flux at center (simple extraction)
                flux = image[int(cy), int(cx)]
                
                wavelengths.append(wavelength.to(u.micrometer).value)
                fluxes.append(flux)
                
        except Exception as e:
            print(f"  Error processing cutout {i}: {e}")
    
    print(f"Successfully processed {len(wavelengths)} cutouts")

# %%
# Plot spectrum
if len(wavelengths) > 0:
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Sort by wavelength
    sorted_indices = np.argsort(wavelengths)
    wavelengths = np.array(wavelengths)[sorted_indices]
    fluxes = np.array(fluxes)[sorted_indices]
    
    ax.plot(wavelengths, fluxes, 'b-', linewidth=1, marker='o', markersize=3)
    ax.set_xlabel('Wavelength (µm)')
    ax.set_ylabel('Surface Brightness (MJy/sr)')
    ax.set_title(f'SPHEREx Spectrum at RA={ra}, Dec={dec}')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('spherex_example_spectrum.png', dpi=150)
    plt.show()
    print("Spectrum saved to spherex_example_spectrum.png")

# %% [markdown]
# ## 8. Clean Up

# %%
if len(results_sia) > 0:
    hdulist.close()
    print("Closed FITS file")

print("\nTutorial complete!")
