# Sprint1 Test Fix — 20251019.1040

## Summary
Fixed CLI test failures by properly handling SystemExit exceptions in test cases. Tests now correctly verify error handling for file not found and invalid extension scenarios.

## Files Changed
- tests/test_cli.py — Added try/except SystemExit blocks to handle sys.exit(1) calls properly
- nova/ai/CLAUDE_CONFIG.md — Updated to make changelog creation mandatory before git commits

## Reason
The CLI tests were failing because sys.exit(1) raises SystemExit exceptions that weren't being caught in the test cases. This fix ensures tests properly verify error messages and exit codes while maintaining the expected CLI behavior.

## Git Commit Hash
`[commit_hash]` - Sprint1: Fix CLI test failures

## Status
✅ Completed
