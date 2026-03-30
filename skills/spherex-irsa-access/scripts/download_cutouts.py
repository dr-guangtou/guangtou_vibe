#!/usr/bin/env python3
"""
Download and package SPHEREx spectral image cutouts.

Usage:
    python download_cutouts.py <ra> <dec> [--size 0.1] [--bandpass SPHEREx-D2] [--parallel]

Example:
    python download_cutouts.py 210.80227 54.34895 --size 0.05 --bandpass SPHEREx-D2 --parallel
"""

import argparse
import sys
import os
import time
import urllib.error
import http.client
import concurrent.futures


def process_single_cutout(row, ra, dec, cache=False):
    """
    Download and process a single SPHEREx cutout.
    
    Parameters
    ----------
    row : dict-like
        Row containing 'uri' key with cutout URL
    ra, dec : float
        RA and Dec in degrees
    cache : bool
        Use astropy caching
    
    Returns
    -------
    dict
        Processed row with HDUs and wavelength info
    """
    from astropy.io import fits
    from astropy.wcs import WCS
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    import numpy as np
    
    try:
        with fits.open(row['uri'], cache=cache) as hdulist:
            header = hdulist['IMAGE'].header
            
            # Get pixel coordinates at cutout position
            spatial_wcs = WCS(header)
            x, y = spatial_wcs.world_to_pixel(
                SkyCoord(ra=ra, dec=dec, unit='deg', frame='icrs')
            )
            
            # Get wavelength at cutout position
            spectral_wcs = WCS(header, fobj=hdulist, key='W')
            spectral_wcs.sip = None
            wavelength, bandwidth = spectral_wcs.pixel_to_world(x, y)
            
            # Collect HDUs with renamed EXTNAMEs
            hdus = []
            for hdu in hdulist[1:]:  # Skip primary
                new_name = f"{hdu.header['EXTNAME']}{row.get('cutout_index', 1)}"
                hdu.header['EXTNAME'] = new_name
                hdus.append(hdu.copy())
            
            return {
                'cutout_index': row.get('cutout_index', 1),
                'observation_date': row.get('time_bounds_lower', 0),
                'central_wavelength': wavelength.to(u.micrometer).value,
                'bandwidth': bandwidth.to(u.micrometer).value,
                'access_url': row['uri'],
                'hdus': hdus,
                'success': True
            }
    except Exception as e:
        return {
            'cutout_index': row.get('cutout_index', 1),
            'access_url': row['uri'],
            'error': str(e),
            'success': False
        }


