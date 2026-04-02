#!/usr/bin/env python
"""Demo: run AutoProf on a single SGA galaxy image.

Must be run with the AutoProf-specific venv:
    /tmp/autoprof_venv/bin/python demo_autoprof.py

Reads a Legacy Survey r-band image (uncompressed), applies pipeline mask,
runs the default FFT-based isophote fitting, and prints the profile.
"""

import os
import sys
import tempfile

import numpy as np
from astropy.io import fits
from autoprof.Pipeline import Isophote_Pipeline


def decompress_fits(fz_path, output_path):
    """Decompress .fits.fz to plain .fits (HDU 1 → HDU 0)."""
    with fits.open(fz_path) as hdul:
        data = hdul[1].data.astype(np.float64)
    fits.PrimaryHDU(data=data).writeto(output_path, overwrite=True)
    return output_path


def run_autoprof_demo(galaxy_name, data_dir, output_dir):
    """Run AutoProf on one galaxy and print results."""
    img_fz = os.path.join(data_dir, galaxy_name,
                          f"{galaxy_name}-largegalaxy-image-r.fits.fz")
    mask_file = os.path.join(data_dir, galaxy_name,
                             f"{galaxy_name}-mask.fits")

    # Decompress image (AutoProf needs plain FITS)
    img_plain = os.path.join(output_dir, f"{galaxy_name}_image.fits")
    decompress_fits(img_fz, img_plain)

    # Run pipeline
    pipeline = Isophote_Pipeline(
        loggername=os.path.join(output_dir, "autoprof.log"),
    )
    result = pipeline.Process_Image(options={
        "ap_image_file": img_plain,
        "ap_mask_file": mask_file,
        "ap_mask_hdu": 0,
        "ap_name": galaxy_name,
        "ap_pixscale": 0.262,
        "ap_zeropoint": 22.5,
        "ap_process_mode": "image",
        "ap_doplot": False,
        "ap_saveto": output_dir,
        "ap_isoclip": True,
        "ap_iso_measurecoefs": (3, 4),
    })

    if result == 1:
        print(f"FAILED: {galaxy_name}")
        return False

    # Read and display profile
    # Format: line 0 = "# units..." (comment), line 1 = "R,SB,..." (names)
    prof_file = os.path.join(output_dir, f"{galaxy_name}.prof")
    data = np.genfromtxt(
        prof_file, delimiter=",", names=True, skip_header=1,
    )
    print(f"Columns: {list(data.dtype.names)}")
    valid = data["SB"] < 90  # filter out 99.999 sentinel values

    print(f"\nGalaxy: {galaxy_name}")
    print(f"Isophotes: {len(data)} total, {valid.sum()} valid")
    print(f"R range: {data['R'][valid].min():.2f} - {data['R'][valid].max():.2f} arcsec")
    print(f"SB range: {data['SB'][valid].min():.2f} - {data['SB'][valid].max():.2f} mag/arcsec^2")
    print(f"Timing: {result}")

    return True


if __name__ == "__main__":
    galaxy = sys.argv[1] if len(sys.argv) > 1 else "PGC2654441"
    data_dir = sys.argv[2] if len(sys.argv) > 2 else "data/demo"

    with tempfile.TemporaryDirectory() as tmpdir:
        run_autoprof_demo(galaxy, data_dir, tmpdir)
