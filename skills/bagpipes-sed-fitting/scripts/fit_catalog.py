#!/usr/bin/env python3
"""
Batch SED fitting with BAGPIPES for a catalog of objects.

Usage:
    python fit_catalog.py --catalog my_catalog.fits --id-col ID --n-cores 4

Example:
    python fit_catalog.py --catalog data.fits --model dblplaw --n-cores 8
"""

import sys
import numpy as np
import bagpipes as pipes
from astropy.table import Table
import argparse


def load_fits_photometry(catalog_file, id_column='ID'):
    """
    Create a data loader function for a FITS catalog.
    
    Parameters:
    -----------
    catalog_file : str
        Path to FITS catalog
    id_column : str
        Name of ID column
        
    Returns:
    --------
    function : Data loader compatible with BAGPIPES
    """
    # Load catalog once
    catalog = Table.read(catalog_file)
    
    # Identify flux and error columns
    # Assumes columns are named like: FLUX_U, FLUXERR_U, etc.
    flux_cols = [col for col in catalog.colnames if col.startswith('FLUX_') 
                 and not col.startswith('FLUXERR_')]
    
    def load_photometry(ID):
        """Load photometry for a single object."""
        # Find row
        mask = catalog[id_column] == ID
        if not np.any(mask):
            raise ValueError(f"ID {ID} not found in catalog")
        
        row = catalog[mask][0]
        
        # Extract fluxes and errors
        fluxes = []
        fluxerrs = []
        
        for flux_col in flux_cols:
            band = flux_col.replace('FLUX_', '')
            err_col = f'FLUXERR_{band}'
            
            flux = row[flux_col]
            fluxerr = row[err_col] if err_col in catalog.colnames else flux * 0.1
            
            # Handle missing/invalid data
            if np.isnan(flux) or np.isnan(fluxerr) or fluxerr <= 0:
                flux = 0.
                fluxerr = 9.9e99
            
            fluxes.append(flux)
            fluxerrs.append(fluxerr)
        
        photometry = np.c_[fluxes, fluxerrs]
        
        # Cap SNR
        for i in range(len(photometry)):
            if photometry[i, 0] > 0 and photometry[i, 1] > 0:
                snr = photometry[i, 0] / photometry[i, 1]
                if snr > 20:
                    photometry[i, 1] = photometry[i, 0] / 20
        
        return photometry
    
    return load_photometry, flux_cols


def create_model_instructions(model_type='tau', fix_redshift=None):
    """
    Create fit instructions dictionary.
    
    Parameters:
    -----------
    model_type : str
        'tau', 'dblplaw', or 'constant'
    fix_redshift : float or None
        If provided, fix redshift to this value
        
    Returns:
    --------
    dict : fit_instructions
    """
    fit_instructions = {}
    
    # Redshift
    if fix_redshift is not None:
        fit_instructions["redshift"] = fix_redshift
    else:
        fit_instructions["redshift"] = (0., 10.)
    
    # SFH model
    if model_type == 'tau':
        sfh = {
            "age": (0.1, 15.),
            "tau": (0.3, 10.),
            "massformed": (1., 15.),
            "metallicity": (0., 2.5),
        }
        fit_instructions["tau"] = sfh
        
    elif model_type == 'dblplaw':
        sfh = {
            "tau": (0., 15.),
            "alpha": (0.01, 1000.),
            "beta": (0.01, 1000.),
            "alpha_prior": "log_10",
            "beta_prior": "log_10",
            "massformed": (1., 15.),
            "metallicity": (0., 2.5),
        }
        fit_instructions["dblplaw"] = sfh
        
    elif model_type == 'constant':
        sfh = {
            "age": (0.1, 15.),
            "massformed": (1., 15.),
            "metallicity": (0., 2.5),
        }
        fit_instructions["constant"] = sfh
    
    # Dust
    fit_instructions["dust"] = {
        "type": "Calzetti",
        "Av": (0., 2.),
    }
    
    # Nebular emission (optional)
    # fit_instructions["nebular"] = {"logU": -3.}
    
    return fit_instructions


