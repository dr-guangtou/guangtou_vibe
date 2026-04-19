# GALFIT Constraint File Grammar

Constraint files are referenced by the `G)` header entry of the main
config. Each non-blank, non-comment line is one constraint entry.

## Six Line Forms

| Form | Example | Semantics |
|---|---|---|
| Soft, relative | `2 x -1 0.5` | x of component 2 within [input-1, input+0.5] |
| Soft, absolute | `3 n 0.7 to 5` | n of component 3 in [0.7, 5] (keyword `to`) |
| Hard offset lock | `3_2_1_9 x offset` | x of components 3,2,1,9 tracks with preserved initial offsets |
| Hard ratio lock | `1_5_3_2 re ratio` | Re of components 1,5,3,2 tracks with preserved initial ratios |
| Soft pairwise diff | `3-7 mag -0.5 3` | (mag_7 - mag_3) within [-0.5, 3] |
| Soft pairwise ratio | `3/5 re 1 3` | (Re_3 / Re_5) within [1, 3] |

Separators in the first column disambiguate the form:

- `_` (underscore) -> hard coupling across N >= 2 components.
- `-` (hyphen) -> soft pairwise difference (exactly 2 components).
- `/` (slash) -> soft pairwise ratio bounds (exactly 2 components).
- No separator -> single component, soft range.

Range column shape disambiguates soft-single between relative and absolute:

- `low high` -> relative to each component's input value.
- `low to high` -> absolute bounds.

## Parameter Name Vocabulary

### Classical names

`x`, `y`, `mag`, `re` or `rs` (equivalent), `n`, `alpha`, `beta`, `gamma`,
`pa`, `q`, `c`.

### Hidden-block mode names

- `f<N>a` - Fourier mode N amplitude (e.g. `f1a`, `f6a`).
- `f<N>p` - Fourier mode N phase angle (e.g. `f1p`).
- `b<N>` - bending mode N amplitude (e.g. `b2`).
- `r<N>` - rotation slot N (e.g. `r5`).

### Integer parameter numbers

For the classical parameters, the integer number used in the `.galfit`
file also works in constraints: e.g. `3 n 0.7 to 5` and `3 5 0.7 to 5`
are equivalent (constrain parameter 5 of component 3 = Sersic n).

## Using the Parser

```python
import galfit_constraints as gc

entries = gc.read_constraints("constraints.txt")
for e in entries:
    print(e.components, e.parameter, e.coupling, e.bounds, e.absolute)

# Build entries programmatically
new = [
    gc.ConstraintEntry(
        components=[3], parameter="n",
        coupling="single", bounds=(0.7, 5.0), absolute=True,
    ),
    gc.ConstraintEntry(
        components=[3, 2, 1, 9], parameter="x",
        coupling="offset", bounds="offset",
    ),
    gc.ConstraintEntry(
        components=[3, 5], parameter="re",
        coupling="ratio_bounds", bounds=(1.0, 3.0),
    ),
]
gc.write_constraints(new, "new_constraints.txt")
```

## Coupling kinds

The parser uses these `coupling` tags (internal representation):

- `single` - single component, soft range.
- `offset` - hard offset lock (N components).
- `ratio` - hard ratio lock (N components).
- `diff` - soft pairwise difference (exactly 2 components).
- `ratio_bounds` - soft pairwise ratio range (exactly 2 components).

## Advisory

From README Section 11: "Parameter constraint files are NOT good to use...
The only constraints that are good to use are the ones in the GALFIT main
menu/template file or the 'offset' constraints in the constraint file."

In practice, prefer:
1. Setting the fit flag to 0 in the main menu (hard-fix a parameter).
2. Hard `offset` coupling when you know components move together (e.g.
   bulge and disk sharing a centroid).

Soft ranges (`low high` or `low to high`) are brittle - they interact
poorly with Levenberg-Marquardt and often push the solution to a bound.
