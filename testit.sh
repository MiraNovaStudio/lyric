#!/bin/bash
# Run Lyric language interpreter tests
# This script works on both Unix/Linux and Windows (with Git Bash)

echo "Running Lyric interpreter tests..."
echo "=================================="

# Run tests from the lyric package
echo "Running lexer tests..."
python -m pytest lyric/tests/test_lexer.py -v

echo ""
echo "Running parser tests..."
python -m pytest lyric/tests/test_parser.py -v

echo ""
echo "Running interpreter tests..."
python -m pytest lyric/tests/test_interpreter.py -v

echo ""
echo "Running all lyric tests..."
python -m pytest lyric/tests/ -v

echo ""
echo "Running root level tests..."
python -m pytest tests/ -v

echo ""
echo "=================================="
echo "All tests completed!"
