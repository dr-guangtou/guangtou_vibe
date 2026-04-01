# STILTS Examples Cookbook

## Format Conversion

### Basic Conversions
```bash
# FITS to VOTable
stilts tcopy in.fits out.vot

# VOTable to FITS with metadata preservation
stilts tcopy catalog.vot catalog.fits ofmt=fits-plus

# CSV to FITS
stilts tcopy data.csv data.fits ifmt=csv

# FITS to ASCII table
stilts tcopy table.fits table.txt ofmt=ascii
```

### Multiple Tables in FITS
```bash
# List tables in a FITS file
stilts tcopy multi.fits ofmt=list

# Extract specific HDU
stilts tcopy 'multi.fits#2' table2.fits

# Extract by name
stilts tcopy 'multi.fits#EVENTS' events.fits
```

---

## Crossmatching

### Simple Sky Crossmatch
```bash
# Match two catalogs within 2 arcsec
stilts tmatch2 in1=cat1.fits in2=cat2.fits \
    matcher=sky \
    values1='ra dec' \
    values2='RAJ2000 DEJ2000' \
    params=2 \
    join=1and2 \
    out=matched.fits
```

### Best Match Only
```bash
# For each object in cat1, find the best match in cat2
stilts tmatch2 in1=survey.fits in2=spec.fits \
    matcher=sky \
    values1='ra dec' \
    values2='ra dec' \
    params=5 \
    join=all1 \
    find=best2 \
    out=with_spec.fits
```

### Internal Duplicate Finding
```bash
# Find duplicates within 1 arcsec in the same catalog
stilts tmatch1 in=catalog.fits \
    matcher=sky \
    values='ra dec' \
    params=1 \
    action=wide2 \
    out=duplicates.fits
```

### Large Catalog Crossmatch (Fast)
```bash
# Use tskymatch2 for large catalogs (>100k rows)
stilts tskymatch2 in1=large1.fits in2=large2.fits \
    ra1=RA dec1=DEC \
    ra2=ra dec2=dec \
    error=3 \
    join=1and2 \
    out=matched.fits
```

### Multi-Catalog Matching
```bash
# Match 3 catalogs simultaneously
stilts tmatchn nin=3 \
    in1=optical.fits in2=ir.fits in3=xray.fits \
    matcher=sky \
    values1='ra dec' \
    values2='ra dec' \
    values3='raj2000 dej2000' \
    params=2 \
    multimode=group \
    out=multi.fits
```

### 3D Matching (with redshift)
```bash
# Match on sky and redshift
stilts tmatch2 in1=spec1.fits in2=spec2.fits \
    matcher=3d \
    values1='ra dec z' \
    values2='ra dec z' \
    params='3 0.01' \
    out=matched.fits
```

---

## Virtual Observatory Queries

### CDS Crossmatch (VizieR)
```bash
# Crossmatch with Gaia DR3
stilts cdsskymatch in=my_catalog.fits \
    ra=RA dec=DEC \
    radius=3 \
    cdstable='I/355/gaiadr3' \
    find=best \
    out=my_gaia.fits

# Common CDS tables:
# I/355/gaiadr3      - Gaia DR3
# I/350/gaiaedr3     - Gaia EDR3
# I/345/gaia2        - Gaia DR2
# V/147/sdss12       - SDSS DR12
# II/328/allwise     - AllWISE
# II/349/ps1         - Pan-STARRS1
# B/vsx/vsx          - Variable stars
```

### TAP ADQL Queries
```bash
# Query Gaia DR3 with ADQL
stilts tapquery \
    tapurl='https://gea.esac.esa.int/tap-server/tap' \
    adql='SELECT source_id, ra, dec, phot_g_mean_mag 
          FROM gaiadr3.gaia_source 
          WHERE CONTAINS(POINT(150.0, 2.0), CIRCLE(ra, dec, 0.1))=1 
          AND phot_g_mean_mag < 20' \
    sync=true \
    out=gaia_cone.fits

# Upload and crossmatch via TAP
stilts tapquery \
    tapurl='http://TAPVizieR.u-strasbg.fr/TAPVizieR/tap' \
    upload1=my_table.fits \
    upname1=mytable \
    adql='SELECT t.*, g.* 
          FROM mytable AS t 
          JOIN "I/355/gaiadr3" AS g 
          ON 1=CONTAINS(POINT(t.ra, t.dec), CIRCLE(g.ra, g.dec, 0.001))' \
    out=crossmatch.fits
```

---

## Table Processing with tpipe

### Row Selection
```bash
# Select bright galaxies
stilts tpipe in=galaxy.fits cmd='select mag_r < 17' out=bright.fits

# Select with multiple conditions
stilts tpipe in=galaxy.fits \
    cmd='select mag_r < 20 && z > 0.1 && z < 1.0 && flag == 0' \
    out=selected.fits

# Select based on null values
stilts tpipe in=galaxy.fits cmd='select !isNull(redshift)' out=with_z.fits
```

### Adding/Modifying Columns
```bash
# Add calculated column
stilts tpipe in=galaxy.fits \
    cmd='addcol g_r mag_g - mag_r' \
    out=with_color.fits

# Add column with expression
stilts tpipe in=galaxy.fits \
    cmd='addcol log_mass log10(stellar_mass)' \
    out=with_logm.fits

# Replace column
stilts tpipe in=galaxy.fits \
    cmd='replacecol mag mag + 0.1' \
    out=adjusted.fits

# Delete column
stilts tpipe in=galaxy.fits cmd='delcol temp_flag' out=cleaned.fits

# Keep only specific columns
stilts tpipe in=galaxy.fits cmd='keepcols "ra dec mag_r z"' out=minimal.fits
```

