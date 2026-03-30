---
name: bagpipes-sed-fitting
description: Bayesian SED fitting with BAGPIPES using default models and nautilus sampler
category: astronomy
tags: [sed-fitting, bagpipes, bayesian, nautilus, galaxy, stellar-population, python]
author: Song Huang
date: 2026-03-30
version: 1.0.0
requirements:
  - bagpipes>=1.3.5
  - numpy
  - matplotlib
  - astropy
  - nautilus-sampler (auto-installed with bagpipes)
---

# BAGPIPES SED Fitting Skill

**BAGPIPES** (Bayesian Analysis of Galaxies for Physical Inference and Parameter EStimation) is a state-of-the-art Python code for generating realistic model galaxy spectra and fitting spectroscopic and photometric observations.

## Overview

BAGPIPES uses Bayesian inference with nested sampling (MultiNest or **nautilus**) to fit spectral energy distributions (SEDs) and extract physical galaxy parameters.

### Key Features
- **Model components**: Flexible star-formation histories, dust attenuation, nebular emission
- **Stellar population models**: BC03, MILES, BPASS (via model_components)
- **Photometric & spectroscopic fitting**: Support for both data types
- **Bayesian inference**: Posterior sampling with evidence calculation
- **Default sampler**: Nautilus (pure Python, auto-installed with bagpipes)

## Installation

```bash
pip install bagpipes
```

**Note**: Do not clone the repository directly - the large model grids are not included. Use pip install.

## Quick Start

### Basic Workflow

```python
import bagpipes as pipes
import numpy as np

# 1. Define data loading function
def load_photometry(ID):
    """Load photometry for a given object ID."""
    # Example: load from catalog
    fluxes = np.array([...])  # Flux values
    fluxerrs = np.array([...])  # Flux errors
    photometry = np.c_[fluxes, fluxerrs]
    return photometry

# 2. Define fit instructions (model + priors)
fit_instructions = {
    "redshift": (0., 10.),  # Uniform prior 0-10
    "tau": {
        "age": (0.1, 15.),          # Age in Gyr
        "tau": (0.3, 10.),          # SFH timescale
        "massformed": (1., 15.),    # log10(M*/M_sun)
        "metallicity": (0., 2.5),   # Z/Z_sun
    },
    "dust": {
        "type": "Calzetti",
        "Av": (0., 2.),             # V-band extinction
    }
}

# 3. Create galaxy object
galaxy = pipes.galaxy("object_id", load_photometry, 
                      spectrum_exists=False,
                      filt_list=filter_list)

# 4. Run fit
fit = pipes.fit(galaxy, fit_instructions, sampler="nautilus")
fit.fit(verbose=False)

# 5. Extract results
print(fit.posterior.samples.keys())  # Available parameters
print(fit.posterior.median)          # Median values
```

## Model Components

### Star Formation History (SFH)

Available SFH components with their parameters:

| Component | Description | Key Parameters |
|-----------|-------------|----------------|
| `burst` | Instantaneous burst | `age`, `massformed`, `metallicity` |
| `constant` | Constant SFH | `age`, `massformed`, `metallicity` |
| `tau` | Exponential decay | `age`, `tau`, `massformed`, `metallicity` |
| `delayed` | Delayed exponential | `age`, `tau`, `massformed`, `metallicity` |
| `lognormal` | Log-normal SFH | `age`, `tau`, `massformed`, `metallicity` |
| `dblplaw` | Double power-law | `age`, `tau`, `alpha`, `beta`, `massformed`, `metallicity` |

**Example - Exponential tau model:**
```python
exp = {
    "age": (0.1, 15.),           # Age: 0.1 to 15 Gyr
    "tau": (0.3, 10.),           # Timescale: 0.3 to 10 Gyr
    "massformed": (1., 15.),     # log10 stellar mass
    "metallicity": (0., 2.5),    # Metallicity: 0 to 2.5 Z_sun
}
fit_instructions["tau"] = exp
```

**Example - Double power-law (more flexible):**
```python
dblplaw = {
    "tau": (0., 15.),            # Time of peak SFR
    "alpha": (0.01, 1000.),      # Falling slope
    "beta": (0.01, 1000.),       # Rising slope
    "alpha_prior": "log_10",     # Log-uniform prior
    "beta_prior": "log_10",
    "massformed": (1., 15.),
    "metallicity": (0., 2.5),
}
fit_instructions["dblplaw"] = dblplaw
```

### Dust Attenuation

| Type | Description | Parameters |
|------|-------------|------------|
| `Calzetti` | Calzetti et al. (2000) | `Av`, optional `eta` |
| `CF00` | Charlot & Fall (2000) two-component | `Av`, `mu` |
| `Salim` | Salim et al. (2018) | `Av`, `delta`, `B`, `Rv` |

