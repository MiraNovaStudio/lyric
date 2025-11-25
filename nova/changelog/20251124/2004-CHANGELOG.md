# Import Path Enhancement — 20251124.2004

## Summary
Enhanced the import statement to search for modules in both the current working directory AND the directory where the script being executed lives. This allows imports to work correctly when running scripts from different directories (e.g., `lyric studio/does_it_work.ly` can now find `utils.ly` in both `.` and `studio/`).

## Files Changed
- lyric/interpreter.py — Added `source_file` parameter to `Interpreter.__init__`; updated `_evaluate_import_statement` to include source file's directory in search paths; updated `evaluate()` helper function to accept `source_file` parameter
- lyric/cli.py — Updated `_execute_file` to pass the source file path to `evaluate()`

## Reason
User requested that imports should search in both:
1. The current working directory (where the command is run)
2. The directory containing the script being executed

This allows for more intuitive imports when scripts are run from different locations.

## Implementation Details
- Modified `Interpreter.__init__` to accept and store an optional `source_file` parameter
- Updated import search logic to include `os.path.dirname(os.path.abspath(self.source_file))` in search paths
- Modified CLI to pass `file_path` to `evaluate()` function
- Search order is now:
  1. Current working directory
  2. Directory of the source file (if known)
  3. LYRIC_PATH environment variable

## Test Results
- All 51 tests in core-0.7.0 pass (100% pass rate)
- No existing functionality broken
- Import tests continue to work correctly

## Git Commit Hash
`TBD` - Import path enhancement

## Status
✅ Completed

