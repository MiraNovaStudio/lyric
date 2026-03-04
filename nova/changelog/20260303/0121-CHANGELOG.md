# Adhoc: Inline Loop Variable Declaration — 20260303.0121

## Summary
Added support for inline loop variable declarations: `for int i in range(5)` and `for str word in words`. Previously, loop variables had to be declared on a separate line before the loop. The inline syntax auto-declares the variable in the current scope, eliminating boilerplate.

## Files Changed
- lyric/ast_nodes.py — Added `iterator_type` field to `LoopNode` dataclass
- lyric/parser.py — Added `TYPE_OR_IDENT IDENT IN` pattern detection in `_parse_loop_block()` before the existing `IDENT IN` check
- lyric/interpreter.py — Added inline declaration handling in both the range() and generic iterator paths of `_evaluate_iterator_loop()`; when `iterator_type` is set, auto-declares the variable instead of requiring pre-declaration
- lyric/tests/core-0.9.0/test_inline_loop_var.py — 14 new tests

## Reason
Declaring loop variables before the loop (`int i` then `for i in range(5)`) was repetitive boilerplate. The inline syntax `for int i in range(5)` is more concise and matches common expectations from other languages. Both syntaxes remain supported.

## Git Commit Hash
`TBD` - Adhoc Inline Loop Variable Declaration

## Status
✅ Completed
