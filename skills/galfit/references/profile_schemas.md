# GALFIT Profile Parameter Cheat Sheet

All 11 supported profiles with the parameter-number -> physical-quantity
mapping. Line `0)` names the profile. Line `1)` is always position unless
noted. Line `Z)` is always the skip-output flag. Every numeric line also
carries a fit flag (`1` = fit, `0` = hold fixed) - position and multi-value
lines like `F1)` carry one flag per value.

## Flux-normalization suffix

Every radial profile name may have `1`, `2`, or `3` appended to change
the flux parameter's meaning. The suffix affects only parameter `3)`:

- `<name>` (default): see each profile below.
- `<name>1`: central surface brightness [mag/arcsec^2].
- `<name>2`: surface brightness at the profile's native size parameter
  (R_e for Sersic, FWHM for Gaussian, r_s for expdisk, etc.).
- `<name>3`: surface brightness at the break radius of an attached
  truncation (valid only when the component is truncation-linked).

Examples: `sersic2`, `gaussian1`, `moffat3`.

## sersic

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | integrated magnitude | mag |
| `4)` | R_e (effective radius) | pixel |
| `5)` | Sersic index n (deVauc = 4, expdisk = 1) | - |
| `9)` | axis ratio b/a | - |
| `10)` | position angle | degrees (up=0, left=90) |
| `Z)` | skip in output | 0 or 1 |

Note: GALFIT 3.0.7 writes reserved placeholder slots `6)`, `7)`, `8)` with
value 0 and fit flag 0 (comment "------") on every sersic restart. The
parser routes these to `extra_params`; leave them alone unless round-trip
requires emitting them.

## devauc

Same as sersic with `n` fixed at 4. No `5)`.

## expdisk

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | integrated magnitude | mag |
| `4)` | R_s (scale length; R_e = 1.678 R_s) | pixel |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

## edgedisk

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | central surface brightness mu_0 | mag/arcsec^2 |
| `4)` | disk scale height h_s | pixel |
| `5)` | disk scale length r_s | pixel |
| `10)` | PA | degrees |

No axis ratio: geometry is determined by `h_s` and `r_s`. No `9)`.

## gaussian

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | integrated magnitude | mag |
| `4)` | FWHM (not sigma; FWHM = 2.354 sigma) | pixel |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

## moffat

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | integrated magnitude | mag |
| `4)` | FWHM | pixel |
| `5)` | n (power-law concentration) | - |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

## nuker

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | mu(R_b) - surface brightness at R_b | mag/arcsec^2 |
| `4)` | R_b (break radius) | pixel |
| `5)` | alpha (transition sharpness) | - |
| `6)` | beta (outer power-law slope) | - |
| `7)` | gamma (inner power-law slope) | - |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

## king

Elson 1999 modified King profile.

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | mu(0) - central surface brightness | mag/arcsec^2 |
| `4)` | R_c (core radius) | pixel |
| `5)` | R_t (truncation radius) | pixel |
| `6)` | alpha (default 2, can be free) | - |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

## ferrer

Modified Ferrer profile - used for bars and lenses.

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | central surface brightness | mag/arcsec^2 |
| `4)` | r_out (outer truncation radius) | pixel |
| `5)` | alpha (outer truncation sharpness) | - |
| `6)` | beta (central slope) | - |
| `9)` | axis ratio | - |
| `10)` | PA | degrees |

Profile is zero beyond r_out.

## psf

Plain point-source; no size or shape parameters.

| Param | Quantity | Units |
|---|---|---|
| `1)` | x, y | pixel |
| `3)` | integrated magnitude | mag |

## sky

Unique: parameters 1/2/3 are not coordinates - they are the DC offset and
linear gradients, each on its own line.

| Param | Quantity | Units |
|---|---|---|
| `1)` | sky DC | ADU |
| `2)` | dsky/dx | ADU/pixel |
| `3)` | dsky/dy | ADU/pixel |

No `9)`, `10)`, C0, B, F, R, or T blocks (GALFIT will accept them but
ignore them, per README).

Sky pivot point is fixed at the image geometric center.

## Attachable hidden blocks

See `hidden_blocks.md` for C0, B*, F*, R*, T* details. Every light profile
(all of the above except psf and sky) supports them. psf and sky ignore any
hidden block attached to them.
