# Bugfix 1 — 20260226.1814

## Summary
Fixed `type()` built-in returning `"pyobject"` for `arr` and `map` values. Added `ArrObject` and `MapObject` checks in `type_builtin` before the generic `pyobject` fallback, using a lazy import to avoid circular import issues.

## Files Changed
- `lyric/runtime.py` — Added `ArrObject`/`MapObject` detection in `type_builtin`; now returns `"arr"` and `"map"` respectively

## Reason
Arrays declared as `arr` in Lyric are stored internally as `ArrObject` instances (not plain Python `list`), so they fell through to the `"pyobject"` catch-all. The same issue existed for `map` / `MapObject`.

## Git Commit Hash
`TBD` - Bugfix1: Fix type() returning pyobject for arr and map values

## Status
✅ Completed
