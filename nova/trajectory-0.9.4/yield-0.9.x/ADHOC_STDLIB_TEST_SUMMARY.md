# Adhoc: lyric.ly standard library unit test

## Summary
Created comprehensive unit test for the Lyric standard library at
`lyric/tests/lib/test_lyric.ly`, exercising all 21 public functions.

## Key Accomplishments
- Tests all stdlib functions: pwd, exists, isfile, isdir, join, path, base, dir, env, set, pid, now, date, datefmt, randflt, randint, randarr, sleep, ls, mkdir/rmdir, cd, rm
- Uses `.len()` method (not builtin `len()`) per Lyric conventions
- Uses `given`/`done` loop syntax (not `while`/`{`)
- Includes multi-call range validation for random functions
- Includes filesystem integration test (mkdir + disk + isfile + rm + rmdir)
- Properly cleans up temp files/dirs in all code paths
- Identified `set()` limitation: `os.environ[]` subscript assignment not supported on PyModuleProxy (marked SKIP)

## Files Created/Modified
- `lyric/tests/lib/test_lyric.ly` — full rewrite

## Status
✅ Completed — 1325/1325 pytest tests passing, lyric test all PASS (2 SKIP)

## Changelog
See `nova/changelog/20260303/2226-CHANGELOG.md`
