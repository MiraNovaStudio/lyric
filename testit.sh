#!/bin/bash
# Run Lyric language interpreter tests
# This script works on both Unix/Linux and Windows (with Git Bash)
#
# Usage:
#   ./testit.sh          - Run tests in normal mode (brief summary)
#   ./testit.sh -v       - Run tests in verbose mode (detailed output)
#   ./testit.sh --verbose - Run tests in verbose mode (detailed output)

# Check for verbose flag
VERBOSE=false
if [[ "$1" == "-v" || "$1" == "--verbose" ]]; then
    VERBOSE=true
fi

if [ "$VERBOSE" = true ]; then
    echo "Running Lyric interpreter tests (VERBOSE MODE)..."
    echo "================================================"
    
    # Run tests from the lyric package with detailed output
    echo "Running lexer tests..."
    python3 -m pytest lyric/tests/test_lexer.py -v
    
    echo ""
    echo "Running parser tests..."
    python3 -m pytest lyric/tests/test_parser.py -v
    
    echo ""
    echo "Running interpreter tests..."
    python3 -m pytest lyric/tests/test_interpreter.py -v
    
    echo ""
    echo "Running all lyric tests..."
    python3 -m pytest lyric/tests/ -v
    
    echo ""
    echo "================================================"
    echo "All tests completed!"
else
    echo "Running Lyric interpreter tests..."
    echo "=================================="
    
    # Run all tests and capture summary
    echo "Running all tests..."
    python3 -m pytest lyric/tests/ --tb=short -q

    echo "Running tests lyric interpreted"
    LYRIC_INTERPRET=1 python3 -m pytest lyric/tests/ --tb=short -q
    
    echo ""
    echo "=================================="
    echo "All tests completed!"
    echo ""
    #echo "For detailed output, run: ./testit.sh -v"
fi


echo "Testing core constructs..."
lyric run ./studio/does_it_work.ly 

echo "Testing core contructs interpreted..."
lyric run ./studio/does_it_work.ly --interpret


