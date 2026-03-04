# Adhoc — stdlib_mode importpy whitelist bypass — 20260303.2212

## Summary
Added `_stdlib_mode` flag to pyproxy.py so that Lyric's standard library
(.ly files loaded from `lib/`) can `importpy` any non-blacklisted Python
module without requiring the `--unsafe` flag or being in the whitelist.
Previously, `lyric.ly` used `importpy glob` which was not whitelisted,
causing failures when loading the stdlib without `--unsafe`.

## Files Changed
- `lyric/pyproxy.py` — Added `_stdlib_mode` flag, `set_stdlib_mode()`, `is_stdlib_mode()` helpers; updated whitelist check to bypass when `_stdlib_mode` is True
- `lyric/interpreter.py` — Added `is_stdlib=False` parameter to `_load_module_file()`; wraps stdlib module evaluation with `set_stdlib_mode(True/False)` using try/finally; passes `is_stdlib=is_reserved` from all three call sites
- `lyric/tests/core-0.9.0/test_importpy_stdlib_mode.py` — 12 new tests covering stdlib_mode flag basics, whitelist bypass, blacklist still enforced, state reset, and full `import lyric` loading

## Reason
The Lyric standard library (`lyric.ly`) is trusted code shipped with the
language itself. It should not be subject to the same whitelist restrictions
as user scripts. The blacklist is still enforced everywhere to prevent
importing CPython-internal modules regardless of context.

## Git Commit Hash
`TBD` - Adhoc stdlib_mode Implementation

## Status
✅ Completed
