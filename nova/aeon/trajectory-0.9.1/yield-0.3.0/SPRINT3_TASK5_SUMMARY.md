# Sprint 3 Task 5 Summary: Exception Handling

## Overview
Successfully implemented exception handling in the Lyric language with `try/catch/finally/fade` blocks and `raise` statement support. This adds robust error handling capabilities to the language, allowing developers to gracefully handle runtime errors.

## Key Features Implemented

### 1. Try/Catch/Finally/Fade Syntax
- **Try Block**: Executes code that may raise exceptions
- **Catch Block**: Handles exceptions raised in try block (mandatory - syntax error if missing)
- **Finally Block**: Always executes after try/catch, regardless of exceptions (optional)
- **Fade**: Block terminator keyword (replaces `end` for exception blocks)

### 2. Raise Statement
- **Syntax**: `raise ExceptionName`
- **Support**: Both Lyric-style names (with Lyric suffix) and standard Python names
- **Examples**: `raise RuntimeErrorLyric`, `raise IndexError`, `raise TypeErrorLyric`
- **No Message**: Simple exception raising without message support (deferred to future sprint)

### 3. Exception Mapping
- **Lyric Exceptions**: `RuntimeErrorLyric`, `IndexErrorLyric`, `TypeErrorLyric`, etc.
- **Python Exceptions**: Maps to Python's built-in exceptions for consistency
- **Integration**: Existing Lyric error types (RuntimeErrorLyric, SyntaxErrorLyric) are catchable

### 4. Scope Behavior
- **Shared Scope**: try, catch, and finally blocks share the same scope
- **Variable Access**: Variables defined in outer scope are accessible and modifiable in all blocks
- **No Isolation**: Variables are not isolated between blocks (simplified for this sprint)

## Technical Implementation

### Lexer Changes (`lyric/lexer.py`)
- **Added Keywords**: `catch`, `fade`, `raise`
- **Removed Keyword**: `except` (replaced with `catch`)
- **Total Keywords**: 17 keywords now recognized

### AST Nodes (`lyric/ast_nodes.py`)
- **Created `TryNode`**: Represents try/catch/finally statement
  - `try_body`: List of statements in try block
  - `catch_body`: List of statements in catch block (Optional)
  - `finally_body`: List of statements in finally block (Optional)
- **Created `RaiseNode`**: Represents raise statement
  - `exception_name`: Name of exception to raise
- **Note**: No separate `CatchNode` or `FinallyNode` - they're part of `TryNode` structure

### Parser Changes (`lyric/parser.py`)
- **Added `_parse_try_block`**: Parses try/catch/finally/fade syntax
  - Validates that catch block is present (raises ParseError if missing)
  - Consumes `fade` keyword to terminate block
  - Handles optional finally block
- **Added `_parse_raise_stmt`**: Parses raise statement
  - Expects exception name (IDENT token) after `raise` keyword
- **Updated `_parse_statement`**: Routes TRY and RAISE tokens to appropriate parsing methods

### Interpreter Changes (`lyric/interpreter.py`)
- **Added `_evaluate_try_statement`**: Evaluates try/catch/finally blocks
  - Executes try body with Python try/except
  - Catches any exception and executes catch block if present
  - Always executes finally block after try/catch
  - Re-raises exception if not caught by catch block
  - Handles ReturnValue instances for proper return propagation
- **Added `_evaluate_raise_statement`**: Raises exceptions
  - Maps exception names to Python exception classes
  - Supports both Lyric-style and Python-style names
  - Defaults to RuntimeErrorLyric for unknown exceptions
- **Exception Mapping**: Comprehensive mapping of Lyric/Python exception names

### Error Types (`lyric/errors.py`)
- No changes required - existing error types already use Lyric postfix naming convention
- Existing types: `LexError`, `ParseError`, `SyntaxErrorLyric`, `RuntimeErrorLyric`, `NameErrorLyric`

## Test Coverage

