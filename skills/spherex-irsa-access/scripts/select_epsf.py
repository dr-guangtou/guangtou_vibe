#!/usr/bin/env python3
"""Select the SPHEREx ePSF zone for a sky position and render a native-pixel stamp.

Works with a QR3 (VERSION 7.x) spectral image or cutout that carries an EPSF binary table,
or with a QR2 image plus a standalone ePSF calibration file from
s3://nasa-irsa-spherex/qr3/epsf/ (recommended by the official September 2026 tutorial
instead of the old QR2 PSF cube).

Usage:
    python select_epsf.py <image_or_cutout_url> <ra> <dec> [--epsf-file <calibration_fits>]
"""

from __future__ import annotations

import argparse

import numpy as np
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.utils.data import conf
from astropy.wcs import WCS

conf.remote_timeout = 180


def open_with_retry(path_or_url: str, attempts: int = 3):
    """Open a FITS file, retrying on transient IRSA errors (HTTP 503, timeouts)."""
    import http.client
    import time
    import urllib.error

    for attempt in range(attempts):
        try:
            return fits.open(path_or_url, cache=False)
        except (TimeoutError, urllib.error.HTTPError, http.client.IncompleteRead):
            if attempt == attempts - 1:
                raise
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("unreachable")


def parent_frame_pixel(image_header, ra_deg: float, dec_deg: float) -> tuple[float, float]:
    """Return 0-based pixel coordinates of a sky position in the parent 2040x2040 frame."""
    wcs = WCS(image_header)
    x_cutout, y_cutout = wcs.world_to_pixel(SkyCoord(ra_deg, dec_deg, unit="deg"))
    x_orig = 1 + float(x_cutout) - image_header.get("CRPIX1A", 1)
    y_orig = 1 + float(y_cutout) - image_header.get("CRPIX2A", 1)
    return x_orig, y_orig


def nearest_epsf_row(epsf_table, x_orig: float, y_orig: float) -> int:
    """Index of the ePSF zone whose centre is closest to the parent-frame position."""
    distance = np.hypot(epsf_table["XCENTER"] - x_orig, epsf_table["YCENTER"] - y_orig)
    return int(np.argmin(distance))


def render_native_stamp(epsf_stamp: np.ndarray, oversampling: tuple[int, int], x0: float, y0: float, size: int = 11):
    """Shift, integrate to native pixels and renormalize the oversampled ePSF (photutils)."""
    from photutils.psf import ImagePSF

    model = ImagePSF(data=epsf_stamp, oversampling=oversampling)
    half = (size - 1) / 2.0
    x_ll, y_ll = int(np.floor(x0 - half)), int(np.floor(y0 - half))
    yy, xx = np.meshgrid(y_ll + np.arange(size), x_ll + np.arange(size), indexing="ij")
    stamp = model.evaluate(xx, yy, flux=1.0, x_0=x0, y_0=y0)
    total = stamp.sum()
    return stamp / total if total > 0 else stamp, x_ll, y_ll


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="spectral image or cutout path/URL")
    parser.add_argument("ra", type=float)
    parser.add_argument("dec", type=float)
    parser.add_argument("--epsf-file", help="standalone ePSF calibration FITS (for QR2 images)")
    args = parser.parse_args()

    with open_with_retry(args.image) as hdulist:
        version = hdulist[0].header.get("VERSION", "unknown")
        image_header = hdulist["IMAGE"].header
        x_orig, y_orig = parent_frame_pixel(image_header, args.ra, args.dec)
        print(f"VERSION {version}; parent-frame pixel = ({x_orig:.2f}, {y_orig:.2f})")
        if "EPSF" in hdulist:
            epsf_hdu = hdulist["EPSF"]
            table, header = epsf_hdu.data, epsf_hdu.header
        elif args.epsf_file:
            with fits.open(args.epsf_file, cache=False) as calibration:
                table, header = calibration["EPSF"].data.copy(), calibration["EPSF"].header.copy()
        else:
            raise SystemExit("No EPSF extension; pass --epsf-file with a qr3/epsf calibration file.")

    row = nearest_epsf_row(table, x_orig, y_orig)
    oversampling = (int(header.get("OVSMPY", 5)), int(header.get("OVSMPX", 5)))
    print(
        f"zone row {row}: BINX={table['BINX'][row]} BINY={table['BINY'][row]} "
        f"center=({table['XCENTER'][row]:.1f}, {table['YCENTER'][row]:.1f}) "
        f"NEFF_MEAN={table['NEFF_MEAN'][row]:.2f} CWAVE={table['CWAVE'][row]:.4f} um "
        f"CBAND={table['CBAND'][row]:.4f} um NSTAR={table['NSTAR'][row]}"
    )
    stamp, x_ll, y_ll = render_native_stamp(np.asarray(table["EPSF"][row]), oversampling, x_orig, y_orig)
    print(f"native 11x11 stamp lower-left parent pixel = ({x_ll}, {y_ll}); peak fraction = {stamp.max():.3f}")


if __name__ == "__main__":
    main()
