#!/bin/bash
# Update STILTS to the latest version
# This script updates the jar in ~/code/

STILTS_JAR="${STILTS_JAR:-$HOME/code/stilts.jar}"
STILTS_DIR=$(dirname "$STILTS_JAR")
SKILL_DIR="/Users/shuang/Desktop/qibin/skills/stilts-cli"
REF_DIR="${SKILL_DIR}/references"

# Ensure directory exists
mkdir -p "$STILTS_DIR"

# Backup current version
if [ -f "$STILTS_JAR" ]; then
    CURRENT_VERSION=$(java -jar "$STILTS_JAR" -version 2>&1 | grep "STILTS version" | awk '{print $3}')
    echo "Current version: $CURRENT_VERSION"
    echo "Backing up..."
    cp "$STILTS_JAR" "${STILTS_JAR%.jar}-${CURRENT_VERSION}.jar.bak"
else
    echo "No existing STILTS jar found at $STILTS_JAR"
fi

# Download new version
echo "Downloading latest STILTS..."
echo "From: https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"
curl -L -o "${STILTS_JAR}.new" "https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar"

# Verify download
if [ $? -ne 0 ]; then
    echo "Error: Download failed"
    rm -f "${STILTS_JAR}.new"
    exit 1
fi

# Get new version
NEW_VERSION=$(java -jar "${STILTS_JAR}.new" -version 2>&1 | grep "STILTS version" | awk '{print $3}')
if [ -z "$NEW_VERSION" ]; then
    echo "Error: Could not determine version"
    rm -f "${STILTS_JAR}.new"
    exit 1
fi
echo "Downloaded version: $NEW_VERSION"

# Replace old version
mv "${STILTS_JAR}.new" "$STILTS_JAR"

# Update VERSION file in skill directory
echo "STILTS_VERSION=$NEW_VERSION" > "${SKILL_DIR}/assets/VERSION"
echo "Updated on $(date)" >> "${SKILL_DIR}/assets/VERSION"

# Update manual
echo ""
echo "Downloading updated manual..."
curl -L -o "${REF_DIR}/sun256.html" "https://www.star.bris.ac.uk/~mbt/stilts/sun256/sun256.html"

echo ""
echo "========================="
echo "Update complete!"
echo "New version: $NEW_VERSION"
echo "Location: $STILTS_JAR"
echo ""
echo "To verify: java -jar $STILTS_JAR -version"
