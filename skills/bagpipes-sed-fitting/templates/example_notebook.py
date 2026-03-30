"""
BAGPIPES SED Fitting Tutorial Notebook (Python script version)
===============================================================

This script demonstrates BAGPIPES SED fitting for photometric data.
Convert to Jupyter notebook with: jupytext --to notebook example_notebook.py

Requirements:
    pip install bagpipes numpy matplotlib astropy
"""

# %% [markdown]
# # BAGPIPES SED Fitting Tutorial
#
# This notebook demonstrates how to:
# 1. Load photometric data
# 2. Define model components and priors
# 3. Run Bayesian SED fitting with nautilus
# 4. Extract and visualize results

# %%
# Imports
import numpy as np
import matplotlib.pyplot as plt
import bagpipes as pipes

print("BAGPIPES version:", pipes.__version__)

# %% [markdown]
# ## 1. Load Photometric Data
#
# BAGPIPES requires a data loading function that takes an object ID and returns
# a 2D array of shape (N_bands, 2) with fluxes and errors in micro-Janskys (uJy).

# %%
def load_example_photometry(ID):
    """
    Example data loader for demonstration.
    
    In practice, replace this with your own catalog loading code.
    """
    # Example: Create synthetic photometry for testing
    np.random.seed(int(ID) if ID.isdigit() else 42)
    
    # 15 photometric bands
    n_bands = 15
    
    # Simulate a galaxy SED (very roughly)
    # UV faint, optical bright, IR decline
    true_sed = np.array([
        0.5, 0.6, 0.8, 1.0, 1.2,  # UV/blue
        1.5, 1.8, 2.0, 1.9, 1.7,  # Optical
        1.4, 1.1, 0.9, 0.7, 0.5   # NIR
    ])
    
    # Add noise
    fluxes = true_sed * np.random.lognormal(0, 0.2, n_bands)
    fluxerrs = fluxes * 0.1  # 10% errors
    
    # Handle missing data (example: last band missing)
    fluxes[-1] = 0.
    fluxerrs[-1] = 9.9e99
    
    return np.c_[fluxes, fluxerrs]


# Example filter list (adjust to your data)
filt_list = np.array([
    "U", "B", "V", "R", "I",
    "J", "H", "Ks", "IRAC1", "IRAC2",
    "IRAC3", "IRAC4", "MIPS24", "MIPS70", "MIPS160"
])

# %%
# Test data loading
object_id = "001"
photometry = load_example_photometry(object_id)

print(f"Photometry shape: {photometry.shape}")
print(f"Fluxes: {photometry[:, 0]}")
print(f"Errors: {photometry[:, 1]}")

# %% [markdown]
# ## 2. Create Galaxy Object

# %%
galaxy = pipes.galaxy(
    object_id,
    load_example_photometry,
    spectrum_exists=False,
    filt_list=filt_list
)

# Plot observed data
fig = galaxy.plot()
plt.title(f"Observed Photometry: {object_id}")
plt.show()

# %% [markdown]
# ## 3. Define Model Components
#
# We'll set up a model with:
# - Exponential tau SFH
# - Calzetti dust attenuation
# - Varying redshift

# %%
# SFH component: Exponential tau model
exp = {}
exp["age"] = (0.1, 15.)           # Age: 0.1 to 15 Gyr
exp["tau"] = (0.3, 10.)           # SFH timescale: 0.3 to 10 Gyr
exp["massformed"] = (1., 15.)     # log10 stellar mass
exp["metallicity"] = (0., 2.5)    # Metallicity: 0 to 2.5 solar

# Dust component
dust = {}
dust["type"] = "Calzetti"
dust["Av"] = (0., 2.)             # V-band extinction

# Combine into fit instructions
fit_instructions = {}
fit_instructions["redshift"] = (0., 10.)  # Uniform prior 0-10
fit_instructions["tau"] = exp
fit_instructions["dust"] = dust

print("Fit instructions:")
for key, value in fit_instructions.items():
    print(f"  {key}: {value}")

# %% [markdown]
# ## 4. Alternative: Double Power-Law SFH
#
# For comparison, here's a more flexible SFH model.

