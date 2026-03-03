# Adhoc: Support Member+Index Assignment and Compound Assignment — 20260302.2333

## Summary
Added support for member+index assignment patterns (`self.data[key] = value` and `self.data[key] += value`). Previously these patterns fell through to the expression parser and produced a misleading "Unexpected '+=' " error. Both regular and compound assignment now work on member-indexed targets like `self.counts[word]`.

## Files Changed
- lyric/parser.py — Added `_peek_at(offset)` helper method; added member+index assignment and compound assignment patterns in `_parse_assignment_or_expr_stmt()`
- lyric/interpreter.py — Added member+index case in `_evaluate_assignment()` that resolves the object member and variable index before assigning
- lyric/tests/core-0.9.0/test_compound_assignment.py — Added 3 new tests for member+index patterns including a word counter example

## Reason
The `self.counts[word] += 1` pattern is essential for classes that manage indexed data structures (maps, arrays) as instance state. Without it, users had to write the verbose `self.counts[word] = self.counts[word] + 1`.

## Git Commit Hash
`TBD` - Adhoc Member+Index Assignment Support

## Status
✅ Completed
