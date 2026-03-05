# Bugfixes — 20260304.1829

## Summary
Three REPL and runtime fixes:
1. **Strict string concatenation**: The `+` operator no longer auto-coerces mixed types (e.g., `"hello" + 5`). Both operands must be strings, or a `TypeErrorLyric` is raised with guidance to use `str()`.
2. **Ctrl+D exits REPL immediately on Windows**: Replaced `input()` with `msvcrt.getwch()`-based raw keystroke reading on Windows so Ctrl+D triggers EOF without requiring Enter. Falls back to `input()` on Unix.
3. **One-line function definitions in REPL**: Fixed double-counting of block depth when `def`/`class`/etc. keywords appear on the same line as `{ }` braces, so `def hello() { print "hi" }` executes immediately.

## Files Changed
- `lyric/interpreter.py` — Changed `+` operator to require both operands be strings for concatenation; raises `TypeErrorLyric` for mixed types
- `lyric/cli.py` — Added `_repl_input()` using `msvcrt.getwch()` for immediate Ctrl+D on Windows; fixed block depth counting for brace-style one-liners; updated welcome message
- `lyric/tests/core-0.3.0/test_runtime_safety.py` — Updated 3 tests to expect `TypeErrorLyric` instead of auto-coercion for `int + str`

## Reason
- String auto-coercion masked type errors; explicit `str()` conversion is safer and clearer.
- Ctrl+D is the standard Unix EOF signal; Windows `input()` only recognises Ctrl+Z, so raw keystroke reading via `msvcrt` was needed.
- One-line function definitions are a common REPL pattern and should execute immediately.

## Git Commit Hash
`TBD`

## Status
✅ Completed
