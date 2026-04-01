#!/bin/bash
# STILTS wrapper script
# This script expects stilts.jar to be in ~/code/
# Download from: https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar

STILTS_JAR="${STILTS_JAR:-$HOME/code/stilts.jar}"

# Check if jar exists
if [ ! -f "$STILTS_JAR" ]; then
    echo "Error: STILTS jar not found at $STILTS_JAR"
    echo ""
    echo "To install STILTS:"
    echo "  mkdir -p ~/code"
    echo "  curl -L -o ~/code/stilts.jar 'https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar'"
    echo ""
    echo "Or set STILTS_JAR environment variable to point to your jar file:"
    echo "  export STILTS_JAR=/path/to/stilts.jar"
    exit 1
fi

# Run STILTS with all arguments
exec java -jar "$STILTS_JAR" "$@"
