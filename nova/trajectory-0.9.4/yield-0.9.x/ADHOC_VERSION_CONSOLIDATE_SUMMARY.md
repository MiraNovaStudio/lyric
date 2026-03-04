# Adhoc: Consolidate __version__ — Summary

## Task
Remove duplicate `__version__` from `cli.py`, import from `__init__.py` instead.

## Key Accomplishments
- Single source of truth for version in `lyric/__init__.py`
- `lyric --version` still works correctly
- All 1180 tests pass

## Status
✅ Completed

See `nova/changelog/20260228/2259-CHANGELOG.md` for full details.
