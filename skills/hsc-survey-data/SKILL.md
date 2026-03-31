---
name: hsc-survey-data
title: HSC Survey Data Access
description: Access Hyper Suprime-Cam (HSC) Subaru Strategic Program (SSP) survey data using official tools
tags: [astronomy, hsc, database, sql, cutout, psf]
---

# HSC Survey Data Access

Access Hyper Suprime-Cam (HSC) Subaru Strategic Program (SSP) survey data using the official HSC data access tools.

## Overview

The HSC survey provides two database systems:

| Type | Release | URL | Credentials |
|------|---------|-----|-------------|
| **Internal** | DR4 / S23B | `hscdata.mtk.nao.ac.jp` | `SSP_IDR_USR` / `SSP_IDR_PWD` |
| **Public** | PDR3 | `hsc-release.mtk.nao.ac.jp` | `SSP_PDR_USR` / `SSP_PDR_PWD` |

## Setup

### 1. Download Official Tools

Clone the official data access tools repository:

```bash
git clone https://hsc-gitlab.mtk.nao.ac.jp/ssp-software/data-access-tools.git
cd data-access-tools
```

### 2. Set Credentials

**For Internal Data Release (DR4/S23B):**
```bash
export SSP_IDR_USR="your_username"
export SSP_IDR_PWD="your_password"
```

**For Public Data Release (PDR3):**
```bash
export SSP_PDR_USR="your_username"
export SSP_PDR_PWD="your_password"
```

## Tool 1: SQL Catalog Query (`hscSspQuery3.py`)

**Location in repo:** `dr4/catalogQuery/hscSspQuery3.py`

**Source:** https://hsc-gitlab.mtk.nao.ac.jp/ssp-software/data-access-tools/blob/master/dr4/catalogQuery/hscSspQuery3.py

### Basic Usage

```bash
python hscSspQuery3.py \
    --user $SSP_IDR_USR \
    --release-version dr4 \
    --format csv \
    query.sql > output.csv
```

### Command-Line Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--user` | `-u` | (required) | STARS account username |
| `--release-version` | `-r` | (required) | Data release: `dr4`, `dr4-citus`, `dr3`, `dr3-citus`, `dr2`, `dr1`, `dr_early` |
| `--format` | `-f` | `csv` | Output format: `csv`, `csv.gz`, `sqlite3`, `fits`, `numpygres-fits`, `fast-fits` |
| `--delete-job` | `-D` | | Delete job after downloading |
| `--nomail` | `-M` | | Suppress email notification |
| `--preview` | `-p` | | Quick preview mode (returns first ~100 rows) |
| `--skip-syntax-check` | `-S` | | Skip SQL syntax validation |
| `--password-env` | | `HSC_SSP_CAS_PASSWORD` | Environment variable containing password |
| `--api-url` | | (see below) | Override default API endpoint |
| `sql-file` | | (required) | Path to SQL file |

### API Endpoints (Default)

- **Internal:** `https://hscdata.mtk.nao.ac.jp/datasearch/api/catalog_jobs/`
- **Public:** `https://hsc-release.mtk.nao.ac.jp/datasearch/api/catalog_jobs/`

### SQL Query Examples

**Cone search around coordinates:**
```sql
SELECT object_id, ra, dec, i_cmodel_flux, i_cmodel_mag
FROM s23b_wide.forced
WHERE coneSearch(coord, 136.47, -0.05, 60)
AND i_cmodel_flux > 0
ORDER BY i_cmodel_flux DESC
```

**Box search:**
```sql
SELECT *
FROM s23b_wide.forced
WHERE boxSearch(coord, 136.0, 137.0, -0.5, 0.5)
LIMIT 1000
```

**Join with photoz:**
```sql
SELECT f.object_id, f.ra, f.dec, f.i_cmodel_mag, p.photoz_best
FROM s23b_wide.forced AS f
JOIN s23b_wide.photoz_mizuki AS p ON f.object_id = p.object_id
WHERE coneSearch(f.coord, 150.0, 2.0, 120)
```

### Python Module Usage

You can also import the script as a module:

