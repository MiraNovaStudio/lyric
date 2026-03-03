# Adhoc: Remove Version Reference from Reserved Import Error — 20260302.2127

## Summary
Removed the "planned for 1.2.0" reference from the reserved import error message since the version target may change. The message now simply states the name is reserved for the Lyric standard library.

## Files Changed
- lyric/interpreter.py — Updated error message to remove version reference
- lyric/tests/core-0.9.0/test_reserved_imports.py — Updated test to match on "standard library" instead of "1.2.0"

## Reason
Version target for the standard library may change; the error message should not hardcode it.

## Git Commit Hash
`TBD` - Adhoc Reserved Import Error Message Fix

## Status
✅ Completed
