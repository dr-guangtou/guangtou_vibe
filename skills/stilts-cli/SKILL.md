---
name: stilts-cli
description: STILTS (Starlink Tables Infrastructure Library Tool Set) - Command-line tools for processing astronomical tabular data
category: research/astronomy
version: 3.5-4
author: Mark Taylor (University of Bristol)
source: https://www.star.bris.ac.uk/~mbt/stilts/
manual_local: references/sun256.html
---

# STILTS CLI Skill

STILTS is a set of command-line tools for processing tabular data, designed primarily for astronomical data but applicable to any tabular data.

## Installation

### 1. Download STILTS

STILTS is distributed as a single Java `.jar` file. You need to download it yourself:

```bash
# Download to ~/code/ (recommended)
mkdir -p ~/code
curl -L -o ~/code/stilts.jar "https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"
```

### 2. Verify Installation

```bash
java -jar ~/code/stilts.jar -version
```

Expected output:
```
This is STILTS, the STIL Tool Set

    STILTS version 3.5-4
    STIL version 4.3-4
    Starjava revision: 7ea205595 (2025-09-12)
    ...
```

### 3. Create Alias (Optional)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
alias stilts='java -jar ~/code/stilts.jar'
```

Then reload: `source ~/.zshrc`

### 4. Alternative: Add to PATH

```bash
# Create wrapper script
mkdir -p ~/bin
cat > ~/bin/stilts << 'EOF'
#!/bin/bash
exec java -jar ~/code/stilts.jar "$@"
EOF
chmod +x ~/bin/stilts

# Add ~/bin to PATH in ~/.zshrc
export PATH="$HOME/bin:$PATH"
```

---

## Quick Reference

### Current Version
- **STILTS Version**: 3.5-4 (released 2025-09-12)
- **STIL Version**: 4.3-4
- **Java Requirement**: JVM 1.8+
- **Download URL**: https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar

### Supported Table Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| FITS | `.fits` | Native binary, multiple tables |
| VOTable | `.vot`, `.xml` | XML-based VO standard |
| CSV | `.csv` | Comma-separated values |
| TSV | `.tsv`, `.txt` | Tab-separated values |
| ASCII | `.txt` | Column-aligned text |
| IPAC | `.tbl` | IRSA table format |
| Parquet | `.parquet` | Apache columnar format |
| SQLite | `.db`, `.sqlite` | SQL database |
| TOPCAT | `.tst` | TOPCAT format |

---

## Core Table Processing Commands

### 1. `tcopy` - Format Conversion
**Purpose**: Convert between table formats

```bash
stilts tcopy in.fits out.vot
stilts tcopy cat.csv cat.fits ofmt=fits-plus
```

**Key Parameters**:
- `ifmt=<format>`: Input format (auto-detected if not specified)
- `ofmt=<format>`: Output format
- `in=<table>`: Input file
- `out=<out-table>`: Output file

**Common Output Formats**:
- `fits`, `fits-plus` (with metadata)
- `votable`, `votable-binary`, `votable-binary2`
- `csv`, `csv-noheader`
- `text`, `ascii`

---

### 2. `tmatch1` - Internal Crossmatch
**Purpose**: Find matches within a single table (find duplicates, groups)

```bash
# Find duplicates within 2 arcsec
stilts tmatch1 in=objects.fits \
    matcher=sky \
    values='RA DEC' \
    params=2 \
    action=wide2 \
    out=duplicates.fits

# Keep only unique objects
stilts tmatch1 in=objects.fits \
    matcher=sky \
    values='RA DEC' \
    params=1 \
    action=keep0 \
    out=unique.fits
