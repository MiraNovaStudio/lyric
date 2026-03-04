# Adhoc: Add .len() Method for Strings — 20260302.2101

## Summary
Added `.len()` method support for `str` values in Lyric. Python strings use the built-in `len()` function rather than a `.len()` method, so this was not available through the generic Python fallback path. Added an explicit string handler in the interpreter's method dispatch that provides `.len()` while preserving access to all native Python string methods (`.upper()`, `.lower()`, `.split()`, `.strip()`, `.replace()`, etc.).

## Files Changed
- lyric/interpreter.py — Added `isinstance(current_obj, str)` handler in method dispatch cascade with `.len()` support
- lyric/tests/core-0.9.0/test_str_len.py — New test file with 9 tests covering .len(), existing Python string methods, and error handling

## Reason
Lyric's `arr` and `map` types already support `.len()` as a method call. Strings should follow the same convention for consistency, but Python strings lack a `.len()` method natively.

## Git Commit Hash
`TBD` - Adhoc String .len() Implementation

## Status
✅ Completed
