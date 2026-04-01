#!/bin/bash
# Quick lookup for STILTS command documentation
# Requires stilts.jar in ~/code/ or set via STILTS_JAR environment variable

STILTS_JAR="${STILTS_JAR:-$HOME/code/stilts.jar}"

# Check if jar exists
if [ ! -f "$STILTS_JAR" ]; then
    echo "Error: STILTS jar not found at $STILTS_JAR"
    echo ""
    echo "To install STILTS:"
    echo "  mkdir -p ~/code"
    echo "  curl -L -o ~/code/stilts.jar 'https://www.star.bris.ac.uk/~mbt/stilts/stilts.jar'"
    exit 1
fi

if [ $# -eq 0 ]; then
    echo "STILTS Command Quick Lookup"
    echo "==========================="
    echo ""
    echo "Usage: lookup.sh <command> [parameter]"
    echo ""
    echo "Core Table Processing:"
    echo "  tcopy      - Format conversion"
    echo "  tmatch1    - Internal crossmatch"
    echo "  tmatch2    - Two-table crossmatch"
    echo "  tmatchn    - N-table crossmatch"
    echo "  tskymatch2 - Optimized sky crossmatch"
    echo "  tjoin      - Side-by-side join"
    echo "  arrayjoin  - Per-row table join"
    echo "  tcat       - Concatenate tables"
    echo "  tcatn      - Concatenate N tables"
    echo ""
    echo "Virtual Observatory:"
    echo "  cone        - Cone search query"
    echo "  tapquery    - TAP server query"
    echo "  cdsskymatch - CDS crossmatch"
    echo "  coneskymatch- Generic cone crossmatch"
    echo ""
    echo "Other useful:"
    echo "  tpipe       - Pipeline processing"
    echo "  calc        - Expression calculator"
    echo "  funcs       - List functions"
    echo ""
    echo "Examples:"
    echo "  lookup.sh tmatch2           # Full help for tmatch2"
    echo "  lookup.sh tmatch2 matcher   # Help for specific parameter"
    echo "  lookup.sh -list             # List all commands"
    exit 0
fi

COMMAND=$1

if [ "$COMMAND" = "-list" ]; then
    java -jar "$STILTS_JAR" -help 2>&1 | grep -A 100 "Known tasks:"
    exit 0
fi

if [ $# -eq 1 ]; then
    # Show full help for command
    java -jar "$STILTS_JAR" "$COMMAND" -help doc=full 2>&1
else
    # Show help for specific parameter
    PARAM=$2
    java -jar "$STILTS_JAR" "$COMMAND" "help=$PARAM" 2>&1
fi
