#!/bin/bash
# Verify STILTS installation and basic functionality
# This script looks for stilts.jar in ~/code/ or uses STILTS_JAR environment variable

set -e

STILTS_JAR="${STILTS_JAR:-$HOME/code/stilts.jar}"
SKILL_DIR="/Users/shuang/Desktop/qibin/skills/stilts-cli"

echo "STILTS Skill Verification"
echo "========================="
echo ""

# Check jar exists
if [ ! -f "$STILTS_JAR" ]; then
    echo "✗ STILTS jar not found at $STILTS_JAR"
    echo ""
    echo "To install STILTS:"
    echo "  mkdir -p ~/code"
    echo "  curl -L -o ~/code/stilts.jar 'https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar'"
    echo ""
    echo "Or set STILTS_JAR environment variable:"
    echo "  export STILTS_JAR=/path/to/stilts.jar"
    exit 1
fi
echo "✓ STILTS jar found at: $STILTS_JAR"

# Check version
echo ""
echo "Version Information:"
java -jar "$STILTS_JAR" -version 2>&1 | head -10
echo ""

# Test calc
echo "Testing calc command..."
RESULT=$(java -jar "$STILTS_JAR" calc "2 + 2" 2>&1 | tr -d '[:space:]')
if [ "$RESULT" = "4" ]; then
    echo "✓ calc works (2+2=4)"
else
    echo "✗ calc failed (got: '$RESULT')"
    exit 1
fi

# Test format conversion
echo ""
echo "Testing format conversion..."
cat > /tmp/test_stilts.csv << 'EOF'
id,ra,dec,mag
1,150.0,2.0,18.5
2,150.1,2.1,19.2
EOF

java -jar "$STILTS_JAR" tcopy /tmp/test_stilts.csv /tmp/test_stilts.fits 2>&1 > /dev/null
if [ -f /tmp/test_stilts.fits ]; then
    echo "✓ Format conversion works (CSV → FITS)"
    rm /tmp/test_stilts.fits
else
    echo "✗ Format conversion failed"
    exit 1
fi
rm /tmp/test_stilts.csv

# Test crossmatch
echo ""
echo "Testing crossmatch..."
cat > /tmp/cat1.csv << 'EOF'
id,ra,dec
A1,150.0,2.0
A2,150.1,2.1
EOF
cat > /tmp/cat2.csv << 'EOF'
id,ra,dec
B1,150.005,2.005
B2,150.105,2.105
EOF

java -jar "$STILTS_JAR" tmatch2 \
    in1=/tmp/cat1.csv in2=/tmp/cat2.csv \
    matcher=sky values1='ra dec' values2='ra dec' \
    params=30 join=1and2 find=all \
    ofmt=csv out=/tmp/matched.csv 2>&1 > /dev/null

MATCHES=$(wc -l < /tmp/matched.csv)
if [ "$MATCHES" -eq 3 ]; then  # Header + 2 matches
    echo "✓ Crossmatch works (found 2 matches)"
else
    echo "✗ Crossmatch failed (expected 2 matches, got $((MATCHES-1)))"
    exit 1
fi

rm /tmp/cat1.csv /tmp/cat2.csv /tmp/matched.csv

# Check documentation
echo ""
echo "Checking documentation..."
if [ -f "${SKILL_DIR}/SKILL.md" ]; then
    echo "✓ SKILL.md present"
fi
if [ -f "${SKILL_DIR}/references/sun256.html" ]; then
    SIZE=$(du -sh "${SKILL_DIR}/references/sun256.html" | cut -f1)
    echo "✓ HTML manual present ($SIZE)"
fi
if [ -f "${SKILL_DIR}/references/examples.md" ]; then
    echo "✓ Examples file present"
fi

echo ""
echo "========================="
echo "✓ All verification tests passed!"
echo ""
echo "Quick start:"
echo "  alias stilts='java -jar $STILTS_JAR'"
echo "  stilts tcopy in.fits out.vot"
echo ""
