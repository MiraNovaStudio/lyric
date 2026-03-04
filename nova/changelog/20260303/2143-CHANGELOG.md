# Adhoc — None as First-Class Nullable Value — 20260303.2143

## Summary
All typed variables can now be assigned None. `None` acts as null in Lyric — the type annotation declares what a variable holds when it's not null, but `None` is always a valid value. Functions can return None regardless of declared return type, and typed parameters accept None.

## Files Changed
- lyric/interpreter.py — Added `if value is None: return True` to both `_is_type_compatible` methods (lines ~948 and ~1647); removed explicit None rejection in `_call_func_def` and `_call_method` parameter checks; removed implicit None return rejection for typed functions
- lyric/tests/core-0.9.0/test_none_nullable.py — New test file with 24 tests: declarations (int/str/flt/arr/map/tup/god/bin = None), reassignment (None↔value), comparisons (== None, != None), conditionals, function params, function returns, operation errors, falsy check
- lyric/tests/core-0.3.0/test_typed_parameters.py — Updated missing param test: None now passes type check, error surfaces at arithmetic
- lyric/tests/core-0.5.0/test_bin_type.py — Updated: bin accepts None (nullable)
- lyric/tests/core-0.5.0/test_god_type.py — Updated: god accepts None (nullable)
- lyric/tests/core-0.6.0/test_constructor_recognition.py — Updated: missing constructor param gets None instead of type error

## Reason
Functions that don't return a value return None, and there are legitimate cases where typed functions should return None (e.g., file not found). Making None a universal nullable value for all types is fundamental to practical Lyric programming.

## Git Commit Hash
`TBD` - Adhoc: None as first-class nullable value for all types

## Status
✅ Completed
