# Sprint10 Task1 (fix) — 20260224.1811

## Summary
Corrected the `sys` module blacklist: `sys` was fully blacklisted, but most of it is
valid and useful in Lyric. Only `sys.settrace` and `sys.setprofile` are dangerous
(they hook into the CPython trace/profile machinery). Moved `sys` out of
`BLACKLISTED_MODULES` and into a new `BLACKLISTED_ATTRIBUTES` dict that blocks
individual attributes on otherwise-allowed modules.

## Files Changed
- `lyric/pyproxy.py` — Removed `sys` from `BLACKLISTED_MODULES`; added `BLACKLISTED_ATTRIBUTES` dict (`sys` → `{settrace, setprofile}`); added attribute-level blacklist check in `PyModuleProxy.__getattr__`
- `lyric/tests/core-0.9.0/test_importpy_blacklist.py` — Replaced `sys` module-level tests with attribute-level tests; added regression tests confirming `sys.version` and `sys.platform` remain accessible

## Reason
`sys.settrace` and `sys.setprofile` hook into CPython's trace/profile mechanism and
are incompatible with the Lyric runtime. The rest of `sys` (version info, platform,
argv, path, etc.) is safe and useful.

## Git Commit Hash
`TBD` - Sprint10 Task1 fix

## Status
✅ Completed