```python
import sys
sys.path.insert(0, '/path/to/data-access-tools/dr4/catalogQuery')
import hscSspQuery3

# Set arguments programmatically
hscSspQuery3.args = type('Args', (), {
    'user': os.environ['SSP_IDR_USR'],
    'release_version': 'dr4',
    'out_format': 'csv',
    'delete_job': True,
    'nomail': True,
    'skip_syntax_check': False,
    'api_url': 'https://hscdata.mtk.nao.ac.jp/datasearch/api/catalog_jobs/',
    'password_env': 'SSP_IDR_PWD'
})()

# Read SQL
with open('query.sql', 'r') as f:
    sql = f.read()

# Get credentials
credential = {
    'account_name': hscSspQuery3.args.user,
    'password': hscSspQuery3.getPassword()
}

# Submit job
job = hscSspQuery3.submitJob(credential, sql, 'csv')
print(f"Job ID: {job['id']}")

# Wait for completion
hscSspQuery3.blockUntilJobFinishes(credential, job['id'])

# Download to file
with open('output.csv', 'wb') as f:
    hscSspQuery3.download(credential, job['id'], f)

# Clean up
hscSspQuery3.deleteJob(credential, job['id'])
```

## Tool 2: Cutout Images (`downloadCutout.py`)

**Location in repo:** `dr4/downloadCutout/downloadCutout.py`

### Basic Usage

```bash
# Download single cutout
python downloadCutout.py \
    --ra 136.471165 \
    --dec -0.046470 \
    --sw 10arcsec \
    --sh 10arcsec \
    --filter HSC-I \
    --rerun s23b_wide \
    --type coadd/bg \
    --image true \
    --mask true \
    --variance true \
    --user $SSP_IDR_USR
```

### Batch Download via List File

Create a coordinate list file `coords.txt`:
```
#? ra dec sw sh filter
136.471165 -0.046470 10arcsec 10arcsec HSC-G
136.471165 -0.046470 10arcsec 10arcsec HSC-R
136.471165 -0.046470 10arcsec 10arcsec HSC-I
136.471165 -0.046470 10arcsec 10arcsec HSC-Z
136.471165 -0.046470 10arcsec 10arcsec HSC-Y
```

Then run:
```bash
python downloadCutout.py \
    --list coords.txt \
    --rerun s23b_wide \
    --type coadd/bg \
    --image true \
    --mask true \
    --variance true \
    --user $SSP_IDR_USR
```

### Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--ra` | Right Ascension (degrees) | `136.471165` |
| `--dec` | Declination (degrees) | `-0.046470` |
| `--sw` | Semi-width (RA direction) | `10arcsec`, `0.002778deg` |
| `--sh` | Semi-height (Dec direction) | `10arcsec` |
| `--filter` | Filter name | `HSC-G`, `HSC-R`, `HSC-I`, `HSC-Z`, `HSC-Y`, `all` |
| `--rerun` | Data release | `s23b_wide`, `s21a_wide`, `pdr3_wide` |
| `--type` | Image type | `coadd`, `coadd/bg`, `warp` |
| `--tract` | Tract number | `9813`, or omit for auto |
| `--image` | Download image plane | `true`/`false` |
| `--mask` | Download mask plane | `true`/`false` |
| `--variance` | Download variance plane | `true`/`false` |

## Tool 3: PSF Download (`downloadPsf.py`)

**Location in repo:** `dr4/downloadPsf/downloadPsf.py`

**⚠️ Important:** S23B data requires the `psf/9` endpoint, while older releases use `psf/8`. Edit the script's `api_url` if needed.

### Basic Usage

```bash
python downloadPsf.py \
    --ra 136.471165 \
    --dec -0.046470 \
    --filter HSC-I \
    --rerun s23b_wide \
    --type coadd \
    --centered true \
    --user $SSP_IDR_USR
```

### Batch PSF Download

Create list file `psf_coords.txt`:
```
#? ra dec filter
136.471165 -0.046470 HSC-G
136.471165 -0.046470 HSC-R
136.471165 -0.046470 HSC-I
136.471165 -0.046470 HSC-Z
136.471165 -0.046470 HSC-Y
```

Run:
```bash
python downloadPsf.py \
    --list psf_coords.txt \
    --rerun s23b_wide \
    --type coadd \
    --centered true \
    --user $SSP_IDR_USR
```

## Database Schema Reference

### Main Catalog Tables (S23B/DR4)

