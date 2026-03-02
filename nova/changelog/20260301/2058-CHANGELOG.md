# Adhoc — 20260301.2058

## Summary
Added short + long option alias support to `getopts()`. Now supports `getopts("h", "help")` where the first argument is the short option and the second is the long option. Also added multi-character short option parsing (`-hc`) and improved auto-help detection to recognize multi-argument getopts calls.

## Files Changed
- lyric/runtime.py — Changed `getopts_builtin()` from single arg to variadic `*args`, loops through all names and returns first match
- lyric/cli.py — Updated `_parse_options()` to support multi-char short options (e.g., `-hc`, `-o=value`); updated `_check_for_auto_help()` to detect `getopts("h", ...)` multi-arg calls and display paired short/long options in auto-help output
- lyric/tests/core-0.8.0/test_getopts.py — Added 5 new tests: short alias match, long alias match, neither match, multi-char short option, and short/long with value

## Reason
Allow Lyric programs to define option aliases like `getopts("h", "help")` so both `-h` and `--help` map to the same variable. Also enables multi-character short options like `-hc` for `getopts("hc", "high-capacity")`.

## Git Commit Hash
`TBD` - Adhoc getopts short/long alias support

## Status
✅ Completed