def download_cutouts(ra, dec, size_deg=0.1, bandpass='SPHEREx-D2', 
                    parallel=True, max_workers=10, cache=False,
                    output_file='spherex_cutouts.fits'):
    """
    Download SPHEREx cutouts and package them into a single MEF.
    
    Parameters
    ----------
    ra, dec : float
        Coordinates in degrees
    size_deg : float
        Cutout size in degrees
    bandpass : str
        Detector bandpass (e.g., 'SPHEREx-D2')
    parallel : bool
        Use parallel downloading
    max_workers : int
        Number of parallel workers
    cache : bool
        Cache downloaded files
    output_file : str
        Output filename
    """
    try:
        import pyvo
        from astropy.io import fits
        from astropy.table import Table
        import numpy as np
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        print("Install with: pip install pyvo astropy")
        sys.exit(1)
    
    # Query TAP for cutout URLs
    print(f"Querying TAP for cutouts at RA={ra}, Dec={dec}...")
    service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")
    
    query = f"""
    SELECT
        'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size_deg}' AS uri,
        p.time_bounds_lower
    FROM spherex.artifact a
    JOIN spherex.plane p ON a.planeid = p.planeid
    WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
            AND p.energy_bandpassname = '{bandpass}'
    ORDER BY p.time_bounds_lower
    """
    
    results = service.search(query)
    results_table = results.to_table()
    
    if len(results_table) == 0:
        print("No cutouts found!")
        return None
    
    print(f"Found {len(results_table)} cutouts")
    
    # Add cutout index
    results_table['cutout_index'] = range(1, len(results_table) + 1)
    
    # Download cutouts
    print(f"Downloading cutouts ({'parallel' if parallel else 'serial'})...")
    t1 = time.time()
    
    rows_list = [dict(zip(results_table.colnames, row)) for row in results_table]
    
    if parallel:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(process_single_cutout, row, ra, dec, cache)
                for row in rows_list
            ]
            processed = [f.result() for f in concurrent.futures.as_completed(futures)]
    else:
        processed = [
            process_single_cutout(row, ra, dec, cache)
            for row in rows_list
        ]
    
    elapsed = time.time() - t1
    print(f"Download completed in {elapsed/60:.1f} minutes")
    
    # Filter successful downloads
    successful = [p for p in processed if p['success']]
    failed = [p for p in processed if not p['success']]
    
    print(f"Successful: {len(successful)}, Failed: {len(failed)}")
    
    if failed:
        print("Failed cutouts:")
        for f in failed:
            print(f"  {f['access_url']}: {f.get('error', 'Unknown error')}")
    
    if len(successful) == 0:
        print("No successful downloads!")
        return None
    
    # Sort by cutout index
    successful.sort(key=lambda x: x['cutout_index'])
    
    # Create summary table HDU
    cols = fits.ColDefs([
        fits.Column(name='cutout_index', format='J', 
                   array=[s['cutout_index'] for s in successful]),
        fits.Column(name='observation_date', format='D',
                   array=[s['observation_date'] for s in successful], unit='d'),
        fits.Column(name='central_wavelength', format='D',
                   array=[s['central_wavelength'] for s in successful], unit='um'),
        fits.Column(name='bandwidth', format='D',
                   array=[s['bandwidth'] for s in successful], unit='um'),
        fits.Column(name='access_url', format='A256',
                   array=[s['access_url'] for s in successful]),
    ])
    table_hdu = fits.BinTableHDU.from_columns(cols)
    table_hdu.header['EXTNAME'] = 'CUTOUT_INFO'
    
    # Combine all HDUs
    primary_hdu = fits.PrimaryHDU()
    primary_hdu.header['RA'] = ra
    primary_hdu.header['DEC'] = dec
    primary_hdu.header['SIZE'] = size_deg
    primary_hdu.header['BAND'] = bandpass
    primary_hdu.header['NCUTOUTS'] = len(successful)
    
    hdulist_list = [primary_hdu, table_hdu]
    for s in successful:
        hdulist_list.extend(s['hdus'])
    
    combined_hdulist = fits.HDUList(hdulist_list)
    
    # Write output
    combined_hdulist.writeto(output_file, overwrite=True)
    print(f"\nOutput saved to: {output_file}")
    print(f"Total size: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Download and package SPHEREx spectral image cutouts'
    )
    parser.add_argument('ra', type=float, help='Right Ascension (degrees)')
    parser.add_argument('dec', type=float, help='Declination (degrees)')
    parser.add_argument('--size', type=float, default=0.1,
                       help='Cutout size in degrees (default: 0.1)')
    parser.add_argument('--bandpass', type=str, default='SPHEREx-D2',
                       help='SPHEREx detector band (default: SPHEREx-D2)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output filename (default: auto-generated)')
    parser.add_argument('--parallel', action='store_true',
                       help='Use parallel downloading')
    parser.add_argument('--workers', type=int, default=10,
                       help='Number of parallel workers (default: 10)')
    parser.add_argument('--cache', action='store_true',
                       help='Cache downloaded files')
    
    args = parser.parse_args()
    
    # Generate output filename if not provided
    if args.output is None:
        args.output = f"spherex_cutouts_ra{args.ra:.4f}_dec{args.dec:.4f}_{args.bandpass}.fits"
    
    download_cutouts(
        args.ra,
        args.dec,
        size_deg=args.size,
        bandpass=args.bandpass,
        parallel=args.parallel,
        max_workers=args.workers,
        cache=args.cache,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
