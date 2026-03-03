# Adhoc: Fix Import Error Line Reporting — 20260302.2226

## Summary
Fixed import error messages to report the actual line number from the imported module instead of the line of the `import` statement in the calling file. Both parse errors and runtime errors in imported modules now include the module filename and the correct line number.

## Files Changed
- lyric/interpreter.py — Updated parse and execution error handlers in `_evaluate_import_statement()` to use the original exception's line/column info

## Reason
Previously, `import utils` on line 2 would report "line 2" for any error in `utils.ly`, making it impossible to locate the actual problem in the imported module.

## Git Commit Hash
`TBD` - Adhoc Import Error Line Reporting Fix

## Status
✅ Completed
