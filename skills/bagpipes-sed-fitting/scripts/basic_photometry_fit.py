#!/usr/bin/env python3
"""
Basic BAGPIPES photometry fitting example with nautilus sampler.

Usage:
    python basic_photometry_fit.py <object_id>

Example:
    python basic_photometry_fit.py 17433
"""

import sys
import numpy as np
import bagpipes as pipes
import matplotlib.pyplot as plt


def load_goodss_photometry(ID):
    """
    Example loader for CANDELS GOODS-South photometry.
    
    This is the example from the BAGPIPES tutorials.
    Adapt to your own data format.
    """
    # Load catalog (adjust path to your data)
    cat_file = "hlsp_candels_hst_wfc3_goodss-tot-multiband_f160w_v1-1photom_cat.txt"
    
    try:
        cat = np.loadtxt(cat_file,
                         usecols=(10, 13, 16, 19, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55,
                                  11, 14, 17, 20, 26, 29, 32, 35, 38, 41, 44, 47, 50, 53, 56))
    except FileNotFoundError:
        print(f"Catalog file not found: {cat_file}")
        print("Creating synthetic data for demonstration...")
        return create_synthetic_photometry()
    
    row = int(ID) - 1
    
    # Extract fluxes and errors
    fluxes = cat[row, :15]
    fluxerrs = cat[row, 15:]
    
    # Combine into 2D array
    photometry = np.c_[fluxes, fluxerrs]
    
    # Handle missing data
    for i in range(len(photometry)):
        if (photometry[i, 0] == 0.) or (photometry[i, 1] <= 0):
            photometry[i, :] = [0., 9.9e99]
    
    # Enforce maximum SNR
    for i in range(len(photometry)):
        max_snr = 20. if i < 10 else 10.
        if photometry[i, 0] / photometry[i, 1] > max_snr:
            photometry[i, 1] = photometry[i, 0] / max_snr
    
    return photometry


def create_synthetic_photometry():
    """Create synthetic photometry for demonstration."""
    # 15 bands with realistic-ish values
    np.random.seed(42)
    fluxes = np.random.lognormal(0, 1, 15) * 10  # uJy
    fluxerrs = fluxes * 0.1  # 10% errors
    return np.c_[fluxes, fluxerrs]


def setup_tau_model():
    """
    Setup fit instructions for exponential tau SFH model.
    
    Returns:
        dict: fit_instructions for BAGPIPES
    """
    # SFH component - exponential tau model
    exp = {}
    exp["age"] = (0.1, 15.)           # Age: 0.1 to 15 Gyr
    exp["tau"] = (0.3, 10.)           # Timescale: 0.3 to 10 Gyr
    exp["massformed"] = (1., 15.)     # log10 stellar mass
    exp["metallicity"] = (0., 2.5)    # Metallicity: 0 to 2.5 Z_sun
    
    # Dust attenuation
    dust = {}
    dust["type"] = "Calzetti"
    dust["Av"] = (0., 2.)             # V-band extinction
    
    # Combine into fit instructions
    fit_instructions = {}
    fit_instructions["redshift"] = (0., 10.)  # Redshift prior
    fit_instructions["tau"] = exp
    fit_instructions["dust"] = dust
    
    return fit_instructions


def setup_dblplaw_model():
    """
    Setup fit instructions for double power-law SFH.
    More flexible than tau model.
    """
    dblplaw = {}
    dblplaw["tau"] = (0., 15.)        # Time of peak SFR
    dblplaw["alpha"] = (0.01, 1000.)  # Falling power-law slope
    dblplaw["beta"] = (0.01, 1000.)   # Rising power-law slope
    dblplaw["alpha_prior"] = "log_10" # Log-uniform prior
    dblplaw["beta_prior"] = "log_10"
    dblplaw["massformed"] = (1., 15.)
    dblplaw["metallicity"] = (0., 2.5)
    
    dust = {}
    dust["type"] = "Calzetti"
    dust["Av"] = (0., 2.)
    
    fit_instructions = {}
    fit_instructions["redshift"] = (0., 10.)
    fit_instructions["dblplaw"] = dblplaw
    fit_instructions["dust"] = dust
    
    return fit_instructions