def run_catalog_fit(catalog_file, id_column='ID', model_type='tau',
                   n_cores=1, output_name='bagpipes_fit',
                   fix_redshift=None, filter_file=None):
    """
    Run BAGPIPES fit for a catalog of objects.
    
    Parameters:
    -----------
    catalog_file : str
        Path to input catalog
    id_column : str
        Name of ID column
    model_type : str
        SFH model type
    n_cores : int
        Number of parallel cores
    output_name : str
        Name for output folder
    fix_redshift : float or None
        Fix redshift to this value
    filter_file : str or None
        File with filter list
    """
    print(f"\n{'='*60}")
    print(f"BAGPIPES Catalog Fitting")
    print(f"{'='*60}")
    print(f"Catalog: {catalog_file}")
    print(f"Model: {model_type}")
    print(f"Cores: {n_cores}")
    print(f"Output: {output_name}")
    print(f"{'='*60}\n")
    
    # Load catalog
    catalog = Table.read(catalog_file)
    ids = catalog[id_column].astype(str).tolist()
    
    print(f"Found {len(ids)} objects to fit")
    print(f"ID range: {ids[0]} to {ids[-1]}")
    
    # Create data loader
    load_photometry, flux_cols = load_fits_photometry(catalog_file, id_column)
    print(f"Photometry: {len(flux_cols)} bands")
    
    # Load filters
    if filter_file:
        filt_list = np.loadtxt(filter_file, dtype=str)
    else:
        # Create dummy filter names
        filt_list = np.array([f"filt_{i}" for i in range(len(flux_cols))])
    
    # Create model instructions
    fit_instructions = create_model_instructions(model_type, fix_redshift)
    
    # Create fit catalogue
    fit_catalogue = pipes.fit_catalogue(
        ids,
        fit_instructions,
        load_photometry,
        spectrum_exists=False,
        filt_list=filt_list,
        run=output_name,
        sampler="nautilus",
    )
    
    # Run fits
    print(f"\nStarting fits with {n_cores} cores...")
    print(f"Progress will be saved to: pipes/{output_name}/")
    print(f"\nThis may take a while...\n")
    
    fit_catalogue.fit(verbose=False, n_cores=n_cores)
    
    # Extract and save results
    print(f"\n{'='*60}")
    print("Extracting results...")
    print(f"{'='*60}\n")
    
    results = []
    
    for id in ids:
        fit = fit_catalogue.fits[id]
        samples = fit.posterior.samples
        
        result = {id_column: id}
        
        # Extract key parameters
        params_to_extract = [
            'redshift',
            'stellar_mass',
            'sfr',
            'ssfr',
            'mass_weighted_age',
        ]
        
        # Add model-specific parameters
        if model_type in samples:
            for param in ['age', 'tau', 'massformed', 'metallicity', 'alpha', 'beta']:
                key = f"{model_type}:{param}"
                if key in samples:
                    params_to_extract.append(key)
        
        # Add dust parameters
        if 'dust:Av' in samples:
            params_to_extract.append('dust:Av')
        
        # Calculate statistics
        for param in params_to_extract:
            if param in samples:
                values = samples[param]
                result[f"{param}_median"] = np.median(values)
                result[f"{param}_err"] = np.std(values)
                result[f"{param}_16th"] = np.percentile(values, 16)
                result[f"{param}_84th"] = np.percentile(values, 84)
        
        # Evidence
        if hasattr(fit.posterior, 'ln_evidence'):
            result['ln_evidence'] = fit.posterior.ln_evidence
        
        results.append(result)
    
    # Save results table
    results_table = Table(results)
    output_file = f"{output_name}_results.fits"
    results_table.write(output_file, overwrite=True)
    
    print(f"Results saved to: {output_file}")
    print(f"\nSummary of fitted parameters:")
    print(f"-" * 40)
    
    for col in results_table.colnames:
        if col.endswith('_median'):
            param = col.replace('_median', '')
            median_val = np.median(results_table[col])
            print(f"{param:25s}: median = {median_val:.3f}")
    
    return fit_catalogue, results_table


def main():
    parser = argparse.ArgumentParser(
        description='Batch SED fitting with BAGPIPES'
    )
    parser.add_argument('--catalog', type=str, required=True,
                       help='Path to input catalog (FITS format)')
    parser.add_argument('--id-col', type=str, default='ID',
                       help='Name of ID column (default: ID)')
    parser.add_argument('--model', type=str, default='tau',
                       choices=['tau', 'dblplaw', 'constant'],
                       help='SFH model type (default: tau)')
    parser.add_argument('--n-cores', type=int, default=1,
                       help='Number of parallel cores (default: 1)')
    parser.add_argument('--output', type=str, default='bagpipes_fit',
                       help='Output folder name (default: bagpipes_fit)')
    parser.add_argument('--fix-redshift', type=float, default=None,
                       help='Fix redshift to this value (default: vary)')
    parser.add_argument('--filters', type=str, default=None,
                       help='File with filter names')
    
    args = parser.parse_args()
    
    run_catalog_fit(
        args.catalog,
        args.id_col,
        args.model,
        args.n_cores,
        args.output,
        args.fix_redshift,
        args.filters
    )
    
    print("\nDone!")


if __name__ == '__main__':
    main()
