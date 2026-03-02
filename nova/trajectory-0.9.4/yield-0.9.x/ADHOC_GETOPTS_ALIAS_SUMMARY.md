# Adhoc: getopts() short/long option aliases

## Summary
Added support for short + long option aliases in `getopts()`, allowing `getopts("h", "help")` to match both `-h` and `--help`.

## Key Accomplishments
- `getopts()` now accepts variadic args: `getopts("h", "help")`, `getopts("hc", "high-capacity")`
- CLI parser now supports multi-char short options: `-hc`, `-o=value`
- Auto-help detection updated to recognize multi-arg getopts calls
- 5 new tests added, 1185 total passing

## Files Modified
- `lyric/runtime.py` — `getopts_builtin()` variadic args
- `lyric/cli.py` — multi-char short options, improved auto-help
- `lyric/tests/core-0.8.0/test_getopts.py` — 5 new tests

## Status
✅ Completed

## Changelog
See `nova/changelog/20260301/2058-CHANGELOG.md`
