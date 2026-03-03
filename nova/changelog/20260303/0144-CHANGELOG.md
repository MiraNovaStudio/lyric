# Adhoc: Fix variable index resolution in compound and regular index assignment parsing — 20260303.0144

## Summary
Fixed the parser to correctly generate `IdentifierNode` (instead of `LiteralNode`) for variable indices in both simple index assignment (`counts[word] = value`) and simple index compound assignment (`counts[word] += value`). Previously, the parser always created `LiteralNode(index_token.value)`, treating the variable name as a literal string key. This caused compound assignments like `counts[word] += 1` to fail with "Key 'word' not found in map" because the READ side of the desugared expression used the literal string "word" instead of the variable's runtime value.

## Files Changed
- lyric/parser.py — Fixed two locations in `_parse_statement()`:
  - Line ~703 (simple index regular assignment): Changed `LiteralNode(index_token.value)` to conditionally create `IdentifierNode` when `index_token.type == 'IDENT'`
  - Line ~721 (simple index compound assignment): Same fix, matching the pattern already used in the member+index compound assignment path at line 685

## Reason
The member+index compound assignment path (line 685) already correctly handled this:
```python
index_expr = LiteralNode(index_token.value) if index_token.type != 'IDENT' else IdentifierNode(index_token.value, index_token.line, index_token.col)
```
But the simple index paths did not. This caused `counts[word] += 1` to fail when `word` was a variable, while `self.counts[word] += 1` worked correctly.

## Git Commit Hash
`TBD` - Adhoc Fix variable index resolution in compound/regular index assignment parsing

## Status
✅ Completed
