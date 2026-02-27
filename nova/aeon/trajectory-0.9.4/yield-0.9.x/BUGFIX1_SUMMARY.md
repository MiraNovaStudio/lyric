# Bugfix 1 Summary — type() returns pyobject for arr/map

## Issue
Calling `type()` on an `arr` value returned `"pyobject"` instead of `"arr"`. The same bug existed for `map` values.

**Reproduction:**
```lyric
arr items = [1, 2, 3]
print(type(items))  // printed: pyobject (bug)
                    // expected: arr
```

## Root Cause
`type_builtin` in `lyric/runtime.py` only checked for plain Python `list`, but Lyric arrays are stored as `ArrObject` instances. Since `ArrObject` is not a `list`, `bool`, `int`, `float`, `str`, or `None`, it fell through to the `"pyobject"` catch-all.

## Fix
Added explicit `ArrObject` and `MapObject` checks at the top of `type_builtin`, using a lazy `from lyric.interpreter import ArrObject, MapObject` import (consistent with the pattern used elsewhere in `runtime.py` to avoid circular imports).

## Key Accomplishments
- `type(arr_value)` now correctly returns `"arr"`
- `type(map_value)` now correctly returns `"map"`
- No test regressions — 1084 tests pass

## Files Modified
- `lyric/runtime.py` — `type_builtin` function

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260226/1814-CHANGELOG.md`
