#!/usr/bin/env python3
"""
Basic SIA query for SPHEREx spectral images.

Usage:
    python query_sia_basic.py <ra> <dec> [--radius 1arcsec] [--collection spherex_qr2]

Example:
    python query_sia_basic.py 210.80227 54.34895 --radius 10arcsec
"""

import argparse
import sys

def query_spherex_sia(ra, dec, radius_arcsec=1, collection='spherex_qr2'):
    """
    Query SPHEREx data using SIA (Simple Image Access) protocol.
    
    Parameters
    ----------
    ra : float
        Right Ascension in degrees
    dec : float
        Declination in degrees
    radius_arcsec : float
        Search radius in arcseconds (default: 1)
    collection : str
        SPHEREx collection name (default: spherex_qr2)
        Options: spherex_qr2, spherex_qr2_deep, spherex_qr2_cal
    
    Returns
    -------
    astropy.table.Table
        Query results with metadata about matching spectral images
    """
    try:
        from astroquery.ipac.irsa import Irsa
        from astropy.coordinates import SkyCoord
        import astropy.units as u
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        print("Install with: pip install astroquery astropy")
        sys.exit(1)
    
    # Increase timeout for large files
    from astropy.utils.data import conf
    conf.remote_timeout = 120
    
    # Define coordinates
    coord = SkyCoord(ra=ra, dec=dec, unit='deg')
    search_radius = radius_arcsec * u.arcsec
    
    print(f"Querying SPHEREx {collection} at RA={ra}, Dec={dec}, radius={radius_arcsec}arcsec...")
    
    # Query IRSA
    results = Irsa.query_sia(
        pos=(coord, search_radius),
        collection=collection
    )
    
    print(f"Found {len(results)} spectral images")
    
    if len(results) > 0:
        print("\nColumns available:", results.colnames)
        print("\nFirst result:")
        for col in ['access_url', 'obs_title', 'energy_bandpassname', 'time_bounds_lower']:
            if col in results.colnames:
                print(f"  {col}: {results[col][0]}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Query SPHEREx spectral images from IRSA using SIA'
    )
    parser.add_argument('ra', type=float, help='Right Ascension (degrees)')
    parser.add_argument('dec', type=float, help='Declination (degrees)')
    parser.add_argument('--radius', type=float, default=1,
                       help='Search radius in arcseconds (default: 1)')
    parser.add_argument('--collection', type=str, default='spherex_qr2',
                       choices=['spherex_qr2', 'spherex_qr2_deep', 'spherex_qr2_cal'],
                       help='SPHEREx collection (default: spherex_qr2)')
    
    args = parser.parse_args()
    
    results = query_spherex_sia(
        args.ra, 
        args.dec, 
        radius_arcsec=args.radius,
        collection=args.collection
    )
    
    # Save results
    if len(results) > 0:
        output_file = f"spherex_sia_results_ra{args.ra}_dec{args.dec}.ecsv"
        results.write(output_file, format='ascii.ecsv', overwrite=True)
        print(f"\nResults saved to: {output_file}")


if __name__ == '__main__':
    main()