# %%
dblplaw = {}
dblplaw["tau"] = (0., 15.)                # Time of peak SFR
dblplaw["alpha"] = (0.01, 1000.)          # Falling slope
dblplaw["beta"] = (0.01, 1000.)           # Rising slope
dblplaw["alpha_prior"] = "log_10"         # Log-uniform prior
dblplaw["beta_prior"] = "log_10"
dblplaw["massformed"] = (1., 15.)
dblplaw["metallicity"] = (0., 2.5)

fit_instructions_dblplaw = {
    "redshift": (0., 10.),
    "dblplaw": dblplaw,
    "dust": {"type": "Calzetti", "Av": (0., 2.)}
}

# %% [markdown]
# ## 5. Run SED Fit with Nautilus

# %%
print("Running SED fit...")
print("This may take a few minutes...")

fit = pipes.fit(galaxy, fit_instructions, sampler="nautilus")
fit.fit(verbose=False)

print("Fit complete!")

# %% [markdown]
# ## 6. Extract and Display Results

# %%
# Posterior samples
samples = fit.posterior.samples

# Print available parameters
print("\nAvailable parameters:")
print(list(samples.keys()))

# %%
# Display median values and uncertainties
print("\n" + "="*60)
print("FIT RESULTS")
print("="*60)

params_to_show = [
    'redshift',
    'tau:age',
    'tau:tau',
    'tau:massformed',
    'tau:metallicity',
    'dust:Av',
    'stellar_mass',
    'sfr',
    'mass_weighted_age',
]

print("\nParameter Estimates (median ± std):")
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

# %% [markdown]
# ## 7. Visualization

# %%
# Spectrum/photometry posterior
fig = fit.plot_spectrum_posterior(save=False, show=False)
plt.title(f"SED Posterior: {object_id}")
plt.show()

# %%
# Star formation history
fig = fit.plot_sfh_posterior(save=False, show=False)
plt.title(f"Star Formation History: {object_id}")
plt.show()

# %%
# Corner plot (may take a moment)
print("Generating corner plot...")
try:
    fig = fit.plot_corner(save=False, show=False)
    plt.suptitle(f"Parameter Posteriors: {object_id}")
    plt.show()
except Exception as e:
    print(f"Corner plot failed: {e}")

# %% [markdown]
# ## 8. Access Posterior Samples

# %%
# Work directly with samples
mass_samples = samples['stellar_mass']
sfr_samples = samples['sfr']

print(f"Stellar mass distribution:")
print(f"  Median: {np.median(mass_samples):.2f}")
print(f"  16th percentile: {np.percentile(mass_samples, 16):.2f}")
print(f"  84th percentile: {np.percentile(mass_samples, 84):.2f}")

# Mass-SFR relation
plt.figure(figsize=(8, 6))
plt.scatter(mass_samples, sfr_samples, alpha=0.3, s=1)
plt.xlabel('log Stellar Mass')
plt.ylabel('log SFR')
plt.title('Mass-SFR Relation from Posterior')
plt.show()

# %% [markdown]
# ## 9. Model Comparison
#
# Compare different SFH models using Bayesian evidence.

# %%
print("\n" + "="*60)
print("Model Comparison")
print("="*60)

# Fit double power-law model
print("\nFitting double power-law model...")
fit_dblplaw = pipes.fit(galaxy, fit_instructions_dblplaw, sampler="nautilus")
fit_dblplaw.fit(verbose=False)

# Compare evidence
lnZ_tau = fit.posterior.ln_evidence
lnZ_dblplaw = fit_dblplaw.posterior.ln_evidence

print(f"\nLog Evidence:")
print(f"  Tau model:      {lnZ_tau:.2f}")
print(f"  Dblplaw model:  {lnZ_dblplaw:.2f}")
print(f"  Delta lnZ:      {lnZ_dblplaw - lnZ_tau:.2f}")

if lnZ_dblplaw - lnZ_tau > 2:
    print("\nDouble power-law is strongly favored")
elif lnZ_dblplaw - lnZ_tau > 0.5:
    print("\nDouble power-law is moderately favored")
else:
    print("\nNo strong preference between models")

# %% [markdown]
# ## 10. Summary
#
# This notebook demonstrated:
# - Loading photometric data
# - Setting up model components with priors
# - Running Bayesian SED fits with nautilus
# - Extracting and visualizing results
# - Comparing different models
#
# For more advanced usage (spectroscopic fitting, custom models, etc.),
# see the BAGPIPES documentation.

# %%
print("\nTutorial complete!")
