# Adhoc: Add .len() Method for Strings — Task Summary

## Summary
Added `.len()` method for `str` type by inserting a string-specific handler in the interpreter's method dispatch cascade, between DskObject and the generic Python fallback.

## Key Accomplishments
- `str` values now support `.len()` returning the string length
- All existing Python string methods (`.upper()`, `.lower()`, `.split()`, `.strip()`, `.replace()`, etc.) continue to work
- 9 new tests all passing, full suite 1237/1237 pass

## Files Created
- lyric/tests/core-0.9.0/test_str_len.py — 9 tests
- nova/changelog/20260302/2101-CHANGELOG.md — Changelog

## Files Modified
- lyric/interpreter.py — String handler in method dispatch

## Status
✅ Completed

## Reference
See nova/changelog/20260302/2101-CHANGELOG.md for full details.
