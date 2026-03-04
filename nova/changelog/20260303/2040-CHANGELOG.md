# Adhoc — Generic Error Catch and Clean Exception Messages — 20260303.2040

## Summary
Two exception handling improvements:
1. `catch Error as e` now catches ALL exceptions (including RuntimeErrorLyric), acting as a true generic catch-all.
2. `str(e)` / `print(e)` on caught exceptions now returns only the clean message — no "Runtime error:" prefix. The CLI adds formatting prefixes itself for uncaught errors.

## Files Changed
- lyric/errors.py — Changed `Error` mapping from `LyricError` to `Exception`; updated `RuntimeErrorLyric.__str__` to return clean message; added `self.message` attribute
- lyric/cli.py — Updated 3 error handlers to add "Runtime error:" prefix themselves (since `__str__` no longer includes it)
- lyric/tests/core-0.3.4/test_pyobject_integration.py — Updated assertion that expected "Runtime error:" in `str(e)`
- lyric/tests/core-0.6.4/test_error_formatting.py — Updated 2 assertions that expected "Runtime error:" prefix in `str(e)`

## Reason
`catch Error as e` was failing to catch `RuntimeErrorLyric` because `Error` mapped to `LyricError` (a child class), not the parent. Users expect `Error` to be a universal catch-all. Additionally, caught exceptions should be silent — users explicitly `print(e)` if they want to see the message, and it should be clean without framework prefixes.

## Git Commit Hash
`TBD` - Adhoc: Generic Error catch-all and clean exception messages

## Status
✅ Completed
