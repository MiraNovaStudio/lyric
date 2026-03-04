# Adhoc: String Format Operator (%)

## Summary
Added Python-style string format operator to Lyric. The `%` operator now works as a format string operator when the left operand is a string, supporting all standard format specifiers (`%s`, `%d`, `%f`, `%x`, `%%`, etc.) with both single values and tuples.

## Key Accomplishments
- Extended `%` binary operator to handle string formatting via Python's native `str.__mod__`
- Supports single value: `"Hello %s" % name`
- Supports tuple: `"Player %s has %d points" % (name, score)`
- Integer modulo (`10 % 3`) and `%=` assignment unchanged
- 11 new tests, all 1289 tests pass

## Files Created/Modified
- `lyric/interpreter.py` — 5-line addition in `_evaluate_binary_operation`
- `lyric/tests/core-0.9.0/test_format_string.py` — New test file (11 tests)

## Status
✅ Completed

## Changelog
See `nova/changelog/20260303/1858-CHANGELOG.md`
