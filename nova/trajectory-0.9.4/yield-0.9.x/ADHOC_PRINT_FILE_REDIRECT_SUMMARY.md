# Adhoc: Print statement file redirection

## Summary
Added support for `print "text" ->> file` and `print "text" -> file` syntax, enabling print-to-file with automatic newlines.

## Key Accomplishments
- `print "text" ->> file` — appends text + newline to dsk object
- `print "text" -> file` — overwrites file with text + newline
- `print "a", "b" ->> file` — multi-arg with space-separated values + newline
- Print does NOT echo to stdout when redirected to file
- Regular `print "text"` and `print()` still work unchanged
- All 1195 tests pass (8 new)

## Files Modified
- `lyric/parser.py` — routing + print arg parsing with file operator detection
- `lyric/interpreter.py` — print redirect handling in `_evaluate_file_op()`
- `lyric/tests/core-0.8.0/test_print_file_redirect.py` — 8 new tests

## Status
✅ Completed

## Changelog
See `nova/changelog/20260301/2145-CHANGELOG.md`
