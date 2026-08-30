# Bugfix — 20260830.1600

## Summary
Fixed a bug where writing non-ASCII characters (e.g. the em dash `—`) to a
file via `dsk` file operations (`->>` append, `->` overwrite, and direct
`.open()`/`.write()`) produced mangled/garbled output. The `DskObject` file
methods in the interpreter opened files with Python's platform-default text
encoding instead of an explicit encoding, so on systems where that default
isn't UTF-8, Unicode characters were corrupted on write. Reproduced with
`pulse.ly` writing `"— MiraNova Studios"` to `test.txt`, which produced a
replacement character instead of the em dash.

## Files Changed
- lyric/interpreter.py — `DskObject.open()`, `DskObject.append()`, and
  `DskObject.overwrite()` now explicitly open text-mode files with
  `encoding='utf-8'`, matching the encoding already used for reading Lyric
  source/module files elsewhere in the interpreter.

## Reason
Text file writes performed by the `dsk` type (used by `->>`/`->` redirection
and `.write()`/`.append()`/`.overwrite()`) relied on Python's implicit
default encoding, which is locale/platform dependent. Any non-ASCII
character written this way could be corrupted depending on the runtime
environment. Explicitly using UTF-8 makes Lyric's file I/O consistent and
portable regardless of host locale.

## Git Commit Hash
`TBD` - Bugfix: UTF-8 encoding for dsk file writes

## Status
✅ Completed
