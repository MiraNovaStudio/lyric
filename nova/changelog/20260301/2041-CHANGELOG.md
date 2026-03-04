# Adhoc — 20260301.2041

## Summary
Fixed exec() on Windows to use the caller's shell instead of always using cmd.exe. On Windows, subprocess.run(shell=True) defaults to cmd.exe, which doesn't understand Unix flags like `mkdir -p`. When Lyric is launched from Git Bash, the SHELL env var now correctly routes commands through bash.

## Files Changed
- lyric/runtime.py — Added `get_shell_args()` helper that detects the caller's shell via the SHELL env var on Windows; updated `exec_builtin()` to use it
- lyric/interpreter.py — Updated all 6 subprocess.run call sites in exec/pipe handlers to use `get_shell_args()`

## Reason
When running `exec("mkdir -p dir")` from Git Bash on Windows, Python's subprocess.run(shell=True) dispatched to cmd.exe, which interpreted `-p` as a literal directory name instead of a flag. The fix detects when SHELL points to a Unix shell and invokes it directly with `-c`.

## Git Commit Hash
`TBD` - Adhoc exec() shell detection fix

## Status
✅ Completed
