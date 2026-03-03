# Adhoc: Fix missing line number in 'in' operator error — 20260303.0133

## Summary
The `'in' requires a container` error was missing line/column information, producing a bare error without position context. Added `node.line` and `node.column` to the `TypeErrorLyric` raise.

## Files Changed
- lyric/interpreter.py — Added line/column args to the `'in' requires a container` error in `_evaluate_binary_operation()`

## Reason
Error messages should always include line numbers so users can locate the problem.

## Git Commit Hash
`TBD` - Adhoc Fix 'in' operator error line number

## Status
✅ Completed
