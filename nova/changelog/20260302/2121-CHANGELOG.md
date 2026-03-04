# Adhoc: Reserve Import Names for Standard Library — 20260302.2121

## Summary
Reserved the module names `lyric`, `lyrical`, and `ly` (including future `ly.*` submodules) for the Lyric standard library planned for version 1.2.0. Attempting to `import` any of these names now raises a clear error message directing the user to choose a different module name.

## Files Changed
- lyric/interpreter.py — Added reserved name check at the top of `_evaluate_import_statement()`
- lyric/tests/core-0.9.0/test_reserved_imports.py — New test file with 4 tests

## Reason
Prevent user-created modules from colliding with future standard library names. The `ly.*` dotted import pattern will be enforced once dotted import syntax is implemented alongside the standard library.

## Git Commit Hash
`TBD` - Adhoc Reserved Import Names

## Status
✅ Completed
