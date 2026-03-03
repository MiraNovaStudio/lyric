# Adhoc: Improve Parser Error Messages — Task Summary

## Summary
Replaced generic "Expected expression" error with context-aware hints for common mistakes.

## Example Improvements
- `{` after class name → "Classes use '+++' as the closing delimiter, not braces."
- Mismatched `}` → "Check for mismatched braces in your function or method body."
- `=` in expression → "Did you mean '==' for comparison?"
- Unknown token → Shows the actual token value and type with guidance
- Full suite 1241/1241 pass

## Files Modified
- lyric/parser.py — Hint table in `_parse_primary()`

## Status
✅ Completed
