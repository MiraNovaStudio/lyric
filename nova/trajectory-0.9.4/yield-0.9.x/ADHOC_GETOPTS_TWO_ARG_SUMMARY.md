# Adhoc: Refactor getopts() to two-argument API

## Summary
Refactored `getopts()` built-in to always require exactly two arguments: `getopts(short, long)` where either can be `None`.

## Key Accomplishments
- `getopts("v", "verbose")` — matches `-v` or `--verbose`
- `getopts(None, "verbose")` — long-only option
- `getopts("v", None)` — short-only option
- Updated all test files to use the new two-arg format
- All 1187 tests pass

## Files Modified
- `lyric/runtime.py` — `getopts_builtin(short_option, long_option)`
- `lyric/cli.py` — `_check_for_auto_help()` parses two-arg getopts calls
- `lyric/tests/core-0.8.0/test_getopts.py` — all getopts calls updated
- `lyric/tests/core-0.8.0/test_auto_help.py` — all getopts calls updated
- `lyric/tests/core-0.8.0/test_cli_args.py` — all getopts calls updated

## Status
✅ Completed

## Changelog
See `nova/changelog/20260301/2108-CHANGELOG.md`