```

**Actions**:
- `identify`: Add group ID column
- `keep0`: Keep only ungrouped rows
- `keep1`: Keep one from each group
- `wide2`: Output pairwise matches
- `wideN`: Output all group members

**Common Matchers**:
- `sky`: Spherical sky positions (params=radius_arcsec)
- `skyerr`: Sky with per-object errors
- `1d`, `2d`, `3d`: Cartesian matching
- `exact`: Exact string match
- `ellipse`: Elliptical regions on sky

---

### 3. `tmatch2` - Two-Table Crossmatch
**Purpose**: Crossmatch two tables using flexible criteria

```bash
# Basic sky crossmatch
stilts tmatch2 in1=catalog1.fits in2=catalog2.fits \
    matcher=sky \
    values1='ra dec' \
    values2='RAJ2000 DEJ2000' \
    params=2 \
    join=1and2 \
    out=matched.fits

# Find best match only, keep all from table 1
stilts tmatch2 in1=survey.fits in2=specz.fits \
    matcher=sky \
    values1='ra dec' \
    values2='RA DEC' \
    params=5 \
    join=all1 \
    find=best2 \
    suffix1=_survey \
    suffix2=_specz \
    out=crossmatched.fits
```

**Join Types**:
- `1and2`: Inner join (matches in both)
- `1or2`: Outer union (all from both)
- `all1`: Keep all from table 1
- `all2`: Keep all from table 2
- `1not2`: Table 1 rows without matches
- `2not1`: Table 2 rows without matches
- `1xor2`: Symmetric difference

**Find Modes**:
- `all`: All matches within radius
- `best`: Best match for each row
- `best1`: Best match from table 1 perspective
- `best2`: Best match from table 2 perspective

---

### 4. `tmatchn` - N-Table Crossmatch
**Purpose**: Crossmatch multiple tables simultaneously

```bash
stilts tmatchn nin=3 \
    in1=optical.fits in2=ir.fits in3=xray.fits \
    matcher=sky \
    values1='ra dec' \
    values2='RA DEC' \
    values3='raj2000 dej2000' \
    params=3 \
    multimode=group \
    join1=match join2=match join3=match \
    out=multimatched.fits
```

**Multi-Mode**:
- `pairs`: Match all pairs of tables
- `group`: Find groups across all tables

**Join Options per Table**:
- `default`: Use multimode setting
- `match`: Row must match
- `nomatch`: Row must not match
- `always`: Include regardless

---

### 5. `tskymatch2` - Optimized Sky Crossmatch
**Purpose**: Fast 2-table sky position crossmatch using HEALPix

```bash
stilts tskymatch2 in1=survey.fits in2=catalog.fits \
    ra1=RA dec1=DEC \
    ra2=raj2000 dec2=dej2000 \
    error=5 \
    join=1and2 \
    tuning=10 \
    out=matched.fits
```

**Parameters**:
- `ra1`, `dec1`: Column expressions for table 1
- `ra2`, `dec2`: Column expressions for table 2
- `error=<arcsec>`: Maximum separation
- `tuning=<k>`: HEALPix resolution (default: 10)

**When to use**: Large catalogs where `tmatch2 matcher=sky` is too slow. Uses HEALPix sky pixelization for efficient pre-filtering.

---

### 6. `tjoin` - Side-by-Side Join
**Purpose**: Join multiple tables horizontally by row index

```bash
stilts tjoin nin=2 \
    in1=ids.fits in2=magnitudes.fits \
    fixcols=dups \
    suffix1=_id suffix2=_mag \
    out=joined.fits
```

**Note**: Tables must have same number of rows. For keyed joins, use `tmatch2` with `join=1and2`.

---

### 7. `arrayjoin` - Per-Row Table Join
**Purpose**: Add table-per-row data as array-valued columns

```bash
stilts arrayjoin in=galaxies.fits \
    atable='spectra/${ID}.fits' \
    afmt=fits \
    aparams='wavelength flux' \
    out=galaxy_spectra.fits
```

**Use case**: Each galaxy has a spectrum in a separate file; add spectrum arrays to the catalog.

---

### 8. `tcat` - Concatenate Tables
**Purpose**: Stack similar tables vertically (same columns)

```bash
stilts tcat in="obs1.fits obs2.fits obs3.fits" \
    seqcol=OBSID \
    out=stacked.fits
