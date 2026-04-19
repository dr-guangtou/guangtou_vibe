# GALFIT Hidden Blocks

"Hidden" in the GALFIT docs means these rows do not appear in the default
menu template - users must add them deliberately. Each block attaches to
the light component whose `0)` line most recently appeared. psf and sky
silently ignore attached hidden blocks.

## Z) - skip in output

Single integer, no fit flag. `Z) 0` keeps the component in the residual
image; `Z) 1` leaves it in the model (does not subtract from data).

```
 Z) 0
```

## C0) - diskyness / boxyness

Single value + fit flag. Controls the isophote shape:

- `C0 < 0` - disky (pointy isophotes).
- `C0 > 0` - boxy (square isophotes).

```
C0) 0.15    1    # positive = boxy
```

Do not add C0 until the underlying ellipsoid has converged (per README
tip 4). A C0 value of exactly 0 is safe (unlike Fourier amplitude 0).

## B<N>) - Bending modes

Non-contiguous positive integer N; GALFIT supports an unrestricted number
of bending modes though "only the first three are most useful":

- `B1` - shear.
- `B2` - banana shape.
- `B3` - S-shape.

Syntax: one value + one fit flag.

```
B1) 0.07    1
B3) 0.02    1      # skipping B2 is fine
```

## F<N>) - Azimuthal Fourier modes

Non-contiguous positive integer N. Two values (amplitude, phase_deg) with
two fit flags:

```
F1) 0.07 30.0 1 1      # mode 1
F6) 0.03 10.5 1 1      # mode 6 (any integer is legal)
F20) 0.01 23.5 1 1     # mode 20
```

Gotcha: when attached to a truncation pseudo-component (T0 block), the
EXAMPLE.INPUT file uses only one fit flag instead of two:

```
F1) 0.1 30     1       # truncation-attached, single fit flag
```

The parser accepts both forms (single flag broadcasts to both values).

Zero-amplitude crashes GALFIT; if the user supplies `0`, GALFIT silently
resets to `0.01`. To keep a mode at zero, fix a different profile parameter
instead of initializing the Fourier amplitude to zero.

## R0)..R10) - Coordinate rotation (spiral structure)

Optional block that bends an underlying round light profile into a
spiral. Attaches to a light component.

### R0) - rotation function type

String, no fit flag. Documented values (README Section 8.3.4):

- `powerlaw` - alpha-tanh rotation (for bar-plus-spiral shapes).
- `log` - log-tanh rotation (logarithmic spiral).
- `none` - disable the block.

EXAMPLE.INPUT mentions `tanh`, `sqrt`, `linear` in a comment, but the
README restricts the implementation to `powerlaw | log | none`. The
parser warns (does not reject) on undocumented modes.

### R1-R10) - numeric rotation params (value + fit flag)

| Slot | Quantity | Units |
|---|---|---|
| `R1)` | bar radius r_in - where theta flattens to 0 | pixel |
| `R2)` | outer radius r_out - where theta hits asymptote | pixel |
| `R3)` | theta_out - cumulative rotation to r_out | degrees |
| `R4)` | alpha (for `powerlaw`) OR r_ws winding scale (for `log`) | - or pixel |
| `R9)` | theta_incl - inclination to line of sight | degrees |
| `R10)` | theta_PA_sky - sky position angle | degrees |

R5-R8 are not explicitly documented in the README but the constraint
grammar (`r5`, `r6`, ...) implies they exist. The parser stores any other
R<N>) slot under `RotationBlock.extra`.

```
R0) powerlaw
R1) 30.0    1
R2) 100.0   1
R3) 275.0   1
R4) 0.5     1
R9) 0.5     1
R10) 30.0   1
```

When R9 = 0 and R10 = 0, the classical `9) q` and `10) PA` of the light
profile still apply directly. When R9/R10 are set, they override the
classical q/PA semantics in a projection-aware way (README App. A).

## T0)..T10) - Truncation pseudo-component

T-blocks are a _standalone component_ (parsed like `0)` blocks but with
`T0)` as the first line), linked to one or two light profiles via `Ti)`
and `To)`. They modify the light profile's radial fall-off.

### T0) - truncation type

String, no fit flag. Types:

- `radial` - Type 1a, inclined axis + PA follow light profile's R-block.
  Uses softening _length_ in T3.
- `radial-b` - Type 1b, non-inclined (plane-of-sky shape).
- `radial2` - Type 2a, inclined, uses softening _radius_ in T3.
- `radial2-b` - Type 2b, non-inclined, softening radius.
- `length` - edgedisk-only: truncate along disk length.
- `height` - edgedisk-only: truncate along disk height.

### T1) - centroid (optional)

Two-value + two-flag, same format as `1)`. If omitted, the truncation
inherits the centroid of the linked light profile.

```
T1) 200.0 150.0  1 1
```

### T2-T10) - truncation numeric params (value + flag)

Authoritative meanings depend on T0 type:

- Type 1 (`radial`, `radial-b`):
  - T2) break radius (flux = 99% of original model at that radius)
  - T3) softening LENGTH (thickness of the transition band)
- Type 2 (`radial2`, `radial2-b`):
  - T2) break radius (inner)
  - T3) softening radius (outer, where flux = 1%)
- T9) optional axis ratio (inherits from light profile if omitted)
- T10) optional PA (inherits from light profile if omitted)
- T4/T5 - EXAMPLE.INPUT uses these interchangeably with T2/T3 due to
  historical inconsistencies. The parser stores whichever numbers appear.

F-modes and B-modes can be attached to a T0 block to modify the truncation
shape independently of the light profile:

```
T0) radial
T1) 200.0 150.0  1 1
T4) 4.42  1       # break radius
T5) 9.18  1       # softening length
T9) 0.7   1
T10) -32. 1
F1) 0.1 30  1     # Fourier mode modifying the truncation shape
```

## Ti) and To) - linked-component truncation references

Attached to a _light_ component (not to a T0 pseudo-component). Single
integer, no fit flag. Points at the component number that provides the
truncation.

```
 0) sersic
 1) 100 100 1 1
 ...
Ti) 5       # component 5 is the inner truncation
To) 2       # component 2 is the outer truncation
 Z) 0
```

The referenced components must themselves be T0 pseudo-component blocks.
Component numbers are 1-indexed in the order they appear in the file.

## Linking rules (README Section 6.2)

When two profiles are linked:
- `f_net(r) = Sum{f_inner(r)} * (1 - s(r)) + Sum{f_outer(r)} * s(r)`
- When linking, the flux parameter meaning shifts: the inner component's
  flux becomes surface brightness at the _original_ R_e (for sersic) or
  mu_0 (for everything else); the outer component's flux becomes surface
  brightness at the break radius.
- Use the `<name>3` flux-normalization suffix to explicitly mark a
  component as outer-truncated (see `profile_schemas.md`).