**Example:**
```python
dust = {
    "type": "Calzetti",
    "Av": (0., 2.),              # V-band extinction mag
}
fit_instructions["dust"] = dust
```

### Nebular Emission

```python
nebular = {
    "logU": -3.0,                # Ionization parameter (fixed)
}
# Or as free parameter:
nebular = {
    "logU": (-4., -1.),          # Varying logU
}
fit_instructions["nebular"] = nebular
```

### AGN Component (optional)

```python
agn = {
    "alpha": (-2., 2.),          # Power-law slope
    "mass": (6., 12.),           # log10 BH mass
}
fit_instructions["agn"] = agn
```

## Priors

Specify priors using `parameter_prior` keyword:

```python
# Uniform prior (default)
component["metallicity"] = (0., 2.5)

# Log-uniform prior
component["metallicity"] = (0.01, 5.)
component["metallicity_prior"] = "log_10"

# Natural log-uniform
component["parameter_prior"] = "log_e"

# Reciprocal (1/x) prior
component["parameter_prior"] = "recip"

# Gaussian prior with limits
component["redshift"] = (0., 1.)
component["redshift_prior"] = "Gaussian"
component["redshift_prior_mu"] = 0.7
component["redshift_prior_sigma"] = 0.2
```

**Available priors:**
- `"uniform"` - Uniform in linear space (default)
- `"log_10"` - Uniform in log10 space
- `"log_e"` - Uniform in natural log space
- `"pow_10"` - Uniform in 10^parameter
- `"recip"` - Uniform in 1/parameter
- `"recipsq"` - Uniform in 1/parameter^2
- `"Gaussian"` - Gaussian with mu and sigma

## Loading Observational Data

### Photometry

```python
def load_photometry(ID):
    """
    Load photometry for object ID.
    
    Returns: 2D array of shape (N_bands, 2) with flux and error.
    Fluxes should be in micro-Janskys (uJy).
    """
    # Load your catalog
    fluxes = catalog[ID]['fluxes']  # uJy
    fluxerrs = catalog[ID]['errors']  # uJy
    
    # Handle missing data
    for i in range(len(fluxes)):
        if fluxes[i] == 0 or fluxerrs[i] <= 0:
            fluxes[i] = 0.
            fluxerrs[i] = 9.9e99  # Large error
    
    # Enforce maximum SNR (optional)
    max_snr = 20.
    for i in range(len(fluxes)):
        if fluxes[i] / fluxerrs[i] > max_snr:
            fluxerrs[i] = fluxes[i] / max_snr
    
    return np.c_[fluxes, fluxerrs]

# Filter list file (one filter name per line)
filt_list = np.loadtxt("filters.txt", dtype=str)

# Create galaxy
galaxy = pipes.galaxy(ID, load_photometry, 
                      spectrum_exists=False,
                      filt_list=filt_list)
```

### Spectroscopy

```python
def load_spectrum(ID):
    """
    Load spectrum for object ID.
    
    Returns: 2D array of shape (N_pixels, 3) with wavelength, flux, error.
    Wavelength in Angstroms, flux in erg/s/cm^2/A.
    """
    wavelength = spectrum['wave']  # Angstroms
    flux = spectrum['flux']        # erg/s/cm^2/A
    error = spectrum['error']      # erg/s/cm^2/A
    
    # Create mask for bad pixels (optional)
    mask = np.ones(len(wavelength), dtype=bool)
    # mask[bad_regions] = False
    
    spectrum_array = np.c_[wavelength, flux, error]
    
    return spectrum_array, mask

# For combined photometry + spectroscopy
galaxy = pipes.galaxy(ID, load_photometry, load_spectrum,
                      spectrum_exists=True,
                      filt_list=filt_list)
```

## Fitting with Nautilus Sampler

```python
# Basic fit with nautilus (default if MultiNest not installed)
fit = pipes.fit(galaxy, fit_instructions, sampler="nautilus")
fit.fit(verbose=False)

# Advanced nautilus options
fit = pipes.fit(
    galaxy, 
    fit_instructions,
    sampler="nautilus",
    n_live=1000,           # Number of live points
    n_eff=10000,           # Target effective sample size
    # resume=True,         # Resume previous run
)
```

**Nautilus advantages:**
- Pure Python (no compilation needed)
- Often faster than MultiNest
- Handles high-dimensional problems well
- Built-in with bagpipes installation

## Extracting Results

