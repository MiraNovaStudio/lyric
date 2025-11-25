# Sprint 8 Task 7: Function Return-Type Declaration Syntax Change

## Date
November 24, 2025 - 21:00

## Task
Changed function return-type declaration syntax to allow typed functions to be declared without the `def` keyword, while retaining `def` for untyped functions.

## Changes

### Parser (`lyric/parser.py`)
- Modified `_parse_statement` to recognize the new syntax `TYPE IDENT(` as a typed function definition
- Updated `_parse_func_def` to handle both syntaxes:
  - **New syntax**: `TYPE funcname(params)` for typed functions
  - **Old syntax**: `def funcname(params)` for untyped functions
  - **Legacy syntax**: `TYPE def funcname(params)` still works for backward compatibility
- Added logic to require `def` keyword for untyped functions (no return type specified)

### New Syntax Examples
```lyric
# New typed function syntax (without def)
int add(int a, int b) {
    return a + b
}

# Untyped function syntax (with def)
def say_hello(name) {
    print name
}

# Old syntax still works
int def add_old_style(int a, int b) {
    return a + b
}
```

### Tests (`lyric/tests/core-0.7.0/test_function_syntax.py`)
- Created comprehensive test suite with 16 tests covering:
  - New typed function syntax for all types (int, str, flt, arr, map, var, rex, god, bin)
  - Untyped functions with `def` keyword
  - Functions with no parameters
  - Functions with mixed parameter types
  - Recursive functions
  - Nested function calls
  - Backward compatibility with old syntax
  - Return type inference for `def` functions

## Test Results
- **All Sprint 8 tests**: 118/118 passed (100%)
- **Function syntax tests**: 16/16 passed (100%)

## Breaking Changes
None. Both old and new syntaxes are supported for full backward compatibility.

## Benefits
- **Cleaner syntax**: Typed functions no longer require the redundant `def` keyword
- **More intuitive**: Follows common programming language conventions
- **Backward compatible**: All existing code continues to work
- **Clear distinction**: Typed vs. untyped functions are now syntactically distinct

## Implementation Notes
- The parser looks ahead three tokens to determine if a statement is a typed function definition
- The `_parse_func_def` method was updated to handle the new syntax while maintaining backward compatibility
- No changes were needed to the lexer, AST nodes, or interpreter
