# Sprint 3 — Type System, Value Validation, and Advanced Runtime

**Project:** Lyric Programming Language  
**Version Target:** 0.3.0  
**Owner:** Michael (Aeonath)  
**Architect:** ChatGPT  
**Engineer:** Claude  
**Duration:** 1 Day  

## Objective

This sprint will focus on expanding Lyric's type system, improving value validation, and extending the runtime with enhanced data types and error safety. It will also include new tests, documentation updates, and refinements to class behavior introduced in Sprint 2.

The result should be a more stable and feature-complete interpreter capable of handling typed variables, stronger runtime enforcement, and cleaner error reporting.

## Task 1 — Type Declaration and Inference

**Goal:** Implement basic type tracking for variables and function returns.

### Work:

- Allow optional type declaration syntax in assignments and function parameters.
- Examples:
  ```lyric
  int x = 5
  str name = "hello"
  flt pi = 3.14
  var dynamic = "anything"
  def add(int a, int b) { return a + b }
  ```
- Store type metadata in the interpreter's environment.
- Implement runtime enforcement for type mismatches when enabled.
- Add simple type inference for obvious numeric and string assignments.
- **Type System Hierarchy:**
  - **Strict Types:** `int`, `str`, `flt` (with strict enforcement)
  - **Dynamic Type:** `var` (can hold any type, no restrictions)
  - **Future Types:** `rex` (regex), `bin`/`god` (boolean)

### Acceptance Criteria:

- **A1)** The interpreter correctly records and enforces type declarations for `int`, `str`, `flt`, and `var`.
- **A2)** Assigning a string to a variable declared as `int` raises a runtime error.
- **A3)** Functions with typed parameters enforce types when called.
- **A4)** Type inference assigns correct default types for literals.
- **A5)** `var` type accepts any value without type checking restrictions.
- **A6)** Explicit `var` declarations work: `var x = 5` assigns value without type restrictions.

## Task 2 — Return Statements and Function Values

**Goal:** Enable functions to return values and use them in expressions.

### Work:

- Add parser support for the return keyword.
- Interpreter must propagate return values to calling context.
- Allow expressions like `x = add(2,3)` and `print(add(2,3))`.

### Acceptance Criteria:

- **A5)** Functions can return values and assign them to variables.
- **A6)** `print(add(2,3))` outputs the correct numeric result.
- **A7)** Missing return defaults to None.

## Task 3 — Built-in Data Structures

**Goal:** Introduce lists and dictionaries as first-class types.

### Work:

- Extend lexer and parser to recognize list and dictionary literals.
- Example:
  ```lyric
  list_example = [1, 2, 3]
  dict_example = {"key": "value"}
  ```
- Interpreter supports indexing, appending, and key lookup.
- Add built-in functions `len()`, `append()`, `keys()`, and `values()`.

### Acceptance Criteria:

- **A8)** Lists and dictionaries can be created, accessed, and modified.
- **A9)** `append()` adds an item to a list.
- **A10)** `len()`, `keys()`, and `values()` return correct results.

## Task 4 — Class Enhancements and Self Behavior

**Goal:** Expand class system to support constructors and instance attribute initialization.

### Work:

- Support an optional `init()` method inside classes that runs on instance creation.
- Enable `self` access within methods to refer to instance variables.
- Allow calling methods through `instance.method()` syntax.
- Allow property assignment like `self.health = 100`.

### Acceptance Criteria:

- **A11)** Classes with `init()` initialize instance variables correctly.
- **A12)** Method calls using `instance.method()` work and print correct values.
- **A13)** Assigning and reading instance variables works correctly.

## Task 5 — Exception Handling

**Goal:** Add try, catch, finally, and fade support to the parser and interpreter.

### Work:

- Extend parser to handle try/catch/finally/fade blocks.
- **Lexer Changes**: Add `catch` and `fade` keywords, remove `except` keyword
- **AST Nodes**: Create `TryNode`, `CatchNode`, `FinallyNode`, `RaiseNode`
- **Syntax**: `try: ... catch: ... finally: ... fade` (no nested try/catch for this sprint)
- **Scope**: Each block (try, catch, finally) has isolated scope - no variable sharing
- **Exception Names**: Use Python-style names with Lyric postfix (e.g., `raise IndexErrorLyric`, `raise TypeErrorLyric`)
- **Raise Syntax**: Simple `raise ExceptionNameLyric` with no message support initially
- **Finally Behavior**: `finally` always executes after `catch` block; try without catch = syntax error
- Map to Python's built-in exceptions for error handling
- Support generic error handling (no specific error types initially)
- Integrate with existing Lyric error types (RuntimeErrorLyric, SyntaxErrorLyric, ParseError, etc.)
- example
```
def main() {
    var items = [1, 2, 3]

    try:
        var x = items[5]         # will raise IndexErrorLyric
        print("This won't run.")
    catch:
        print("An error occurred.")
    finally:
        print("Cleanup runs no matter what.")
    fade
}
```
- Interpreter catches runtime errors and executes catch or finally blocks accordingly.
- Errors raised manually with `raise` keyword are caught by catch (generic errors only).
- Existing Lyric error types (RuntimeErrorLyric, SyntaxErrorLyric, ParseError) should be catchable by try/catch blocks.

### Acceptance Criteria:

- **A14)** try/catch/finally blocks function correctly.
- **A15)** Raising a runtime error triggers the correct handler.
- **A16)** finally always executes regardless of exceptions.

## Task 6 — Runtime Safety and Error Messages

**Goal:** Improve runtime error clarity and introduce value type checking for function parameters.

### Work:

- Implement runtime type verification before function execution.
- Enhance all error messages to include filename, line number, and offending statement.
- Ensure consistent error categories for runtime, type, and attribute errors.

### Acceptance Criteria:

- **A17)** Errors show precise file and line references.
- **A18)** Calling a function with incorrect argument types raises a descriptive error.
- **A19)** No Python stack traces appear in user-facing output.

## Task 7 — Test Suite Expansion

**Goal:** Extend test coverage for all new Sprint 3 features.

### Work:

- Add new test files:
  - `type_tests.ly`
  - `list_dict_tests.ly`
  - `exception_tests.ly`
  - `class_init_tests.ly`
- Add corresponding pytest files to verify runtime and error outputs.
- Confirm all tests pass cleanly before tagging.

### Acceptance Criteria:

- **A20)** All new test files run successfully through the CLI.
- **A21)** pytest returns all tests passed.
- **A22)** All previously implemented features remain functional.

## Task 8 — Documentation and Version Update

**Goal:** Update project documentation to reflect the new version and features.

### Work:

- Update changelog with a new entry for version 0.3.0, summarizing all Sprint 3 changes.
- Verify README.md includes examples of:
  - Typed variables
  - Lists and dictionaries
  - Class with `init()`
  - try/except/finally usage
- Increment version numbers in pyproject.toml and cli.py to the final Sprint 3 version.

### Acceptance Criteria:

- **A23)** Changelog includes a section for the final Sprint 3 version with completed Sprint 3 notes.
- **A24)** README.md contains up-to-date examples and matches actual syntax.
- **A25)** Version output from `lyric --version` shows the final Sprint 3 version.

## Definition of Done for Sprint 3

### Final Goal:
- All tasks from 1 through 8 are implemented and verified.
- The Lyric interpreter supports typed variables, return statements, built-in data structures, constructors, and exception handling.
- All tests and examples execute successfully through the CLI.
- Changelog and README.md are updated to reflect final Sprint 3 version.
- Version numbers in the codebase are incremented to final Sprint 3 version.
- The code is committed and tagged as the final Sprint 3 version in the GitHub repository.