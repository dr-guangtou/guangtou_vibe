#!/usr/bin/env python3
"""
Query SPHEREx cutouts using TAP (Table Access Protocol).
TAP provides immediate access to newly ingested data (no SIA lag).

Usage:
    python query_tap_cutouts.py <ra> <dec> [--size 0.1deg] [--bandpass SPHEREx-D2]

Example:
    python query_tap_cutouts.py 210.80227 54.34895 --size 0.05 --bandpass SPHEREx-D2
"""

import argparse
import sys


def query_spherex_tap(ra, dec, size_deg=0.1, bandpass='SPHEREx-D2'):
    """
    Query SPHEREx cutouts using TAP protocol.
    
    Parameters
    ----------
    ra : float
        Right Ascension in degrees
    dec : float
        Declination in degrees  
    size_deg : float
        Cutout size in degrees (default: 0.1)
    bandpass : str
        SPHEREx detector bandpass (default: SPHEREx-D2)
        Options: SPHEREx-D1 through SPHEREx-D6
    
    Returns
    -------
    astropy.table.Table
        Table with cutout URLs and observation times
    """
    try:
        import pyvo
        import astropy.units as u
        from astropy.table import Table
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        print("Install with: pip install pyvo astropy")
        sys.exit(1)
    
    # Define TAP service
    service = pyvo.dal.TAPService("https://irsa.ipac.caltech.edu/TAP")
    
    print(f"Querying TAP for cutouts at RA={ra}, Dec={dec}, size={size_deg}deg, band={bandpass}...")
    
    # Build TAP query
    query = f"""
    SELECT
        'https://irsa.ipac.caltech.edu/' || a.uri || '?center={ra},{dec}d&size={size_deg}' AS uri,
        p.time_bounds_lower,
        p.energy_bandpassname
    FROM spherex.artifact a
    JOIN spherex.plane p ON a.planeid = p.planeid
    WHERE 1 = CONTAINS(POINT('ICRS', {ra}, {dec}), p.poly)
            AND p.energy_bandpassname = '{bandpass}'
    ORDER BY p.time_bounds_lower
    """
    
    import time
    t1 = time.time()
    results = service.search(query)
    elapsed = time.time() - t1
    
    print(f"Query completed in {elapsed:.2f} seconds")
    print(f"Found {len(results)} cutouts")
    
    # Convert to astropy Table
    table = results.to_table()
    
    if len(table) > 0:
        print("\nFirst few results:")
        print(table[:5])
    
    return table


def main():
    parser = argparse.ArgumentParser(
        description='Query SPHEREx cutouts from IRSA using TAP'
    )
    parser.add_argument('ra', type=float, help='Right Ascension (degrees)')
    parser.add_argument('dec', type=float, help='Declination (degrees)')
    parser.add_argument('--size', type=float, default=0.1,
                       help='Cutout size in degrees (default: 0.1)')
    parser.add_argument('--bandpass', type=str, default='SPHEREx-D2',
                       choices=[f'SPHEREx-D{i}' for i in range(1, 7)],
                       help='SPHEREx detector band (default: SPHEREx-D2)')
    
    args = parser.parse_args()
    
    results = query_spherex_tap(
        args.ra,
        args.dec,
        size_deg=args.size,
        bandpass=args.bandpass
    )
    
    # Save results
    if len(results) > 0:
        output_file = f"spherex_tap_results_ra{args.ra}_dec{args.dec}.ecsv"
        results.write(output_file, format='ascii.ecsv', overwrite=True)
        print(f"\nResults saved to: {output_file}")
        
        # Also save URL list for easy download
        url_file = f"spherex_cutout_urls_ra{args.ra}_dec{args.dec}.txt"
        with open(url_file, 'w') as f:
            for url in results['uri']:
                f.write(f"{url}\n")
        print(f"URL list saved to: {url_file}")


if __name__ == '__main__':
    main()
