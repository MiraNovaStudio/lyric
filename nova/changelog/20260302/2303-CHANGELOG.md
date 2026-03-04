# Adhoc: Add Colon Convention for getopts Value Options — 20260302.2303

## Summary
Added POSIX-style colon convention to `getopts()` for options that expect a value argument. Appending `:` to an option name (e.g., `getopts("f:", "file:")`) enables space-separated value syntax (`-f config.txt` or `--file config.txt`) in addition to the existing equals syntax (`-f=config.txt`).

## Files Changed
- lyric/runtime.py — Added `_command_line_raw_args` storage, updated `set_command_line_options()` to accept raw args, updated `getopts_builtin()` to handle `:` suffix and scan raw args for space-separated values
- lyric/cli.py — Updated both `run` and shorthand `.ly` paths to pass raw args to `set_command_line_options()`

## Reason
Options like `-f config_file` are a common CLI pattern. Without the colon convention, users had to use the equals syntax (`-f=config_file`), which is less intuitive.

## Git Commit Hash
`TBD` - Adhoc getopts Colon Convention

## Status
✅ Completed
