# Lyric Language — Version 0.0.3

**Release Date:** December 2024

## Summary

This version completes Sprint 2 (Control Flow, Error Handling, and Class Support). The language now supports nested control flow, comprehensive error reporting, class instantiation and methods, runtime enhancements, and extensive test coverage.

## Added

- **Nested Control Flow**: Full support for nested if/else/end and given/done blocks
- **Boolean and Comparison Operations**: Complete implementation of ==, !=, <, <=, >, >=, and, or, not operators
- **Error Reporting System**: Enhanced error handling with SyntaxErrorLyric, RuntimeErrorLyric, NameErrorLyric including line numbers and filenames
- **Comment Syntax**: Full-line and inline comment support using # symbol
- **Class Parsing and Structure**: Complete class definition parsing with +++ terminator
- **Class Interpretation**: Full runtime support for class instantiation, method calls, and attribute access
- **Runtime Enhancements**: Added isinstance() and type() built-in functions for type checking and introspection
- **Enhanced Print Function**: Improved handling of None values and compound types
- **Comprehensive Test Suite**: 88 tests covering all features including CLI integration tests
- **New Example Programs**: class_test.ly, nested_flow.ly, boolean_test.ly, runtime_test.ly, and error demonstration files

## Changed

- **Enhanced Error Messages**: All errors now include filename, line number, and column information
- **Improved Print Function**: Better formatting for None values and compound data types
- **Extended Range Function**: Confirmed support for range(start, stop) parameters
- **Class System**: Full object-oriented programming support with instances and bound methods

## Fixed

- **Code Quality**: Resolved all flake8 warnings and style issues
- **Documentation**: Added comprehensive docstrings to all new classes and functions
- **Test Coverage**: Expanded test suite from 56 to 88 tests with CLI integration testing
- **Error Handling**: Eliminated Python tracebacks in favor of user-friendly error messages

## Notes

- This version represents a major milestone with full object-oriented programming support
- All Sprint 2 features are fully implemented and tested
- Ready for version tag v0.0.3 and transition to Sprint 3
- 88 tests passing with 100% success rate
- CLI integration tests ensure user-facing functionality works correctly

---

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
