# Import Restriction Update — 20251124.1951

## Summary
Updated the import statement to only allow importing functions and classes from Lyric modules. Variables (including arrays, maps, and other types) are no longer imported, preventing namespace pollution and enforcing cleaner module boundaries.

## Files Changed
- lyric/interpreter.py — Modified `_evaluate_import_statement` to only import functions and classes; attached module scope to imported functions; updated `_call_function` to use module scope for imported functions
- lyric/tests/core-0.7.0/test_import_statement.py — Completely rewrote test file to properly test the import restriction

## Reason
User requested that the import statement should throw an error if attempting to import anything other than functions or classes from a Lyric module. This change:
1. Prevents accidental namespace pollution from imported module variables
2. Maintains clear module boundaries
3. Allows imported functions to still access their module's variables through closure (module scope)
4. Enforces better encapsulation and API design

## Implementation Details
- Modified `_evaluate_import_statement` to skip importing from `module_interpreter.global_scope`
- Attached `module_scope` reference to each imported function definition
- Updated `_call_function` to use the attached `module_scope` when executing imported functions
- This allows imported functions to access their module's variables while preventing direct access to those variables from the importing scope

## Test Results
- All 51 tests in core-0.7.0 pass (100% pass rate)
- New test `test_import_rejects_variables` verifies that attempting to access imported variables raises `RuntimeErrorLyric`
- Test `test_import_preserves_module_scope` verifies that imported functions can still access their module's variables

## Git Commit Hash
`TBD` - Import restriction implementation

## Status
✅ Completed

