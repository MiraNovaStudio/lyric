# Sprint10 Task1.1 — 20260224.1840

## Summary
Expanded the `sys` attribute blacklist from 2 entries to 9, covering all CPython
frame, trace, profile, reference-counting, and audit-hook APIs. Also updated the
git commit directive in CLAUDE.md from `git add *` to `git add .`.

## Files Changed
- `lyric/pyproxy.py` — Added 7 new entries to `BLACKLISTED_ATTRIBUTES['sys']`:
  `gettrace`, `getprofile`, `_getframe`, `_current_frames`, `getrefcount`,
  `addaudithook`, `exc_info` (with inline comments explaining each)
- `lyric/tests/core-0.9.0/test_importpy_blacklist.py` — Added 9 membership tests
  and 7 runtime error tests for the new blacklisted attributes
- `CLAUDE.md` — Changed `git add *` to `git add .` in Git Commit Format section

## Reason
`_getframe` and `_current_frames` expose live CPython frame objects directly.
`getrefcount` exposes reference-counting internals (was in the original sprint plan).
`gettrace`/`getprofile` are inconsistent to leave open when their setters are blocked.
`addaudithook` installs a permanent process-wide hook that can observe all Python
operations including the Lyric interpreter internals. `exc_info` returns a traceback
object containing frame references.

## Git Commit Hash
`TBD` - Sprint10 Task1.1 Implementation

## Status
✅ Completed
