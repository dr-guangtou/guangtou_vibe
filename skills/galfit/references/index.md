# GALFIT Reference Index

Load files on demand. Never load everything at once.

| File | Use when |
|---|---|
| `profile_schemas.md` | You need the parameter-number -> physical-quantity mapping for any of the 11 profiles, or you're editing parameter values by number. |
| `hidden_blocks.md` | The file contains (or you need to write) C0, B1/B2/B3, F1/F6/F20, R0-R10, T0-T10, Ti, To. |
| `output_decorations.md` | You're parsing or writing a `galfit.NN` restart/output file. Anything with `[val]`, `{val}`, `*val*`, or `(err)` tokens. |
| `constraint_grammar.md` | The task involves the constraint file referenced by the `G)` header entry. |
| `binary_usage.md` | You need to invoke the GALFIT binary, pick command-line flags, read `imgblock.fits`, or interpret exit codes. |
| `top10_gotchas.md` | Fit is failing or behaving unexpectedly; quick distilled pitfalls from the official TOP10 and advisory pages. |

## Authoritative Sources

- `README.pdf` on the GALFIT website at
  https://users.obs.carnegiescience.edu/peng/work/galfit/README.pdf
- `EXAMPLE.INPUT` and `EXAMPLE.CONSTRAINTS` ship with the GALFIT source
  install (on this machine: `/Users/shuang/code/galfit/`).
- Target GALFIT version: 3.0.4+ (tested against 3.0.7).

## Parser Surface (for quick recall)

- `galfit_io.read_galfit(path) -> GalfitFile`
- `galfit_io.write_galfit(gf, path, *, preserve_decorations=False)`
- `galfit_io.to_yaml(gf) / from_yaml(text)`
- `galfit_io.to_json(gf) / from_json(text)`
- `galfit_io.to_dict(gf) / from_dict(data)`
- `galfit_constraints.read_constraints(path) -> list[ConstraintEntry]`
- `galfit_constraints.write_constraints(entries, path)`
- `galfit_constraints.to_yaml_constraints / from_yaml_constraints`

Component classes: `SersicComponent`, `DevaucComponent`, `ExpdiskComponent`,
`EdgediskComponent`, `GaussianComponent`, `MoffatComponent`, `NukerComponent`,
`KingComponent`, `FerrerComponent`, `PsfComponent`, `SkyComponent`,
`TruncationComponent`. Use `isinstance(c, SersicComponent)` to dispatch.
