# Sprint 2 — Control Flow, Error Handling, and Class Support

**Project:** Lyric Programming Language  
**Version Target:** 0.0.3  
**Owner:** Michael Stone  
**Architect:** ChatGPT  
**Engineer:** Claude  
**Duration:** 1 Week  

## Objective

This sprint will expand the Lyric language interpreter to handle advanced control flow, error reporting with line numbers, and the first stage of class support using the `+++` syntax. It will also refine CLI behavior and test coverage. By the end of this sprint, Lyric should be capable of executing nested control structures, reporting clear syntax and runtime errors, and parsing simple class containers with methods and attributes.

## Task 1 — Nested Control Flow

**Goal:** Extend the parser and interpreter to correctly handle nested if, else, end, and given, done blocks.

### Work:
- Update parser to support nested block tracking and recursive descent through conditionals and loops.
- Verify that nested indentation or block closings do not break existing flat structures.
- Interpreter must correctly maintain scope for nested control flow.

### Acceptance Criteria:
- **A1)** A Lyric program containing nested if and given blocks executes correctly.
- **A2)** Example: an if statement inside a loop and a loop inside an if both work.
- **A3)** The output matches expected logical results without raising structure errors.

## Task 2 — Boolean and Comparison Operations

**Goal:** Implement proper boolean logic evaluation for conditionals and loops.

### Work:
- Add evaluation of operators `==`, `!=`, `<`, `<=`, `>`, `>=`, and logical operators `and`, `or`, `not`.
- Ensure truthiness rules for strings, numbers, and None values are respected.
- Extend parser expression grammar to support these operators with correct precedence.

### Acceptance Criteria:
- **A4)** All comparison and logical operators function as expected.
- **A5)** If/else and given blocks behave consistently with boolean conditions.
- **A6)** Example test passes for evaluating `range(3)` and numeric comparisons.

## Task 3 — Error Reporting System

**Goal:** Introduce consistent error handling with clear messages and line number references.

### Work:
- Expand `errors.py` with classes for `SyntaxErrorLyric`, `RuntimeErrorLyric`, and `NameErrorLyric`.
- Parser must raise `SyntaxErrorLyric` on unexpected tokens or incomplete blocks.
- Interpreter must raise `RuntimeErrorLyric` when undefined variables or functions are used.
- Each error should include file name and line number from token data.
- CLI should catch and print readable error messages instead of Python tracebacks.

### Acceptance Criteria:
- **A7)** Invalid syntax such as missing `end` or `done` triggers `SyntaxErrorLyric` with correct line.
- **A8)** Referencing an undefined variable triggers `RuntimeErrorLyric`.
- **A9)** CLI output shows "Error [line x]: description" format for all user-visible errors.

## Task 4 — Class Parsing and Structure

**Goal:** Extend parser to support class definitions using the `+++` terminator.

### Work:
- Parser recognizes `"class Name:"` followed by statements until `+++`.
- Allowed statements inside class are assignments and function definitions only.
- AST includes `ClassNode` with name and members.
- Add parser test for nested function definitions inside a class.

### Acceptance Criteria:
- **A10)** Class definitions parse successfully without breaking program structure.
- **A11)** Parser test passes for:
  ```lyric
  class Player:
      name = "Guest"
      def greet() { print("Hello,", self.name) }
  +++
  ```

## Task 5 — Class Interpretation (Stub Implementation)

**Goal:** Introduce minimal runtime behavior for classes.

### Work:
- Interpreter registers classes as callable constructors that create object dictionaries.
- Support attribute access and method invocation syntax `self.attribute` and `self.method()`.
- Store instance attributes when class methods assign `self.x`.
- Support instantiation syntax like `player = Player()`.

### Acceptance Criteria:
- **A12)** Defining a class and creating an instance works without runtime errors.
- **A13)** Calling an instance method prints correct output and accesses attributes correctly.
- **A14)** Instance variables are stored in each object dictionary.

## Task 6 — Runtime Enhancements

**Goal:** Improve built-in library and environment safety.

### Work:
- Add `isinstance` built-in function for checking type names.
- Add `type()` built-in returning the object's class name or Python type.
- Add a safe print for None and compound types.
- Expand `range()` to handle `range(start, stop)`.

### Acceptance Criteria:
- **A15)** `isinstance` and `type` functions return correct results.
- **A16)** `range(start, stop)` produces correct sequence.
- **A17)** `print()` displays None and lists gracefully.

## Task 7 — Test Suite Expansion

**Goal:** Add new tests covering all Sprint 2 features.

### Work:
- Add new files in `tests/examples/`:
  - `nested_flow.ly`
  - `class_test.ly`
  - `error_demo.ly`
- Add new unit tests under `tests/test_interpreter.py` for class instantiation, nested control flow, and error reporting.
- Add integration tests to verify CLI error messages.

### Acceptance Criteria:
- **A18)** All new tests pass successfully.
- **A19)** CLI run of `class_test.ly` prints correct greeting.
- **A20)** CLI run of `error_demo.ly` produces expected error messages without Python tracebacks.

## Task 8 — Code Quality and Documentation

**Goal:** Maintain readability and ensure code meets style and documentation standards.

### Work:
- Run `flake8` on all modules and fix warnings.
- Add docstrings to new interpreter and parser functions.
- Update `README.md` to include class syntax example.
- Update `CHANGELOG.md` with version 0.0.3 section when complete.

### Acceptance Criteria:
- **A21)** No flake8 critical errors remain.
- **A22)** Docstrings describe the purpose of each new class and function.
- **A23)** CHANGELOG and README are updated correctly before tag.

## Definition of Done for Sprint 2

- All tasks from 1 through 8 completed and verified.
- Lyric programs with nested control flow and simple class structures execute correctly.
- Errors are reported cleanly with file name and line number.
- All tests pass with pytest.
- The code is tagged as `dev-0.0.3` and prepared for Sprint 3 (type system and extended runtime).