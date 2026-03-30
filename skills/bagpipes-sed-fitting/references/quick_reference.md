# BAGPIPES Quick Reference

## Installation
```bash
pip install bagpipes
```

## Basic Workflow
```python
import bagpipes as pipes

# 1. Load data
galaxy = pipes.galaxy(ID, load_function, filt_list=filters)

# 2. Define model
fit_instructions = {
    "redshift": (0., 10.),
    "tau": {"age": (0.1, 15.), "tau": (0.3, 10.), ...},
    "dust": {"type": "Calzetti", "Av": (0., 2.)},
}

# 3. Run fit
fit = pipes.fit(galaxy, fit_instructions, sampler="nautilus")
fit.fit()

# 4. Extract results
samples = fit.posterior.samples
median_mass = np.median(samples['stellar_mass'])
```

## SFH Components

| Component | Key Parameters |
|-----------|----------------|
| `burst` | `age`, `massformed`, `metallicity` |
| `constant` | `age`, `massformed`, `metallicity` |
| `tau` | `age`, `tau`, `massformed`, `metallicity` |
| `delayed` | `age`, `tau`, `massformed`, `metallicity` |
| `lognormal` | `age`, `tau`, `massformed`, `metallicity` |
| `dblplaw` | `age`, `tau`, `alpha`, `beta`, `massformed`, `metallicity` |

## Dust Models

| Type | Parameters |
|------|------------|
| `Calzetti` | `Av`, optional `eta` |
| `CF00` | `Av`, `mu` (two-component) |
| `Salim` | `Av`, `delta`, `B`, `Rv` |

## Priors

```python
# Uniform (default)
component["param"] = (min, max)

# Log-uniform
component["param"] = (0.01, 100)
component["param_prior"] = "log_10"

# Gaussian with limits
component["param"] = (0., 1.)
component["param_prior"] = "Gaussian"
component["param_prior_mu"] = 0.5
component["param_prior_sigma"] = 0.1
```

**Available:** `uniform`, `log_10`, `log_e`, `pow_10`, `recip`, `recipsq`, `Gaussian`

## Data Format

### Photometry (uJy)
```python
def load_photometry(ID):
    fluxes = [...]      # Shape: (N_bands,)
    fluxerrs = [...]    # Shape: (N_bands,)
    return np.c_[fluxes, fluxerrs]  # Shape: (N_bands, 2)
```

### Spectroscopy (erg/s/cm^2/A)
```python
def load_spectrum(ID):
    wave = [...]        # Angstroms
    flux = [...]
    error = [...]
    spec = np.c_[wave, flux, error]
    mask = np.ones(len(wave), dtype=bool)
    return spec, mask
```

## Common Fit Instructions

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

### With Nebular Emission
```python
fit_instructions["nebular"] = {"logU": -3.}
# Or varying: {"logU": (-4., -1.)}
```

### Fixed Redshift
```python
fit_instructions["redshift"] = 1.5  # Fixed value
```

## Nautilus Sampler Options

```python
fit = pipes.fit(
    galaxy, 
    fit_instructions,
    sampler="nautilus",
    n_live=1000,      # Number of live points
    n_eff=10000,      # Target effective sample size
)
```

## Extracting Results

```python
# Posterior samples dict
samples = fit.posterior.samples

# Median values
median = fit.posterior.median

# Confidence intervals
conf_int = fit.posterior.conf_int

# Specific parameter
mass = samples['stellar_mass']
print(f"log M* = {np.median(mass):.2f} ± {np.std(mass):.2f}")

# Evidence
evidence = fit.posterior.ln_evidence

# Max likelihood
max_like = fit.posterior.max_like_params
```

## Plotting

```python
# Fit results
fit.plot_spectrum_posterior()
fit.plot_sfh_posterior()
fit.plot_corner()
fit.plot_calibration()  # For spectroscopy

# Observed data
galaxy.plot()
```

## Batch Fitting

```python
fit_catalogue = pipes.fit_catalogue(
    ids, 
    fit_instructions,
    load_photometry,
    spectrum_exists=False,
    filt_list=filt_list,
    run="my_run",
)
fit_catalogue.fit(verbose=False, n_cores=4)

# Access individual fits
fit = fit_catalogue.fits[id]
```

## Best Practices

1. **Data prep:** Handle missing data (flux=0, error=9.9e99)
2. **SNR limits:** Cap at ~20-30 to prevent overfitting
3. **Start simple:** Use tau model before complex SFH
4. **Check convergence:** N_eff should be > 1000
5. **Physical priors:** Use reasonable parameter ranges
6. **Fix redshift:** If known from spectroscopy

## Citation

```
Carnall et al. (2018): Main code paper, MNRAS, 480, 4379
Carnall et al. (2019): Spectroscopic fitting, MNRAS, 483, 3636
Lange et al. (2023): Nautilus sampler, MNRAS, 525, 3181
```

## Links

- Documentation: https://bagpipes.readthedocs.io/
- GitHub: https://github.com/ACCarnall/bagpipes
- Paper: https://arxiv.org/abs/1712.04452
