# Sprint10 Task3 — 20260225.2001

## Summary
Updated function definition syntax to eliminate the redundant `TYPE def funcname()` form.
Valid forms are now `TYPE funcname()` (typed) or `def funcname()` (untyped).
The old `int def add()` style now raises a descriptive `ParseError` with guidance
on the correct alternatives.

## Files Changed
- `lyric/parser.py` — Replaced the old-style `TYPE_OR_IDENT` + `DEF` branch in
  `_parse_statement()` and `_parse_func_def()` with explicit `ParseError` raises
  that include a helpful error message pointing users to the correct syntax.
- `lyric/tests/core-0.7.0/test_function_syntax.py` — Added `ParseError` import;
  renamed `test_old_syntax_still_works` to `test_old_syntax_rejected` and updated
  it to assert that `int def funcname()` raises `ParseError`.
- `lyric/tests/core-0.7.0/test_arr_type.py` — Updated `test_arr_in_function_return`
  from `arr def get_list()` to `arr get_list()` (new syntax).
- `lyric/tests/core-0.7.0/test_map_type.py` — Updated `test_map_in_function_return`
  from `map def get_dict()` to `map get_dict()` (new syntax).
- `lyric/tests/core-0.9.0/test_function_def_syntax.py` — New test file covering
  positive cases (typed and untyped functions) and negative cases (all `TYPE def`
  permutations rejected, helpful error message verified).

## Reason
`int def add()` was grammatically redundant — the type already implies a typed
function, so the `def` keyword is superfluous. Removing it simplifies the language
grammar and eliminates ambiguity.

## Git Commit Hash
`TBD` - Sprint10 Task3 Implementation

## Status
✅ Completed
