# Lyric Language — Version 0.1.6

**Release Date:** December 2024

## Summary

This version completes Sprint 4 (Variable Handling & Declaration Syntax) with all 5 tasks implemented. The language now supports dynamic typing with the `var` keyword, strict declaration enforcement, multi-variable declarations, comprehensive documentation, and extensive validation. This milestone represents a significant enhancement to Lyric's variable system with 226+ passing tests and production-ready features.

## Added (Sprint 4 - Complete)

- **Dynamic Typing**: Complete `var` keyword implementation with full type flexibility
- **Declaration Enforcement**: Strict variable declaration requirements preventing implicit creation
- **Multi-Variable Declarations**: Comma-separated syntax supporting mixed-type declarations
- **Comprehensive Documentation**: Updated specification with formal grammar and examples
- **Extensive Validation**: 38 dedicated Sprint 4 tests with 100% success rate

## Changed

- **Version Number**: Updated from 0.1.4 to 0.1.6 (Sprint 4 complete)
- **Variable System**: Enhanced with dynamic typing and declaration enforcement
- **Documentation**: Complete specification update with formal grammar rules
- **Test Coverage**: Expanded to 226+ tests with comprehensive Sprint 4 coverage

## Notes

- Sprint 4 is complete with all 5 tasks implemented and verified
- All Definition of Done criteria met and validated
- Ready for production use with `dev-0.1.6` tag
- Comprehensive documentation and specification available
- All 226+ tests passing with 100% success rate

---

# Lyric Language — Version 0.1.4

**Release Date:** December 2024

## Summary

This version introduces Sprint 4 Task 1 (Dynamic Typing with `var` keyword) and completes Sprint 3 (Type System, Value Validation, and Advanced Runtime). The language now supports both dynamic typing with the `var` keyword and static typing, built-in data structures (lists and dictionaries), enhanced error handling, runtime safety, and comprehensive test coverage with 198+ passing tests.

## Added (Sprint 4 - Task 1)

- **Dynamic Typing**: New `var` keyword for dynamically typed variables that can change type at runtime
- **Type Flexibility**: Variables declared with `var` can be reassigned to different types without type checking
- **Python-like Behavior**: `var` variables behave like Python variables with full dynamic typing
- **Enhanced Test Coverage**: 10 new tests specifically for `var` keyword functionality

## Added (Sprint 4 - Task 2)

- **Declaration Enforcement**: All variables must now be explicitly declared before use (`var`, `int`, `str`, etc.)
- **Strict Variable Management**: Prevents implicit variable creation and improves code safety
- **Clear Error Messages**: Specific error messages for undeclared and uninitialized variables
- **Enhanced Test Coverage**: 14 new tests for declaration enforcement scenarios

## Added (Sprint 4 - Task 3)

- **Multi-Variable Declarations**: Support for comma-separated variable declarations in a single line
- **Mixed Type Declarations**: Variables of different types can be declared together (e.g., `var x, int y, str z`)
- **Flexible Declaration Syntax**: Support for both simple and mixed-type multi-declarations
- **Enhanced Test Coverage**: 14 new tests for multi-variable declaration scenarios

## Added (Sprint 3)

- **Type System**: Complete type declaration and inference system with int, float, str, god, and None types
- **Type Enforcement**: Runtime type checking for function parameters and variable assignments
- **Built-in Data Structures**: Full support for lists and dictionaries with indexing and operations
- **Enhanced Error Handling**: Improved error messages with filename, line number, and context information
- **Runtime Safety**: Enhanced runtime error reporting and type verification
- **Comprehensive Test Suite**: 188 tests covering all Sprint 3 features including type system, data structures, and error handling
- **New Example Programs**: type_tests.ly, list_dict_tests.ly, exception_tests.ly, class_init_tests.ly

## Changed

- **Version Number**: Updated from 0.1.3 to 0.1.4 (final Sprint 3 version)
- **Error Messages**: All runtime errors now include precise file and line references
- **Type System**: Variables can now be declared with explicit types and enforced at runtime
- **Data Structures**: Lists and dictionaries are now first-class types with full operation support

## Fixed

- **Type Safety**: All type mismatches are now caught and reported with clear error messages
- **Data Structure Operations**: List indexing and dictionary key access with proper error handling
- **Test Coverage**: Expanded test suite from 88 to 188 tests with comprehensive Sprint 3 coverage
- **Documentation**: Updated README.md and CHANGELOG.md to reflect all new features

## Notes

- This version represents the completion of Sprint 3 with all 8 tasks implemented
- Type system provides both explicit declarations and automatic inference
- Data structures support nested access and comprehensive operations
- All 188 tests pass with 100% success rate
- Ready for version tag v0.1.4 and transition to Sprint 4

---

# Lyric Language — Version 0.1.3

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
- **New Example Programs**: class_test.ly, nested_flow.ly, godean_test.ly, runtime_test.ly, and error demonstration files

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
