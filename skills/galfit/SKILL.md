---
name: galfit
description: Guidance and a bundled round-tripping parser for the GALFIT 2-D galaxy image-fitting code (Peng 2002/2010). Use when the task involves GALFIT input/output files (`.galfit`, `.feedme`, `galfit.NN` restart files), GALFIT constraint files, invoking the GALFIT binary, converting GALFIT configs to or from YAML/JSON, or questions about GALFIT profile parameters (sersic, nuker, moffat, king, ferrer, edgedisk, expdisk, devauc, gaussian, psf, sky) and hidden blocks (C0 diskyness/boxyness, Fourier modes, bending modes, coordinate rotation R0-R10, truncation T0-T10).
---

# GALFIT

Use this skill when you need to read, write, analyze, or modify GALFIT config
and output files, or to drive the GALFIT binary itself. A fully tested
parser is shipped under `scripts/`.

## Quick Start

1. Confirm what the task needs: reading a `.galfit` input, reading a
   `galfit.NN` restart/output, editing parameters, running a fit, or
   writing constraint files.
2. Load only the minimal reference files needed:
   - `references/index.md` always first.
   - Profile-parameter questions: `references/profile_schemas.md`.
   - Hidden block questions (C0, B/F/R/T): `references/hidden_blocks.md`.
   - Interpreting a `galfit.NN` output: `references/output_decorations.md`.
   - Constraint files: `references/constraint_grammar.md`.
   - Running the binary: `references/binary_usage.md`.
   - Debugging weird outputs: `references/top10_gotchas.md`.
3. Use the bundled parser to read/write/round-trip. Prefer the parser over
   hand-rolling regex - it correctly handles every documented form plus the
   real-world quirks (GALFIT 3.0.7's reserved `6)/7)/8)` placeholders on
   sersic, 1-flag-broadcast Fourier on truncation blocks, envelope
   composition `[*value*]`, etc.).

## Using the Parser

The parser lives at `<skill-dir>/scripts/`. Two modules:

- `galfit_io.py` - `.galfit` / `.feedme` / `galfit.NN` files.
- `galfit_constraints.py` - constraint files referenced by the `G)` header.

### From Python

```python
import sys
sys.path.insert(0, "<skill-dir>/scripts")

import galfit_io
import galfit_constraints

# Read an input or restart file
gf = galfit_io.read_galfit("galfit.01")
print(gf.header.zeropoint, len(gf.components))

# Inspect a Sersic component
sersic = next(c for c in gf.components if isinstance(c, galfit_io.SersicComponent))
print(sersic.mag.value, sersic.mag.uncertainty)   # uncertainty only in outputs

# Modify and write back (output-decoration stripping by default)
sersic.mag.value = 19.8
galfit_io.write_galfit(gf, "galfit.02")

# Round-trip through YAML for structured config management
yaml_text = galfit_io.to_yaml(gf)
gf2 = galfit_io.from_yaml(yaml_text)
assert galfit_io.to_dict(gf) == galfit_io.to_dict(gf2)

# Constraint files
entries = galfit_constraints.read_constraints("constraints.txt")
for e in entries:
    print(e.components, e.parameter, e.bounds, e.coupling)
```

### From the shell

The parser supplies a convenience CLI for common tasks:

```bash
python <skill-dir>/scripts/galfit_cli.py to-yaml galfit.01 galfit.01.yaml
python <skill-dir>/scripts/galfit_cli.py from-yaml galfit.01.yaml galfit.02
python <skill-dir>/scripts/galfit_cli.py summary galfit.01
```

## Design Notes (why the parser is worth using)

- Tagged-union component classes: one `@dataclass` per profile, each with
  profile-specific fields (e.g. `NukerComponent.alpha` / `.beta` / `.gamma`
  but `SersicComponent.n` only). A flat `dict[str, float]` would lose those
  semantics on round-trip.
- `FittedValue` captures the four output-file decorations independently so
  `[*value*]` (held and suspicious) round-trips correctly.
- `extra_params` on every component absorbs GALFIT's reserved placeholder
  slots (`6) 7) 8)` on sersic in 3.0.7 output) - community parsers silently
  drop these and break round-trip.
- `HiddenBlocks` uses sparse `dict[int, ...]` for bending and Fourier modes
  because GALFIT indices are not contiguous (you can have F1, F6, F20 in
  one block).

## Running the GALFIT Binary

Consult `references/binary_usage.md` before running. Baseline recipe:

```bash
# <galfit-binary> <feedme-file>
galfit -imax 50 my_fit.feedme        # bounded iteration count
galfit -o1 my_fit.feedme             # generate model only, no fit
galfit -noskyest my_fit.feedme       # skip internal sky estimate
```

After a run, read `galfit.NN` (the highest-numbered restart) with this
parser to get structured post-fit parameters plus uncertainties.

## References

- `references/index.md` - table of contents for references, load this first
- `references/profile_schemas.md` - parameter tables for all 11 profiles
- `references/hidden_blocks.md` - Z, C0, B/F/R/T and the truncation block
- `references/output_decorations.md` - `[]`, `{}`, `*`, `(err)` semantics
- `references/constraint_grammar.md` - 6 constraint line forms
- `references/binary_usage.md` - invoking the GALFIT binary
- `references/top10_gotchas.md` - distilled pitfalls from GALFIT docs

## Scripts

- `scripts/galfit_io.py` - parser for `.galfit` / `.feedme` / `galfit.NN`
- `scripts/galfit_constraints.py` - parser for constraint files
- `scripts/galfit_cli.py` - thin CLI wrapper for common conversions
