# Bugfix 2 — 20260226.1928

## Summary
Added the modulus operator `%` to Lyric. Both operands must be `int`; the result is `int`. Division by zero raises a `ZeroDivisionErrorLyric`. Also updated the CLI version test regex to accept four-segment versions (X.Y.Z.W).

## Files Changed
- `lyric/lexer.py` — Added `%` to `SINGLE_CHARS` and mapped it to `PERCENT` in `OPERATOR_TYPES`
- `lyric/parser.py` — Added `PERCENT` to `_parse_factor()` match (same precedence as `*` and `/`)
- `lyric/interpreter.py` — Added `%` case in `_evaluate_binary_operation` with int-only enforcement and zero-divisor check
- `lyric/tests/core-0.1.0/test_cli.py` — Updated version regex to allow four-segment version strings

## Reason
The modulus operator was never implemented in Lyric. The CLI version test regex was too narrow after the 0.9.3.1 bump.

## Git Commit Hash
`TBD` - Bugfix2: Add modulus operator %

## Status
✅ Completed
