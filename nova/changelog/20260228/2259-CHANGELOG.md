# Adhoc: Consolidate __version__ to single source — 20260228.2259

## Summary
Removed duplicate `__version__` definition from `cli.py`. It now imports from `lyric/__init__.py` as the single source of truth.

## Files Changed
- lyric/cli.py — Replaced hardcoded `__version__ = "0.9.6"` with `from lyric import __version__`

## Reason
Version was defined in both `__init__.py` and `cli.py`, creating a maintenance burden where both files needed updating on every version bump. Now only `__init__.py` and `pyproject.toml` need updating.

## Git Commit Hash
`TBD` - Adhoc: Consolidate __version__

## Status
✅ Completed
