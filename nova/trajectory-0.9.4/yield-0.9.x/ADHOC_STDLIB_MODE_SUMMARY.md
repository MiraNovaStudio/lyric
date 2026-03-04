# Adhoc: stdlib_mode importpy whitelist bypass

## Summary
Implemented `_stdlib_mode` flag in pyproxy.py that allows Lyric's standard
library to import any non-blacklisted Python module without requiring the
`--unsafe` flag or whitelist membership. The interpreter sets this flag
while loading stdlib `.ly` files and resets it afterward via try/finally.

## Key Accomplishments
- Added `_stdlib_mode` flag with `set_stdlib_mode()`/`is_stdlib_mode()` to pyproxy.py
- Updated whitelist check: bypassed when `_stdlib_mode` is True, blacklist still enforced
- Added `is_stdlib` parameter to `_load_module_file()` in interpreter.py
- All 3 call sites for reserved module loading now pass `is_stdlib=is_reserved`
- Fixed existing bug: `importpy glob` in `lyric.ly` was not whitelisted

## Files Created/Modified
- `lyric/pyproxy.py` — stdlib_mode flag and helpers
- `lyric/interpreter.py` — is_stdlib parameter on `_load_module_file()`
- `lyric/tests/core-0.9.0/test_importpy_stdlib_mode.py` — 12 new tests

## Status
✅ Completed — 1325/1325 tests passing

## Changelog
See `nova/changelog/20260303/2212-CHANGELOG.md`
