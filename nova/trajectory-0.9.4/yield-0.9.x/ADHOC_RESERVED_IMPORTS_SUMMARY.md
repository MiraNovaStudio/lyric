# Adhoc: Reserve Import Names for Standard Library — Task Summary

## Summary
Reserved `lyric`, `lyrical`, and `ly` as import names for the future standard library (1.2.0). The `ly.*` dotted pattern will be enforced when dotted import syntax is added.

## Key Accomplishments
- `import lyric`, `import lyrical`, `import ly` all raise RuntimeErrorLyric with a clear message
- Error message references the 1.2.0 version target
- 4 new tests, full suite 1241/1241 pass

## Files Created
- lyric/tests/core-0.9.0/test_reserved_imports.py — 4 tests
- nova/changelog/20260302/2121-CHANGELOG.md — Changelog

## Files Modified
- lyric/interpreter.py — Reserved name check in import handler

## Status
✅ Completed
