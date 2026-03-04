# Adhoc: Fix Import Error Line Reporting — Task Summary

## Summary
Fixed import error messages to report the correct line number from the imported module file, not the `import` statement line in the calling file.

## Key Accomplishments
- Parse errors now show: `Error parsing module 'utils' (utils.ly line 8): ...`
- Runtime errors now show: `Error in module 'utils' (utils.ly line 5): ...`
- Full suite 1241/1241 pass

## Files Modified
- lyric/interpreter.py — Updated error handlers in `_evaluate_import_statement()`

## Status
✅ Completed
