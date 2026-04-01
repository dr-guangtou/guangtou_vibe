# STILTS CLI Skill

**STILTS** (Starlink Tables Infrastructure Library Tool Set) - Command-line tools for processing astronomical tabular data.

---

## ⚠️ Prerequisites: Install STILTS First

This skill contains documentation and helper scripts, but **does NOT include the STILTS jar file**. You must download it yourself.

### Quick Install

```bash
# 1. Create ~/code/ directory if it doesn't exist
mkdir -p ~/code

# 2. Download STILTS
curl -L -o ~/code/stilts.jar "https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"

# 3. Verify installation
java -jar ~/code/stilts.jar -version
```

### Alternative Locations

If you prefer a different location, set the environment variable:

```bash
export STILTS_JAR=/path/to/your/stilts.jar
```

All scripts in this skill will respect this variable.

---

## What's Included

| Directory | Contents |
|-----------|----------|
| `SKILL.md` | Complete documentation for all commands |
| `QUICKREF.md` | One-page quick reference |
| `references/` | Local HTML manual (sun256.html), examples, help data |
| `scripts/` | Helper scripts (stilts.sh, lookup.sh, update.sh, verify.sh) |

---

## Quick Start

### Option 1: Use Alias

```bash
alias stilts='java -jar ~/code/stilts.jar'
# Add to ~/.zshrc or ~/.bashrc to make permanent

stilts tcopy in.fits out.vot
```

### Option 2: Use Wrapper Script

```bash
~/Desktop/qibin/skills/stilts-cli/scripts/stilts.sh tcopy in.fits out.vot
```

### Option 3: Add to PATH

```bash
# Create wrapper in ~/bin
mkdir -p ~/bin
cp ~/Desktop/qibin/skills/stilts-cli/scripts/stilts.sh ~/bin/stilts

# Add ~/bin to PATH in ~/.zshrc
export PATH="$HOME/bin:$PATH"

# Now use directly
stilts tcopy in.fits out.vot
```

---

## Key Commands

### Table Processing
- `tcopy` - Format conversion (FITS ↔ VOTable ↔ CSV)
- `tmatch1` - Find duplicates within a catalog
- `tmatch2` - Crossmatch two catalogs
- `tmatchn` - Crossmatch multiple catalogs
- `tskymatch2` - Fast sky crossmatch (HEALPix optimized)
- `tcat` - Concatenate tables
- `tpipe` - Pipeline processing (filter, add columns, etc.)

### Virtual Observatory
- `cdsskymatch` - Crossmatch with VizieR/SIMBAD
- `tapquery` - Query TAP servers with ADQL
- `cone` - Cone search queries

---

## Documentation

| Resource | Path |
|----------|------|
| Full manual (local) | `references/sun256.html` (2.5 MB) |
| Example recipes | `references/examples.md` |
| This skill's docs | `SKILL.md` |
| Quick reference | `QUICKREF.md` |
| Online | https://www.star.bris.ac.uk/~mbt/stilts/ |

---

## Helper Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `verify.sh` | Verify installation | `./scripts/verify.sh` |
| `lookup.sh` | Quick command help | `./scripts/lookup.sh tmatch2` |
| `update.sh` | Update STILTS | `./scripts/update.sh` |
| `stilts.sh` | Wrapper script | `./scripts/stilts.sh tcopy ...` |

---

## Common Examples

### Format Conversion
```bash
stilts tcopy survey.fits survey.vot
stilts tcopy data.csv data.fits ofmt=fits-plus
```

### Sky Crossmatch
```bash
stilts tmatch2 in1=cat1.fits in2=cat2.fits \
    matcher=sky values1='ra dec' values2='ra dec' \
    params=2 join=1and2 find=best out=matched.fits
```

### Query Gaia DR3
```bash
stilts cdsskymatch in=my_catalog.fits \
    ra=RA dec=DEC radius=3 \
    cdstable='I/355/gaiadr3' find=best out=with_gaia.fits
```

### Pipeline Processing
```bash
stilts tpipe in=galaxy.fits \
    cmd='select mag_r < 20' \
    cmd='addcol g_r mag_g - mag_r' \
    cmd='sort mag_r' \
    out=processed.fits
```

---

## Version

- **Current STILTS**: 3.5-4 (2025-09-12)
- **STIL Version**: 4.3-4
- **Download URL**: https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar

To update to the latest version:
```bash
./scripts/update.sh
```

---

## Troubleshooting

### "Error: STILTS jar not found"
Download and install STILTS first:
```bash
mkdir -p ~/code
curl -L -o ~/code/stilts.jar "https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"
```

### "java: command not found"
Install Java (JVM 1.8+ required):
```bash
# macOS with Homebrew
brew install openjdk

# Ubuntu/Debian
sudo apt-get install default-jre
```

### Permission denied on scripts
```bash
chmod +x ~/Desktop/qibin/skills/stilts-cli/scripts/*.sh
```

---

## License

STILTS is developed by Mark Taylor at the University of Bristol.
- Website: https://www.star.bris.ac.uk/~mbt/stilts/
- Part of the Starlink software collection
