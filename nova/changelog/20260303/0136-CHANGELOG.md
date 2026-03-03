# Adhoc: Fix variable index resolution in simple index assignment — 20260303.0136

## Summary
Fixed a bug where `obj[var] = value` used the variable name as a literal string key instead of resolving it to the variable's runtime value. For example, `counts[word] = 1` was setting the key `"word"` instead of the value of the `word` variable.

## Files Changed
- lyric/interpreter.py — Added variable resolution in the simple index assignment path of `_evaluate_assignment()`. The index string is now checked against `global_scope` to resolve variable references, matching the behavior of the member+index path and the read path (`_evaluate_index`).

## Reason
The member+index assignment path (`self.counts[word] = 1`) already resolved variable indices correctly, but the simple index assignment path (`counts[word] = 1`) did not. This caused maps indexed by variables to always use the variable name as a literal key.

## Git Commit Hash
`TBD` - Adhoc Fix variable index resolution in assignment

## Status
✅ Completed
