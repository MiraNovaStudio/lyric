# Adhoc: Fix obj.member[key] assignment for Python proxy objects

## Summary
Fixed the `obj.member[key] = value` assignment code path in the interpreter
to resolve members via `hasattr`/`getattr` when the object is not a `dict`.
This fixes `os.environ[name] = value` used by `lyric.set()` in the stdlib.

## Key Accomplishments
- Added `elif hasattr(obj, member_name)` fallback in `_evaluate_assignment()`
- `lyric.set()` now works correctly
- Updated `test_lyric.ly` — all 21 stdlib functions now PASS (0 SKIP)

## Files Created/Modified
- `lyric/interpreter.py` — member+index assignment fix
- `lyric/tests/lib/test_lyric.ly` — removed SKIP markers

## Status
✅ Completed — 1325/1325 pytest tests passing, stdlib test all PASS

## Changelog
See `nova/changelog/20260303/2230-CHANGELOG.md`
