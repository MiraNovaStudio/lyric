# Adhoc: Improve Parser "Expected Expression" Error Messages — 20260302.2229

## Summary
Replaced the generic "Expected expression" parse error with context-aware messages that tell the user what went wrong and how to fix it. The parser now provides specific hints for common mistakes like using `{` after a class name, mismatched braces, unexpected block terminators, and using `=` instead of `==`.

## Files Changed
- lyric/parser.py — Replaced generic error at end of `_parse_primary()` with a hint table for known token types and a descriptive fallback showing the actual unexpected token

## Reason
The previous "Expected expression" message gave no indication of what was wrong or how to fix it, making debugging difficult especially in imported modules.

## Git Commit Hash
`TBD` - Adhoc Parser Error Message Improvement

## Status
✅ Completed