def run_fit(object_id, model_type="tau", run_name=None):
    """
    Run BAGPIPES fit for a single object.
    
    Parameters:
    -----------
    object_id : str
        Object identifier
    model_type : str
        "tau" or "dblplaw"
    run_name : str
        Name for output folder (auto-generated if None)
    """
    print(f"\n{'='*60}")
    print(f"BAGPIPES SED Fitting")
    print(f"Object: {object_id}")
    print(f"Model: {model_type}")
    print(f"Sampler: nautilus")
    print(f"{'='*60}\n")
    
    # Load filter list (adjust path)
    try:
        filt_list = np.loadtxt("filters/goodss_filt_list.txt", dtype=str)
    except FileNotFoundError:
        print("Filter list not found, using default filters")
        filt_list = np.array([f"filter_{i}" for i in range(15)])
    
    # Create galaxy object
    galaxy = pipes.galaxy(
        object_id, 
        load_goodss_photometry,
        spectrum_exists=False,
        filt_list=filt_list
    )
    
    # Plot observed data
    print("Plotting observed photometry...")
    fig = galaxy.plot()
    plt.savefig(f"{object_id}_observed.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # Setup model
    if model_type == "tau":
        fit_instructions = setup_tau_model()
    elif model_type == "dblplaw":
        fit_instructions = setup_dblplaw_model()
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
    
    # Generate run name
    if run_name is None:
        run_name = f"{object_id}_{model_type}_nautilus"
    
    # Create fit object
    fit = pipes.fit(galaxy, fit_instructions, run=run_name)
    
    # Run fit with nautilus
    print(f"\nRunning fit with nautilus...")
    print(f"Output folder: pipes/{run_name}")
    fit.fit(verbose=False)
    
    # Print results
    print(f"\n{'='*60}")
    print("FIT RESULTS")
    print(f"{'='*60}")
    
    samples = fit.posterior.samples
    
    # Key parameters to display
    params_to_show = [
        'redshift',
        f'{model_type}:age' if model_type == 'tau' else f'{model_type}:tau',
        f'{model_type}:massformed',
        f'{model_type}:metallicity',
        'dust:Av',
        'stellar_mass',
        'sfr',
        'mass_weighted_age',
    ]
    
    print("\nParameter Estimates (median ± 1sigma):")
    print("-" * 40)
    
    for param in params_to_show:
        if param in samples:
            median = np.median(samples[param])
            std = np.std(samples[param])
            print(f"{param:25s}: {median:8.3f} ± {std:6.3f}")
    
    # Log evidence
    if hasattr(fit.posterior, 'ln_evidence'):
        print(f"\n{'ln(evidence)':25s}: {fit.posterior.ln_evidence:8.2f}")
    
    # Effective sample size
    if hasattr(fit.posterior, 'n_eff'):
        print(f"{'N_eff':25s}: {fit.posterior.n_eff:8.0f}")
    
    # Create plots
    print(f"\nGenerating plots...")
    
    # Spectrum posterior
    fig = fit.plot_spectrum_posterior(save=False, show=False)
    plt.savefig(f"{object_id}_{model_type}_spectrum.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # SFH posterior
    fig = fit.plot_sfh_posterior(save=False, show=False)
    plt.savefig(f"{object_id}_{model_type}_sfh.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    # Corner plot (may take time)
    try:
        fig = fit.plot_corner(save=False, show=False)
        plt.savefig(f"{object_id}_{model_type}_corner.png", dpi=150, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"Corner plot failed: {e}")
    
    print(f"\nPlots saved to:")
    print(f"  - {object_id}_observed.png")
    print(f"  - {object_id}_{model_type}_spectrum.png")
    print(f"  - {object_id}_{model_type}_sfh.png")
    print(f"  - {object_id}_{model_type}_corner.png")
    
    return fit


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Basic BAGPIPES photometry fitting'
    )
    parser.add_argument('object_id', type=str, nargs='?', default='17433',
                       help='Object ID to fit (default: 17433)')
    parser.add_argument('--model', type=str, default='tau',
                       choices=['tau', 'dblplaw'],
                       help='SFH model type (default: tau)')
    parser.add_argument('--run-name', type=str, default=None,
                       help='Name for output folder')
    
    args = parser.parse_args()
    
    fit = run_fit(args.object_id, args.model, args.run_name)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
