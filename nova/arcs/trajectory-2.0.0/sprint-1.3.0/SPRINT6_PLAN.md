# Sprint 6 — Runtime Stability and Error Handling

**Target Version:** 0.7.0

## Sprint Goal

Improve Lyric's runtime stability, finalize scope and type enforcement, and introduce the new exception-handling system using the keywords `try`, `catch`, `finally`, and `fade`.

## Task 1 — Nested Scope Resolution

Ensure variables declared inside inner blocks shadow outer ones correctly and restore the parent scope when the block exits.

**Implementation:**
- Add lookup logic that searches local → enclosing → global scopes.
- Confirm function scopes and nested try/catch scopes behave independently.

### Acceptance Criteria:
- Inner-scope variables do not overwrite outer-scope values.
- Variables declared inside try/catch or functions are destroyed when the block closes.
- Variable lookups resolve in correct scope order.
- Shadowing confirmed through tests and printed output.

## Task 2 — Type Enforcement Verification

Verify that declared types (`int`, `flt`, `str`, `rex`, `god`, `var`) are enforced at runtime.

**Requirements:**
- Assignments violating declared types must raise a `TypeError`.
- Return types from functions must match declared type signatures.

### Acceptance Criteria:
- Type errors produce clear messages showing variable name, expected type, and actual type.
- Return-type mismatches trigger errors.
- No silent type coercions unless explicitly handled.
- Unit tests pass for mixed type assignment and function returns.

## Task 3 — Implement Try / Catch / Finally / Fade Syntax

Add structured exception handling using the following grammar:

```lyric
try:
    <code block>
catch:
    <code block>
finally:
    <code block>
fade
```

**Key Points:**
- The `fade` keyword terminates the entire exception block.
- Both `catch` and `finally` are optional.
- The interpreter executes `catch` when an error occurs in `try`, then executes `finally` (if present), and ends the block on `fade`.

**Example:**
```lyric
try:
    int x = 10
    x = "bad"
catch:
    print("Type error caught")
finally:
    print("Cleanup complete")
fade
```

### Acceptance Criteria:
- Parser recognizes `try`, `catch`, `finally`, and `fade` as block keywords.
- Runtime correctly executes `try`, optional `catch`, optional `finally`, then resumes after `fade`.
- Nested try blocks handled correctly.
- `fade` required to close any try/catch/finally sequence.
- Errors raised in `catch` or `finally` propagate outward unless handled.

## Task 4 — Add Raise Keyword and Error Hierarchy

Implement a `raise` keyword for throwing exceptions.

**Implementation:**
- Create a minimal built-in hierarchy: `Error` (base), `TypeError`, `ValueError`, `NameError`, `RuntimeError`.
- Allow `raise "message"` for simple text errors or `raise TypeError("message")` for typed errors.
- Unhandled errors should bubble up to CLI output.

### Acceptance Criteria:
- `raise` keyword functional in any code block.
- Errors can be caught with `catch` or remain unhandled to top level.
- Error output includes error type, message, line number, and file.
- Built-in error classes available from the global scope.

## Task 5 — CLI Error Integration and Runtime Stability

Integrate exception handling with the `lyric run` command.

**Requirements:**
- Unhandled errors must display formatted output and exit with non-zero status.
- Ensure interpreter never crashes with raw Python tracebacks.

### Acceptance Criteria:
- CLI prints readable "Traceback" style messages for unhandled errors.
- Exit code ≠ 0 on unhandled error.
- All exceptions within CLI context handled gracefully.

## Task 6 — Documentation and Changelog

Update `README.md` and `CHANGELOG.md` to document:

**Content:**
- New `try` / `catch` / `finally` / `fade` syntax.
- `raise` keyword and error hierarchy.
- Examples showing nested exception handling and `fade` terminator.
- Include note that `fade` is used exclusively for error flow blocks.

### Acceptance Criteria:
- All new keywords described with examples in README.
- CHANGELOG entry added for version 0.2.1.

## Definition of Done

- Nested scope resolution stable.
- Type enforcement confirmed.
- `try` / `catch` / `finally` / `fade` syntax fully implemented and tested.
- `raise` keyword and error hierarchy functional.
- CLI prints clean error output and handles exceptions gracefully.
- Documentation and CHANGELOG updated.
