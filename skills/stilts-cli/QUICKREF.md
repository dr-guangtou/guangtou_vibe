# STILTS Quick Reference Card

## Installation

### Download (One-time setup)
```bash
mkdir -p ~/code
curl -L -o ~/code/stilts.jar 'https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar'
java -jar ~/code/stilts.jar -version
```

### Create Alias
```bash
alias stilts='java -jar ~/code/stilts.jar'
# Add to ~/.zshrc or ~/.bashrc to make permanent
```

### Or add to PATH
```bash
mkdir -p ~/bin
cat > ~/bin/stilts << 'EOF'
#!/bin/bash
exec java -jar ~/code/stilts.jar "$@"
EOF
chmod +x ~/bin/stilts
# Ensure ~/bin is in your PATH
```

---

## Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `tcopy` | Format conversion | `stilts tcopy in.fits out.vot` |
| `tmatch1` | Internal crossmatch | Find duplicates within a catalog |
| `tmatch2` | Two-table crossmatch | Match two catalogs |
| `tmatchn` | N-table crossmatch | Match multiple catalogs |
| `tskymatch2` | Fast sky crossmatch | Optimized for large catalogs |
| `tjoin` | Side-by-side join | Combine tables by row index |
| `tcat` | Concatenate | Stack tables vertically |
| `tpipe` | Pipeline processing | Filter, add columns, etc. |

---

## VO Queries

| Command | Purpose | Example |
|---------|---------|---------|
| `cdsskymatch` | Crossmatch with CDS | Match with VizieR/SIMBAD |
| `tapquery` | TAP ADQL query | Query any TAP server |
| `cone` | Cone search | Query cone service |
| `coneskymatch` | Generic cone match | Match against cone service |

---

## Common Options

### Matching (`tmatch1`, `tmatch2`, `tmatchn`)
```
matcher=sky       params=<arcsec>         # Sky position matching
matcher=exact     values='column'         # Exact string match
matcher=2d        params='<err_x> <err_y>' # 2D Cartesian
matcher=3d        params='<err> <err_z>'   # 3D with redshift
```

### Join Types (`tmatch2`, `tmatchn`)
```
join=1and2   # Inner join
join=1or2    # Outer union
join=all1    # Keep all from table 1
join=all2    # Keep all from table 2
join=1not2   # Table 1 without matches
```

### Find Modes (`tmatch2`, `tskymatch2`, `cdsskymatch`)
```
find=all     # All matches within radius
find=best    # Best match only
find=best1   # Best from table 1 perspective
find=best2   # Best from table 2 perspective
```

### Output Modes (all commands)
```
omode=out     # Write to file (default)
omode=meta    # Show metadata only
omode=stats   # Show statistics
omode=count   # Count rows only
```

---

## Table Formats

| Format | `ifmt=` / `ofmt=` | Notes |
|--------|-------------------|-------|
| FITS | `fits`, `fits-plus` | Binary, + = with metadata |
| VOTable | `votable` | XML format |
| VOTable Binary | `votable-binary2` | Compact binary |
| CSV | `csv` | Comma-separated |
| TSV | `tsv` | Tab-separated |
| ASCII | `text` | Human-readable |
| Parquet | `parquet` | Apache format |

---

## Expression Syntax

### Functions
```
skyDistance(ra1, dec1, ra2, dec2)   # Separation in arcsec
log10(x), log(x), exp(x), sqrt(x)   # Math functions
degrees(rad), radians(deg)          # Conversion
isNull(col), NULL                   # Null handling
```

### Constants
```
PI, DEGREE, NaN, true, false
```

---

## tpipe Commands

```bash
# Select rows
stilts tpipe in.fits cmd='select mag < 20' out=bright.fits

# Add column
stilts tpipe in.fits cmd='addcol g_r mag_g - mag_r' out=with_color.fits

# Delete column
stilts tpipe in.fits cmd='delcol obsolete_col' out=clean.fits

# Keep columns only
stilts tpipe in.fits cmd='keepcols "ra dec mag"' out=minimal.fits

# Sort
stilts tpipe in.fits cmd='sort mag' out=sorted.fits

# Head/tail
stilts tpipe in.fits cmd='head 100' out=first100.fits
stilts tpipe in.fits cmd='tail 100' out=last100.fits

# Multiple operations (chained)
stilts tpipe in.fits \
    cmd='select mag < 20' \
    cmd='addcol log_flux log10(flux)' \
    cmd='sort mag' \
    out=processed.fits
```

---

## CDS/VizieR Tables (Common)

| Table Name | Description |
|------------|-------------|
| `I/355/gaiadr3` | Gaia DR3 |
| `I/350/gaiaedr3` | Gaia EDR3 |
| `V/147/sdss12` | SDSS DR12 |
| `II/328/allwise` | AllWISE |
| `II/349/ps1` | Pan-STARRS1 |
| `II/306/sdss9` | SDSS DR9 |

---

## Performance Tips

```bash
# Parallel processing
... runner=parallel4    # Use 4 threads
... runner=parallel     # Use all CPUs

# Progress reporting
... progress=time       # Show ETA

# Memory vs Disk
stilts -disk tmatch2 ...   # Force disk (large tables)
stilts -memory tmatch2 ... # Force memory (default)

# Fast sky matching for large catalogs
# Use tskymatch2 instead of tmatch2 matcher=sky
```

---

## TAP URLs (Common)

```
Gaia (ESAC):     https://gea.esac.esa.int/tap-server/tap
VizieR (CDS):    http://TAPVizieR.u-strasbg.fr/TAPVizieR/tap
HEASARC:         https://heasarc.gsfc.nasa.gov/xamin/vo/tap
NED:             https://ned.ipac.caltech.edu/tap/
SIMBAD:          http://simbad.u-strasbg.fr/simbad/sim-tap
```

---

## Help Commands

```bash
# List all tasks
stilts -help

# Command help
stilts tmatch2 -help

# Specific parameter help
stilts tmatch2 help=matcher
stilts tmatch2 help=join

# Full documentation
stilts tmatch2 -help doc=full

# Local HTML manual
open ~/Desktop/qibin/skills/stilts-cli/references/sun256.html
```

Or use Java directly:
```bash
java -jar ~/code/stilts.jar tmatch2 -help
```

---

## File Locations

### STILTS Jar (User-installed)
```
~/code/stilts.jar           # Main executable (download yourself)
```

### Skill Documentation
```
~/Desktop/qibin/skills/stilts-cli/
├── assets/
│   └── VERSION             # Version tracking
├── references/
│   ├── sun256.html         # Full manual (2.5 MB)
│   ├── examples.md         # Example recipes
│   └── command_help.json   # Machine-readable help
├── scripts/
│   ├── stilts.sh           # Wrapper script
│   ├── lookup.sh           # Quick command lookup
│   ├── update.sh           # Update STILTS
│   └── verify.sh           # Verify installation
├── SKILL.md                # Full documentation
└── QUICKREF.md             # This quick reference
```
