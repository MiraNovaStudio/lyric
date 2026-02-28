# Sprint 10 Task 3 — Function Definition Syntax Update

## Task
Update function definition syntax to remove the redundant `TYPE def funcname()` form.

## Key Accomplishments
- **Parser updated:** Both `_parse_statement()` and `_parse_func_def()` in `lyric/parser.py`
  now raise a descriptive `ParseError` when `TYPE def funcname()` is encountered, guiding
  the user to the correct alternatives (`TYPE funcname()` or `def funcname()`).
- **Existing tests updated:**
  - `test_function_syntax.py` — `test_old_syntax_still_works` replaced by `test_old_syntax_rejected`
  - `test_arr_type.py` — `arr def get_list()` updated to `arr get_list()`
  - `test_map_type.py` — `map def get_dict()` updated to `map get_dict()`
- **New test file created:** `lyric/tests/core-0.9.0/test_function_def_syntax.py`
  with 9 positive tests (valid syntax) and 7 negative tests (old syntax rejected).
- **All 1084 tests pass.**

## Files Created/Modified
| File | Change |
|------|--------|
| `lyric/parser.py` | Replace old-style parse path with explicit ParseError in two locations |
| `lyric/tests/core-0.7.0/test_function_syntax.py` | Flip old-syntax test to rejection test |
| `lyric/tests/core-0.7.0/test_arr_type.py` | Update `arr def` → `arr` syntax |
| `lyric/tests/core-0.7.0/test_map_type.py` | Update `map def` → `map` syntax |
| `lyric/tests/core-0.9.0/test_function_def_syntax.py` | New comprehensive test file |
| `nova/changelog/20260225/2001-CHANGELOG.md` | Changelog entry |

## Status
✅ Completed

## Reference
See `nova/changelog/20260225/2001-CHANGELOG.md` for full details.