### New Test File: `lyric/tests/test_exception_handling.py`
- **22 comprehensive test cases** covering:
  - Basic try/catch functionality
  - Try/catch with exceptions
  - Try/catch/finally execution order
  - Finally always executes
  - Raising different exception types
  - Uncaught exception propagation
  - Exception handling in function calls
  - Try without catch syntax error
  - Scope behavior (shared scope)
  - Multiple statements in each block
  - Standard Python exception names
  - Print statements in exception blocks
  - Lexer keyword verification
  - AST structure verification

### Test Results
- **All 22 new tests pass** ✅
- **Full test suite**: 223 tests pass ✅
- **No regressions** introduced

## Code Examples

### Basic Exception Handling
```lyric
def main() {
    var result = 0
    try:
        result = 10
    catch:
        result = 20
    fade
    return result
}
```

### Exception Handling with Finally
```lyric
def main() {
    var result = 0
    try:
        raise RuntimeErrorLyric
    catch:
        result = 20
    finally:
        result = result + 5
    fade
    return result  # Returns 25
}
```

### Exception in Function Call
```lyric
def risky_function() {
    raise RuntimeErrorLyric
    return 10
}

def main() {
    var result = 0
    try:
        result = risky_function()
    catch:
        result = 99
    fade
    return result  # Returns 99
}
```

## Error Handling

### Syntax Errors
- **Try without catch**: Raises ParseError: "try block must have a catch block"
- **Missing fade**: Raises ParseError: "Expected 'fade' to end try block"

### Runtime Errors
- **Uncaught exceptions**: Propagate outside try/catch if no catch block handles them
- **Unknown exceptions**: Default to RuntimeErrorLyric for unknown exception names

## Integration

### With Previous Sprint 3 Features
- **Type Declarations**: Work seamlessly in exception blocks
- **Typed Parameters**: Exception handling works with typed function parameters
- **Data Structures**: Lists and dictionaries work normally in exception blocks
- **Class Methods**: Exception handling works with class methods and init() functions

### Backward Compatibility
- Existing error handling mechanisms remain unchanged
- No breaking changes to existing syntax
- All previous tests continue to pass

## Design Decisions Documented

### 1. AST Node Structure
**Decision**: Combined try, catch, and finally into a single `TryNode` instead of separate nodes for each.
**Rationale**: Simplifies AST structure and evaluation logic, as these blocks are always parsed together as a single unit.

### 2. Scope Isolation
**Decision**: try, catch, and finally blocks share the same scope without isolation.
**Rationale**: Simpler implementation for this sprint. Variable isolation can be added in future sprints if needed.

### 3. Catch Block Requirement
**Decision**: Try without catch is a syntax error.
**Rationale**: Aligns with user requirements. A try block without error handling serves no purpose.

### 4. Exception Names
**Decision**: Support both Lyric-style names (IndexErrorLyric) and Python-style names (IndexError).
**Rationale**: Provides flexibility and familiarity for developers coming from Python.

### 5. Finally Execution
**Decision**: Finally always executes after catch block code, regardless of exceptions or returns.
**Rationale**: Standard exception handling behavior ensures cleanup code always runs.

## Performance Considerations
- **Minimal Overhead**: Exception handling uses Python's native try/except mechanism
- **No Nesting**: No nested try/catch support in this sprint (can be added if needed)
- **Direct Mapping**: Direct mapping to Python exceptions for efficient error handling

## Future Enhancements
- **Specific Exception Types**: Catch specific exception types (e.g., `catch IndexError:`)
- **Exception Object Access**: Access exception object in catch block (`catch as e:`)
- **Multiple Catch Blocks**: Support multiple catch blocks for different exception types
- **Custom Messages**: Support `raise ExceptionName "custom message"` syntax
- **Nested Try/Catch**: Allow nested exception handling blocks
- **Exception Chaining**: Support `raise ... from ...` syntax

## Conclusion
Sprint 3 Task 5 successfully adds exception handling to Lyric, providing:
- Complete try/catch/finally/fade syntax
- Raise statement for manual exception raising
- Integration with existing Lyric error types
- Comprehensive test coverage with no regressions

The implementation is simple, efficient, and lays the foundation for more advanced exception handling features in future sprints. All 223 tests pass, confirming the stability and correctness of the implementation.
