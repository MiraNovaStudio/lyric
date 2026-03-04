# Adhoc: Compound Assignment Operators — 20260302.2018

## Summary
Added compound assignment operators (`+=`, `-=`, `*=`, `/=`, `%=`) to the Lyric language. Implemented via parse-time desugaring: `x += 5` is transformed into `x = x + 5` at the AST level, requiring no interpreter changes. All five operators work on `int` and `flt`, with `+=` (concatenation) and `*=` (repetition) also supported on `str`.

## Files Changed
- lyric/lexer.py — Added 5 new token types (PLUS_ASSIGN, MINUS_ASSIGN, MULTIPLY_ASSIGN, DIVIDE_ASSIGN, PERCENT_ASSIGN) and lexing logic for `+=`, `-=`, `*=`, `/=`, `%=`
- lyric/parser.py — Added COMPOUND_ASSIGN_TYPES/COMPOUND_ASSIGN_OPS class constants and desugaring logic for simple variable, member access, and index compound assignments
- lyric/tests/core-0.9.0/test_compound_assignment.py — New test file with 33 tests covering all operators, types, member/index access, loops, type errors, and division by zero

## Reason
Compound assignment operators are a fundamental convenience expected in modern programming languages. They reduce boilerplate in common patterns like accumulators (`total += x`), counters (`self.count += 1`), and string building (`result += word`).

## Git Commit Hash
`TBD` - Adhoc Compound Assignment Operators Implementation

## Status
✅ Completed