```python
# Posterior samples dictionary
samples = fit.posterior.samples

# Available keys (depends on model)
print(samples.keys())
# ['redshift', 'tau:age', 'tau:tau', 'tau:massformed', 
#  'tau:metallicity', 'dust:Av', 'stellar_mass', 'sfr', 
#  'mass_weighted_age', 'ssfr', ...]

# Median and uncertainties
median = fit.posterior.median  # Dict of median values
conf_int = fit.posterior.conf_int  # 16th and 84th percentiles

# Specific parameter
mass = samples['stellar_mass']
print(f"log M* = {np.median(mass):.2f} +/- {np.std(mass):.2f}")

# Evidence (Bayesian model comparison)
evidence = fit.posterior.ln_evidence

# Maximum likelihood model
max_like_params = fit.posterior.max_like_params
```

## Visualization

```python
# Plot spectrum/photometry posterior
fig = fit.plot_spectrum_posterior(save=False, show=True)

# Plot star-formation history
fig = fit.plot_sfh_posterior(save=False, show=True)

# Corner plot of parameters
fig = fit.plot_corner(save=False, show=True)

# Calibration plot (for spectroscopy)
fig = fit.plot_calibration(save=False, show=True)

# Observed data only
fig = galaxy.plot()
```

## Fitting Catalogs

```python
# Define IDs to fit
ids = ["001", "002", "003", ...]

# Create fit catalogue
fit_catalogue = pipes.fit_catalogue(
    ids, 
    fit_instructions, 
    load_photometry,
    spectrum_exists=False,
    filt_list=filt_list,
    run="my_run",           # Output folder name
    sampler="nautilus",
)

# Run fits
fit_catalogue.fit(verbose=False, n_cores=4)  # Parallel fitting

# Access results
for id in ids:
    fit = fit_catalogue.fits[id]
    mass = fit.posterior.samples['stellar_mass']
    print(f"{id}: log M* = {np.median(mass):.2f}")
```

## Common Model Setups

### Simple Exponential SFH
```python
fit_instructions = {
    "redshift": (0., 10.),
    "tau": {
        "age": (0.1, 15.),
        "tau": (0.3, 10.),
        "massformed": (1., 15.),
        "metallicity": (0., 2.5),
    },
    "dust": {
        "type": "Calzetti",
        "Av": (0., 2.),
    }
}
```

### Complex SFH with Nebular
```python
fit_instructions = {
    "redshift": (0., 10.),
    "dblplaw": {
        "tau": (0., 15.),
        "alpha": (0.01, 1000.),
        "beta": (0.01, 1000.),
        "alpha_prior": "log_10",
        "beta_prior": "log_10",
        "massformed": (1., 15.),
        "metallicity": (0., 2.5),
    },
    "dust": {
        "type": "Calzetti",
        "Av": (0., 3.),
    },
    "nebular": {
        "logU": (-4., -1.),
    }
}
```

### Fixed Redshift Fit
```python
fit_instructions = {
    "redshift": 1.5,  # Fixed value
    "tau": {
        "age": (0.1, 13.5),  # Universe age at z=1.5
        "tau": (0.3, 10.),
        "massformed": (1., 15.),
        "metallicity": (0., 2.5),
    },
    "dust": {
        "type": "Calzetti",
        "Av": (0., 2.),
    }
}
```

## Best Practices

### Data Preparation
1. **Flux units**: Photometry in uJy, spectroscopy in erg/s/cm^2/A
2. **Missing data**: Set flux=0 and large error (e.g., 9.9e99)
3. **SNR limits**: Cap maximum SNR to ~20-30 to prevent overfitting
4. **Filters**: Use consistent filter transmission curves

### Model Selection
1. **Start simple**: Begin with tau model, add complexity as needed
2. **Prior ranges**: Use physically motivated ranges
3. **Redshift**: Fix if known from spectroscopy
4. **Nebular emission**: Include for emission-line galaxies

### Convergence Checks
```python
# Check effective sample size
print(f"N_eff = {fit.posterior.n_eff}")

# Should be > 1000 for reliable results
if fit.posterior.n_eff < 1000:
    print("Warning: Low effective sample size!")
```

## Citation

If using BAGPIPES, cite:
- **Carnall et al. (2018)**: Primary code paper (MNRAS, 480, 4379)
- **Carnall et al. (2019)**: Spectroscopic fitting (MNRAS, 483, 3636)
- **Lange et al. (2023)**: Nautilus sampler (MNRAS, 525, 3181)

## External Resources

- **Documentation**: https://bagpipes.readthedocs.io/
- **GitHub**: https://github.com/ACCarnall/bagpipes
- **Tutorials**: https://github.com/ACCarnall/bagpipes/tree/master/examples
- **Paper**: https://arxiv.org/abs/1712.04452
