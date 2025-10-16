# Lyric Language — Version 0.0.2

**Release Date:** December 15, 2024

## Summary

This version completes Sprint 1 (Lyric Core Foundations). The core language pipeline is now functional, including lexing, parsing, interpretation, and CLI execution.

## Added

- Implemented the initial lexer with full keyword and symbol recognition
- Implemented parser with support for def, if, else, end, given, done, and +++ class terminator
- Added AST node structures for program, function, if, loop, class, assignment, and call
- Added interpreter that executes basic expressions, print statements, and functions
- Added runtime with built-in functions: print, input, int, float, str, range, len, open
- Implemented CLI command "lyric run <file.ly>" with version flag support
- Added initial test suite covering lexer, parser, and interpreter
- Added three working example programs (hello.ly, if_demo.ly, loop.ly)

## Changed

- Standardized Lyric source file extension from .lyr to .ly
- Confirmed all tests reference .ly files and pass successfully

## Fixed

- Minor token alignment issues in the parser
- Cleaned up variable scoping inside the interpreter environment
- Resolved incorrect handling of "else if" parsing

## Notes

- This version represents the first complete end-to-end execution path
- All examples now run via CLI and produce expected output
- Ready for version tag v0.0.2 and transition to Sprint 2

---

# Version 0.0.1

**Release Date:** Initial Release

## Summary

Initial repository structure and project scaffolding before the interpreter was operational.
