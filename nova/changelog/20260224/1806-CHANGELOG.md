# Sprint10 Task1 — 20260224.1806

## Summary
Added a blacklist of Python modules that rely on CPython bytecode, frames, object identity, or interpreter internals. Attempting to `importpy` any blacklisted module now raises a `RuntimeErrorLyric` with a clear explanation of why the module is blocked in Lyric.

## Files Changed
- `lyric/pyproxy.py` — Added `BLACKLISTED_MODULES` frozenset and `_BLACKLIST_REASON` constant; added blacklist check in `PyModuleProxy.__init__` before `__import__`
- `lyric/tests/core-0.9.0/__init__.py` — New test package for Sprint 10
- `lyric/tests/core-0.9.0/test_importpy_blacklist.py` — 43 tests covering blacklist membership, runtime error raising, error message content, and regression tests for allowed modules

## Reason
Modules that expose CPython internals (bytecode, frame objects, object identity, garbage collector state, etc.) are incompatible with the Lyric runtime model. Blacklisting them gives users a clear error rather than undefined or misleading behaviour.

## Git Commit Hash
`TBD` - Sprint10 Task1 Implementation

## Status
✅ Completed
