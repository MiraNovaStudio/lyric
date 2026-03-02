# Adhoc: Fix exec() shell detection on Windows

## Summary
Fixed exec() to respect the caller's shell environment on Windows. Commands like `mkdir -p` now work correctly when Lyric is launched from Git Bash.

## Key Accomplishments
- Added `get_shell_args()` helper in runtime.py that detects Git Bash via SHELL env var
- Updated all 7 subprocess.run call sites (1 in runtime.py, 6 in interpreter.py)
- On Windows + Git Bash: uses `[bash, '-c', command]` with shell=False
- On Windows + cmd.exe (or other platforms): uses default shell=True behavior
- All 1180 tests pass
- Verified `mkdir -p` works correctly from Git Bash

## Files Modified
- `lyric/runtime.py` — Added `get_shell_args()`, updated `exec_builtin()`
- `lyric/interpreter.py` — Updated 6 subprocess.run call sites

## Status
✅ Completed

## Changelog
See `nova/changelog/20260301/2041-CHANGELOG.md`