```

**Key Parameters**:
- `seqcol=<name>`: Add column with sequence number
- `loccol=<name>`: Add column with source file path
- `uloccol=<name>`: Add column with unique file identifier
- `lazy=true`: Don't check column compatibility upfront

---

### 9. `tcatn` - Concatenate N Tables
**Purpose**: Stack multiple tables with explicit enumeration

```bash
stilts tcatn nin=3 \
    in1=part1.fits in2=part2.fits in3=part3.fits \
    seqcol=CHUNK \
    out=combined.fits
```

**When to use**: When you need more control over inputs than `tcat` provides.

---

## Virtual Observatory Commands

### 10. `cone` - Cone Search Query
**Purpose**: Execute a single cone search query

```bash
stilts cone \
    serviceurl='http://vizier.u-strasbg.fr/viz-bin/conesearch/I/355/gaiadr3?' \
    lon=150.0 lat=2.0 \
    radius=0.1 \
    out=local_gaia.fits
```

**Service Types**:
- `cone`: Simple Cone Search
- `sia`: Simple Image Access
- `ssa`: Simple Spectral Access

---

### 11. `tapquery` - TAP Server Query
**Purpose**: Query Table Access Protocol servers with ADQL

```bash
# Simple query
stilts tapquery \
    tapurl='http://TAPVizieR.u-strasbg.fr/TAPVizieR/tap' \
    adql='SELECT * FROM "I/355/gaiadr3" WHERE CONTAINS(POINT(150, 2), CIRCLE(ra, dec, 0.1))=1' \
    sync=true \
    maxrec=10000 \
    out=gaia_cone.fits

# Upload and crossmatch
stilts tapquery \
    tapurl='http://TAPVizieR.u-strasbg.fr/TAPVizieR/tap' \
    upload1=mytable.fits \
    upname1=mytable \
    adql='SELECT t.*, g.* FROM mytable AS t JOIN "I/355/gaiadr3" AS g ON 1=CONTAINS(POINT(t.ra, t.dec), CIRCLE(g.ra, g.dec, 0.001))' \
    out=crossmatched.fits
```

**Execution Modes**:
- `sync=true`: Synchronous (fast, small results)
- `sync=false`: Asynchronous (large results, long queries)

---

### 12. `cdsskymatch` - CDS Crossmatch
**Purpose**: Crossmatch against VizieR/SIMBAD tables

```bash
stilts cdsskymatch in=survey.fits \
    ra=RA dec=DEC \
    radius=3 \
    cdstable='I/355/gaiadr3' \
    find=best \
    maxrec=1000000 \
    out=survey_gaia.fits
```

**Find Modes**:
- `all`: All matches within radius
- `best`: Best match only
- `best-remote`: Best match per remote object
- `each`: One match per input row

**CDS Tables** (VizieR):
- `I/355/gaiadr3`: Gaia DR3
- `I/350/gaiaedr3`: Gaia EDR3
- `V/147/sdss12`: SDSS DR12
- `II/328/allwise`: AllWISE

---

### 13. `coneskymatch` - Generic Cone Crossmatch
**Purpose**: Crossmatch table against remote cone service

```bash
stilts coneskymatch in=sources.fits \
    ra=RA dec=DEC \
    sr=0.1 \
    serviceurl='http://vizier.u-strasbg.fr/viz-bin/conesearch/I/355/gaiadr3?' \
    find=best \
    suffix0=_input suffix1=_gaia \
    out=matched.fits
```

**vs `cdsskymatch`**: More generic - works with any Cone Search service, not just CDS.

---

## Common Workflows

### Convert FITS to VOTable with Binary Encoding
```bash
stilts tcopy in.fits out.vot ofmt=votable-binary2
```

### Crossmatch Two Catalogs on Sky Position
```bash
stilts tmatch2 in1=sdss.fits in2=wise.fits \
    matcher=sky \
    values1='ra dec' \
    values2='ra dec' \
    params=2 \
    join=1and2 \
    find=best \
    suffix1=_sdss suffix2=_wise \
    out=sdss_wise.fits
