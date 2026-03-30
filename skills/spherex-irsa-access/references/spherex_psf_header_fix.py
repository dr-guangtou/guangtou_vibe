#!/usr/bin/env python3
"""
Fix PSF header indexing for SPHEREx Spectral Image versions <= 6.5.5.

Earlier versions had a mismatch between spatial layout of PSF zones and 
the indexing of PSF zones in the image header. This has been fixed in 
versions 6.5.6 and beyond.

Usage:
    from spherex_psf_header_fix import update_psf_header
    fixed_hdulist = update_psf_header(old_hdulist)

Reference: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/psfhdrerr.html
"""

import re
import numpy as np
from packaging.version import Version
from astropy.io import fits


def update_psf_header(old_hdul):
    """
    Fix an old PSF FITS file header by rewriting only the per-plane header metadata
    so that plane k corresponds to x-fast ordering:
        k0 = iy * bins_x + ix

    The cube data are left untouched.

    Parameters
    ----------
    old_hdul : fits.HDUList
        Old SPHEREx Spectral Image HDUL

    Returns
    -------
    new_hdul : fits.HDUList
        New SPHEREx Spectral Image HDUL with updated PSF zone data in header 
        and updated version number
    """

    VERSION_FIXED = Version("6.5.6")
    PSF_FIX_TAG = "psffix1"

    def psf_fix_applied(hdul) -> bool:
        """
        Return True if the PSF fix has been applied.

        Rules:
        - If the VERSION header is missing in the primary HDU, the fix is not applied.
        - If VERSION >= VERSION_FIXED, the fix is included in the software release.
        - Otherwise the local version tag (+...) must contain PSF_FIX_TAG.
        """
        header = hdul[0].header

        if "VERSION" not in header:
            return False

        v = Version(header["VERSION"])

        if v >= VERSION_FIXED:
            return True

        return v.local is not None and PSF_FIX_TAG in v.local

    # Check if fix is needed
    if psf_fix_applied(old_hdul):
        print("PSF fix already applied, returning original HDUList")
        return old_hdul

    # Helper functions
    def parse_ixiy_from_comment(comment):
        """Parse zone indices (ix, iy) from header comment."""
        _zone_pat = re.compile(r"\((\d+)\s*,\s*(\d+)\)")
        m = _zone_pat.search(str(comment))
        if not m:
            raise ValueError(f"Could not parse zone indices from comment: {comment!r}")
        return int(m.group(1)), int(m.group(2))

    def infer_grid_shape_from_header_comments(hdr, nzone):
        """Infer grid shape (bins_x, bins_y) from header comments."""
        max_ix = -1
        max_iy = -1

        for k1 in range(1, nzone + 1):
            key = f"XCTR_{k1}"
            if key not in hdr:
                raise KeyError(f"Missing required key: {key}")
            ix, iy = parse_ixiy_from_comment(hdr.comments[key])
            max_ix = max(max_ix, ix)
            max_iy = max(max_iy, iy)

        bins_x = max_ix + 1
        bins_y = max_iy + 1

        if bins_x * bins_y != nzone:
            raise ValueError(
                f"Inconsistent grid inferred from comments: "
                f"bins_x={bins_x}, bins_y={bins_y}, nzone={nzone}"
            )

        return bins_x, bins_y

    def collect_axis_values_by_zone(hdr, nzone):
        """
        Read the old header and collect unique x/y centers and widths by zone index
        labels found in the comments.
        """
        x_center_by_ix = {}
        y_center_by_iy = {}
        x_width_by_ix = {}
        y_width_by_iy = {}

        for k1 in range(1, nzone + 1):
            ix, iy = parse_ixiy_from_comment(hdr.comments[f"XCTR_{k1}"])

            xck = f"XCTR_{k1}"
            yck = f"YCTR_{k1}"
            xwk = f"XWID_{k1}"
            ywk = f"YWID_{k1}"

            if xck in hdr:
                val = hdr[xck]
                if ix in x_center_by_ix and not np.isclose(x_center_by_ix[ix], val):
                    raise ValueError(
                        f"Inconsistent XCTR for ix={ix}: "
                        f"{x_center_by_ix[ix]} vs {val}"
                    )
                x_center_by_ix[ix] = val

            if yck in hdr:
                val = hdr[yck]
                if iy in y_center_by_iy and not np.isclose(y_center_by_iy[iy], val):
                    raise ValueError(
                        f"Inconsistent YCTR for iy={iy}: "
                        f"{y_center_by_iy[iy]} vs {val}"
                    )
                y_center_by_iy[iy] = val

            if xwk in hdr:
                val = hdr[xwk]
                if ix in x_width_by_ix and not np.isclose(x_width_by_ix[ix], val):
                    raise ValueError(
                        f"Inconsistent XWID for ix={ix}: "
                        f"{x_width_by_ix[ix]} vs {val}"
                    )
                x_width_by_ix[ix] = val

            if ywk in hdr:
                val = hdr[ywk]
                if iy in y_width_by_iy and not np.isclose(y_width_by_iy[iy], val):
                    raise ValueError(
                        f"Inconsistent YWID for iy={iy}: "
                        f"{y_width_by_iy[iy]} vs {val}"
                    )
                y_width_by_iy[iy] = val

        return x_center_by_ix, y_center_by_iy, x_width_by_ix, y_width_by_iy

    # Get PSF HDU
    extname = "PSF"
    hdu = old_hdul[extname]
    hdr = hdu.header.copy()
    nzone = hdr["NAXIS3"]

    # Infer grid shape from comments
    bins_x, bins_y = infer_grid_shape_from_header_comments(hdr, nzone)
    print(f"Inferred grid: {bins_x}x{bins_y} = {nzone} zones")

    # Collect axis values
    x_center_by_ix, y_center_by_iy, x_width_by_ix, y_width_by_iy = \
        collect_axis_values_by_zone(hdr, nzone)

    # Create new header with corrected indexing
    new_hdr = fits.Header()

    # Copy required WCS keywords
    for key in ["XTENSION", "BITPIX", "NAXIS", "NAXIS1", "NAXIS2", "NAXIS3",
                "PCOUNT", "GCOUNT", "EXTNAME", "OVERSAMP"]:
        if key in hdr:
            new_hdr[key] = hdr[key]

    # Write new zone metadata in x-fast order
    for k0 in range(nzone):
        iy = k0 // bins_x
        ix = k0 % bins_x
        k1 = k0 + 1  # FITS cards are 1-indexed

        new_hdr[f"XCTR_{k1}"] = x_center_by_ix[ix]
        new_hdr.comments[f"XCTR_{k1}"] = f"Zone ({ix},{iy}) X center"

        new_hdr[f"YCTR_{k1}"] = y_center_by_iy[iy]
        new_hdr.comments[f"YCTR_{k1}"] = f"Zone ({ix},{iy}) Y center"

        new_hdr[f"XWID_{k1}"] = x_width_by_ix[ix]
        new_hdr.comments[f"XWID_{k1}"] = f"Zone ({ix},{iy}) X width"

        new_hdr[f"YWID_{k1}"] = y_width_by_iy[iy]
        new_hdr.comments[f"YWID_{k1}"] = f"Zone ({ix},{iy}) Y width"

    # Create new HDU with same data but new header
    new_hdu = fits.ImageHDU(data=hdu.data, header=new_hdr)

    # Build new HDUList
    new_hdul = fits.HDUList()
    for h in old_hdul:
        if h.name == extname:
            new_hdul.append(new_hdu)
        else:
            new_hdul.append(h.copy())

    # Update version to indicate fix has been applied
    old_version = Version(new_hdul[0].header.get("VERSION", "0.0.0"))
    new_version = f"{old_version}+{PSF_FIX_TAG}"
    new_hdul[0].header["VERSION"] = new_version
    new_hdul[0].header["HISTORY"] = f"PSF header fix applied ({PSF_FIX_TAG})"

    print(f"PSF header fixed. Version updated: {old_version} -> {new_version}")
    
    return new_hdul


