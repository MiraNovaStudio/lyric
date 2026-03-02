# Adhoc — 20260301.2108

## Summary
Refactored `getopts()` to always require exactly two arguments: `getopts(short, long)` where either can be `None`. This replaces the previous variadic API. Updated all test files (`test_getopts.py`, `test_auto_help.py`, `test_cli_args.py`) to use the new two-argument format.

## Files Changed
- lyric/runtime.py — Changed `getopts_builtin()` from variadic `*args` to `(short_option, long_option)` with exactly two positional parameters
- lyric/cli.py — Updated `_check_for_auto_help()` to parse two-argument `getopts(short, long)` calls and display paired short/long options in auto-help
- lyric/tests/core-0.8.0/test_getopts.py — Rewrote all getopts calls to two-arg format; added tests for `getopts(None, "verbose")`, `getopts("v", None)`, and alias tests
- lyric/tests/core-0.8.0/test_auto_help.py — Updated all getopts calls from single-arg to two-arg format (e.g., `getopts("a")` → `getopts("a", None)`)
- lyric/tests/core-0.8.0/test_cli_args.py — Updated all getopts calls from single-arg to two-arg format

## Reason
Standardize the `getopts()` API so the first argument is always the short option and the second is always the long option, making the intent explicit and enabling short/long aliases like `getopts("h", "help")`.

## Git Commit Hash
`TBD` - Adhoc getopts two-argument API

## Status
✅ Completed
