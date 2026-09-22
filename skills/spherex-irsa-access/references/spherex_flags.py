"""Canonical SPHEREx Level 2 FLAGS bit definitions and mask helpers.

Source: SPHEREx Explanatory Supplement v2.0 (2026-08-25) Table 16, the IRSA
Spectrophotometry Tool help page, and live QR2 (VERSION 6.5.7) and QR3 (VERSION 7.0.5)
headers inspected on 2026-09-22.

Do not derive bit names from FITS headers: QR2 files use ``MP_<NAME>`` keywords, QR3 files
use ``MSKN####``/``MSKM####`` keywords and omit unused planes. This table is the same for
both releases.
"""

from __future__ import annotations

import numpy as np

FLAG_BITS: dict[str, int] = {
    "TRANSIENT": 0,
    "OVERFLOW": 1,
    "SUR_ERROR": 2,
    "PHANTOM": 4,  # QR2 headers only
    "REFERENCE": 5,  # QR2 headers only
    "NONFUNC": 6,
    "DICHROIC": 7,
    "MISSING_DATA": 9,
    "HOT": 10,
    "COLD": 11,
    "FULLSAMPLE": 12,
    "SUR_MISMATCH": 13,
    "PHANMISS": 14,
    "NONLINEAR": 15,
    "VAR_UNDER": 16,
    "PERSIST": 17,
    "PERSIST_UNK": 18,
    "OUTLIER": 19,
    "CROSSTALK": 20,
    "SOURCE": 21,
    "GHOST": 22,
    "GHOST_FPA": 23,
    "GHOST_EXT": 24,
    "STREAK": 25,
    "BLOOM": 26,
    "SNOWBALL": 27,
    "HALO": 28,
    "SATELLITE_HALO": 29,
    # Spectrophotometry Tool output only (not present in image FLAGS):
    "CONTAINS_BAD_PIXEL": 32,
    "FIT_ERROR": 33,
}

# Pixels the IRSA Spectrophotometry Tool ignores in the Tractor fit.
PHOTOMETRY_EXCLUDE = (
    "SUR_ERROR",
    "NONFUNC",
    "MISSING_DATA",
    "HOT",
    "COLD",
    "NONLINEAR",
    "PERSIST",
    "BLOOM",
    "SNOWBALL",
    "HALO",
    "SATELLITE_HALO",
)

# Pixels the IRSA Mosaic Tool drops before coadding (OVERFLOW, SOURCE, OUTLIER are
# propagated rather than excluded).
MOSAIC_EXCLUDE = PHOTOMETRY_EXCLUDE + (
    "TRANSIENT",
    "DICHROIC",
    "PHANMISS",
    "CROSSTALK",
    "GHOST",
    "GHOST_FPA",
    "GHOST_EXT",
    "STREAK",
)

# Conservative set for aperture photometry on galaxies: everything that marks a pixel as
# unreliable, plus OUTLIER; SOURCE is informational (the target itself is flagged SOURCE).
GALAXY_APERTURE_EXCLUDE = MOSAIC_EXCLUDE + ("OVERFLOW", "OUTLIER", "FULLSAMPLE")


def bitmask_for(names: tuple[str, ...] | list[str]) -> int:
    """Return the integer bitmask combining the named flags."""
    mask = 0
    for name in names:
        mask |= 1 << FLAG_BITS[name]
    return mask


def bad_pixel_mask(flags: np.ndarray, names: tuple[str, ...] | list[str] = GALAXY_APERTURE_EXCLUDE) -> np.ndarray:
    """Boolean array that is True where any of the named flags is set."""
    return (flags.astype(np.int64) & bitmask_for(names)) != 0


def decode(value: int) -> list[str]:
    """List the flag names set in an integer flag value."""
    value = int(value)
    return [name for name, bit in FLAG_BITS.items() if value & (1 << bit)]


def is_clean_measurement(value: int) -> bool:
    """True when a Spectrophotometry Tool row used only nominal pixels (0 or SOURCE only)."""
    return int(value) in (0, 1 << FLAG_BITS["SOURCE"])


if __name__ == "__main__":
    print("GALAXY_APERTURE_EXCLUDE mask =", bitmask_for(GALAXY_APERTURE_EXCLUDE))
    print("decode(4297064449) =", decode(4297064449))
