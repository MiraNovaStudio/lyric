# Adhoc: Generic Error Catch-All and Clean Exception Messages

## Summary
Made `catch Error as e` a true universal catch-all and cleaned up exception `__str__` so caught exceptions are silent unless explicitly printed.

## Key Accomplishments
- `Error` in EXCEPTION_TYPES now maps to `Exception` (was `LyricError`) — catches everything
- `RuntimeErrorLyric.__str__` returns clean message only (no "Runtime error:" prefix)
- CLI error handlers add their own formatting prefix for uncaught errors
- 3 existing tests updated to match new clean `str(e)` behavior
- All 1289 tests pass

## Files Created/Modified
- `lyric/errors.py` — `Error` → `Exception` mapping; clean `__str__`
- `lyric/cli.py` — CLI adds "Runtime error:" prefix itself
- `lyric/tests/core-0.3.4/test_pyobject_integration.py` — Updated assertion
- `lyric/tests/core-0.6.4/test_error_formatting.py` — Updated 2 assertions

## Status
✅ Completed

## Changelog
See `nova/changelog/20260303/2040-CHANGELOG.md`
