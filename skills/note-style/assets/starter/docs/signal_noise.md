# Signal and noise

This note describes a simplified counting-noise model for a measurement.
It establishes the assumptions and notation before using the equation in
a calculation.

## Assumptions

Signal and background counts follow independent Poisson processes. Read
noise is independent between detector samples. All counts refer to the
same measurement aperture and exposure.

The background contribution below describes the noise present in the
measurement. Additional uncertainty from estimating the background must
be included when the estimation procedure introduces it.

## Model

Let $S$ and $B$ be the expected signal and background electron counts.
Let $n$ be the number of independent detector samples and $r$ the
root-mean-square read-noise contribution per sample, expressed numerically
in electrons.

```{math}
:label: eq_signal_noise
\mathrm{SNR} = \frac{S}{\sqrt{S + B + n r^2}}
```

Equation {eq}`eq_signal_noise` combines the independent variance terms.
The denominator is the root-mean-square uncertainty of the measurement.

| Symbol | Meaning | Convention |
| --- | --- | --- |
| $S$ | Expected signal count | Electron count within the measurement aperture |
| $B$ | Expected background count | Electron count within the same aperture |
| $n$ | Number of independent samples | Detector samples included in the measurement |
| $r$ | Read noise per sample | Root-mean-square electron count |

## Calculation

The implementation keeps the physical quantities explicit.

```python
def signal_noise_ratio(signal_count, background_count, sample_count, read_noise):
    variance = signal_count + background_count + sample_count * read_noise**2
    return signal_count / variance**0.5
```

```{note}
This expression assumes non-negative expected counts and positive total
variance. A project implementation should define how it handles invalid
inputs and measurements outside those assumptions.
```

## Extending the model

Correlated detector noise, background-estimation uncertainty, calibration
errors, and extraction weights can change the variance model. Record each
additional contribution and the conditions under which it applies before
comparing results between simulations.

Return to the [project overview](index.md) to explore the document structure.
