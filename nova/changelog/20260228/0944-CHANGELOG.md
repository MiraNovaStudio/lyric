# Sprint10 Task4 — 20260228.0944

## Summary
Added a module whitelist for `importpy` in Lyric. Non-whitelisted, non-blacklisted modules are now blocked by default. Added `--unsafe` CLI flag to allow importing non-whitelisted modules at runtime. Added `--blacklist` and `--whitelist` CLI flags to print the respective module lists. Updated two older tests that checked for the old "cannot import" message which is now superseded by the whitelist error.

## Files Changed
- `lyric/pyproxy.py` — Added `WHITELISTED_MODULES` frozenset (`math`, `time`, `datetime`, `os`, `sys`), `_unsafe_mode` global, `set_unsafe_mode()`, `is_unsafe_mode()`, and whitelist enforcement in `PyModuleProxy.__init__`
- `lyric/cli.py` — Added `--blacklist` and `--whitelist` top-level commands; added `--unsafe` flag activation in `run` and shorthand `.ly` branches; updated help text
- `lyric/tests/core-0.9.0/test_importpy_whitelist.py` — New: unit tests for whitelist membership, whitelisted imports, blocked non-whitelisted imports, --unsafe bypass, blacklist still enforced with --unsafe
- `lyric/tests/core-0.3.4/test_pyobject_integration.py` — Updated two assertions to use generic "ImportError + module name" checks instead of the old exact "cannot import" message (now superseded by whitelist error)

## Reason
Task 4 of the Sprint 10 plan: establish a known-safe whitelist so only vetted modules work with `importpy` by default, with an explicit escape hatch (`--unsafe`) for advanced users who need unlisted modules.

## Git Commit Hash
`TBD` - Sprint10 Task4 Implementation

## Status
✅ Completed
