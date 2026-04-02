---
name: pysersic
title: PySersic Galaxy Profile Fitting
description: Bayesian Sérsic profile fitting for galaxy photometry using JAX/NumPyro. Use when fitting galaxy surface brightness profiles, extracting structural parameters, or performing multi-component galaxy decomposition.
tags: [astronomy, galaxy, photometry, sersic, bayesian]
---

# PySersic — Bayesian Galaxy Profile Fitting

Fit Sérsic (and related) profiles to galaxy images using JAX-accelerated Bayesian inference via NumPyro.

- **Docs:** https://pysersic.readthedocs.io/en/latest/
- **Code:** https://github.com/pysersic/pysersic
- **Paper:** https://arxiv.org/abs/2306.05454 (Pasha & Miller 2023, JOSS)
- **Example notebooks:** https://github.com/pysersic/pysersic/tree/main/docs

## Installation

```bash
pip install pysersic
# If arviz 1.0+ breaks it:
pip install 'arviz<1.0'
# If photutils is too old for numpy 2:
pip install --upgrade photutils
```

**JAX backend:**
- CPU (macOS/Linux): `pip install 'jax[cpu]'`
- GPU (Linux NVIDIA CUDA 12): `pip install --upgrade 'jax[cuda12]'`

Dependencies: JAX, NumPyro, astropy, photutils, scipy, matplotlib, arviz (<1.0), asdf, corner, equinox, interpax, tqdm.

## Profile Types

| `profile_type` | Description |
|----------------|-------------|
| `"sersic"` | General Sérsic (free n) |
| `"exp"` | Exponential (n=1, disk) |
| `"dev"` | de Vaucouleurs (n=4, bulge) |
| `"doublesersic"` | Two Sérsic components |
| `"pointsource"` | Unresolved source |

## Core Workflow

### 1. Prepare inputs (numpy arrays)

```python
import numpy as np
from astropy.io import fits

# Image cutout, RMS (sigma/noise) map, PSF, mask (True = bad pixel)
image = fits.getdata("image.fits").astype(float)
rms = np.sqrt(fits.getdata("variance.fits").astype(float))
psf = fits.getdata("psf.fits").astype(float)
psf /= psf.sum()  # normalize
mask = fits.getdata("mask.fits").astype(bool)  # True = masked
```

### 2. Validate inputs

```python
from pysersic import check_input_data
check_input_data(data=image, rms=rms, psf=psf, mask=mask)
```

### 3. Set up prior

**Auto-prior (recommended for quick start):**

```python
from pysersic.priors import autoprior

prior = autoprior(
    image=image,
    profile_type="sersic",
    mask=mask,
    sky_type="none",  # "none", "flat", or "tilted-plane"
)
```

**Manual prior via SourceProperties:**

```python
from pysersic.priors import SourceProperties

props = SourceProperties(image, mask=mask)
# Override guesses if needed:
# props.set_flux_guess(flux, flux_err)
# props.set_r_eff_guess(r_eff, r_eff_err)
prior = props.generate_prior("sersic", sky_type="none")
```

### 4. Create fitter and run

```python
from pysersic import FitSingle
from pysersic.loss import gaussian_loss, student_t_loss
from jax.random import PRNGKey

fitter = FitSingle(
    data=image,
    rms=rms,
    psf=psf,
    prior=prior,
    mask=mask,
    loss_func=student_t_loss,  # robust to outliers
)

# MAP (fast, seconds)
map_params = fitter.find_MAP(rkey=PRNGKey(42))

# Posterior approximation (minutes)
svi_res = fitter.estimate_posterior(rkey=PRNGKey(43), method="svi-flow")

# Full NUTS sampling (slower, most accurate)
fitter.sample(rkey=PRNGKey(44))
sampling_res = fitter.sampling_results
```

### 5. Results

```python
from pysersic.results import plot_residual

# Residual plot: data | model | residual
fig, ax = plot_residual(image, map_params["model"], mask=mask, vmin=-1, vmax=1)

# Parameter summary
sampling_res.summary()

# Corner plot
fig = sampling_res.corner()

# Quantiles as DataFrame
df = sampling_res.retrieve_param_quantiles(return_dataframe=True)

# LaTeX table
sampling_res.latex_table()

# Save to ASDF
sampling_res.save_result("fit_result.asdf")
```

## Multi-Source Fitting

```python
from pysersic import FitMulti
from pysersic.priors import PySersicMultiPrior, estimate_sky
from pysersic.results import parse_multi_results

# Source catalog (from sep, photutils, or manual)
catalog = {
    "flux": [1000, 500, 50],
    "x": [50.0, 30.0, 70.0],
    "y": [50.0, 60.0, 40.0],
    "r": [5.0, 3.0, 1.0],       # effective radius guess
    "type": ["sersic", "sersic", "pointsource"],
}

# Sky estimate
med_sky, std_sky, n_pix = estimate_sky(image, mask)

prior = PySersicMultiPrior(
    catalog=catalog,
    sky_type="flat",
    sky_guess=med_sky,
    sky_guess_err=2 * std_sky / np.sqrt(n_pix),
)

fm = FitMulti(data=image, rms=rms, psf=psf, prior=prior)
map_dict = fm.find_MAP(rkey=PRNGKey(99))

# Extract single source from multi-fit
fm.estimate_posterior(method="laplace", rkey=PRNGKey(100))
source_2 = parse_multi_results(fm.svi_results, 2)
source_2.summary()
```

## Key Parameters (Sérsic fit)

| Parameter | Description | Typical range |
|-----------|-------------|---------------|
| `xc`, `yc` | Centroid (pixels) | image center ± few pix |
| `flux` / `Ftot` | Total flux | > 0 |
| `r_eff` | Half-light radius (pixels) | 1–100 |
| `n` | Sérsic index | 0.5–8 |
| `ellip` | Ellipticity (1 - b/a) | 0–0.9 |
| `theta` | Position angle (radians) | 0–π |

## Tips

- **Loss function:** Use `student_t_loss` for robustness to bad pixels/artifacts; `gaussian_loss` for clean data.
- **Sky model:** Use `sky_type="none"` if background is already subtracted; `"flat"` to fit a constant residual.
- **PSF:** Must be normalized (sum=1), same pixel scale as image. Odd dimensions preferred.
- **Mask convention:** `True` = bad/masked pixel (excluded from fit).
- **Speed:** MAP takes seconds; `svi-flow` takes minutes; NUTS sampling takes 5–30 min per source.
- **macOS:** JAX GPU not supported; CPU-only. Still fast for individual sources.
- **Multi-band:** Not natively supported as a single call. Fit bands independently, then combine posteriors. Or define custom NumPyro model for joint fitting.
