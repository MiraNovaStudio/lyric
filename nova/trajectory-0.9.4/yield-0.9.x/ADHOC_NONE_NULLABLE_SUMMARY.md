# Adhoc: None as First-Class Nullable Value

## Summary
Made None a valid value for all typed variables in Lyric. Any type (int, str, flt, arr, map, tup, god, bin, etc.) can now hold None. The type annotation declares what the variable holds when not null; None means "declared but null."

## Key Accomplishments
- `int x = None`, `str s = None`, `map m = None`, etc. all work
- Variables can be reassigned between None and typed values freely
- `if x == None:` conditional checks work correctly
- Typed function parameters accept None
- Typed functions can return None (explicit or implicit)
- Operations on None (arithmetic, etc.) still fail with clear error messages
- 24 new tests, all 1313 tests pass

## Files Created/Modified
- `lyric/interpreter.py` — 5 surgical edits to type compatibility and parameter/return checking
- `lyric/tests/core-0.9.0/test_none_nullable.py` — New (24 tests)
- `lyric/tests/core-0.3.0/test_typed_parameters.py` — Updated assertion
- `lyric/tests/core-0.5.0/test_bin_type.py` — Updated for nullable
- `lyric/tests/core-0.5.0/test_god_type.py` — Updated for nullable
- `lyric/tests/core-0.6.0/test_constructor_recognition.py` — Updated for nullable

## Status
✅ Completed

## Changelog
See `nova/changelog/20260303/2143-CHANGELOG.md`
