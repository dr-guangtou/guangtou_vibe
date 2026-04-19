# GALFIT TOP 10 Gotchas (Parser + Fitter)

Distilled from the official TOP10 page, the advisory page, and real-world
experience with GALFIT 3.0.7.

## Parser-Level

1. **Row order within a block is arbitrary.** The only fixed rule is that
   `0)` (or `T0)`) comes first. Everything else keys on the letter/number.
   A parser that position-locks will break on real files.

2. **Column alignment is aesthetic only.** At least one whitespace between
   `)` and the first value, otherwise anything goes.

3. **Fourier mode indices are sparse.** You can have `F1`, `F6`, `F20` in
   one block, nothing in between. Any positive integer is legal.

4. **Truncation-attached `F<N>)` sometimes uses 1 fit flag instead of 2.**
   See EXAMPLE.INPUT. The parser broadcasts a single flag to both values.

5. **GALFIT 3.0.7 emits reserved placeholder slots.** Sersic output contains
   `6) 0.0 0 # ------`, same for `7)` and `8)`. A strict schema-only parser
   rejects the file. The shipped parser puts these in `extra_params`.

6. **Output decorations compose in any order.** `[*0.15*]` (held + suspicious),
   `{0.3}` (constrained), `[4.0]` (fixed). Peel layer by layer; do not
   assume a fixed ordering.

7. **Version 2 to 3 renumbering.** Old files used `8) q 9) PA 10) C0`. New
   files use `9) q 10) PA C0)`. If a file has `8)` with a non-zero value
   and fit flag set, it's probably legacy. Parser warns and remaps.

## Fitter-Level

8. **Never trust a `*value*` result.** Even if the fit "converged",
   asterisks mean the covariance matrix was pathological. Re-fit with
   that parameter held fixed or with better initial guesses.

9. **FWHM parameter is in pixels, not arcsec.** For Moffat and Gaussian,
   both the README and EXAMPLE.INPUT clearly say so. Convert via `K)`
   plate scale if you're thinking in angular units.

10. **Fourier amplitudes cannot start at exactly 0.** GALFIT silently
    resets `F<N>) 0 ...` to `0.01`. If you want a mode to stay near zero
    after a fit, hold the amplitude fixed via the fit flag instead of
    relying on the initial value.

## Workflow-Level

11. **`galfit.NN` counter monotonically increases in a directory.** Start
    in a clean directory or clean old restart files if the numbering
    confuses you.

12. **`fit.log` is appended across runs.** To isolate one run's log, note
    the file length before the run and `tail` after.

13. **Add C0 and Fourier modes only after the ellipsoid has converged.**
    Adding high-order shape terms at the start leads to degenerate
    solutions.

14. **The `G) constraints.txt` path is resolved from cwd, not the feedme
    location.** Same rule as for the data image.

15. **Constraint files are dangerous (README Section 11).** Only the
    `offset` hard coupling is considered safe. Prefer setting fit flags
    in the main file over soft ranges.

## Numerical Conditioning

16. **R_e < ~0.5 pixels triggers convergence problems.** Trims with the
    PSF-FWHM or upsamples the PSF via `E)` may help.

17. **Very low axis ratios (q < 0.1)** often get asterisked due to
    parameter degeneracies with the disk scale length.

18. **Strong bar-plus-disk models are prone to bar length / disk
    length swaps** if the initial guesses are too close. Enforce hard
    `offset` coupling on the centroids and let the size parameters fit
    freely.
