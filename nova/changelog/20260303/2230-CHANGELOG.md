# Adhoc — Fix obj.member[key] assignment for Python proxy objects — 20260303.2230

## Summary
Fixed `obj.member[key] = value` assignment to work with PyModuleProxy and other
non-dict objects that support attribute access. Previously, the member+index
assignment code path only checked `isinstance(obj, dict)`, so `os.environ[name]`
assignments failed with "Cannot access member 'environ' of 'os'". Added a
`hasattr`/`getattr` fallback so any object with the named attribute can be
resolved. Also updated the stdlib test to remove SKIP markers on `set()`.

## Files Changed
- `lyric/interpreter.py` — Added `elif hasattr(obj, member_name)` fallback in `_evaluate_assignment()` member+index path (line ~1473)
- `lyric/tests/lib/test_lyric.ly` — Removed SKIP markers on `set()` tests, now fully PASS

## Reason
`lyric.set()` in the standard library uses `os.environ[name] = value`. The
interpreter's assignment handler only recognized `dict` objects for
`obj.member[key]` patterns, but `os` is a `PyModuleProxy` and `os.environ`
is a Python `os._Environ` mapping accessed via `getattr`. This fix enables
any object with attribute access to participate in member+index assignment.

## Git Commit Hash
`TBD` - Adhoc member+index assignment fix

## Status
✅ Completed