def check_psf_header(hdulist):
    """
    Check if PSF header needs fixing.
    
    Parameters
    ----------
    hdulist : astropy.io.fits.HDUList
        SPHEREx spectral image HDUList
    
    Returns
    -------
    dict
        Information about PSF header status
    """
    primary = hdulist[0].header
    
    if "VERSION" not in primary:
        return {
            'needs_fix': True,
            'reason': 'VERSION keyword not found in primary header',
            'version': None
        }
    
    version = Version(primary["VERSION"])
    contains_psffix1 = version.local is not None and "psffix1" in version.local
    
    if version <= Version("6.5.5") and not contains_psffix1:
        return {
            'needs_fix': True,
            'reason': f'Version {version} <= 6.5.5 without psffix1',
            'version': str(version)
        }
    else:
        return {
            'needs_fix': False,
            'reason': 'Header is up to date',
            'version': str(version)
        }


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python spherex_psf_header_fix.py <fits_file>")
        print("\nThis script checks and fixes PSF headers for SPHEREx data versions <= 6.5.5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.fits', '_psffixed.fits')
    
    print(f"Loading {input_file}...")
    hdulist = fits.open(input_file)
    
    # Check status
    status = check_psf_header(hdulist)
    print(f"\nPSF Header Status:")
    print(f"  Version: {status['version']}")
    print(f"  Needs fix: {status['needs_fix']}")
    print(f"  Reason: {status['reason']}")
    
    if status['needs_fix']:
        print(f"\nApplying PSF header fix...")
        fixed_hdulist = update_psf_header(hdulist)
        
        print(f"Saving to {output_file}...")
        fixed_hdulist.writeto(output_file, overwrite=True)
        print("Done!")
    else:
        print("\nNo fix needed.")
