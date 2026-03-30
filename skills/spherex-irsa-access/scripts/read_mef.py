#!/usr/bin/env python3
"""
Read and inspect SPHEREx Multi-Extension FITS (MEF) files.

Usage:
    python read_mef.py <fits_file_or_url>

Example:
    python read_mef.py spherex_image.fits
    python read_mef.py https://irsa.ipac.caltech.edu/.../image.fits
"""

import argparse
import sys
import time
import urllib.error
import http.client


def read_spherex_mef(file_path, verbose=True):
    """
    Read a SPHEREx MEF file with retry logic for transient errors.
    
    Parameters
    ----------
    file_path : str
        Path to local FITS file or URL
    verbose : bool
        Print information about the file
    
    Returns
    -------
    astropy.io.fits.HDUList
        The loaded FITS file
    """
    try:
        from astropy.io import fits
        from astropy.utils.data import conf
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        print("Install with: pip install astropy")
        sys.exit(1)
    
    # Increase timeout for large files
    conf.remote_timeout = 120
    
    # Load with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if verbose:
                print(f"Loading {file_path}...")
            hdulist = fits.open(file_path)
            break
        except (TimeoutError, urllib.error.HTTPError, http.client.IncompleteRead) as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
            wait_time = 10 * (attempt + 1)
            if verbose:
                print(f"Error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
            time.sleep(wait_time)
    
    if verbose:
        print("\n" + "="*60)
        print("FITS FILE STRUCTURE")
        print("="*60)
        hdulist.info()
        
        print("\n" + "="*60)
        print("PRIMARY HEADER")
        print("="*60)
        primary = hdulist[0].header
        for key in ['MISSION', 'TELESCOP', 'INSTRUME', 'VERSION', 'DATE']:
            if key in primary:
                print(f"  {key}: {primary[key]}")
        
        if 'IMAGE' in hdulist:
            print("\n" + "="*60)
            print("IMAGE EXTENSION")
            print("="*60)
            img_hdr = hdulist['IMAGE'].header
            for key in ['EXTNAME', 'NAXIS1', 'NAXIS2', 'BUNIT', 'DETECTOR', 
                       'WAVELMIN', 'WAVELMAX', 'PSF_FWHM']:
                if key in img_hdr:
                    print(f"  {key}: {img_hdr[key]}")
            
            # Print WCS info
            if 'WCSNAMEW' in img_hdr:
                print(f"  WCSNAMEW: {img_hdr['WCSNAMEW']}")
        
        if 'PSF' in hdulist:
            print("\n" + "="*60)
            print("PSF EXTENSION")
            print("="*60)
            psf_hdr = hdulist['PSF'].header
            psf_data = hdulist['PSF'].data
            print(f"  Shape: {psf_data.shape}")
            for key in ['EXTNAME', 'OVERSAMP', 'NAXIS1', 'NAXIS2', 'NAXIS3']:
                if key in psf_hdr:
                    print(f"  {key}: {psf_hdr[key]}")
    
    return hdulist


def extract_wavelength_info(hdulist, x=None, y=None):
    """
    Extract wavelength information at a specific pixel or center.
    
    Parameters
    ----------
    hdulist : astropy.io.fits.HDUList
        Loaded SPHEREx MEF
    x, y : float, optional
        Pixel coordinates. If None, uses image center.
    
    Returns
    -------
    dict
        Wavelength information
    """
    from astropy.wcs import WCS
    import astropy.units as u
    
    image_header = hdulist['IMAGE'].header
    
    # Get spatial WCS
    spatial_wcs = WCS(image_header)
    
    # Get spectral WCS
    spectral_wcs = WCS(image_header, fobj=hdulist, key='W')
    spectral_wcs.sip = None
    
    # Use center if coordinates not provided
    if x is None:
        x = image_header.get('NAXIS1', 2040) / 2
    if y is None:
        y = image_header.get('NAXIS2', 2040) / 2
    
    # Get wavelength at position
    wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
    
    # Get world coordinates
    from astropy.coordinates import SkyCoord
    coord = spatial_wcs.pixel_to_world(x, y)
    
    return {
        'pixel_x': x,
        'pixel_y': y,
        'ra': coord.ra.deg,
        'dec': coord.dec.deg,
        'wavelength_um': wavelength.to(u.micrometer).value,
        'bandwidth_um': bandwidth.to(u.micrometer).value,
        'detector': image_header.get('DETECTOR', 'Unknown')
    }


def main():
    parser = argparse.ArgumentParser(
        description='Read and inspect SPHEREx MEF files'
    )
    parser.add_argument('file', help='Path to FITS file or URL')
    parser.add_argument('--wavelength-at', metavar='X,Y',
                       help='Print wavelength at pixel position (e.g., 1020,1020)')
    
    args = parser.parse_args()
    
    # Read file
    hdulist = read_spherex_mef(args.file, verbose=True)
    
    # Extract wavelength info if requested
    if args.wavelength_at:
        try:
            x, y = map(float, args.wavelength_at.split(','))
            info = extract_wavelength_info(hdulist, x, y)
            print("\n" + "="*60)
            print("WAVELENGTH INFORMATION")
            print("="*60)
            for key, value in info.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.6f}")
                else:
                    print(f"  {key}: {value}")
        except ValueError:
            print("Error: --wavelength-at should be in format X,Y (e.g., 1020,1020)")
    
    print("\nFile loaded successfully. Use hdulist['EXTENSION_NAME'] to access data.")
    
    # Keep reference available for interactive use
    return hdulist


if __name__ == '__main__':
    main()