```

### Remove Duplicate Sources from Catalog
```bash
stilts tmatch1 in=catalog.fits \
    matcher=sky \
    values='ra dec' \
    params=1 \
    action=keep0 \
    out=unique.fits
```

### Stack Multiple Observation Files
```bash
stilts tcat "obs_*.fits" seqcol=OBSID loccol=FILE out=all_obs.fits
```

### Query Gaia DR3 Around Positions
```bash
stilts cdsskymatch in=targets.fits \
    ra=RA dec=DEC radius=5 \
    cdstable='I/355/gaiadr3' \
    find=best \
    out=targets_gaia.fits
```

---

## Expression Syntax

### Column References
```bash
# Simple column name
stilts tpipe in=cat.fits cmd='select magnitude < 20'

# Expression with units
stilts tpipe in=cat.fits cmd='addcol mag_ab mag_vega + 0.1'

# Array access
stilts tpipe in=cat.fits cmd='select MAG[0] < 20'
```

### Common Functions
- `NULL`: Null value
- `NaN`: Not-a-number
- `PI`, `DEGREE`: Constants
- `abs(x)`, `sqrt(x)`, `log(x)`, `log10(x)`, `exp(x)`
- `sin(x)`, `cos(x)`, `tan(x)` (radians)
- `degrees(x)`, `radians(x)`
- `skyDistance(ra1, dec1, ra2, dec2)`: Arcsec separation

### Table Filters (tpipe)
```bash
# Select rows
stilts tpipe in=cat.fits cmd='select mag < 20 && flag == 0'

# Add column
stilts tpipe in=cat.fits cmd='addcol log_flux log10(flux)'

# Delete column
stilts tpipe in=cat.fits cmd='delcol DETECTION_FLAG'

# Sort
stilts tpipe in=cat.fits cmd='sort mag'

# Head/tail
stilts tpipe in=cat.fits cmd='head 100'
```

---

## Advanced Features

### Parallel Processing
```bash
stilts tmatch2 ... runner=parallel4  # Use 4 threads
stilts tmatch2 ... runner=parallel   # Use all CPUs
```

### Memory vs Disk
```bash
# Force disk-based processing for large tables
stilts -disk tmatch2 ...

# Force in-memory (default)
stilts -memory tmatch2 ...
```

### Progress Reporting
```bash
stilts tmatch2 ... progress=time    # Show time estimates
stilts tmatch2 ... progress=log     # Log progress
```

---

## Tips & Pitfalls

1. **Column names with spaces**: Use `$'column name'` syntax
2. **Units in expressions**: Convert to consistent units before calculations
3. **Large tables**: Use `tskymatch2` instead of `tmatch2 matcher=sky` for speed
4. **Output formatting**: Use `fits-plus` to preserve metadata
5. **Missing values**: Use `NULL` in expressions, check with `isNull(col)`

---

## Documentation References

- **Local HTML Manual**: `references/sun256.html` (2.6 MB, complete reference)
- **Command Help**: `java -jar ~/code/stilts.jar <command> -help`
- **Parameter Help**: `java -jar ~/code/stilts.jar <command> -help <param>`
- **Online**: https://www.star.bris.ac.uk/~mbt/stilts/

## Version History

| Date | STILTS | STIL | Notes |
|------|--------|------|-------|
| 2025-09-12 | 3.5-4 | 4.3-4 | Latest - Bugfixes |

To update:
```bash
# Backup current
cp ~/code/stilts.jar ~/code/stilts-$(date +%Y%m%d).jar.bak

# Download new
curl -L -o ~/code/stilts.jar "https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"

# Verify
java -jar ~/code/stilts.jar -version
```