### Sorting and Sampling
```bash
# Sort by magnitude
stilts tpipe in=galaxy.fits cmd='sort mag_r' out=sorted.fits

# Reverse sort
stilts tpipe in=galaxy.fits cmd='sort -mag_r' out=reverse_sorted.fits

# Random sample (1%)
stilts tpipe in=galaxy.fits cmd='select random() < 0.01' out=sample.fits

# Every Nth row
stilts tpipe in=galaxy.fits cmd='select $0 % 100 == 0' out=subsample.fits
```

### Multiple Operations
```bash
# Chain multiple commands
stilts tpipe in=raw.fits \
    cmd='select mag < 20' \
    cmd='addcol log_flux log10(flux)' \
    cmd='delcol temp_col' \
    cmd='sort mag' \
    cmd='head 1000' \
    out=processed.fits
```

---

## Concatenation

### Stack Similar Tables
```bash
# Simple concatenation
stilts tcat "obs_*.fits" out=all_obs.fits

# With sequence tracking
stilts tcat "obs_*.fits" \
    seqcol=OBSNUM \
    loccol=FILENAME \
    out=all_obs.fits

# Explicit list
stilts tcatn nin=3 \
    in1=part1.fits in2=part2.fits in3=part3.fits \
    out=combined.fits
```

---

## Joining Tables

### Side-by-Side Join
```bash
# Join by row number (tables must have same length)
stilts tjoin nin=2 \
    in1=ids.fits in2=data.fits \
    fixcols=dups \
    suffix1=_id suffix2=_data \
    out=joined.fits
```

### Keyed Join (Crossmatch)
```bash
# Join on common key column
stilts tmatch2 in1=cat1.fits in2=cat2.fits \
    matcher=exact \
    values1='id' \
    values2='ID' \
    join=1and2 \
    out=joined.fits
```

---

## Coordinate Transformations

### Calculate Separations
```bash
# Add separation column
stilts tpipe in=pairs.fits \
    cmd='addcol separation skyDistance(ra1, dec1, ra2, dec2)' \
    out=with_sep.fits
```

### Coordinate Conversions
```bash
# Using functions (if available in expression language)
stilts tpipe in=galactic.fits \
    cmd='addcol ra_icrs gal2icrsRa(l, b)' \
    cmd='addcol dec_icrs gal2icrsDec(l, b)' \
    out=icrs.fits
```

---

## Metadata and Inspection

### Table Information
```bash
# Show table metadata
stilts tcopy in.fits ofmt=meta

# Count rows
stilts tpipe in.fits omode=count

# Column statistics
stilts tpipe in.fits cmd='colmeta -name' omode=stats
```

### VOTable Validation
```bash
# Validate VOTable
stilts votlint in.vot

# Check Cone Search service
stilts conelint serviceurl.xml
```

---

## Parallel Processing

### Speed Up Large Jobs
```bash
# Use 4 threads
stilts tmatch2 ... runner=parallel4

# Use all CPUs
stilts tmatch2 ... runner=parallel

# With progress reporting
stilts tmatch2 ... runner=parallel progress=time
```

---

## Working with Large Files

### Memory Management
```bash
# Force disk-based processing
stilts -disk tmatch2 in1=huge1.fits in2=huge2.fits ...

# Monitor memory
stilts -verbose -memory tmatch2 ...
```

---

## Common Patterns

### Create Master Catalog with Crossmatches
```bash
#!/bin/bash
# Crossmatch multiple surveys to create master catalog

# Start with base catalog
stilts tcopy sdss.fits master.fits

# Crossmatch with WISE
stilts tmatch2 in1=master.fits in2=wise.fits \
    matcher=sky values1='ra dec' values2='ra dec' params=3 \
    join=all1 find=best suffix1='' suffix2=_wise \
    out=tmp1.fits

# Crossmatch with GALEX
stilts tmatch2 in1=tmp1.fits in2=galex.fits \
    matcher=sky values1='ra dec' values2='ra dec' params=4 \
    join=all1 find=best suffix1='' suffix2=_galex \
    out=tmp2.fits

# Crossmatch with ROSAT
stilts tmatch2 in1=tmp2.fits in2=rosat.fits \
    matcher=sky values1='ra dec' values2='ra dec' params=10 \
    join=all1 find=best suffix1='' suffix2=_xray \
    out=master_multiwavelength.fits

rm tmp1.fits tmp2.fits
```

### Quality Cuts Pipeline
```bash
#!/bin/bash
# Apply standard quality cuts

INPUT=$1
OUTPUT=$2

stilts tpipe in=$INPUT \
    cmd='select !isNull(mag_r)' \
    cmd='select mag_r < 22' \
    cmd='select mag_r > 14' \
    cmd='select snr > 5' \
    cmd='select flags == 0' \
    cmd='select fwhm > 1.0 && fwhm < 5.0' \
    out=$OUTPUT
```

### Calculate Derived Quantities
```bash
#!/bin/bash
# Add common derived quantities

stilts tpipe in=galaxies.fits \
    cmd='addcol g_r mag_g - mag_r' \
    cmd='addcol r_i mag_r - mag_i' \
    cmd='addcol color_gr g_r' \
    cmd='addcol abs_mag_r mag_r - 5*log10(luminosity_distance/10e-6)' \
    cmd='addcol log_sfr log10(sfr)' \
    cmd='addcol ssfr sfr/stellar_mass' \
    out=galaxies_enhanced.fits
```
