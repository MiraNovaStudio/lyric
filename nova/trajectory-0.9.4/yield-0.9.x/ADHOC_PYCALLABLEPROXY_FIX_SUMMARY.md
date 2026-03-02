# Adhoc: PyCallableProxy Attribute Access Fix

## Summary
Fixed a bug where `PyCallableProxy` did not forward attribute access to the underlying Python object. This caused selectively imported classes (e.g., `importpy datetime; datetime`) to fail when accessing class methods like `.now()`.

## Key Accomplishments
- Added `__getattr__` method to `PyCallableProxy` in `lyric/pyproxy.py`
- All 1180 tests pass
- `studio/pulse.ly` now works correctly with `importpy datetime; datetime`

## Files Modified
- `lyric/pyproxy.py` — Added `__getattr__` to `PyCallableProxy`

## Status
Completed

## Changelog
See `nova/changelog/20260301/2012-CHANGELOG.md`