| Table | Description |
|-------|-------------|
| `s23b_wide.forced` | Forced photometry (CModel fluxes, coordinates) |
| `s23b_wide.forced2` | PSF + Kron photometry, SDSS shapes |
| `s23b_wide.forced3` | Aperture photometry |
| `s23b_wide.forced4` | Convolved fluxes |
| `s23b_wide.forced5` | Undeblended convolved flux |
| `s23b_wide.forced6` | GaaP fluxes |
| `s23b_wide.photoz_mizuki` | Mizuki photometric redshifts |
| `s23b_wide.masks` | Bright star masks |

**Note:** The `forced` table is split into 6 parts due to PostgreSQL column limits. To get both CModel and PSF fluxes, JOIN on `object_id`:

```sql
SELECT f.object_id, f.ra, f.dec, 
       f.i_cmodel_flux, f2.i_psfflux_flux
FROM s23b_wide.forced AS f
LEFT JOIN s23b_wide.forced2 AS f2 
    ON f.object_id = f2.object_id
WHERE coneSearch(f.coord, 136.47, -0.05, 60)
```

### Useful SQL Functions

| Function | Description |
|----------|-------------|
| `coneSearch(coord, ra, dec, radius_arcsec)` | Cone search |
| `boxSearch(coord, ra1, ra2, dec1, dec2)` | Box search |
| `tractSearch(object_id, tract)` | Tract selection |

### Flux Units

- **Fluxes:** nano-Janskys (nJy)
- **Magnitudes:** AB mag (stored as `_mag` columns)
- **Coordinates:** degrees (J2000)

## Complete Workflow Example

```bash
#!/bin/bash

# Set credentials
export SSP_IDR_USR="your_username"
export SSP_IDR_PWD="your_password"

# Target coordinates
RA=136.471165
DEC=-0.046470

# 1. Query catalog
cat > query.sql << EOF
SELECT object_id, ra, dec, 
    g_cmodel_mag, r_cmodel_mag, i_cmodel_mag, z_cmodel_mag, y_cmodel_mag
FROM s23b_wide.forced
WHERE coneSearch(coord, $RA, $DEC, 10)
AND i_cmodel_flux > 0
ORDER BY i_cmodel_flux DESC
LIMIT 10
EOF

python hscSspQuery3.py \
    --user $SSP_IDR_USR \
    --release-version dr4 \
    --format csv \
    query.sql > catalog.csv

# 2. Download cutouts
cat > cutout_list.txt << EOF
#? ra dec sw sh filter type
$RA $DEC 10arcsec 10arcsec HSC-G coadd/bg
$RA $DEC 10arcsec 10arcsec HSC-R coadd/bg
$RA $DEC 10arcsec 10arcsec HSC-I coadd/bg
$RA $DEC 10arcsec 10arcsec HSC-Z coadd/bg
$RA $DEC 10arcsec 10arcsec HSC-Y coadd/bg
EOF

python downloadCutout.py \
    --list cutout_list.txt \
    --rerun s23b_wide \
    --image true --mask true --variance true \
    --user $SSP_IDR_USR

# 3. Download PSFs
cat > psf_list.txt << EOF
#? ra dec filter
$RA $DEC HSC-G
$RA $DEC HSC-R
$RA $DEC HSC-I
$RA $DEC HSC-Z
$RA $DEC HSC-Y
EOF

python downloadPsf.py \
    --list psf_list.txt \
    --rerun s23b_wide \
    --type coadd \
    --centered true \
    --user $SSP_IDR_USR
```

## Troubleshooting

### PSF Download 404 Error

If PSF download fails with 404 for S23B data, edit `downloadPsf.py` and change:
```python
api_url = "https://hscdata.mtk.nao.ac.jp/psf/8"
```
to:
```python
api_url = "https://hscdata.mtk.nao.ac.jp/psf/9"
```

### Authentication Errors

- Check that environment variables are set: `echo $SSP_IDR_USR`
- For PDR3, use `SSP_PDR_USR`/`SSP_PDR_PWD`
- Password can also be provided via `--password-env` or interactively

### Query Timeout

- Use `--preview` first to test queries
- Add `LIMIT` to your SQL for large queries
- Use `coneSearch()` or `boxSearch()` instead of manual coordinate comparisons

## References

- Official repository: https://hsc-gitlab.mtk.nao.ac.jp/ssp-software/data-access-tools
- Schema browser (Internal): https://hscdata.mtk.nao.ac.jp/schema_browser3/
- Schema browser (Public): https://hsc-release.mtk.nao.ac.jp/schema/
- PDR3 documentation: https://hsc-release.mtk.nao.ac.jp/doc/
