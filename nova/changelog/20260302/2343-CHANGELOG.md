# Adhoc: Allow Variable Redeclaration as Reassignment — 20260302.2343

## Summary
Changed variable redeclaration in the same scope to act as reassignment instead of raising a "Variable already declared" error. This fixes a common pattern where `var x = expr` or `int x = expr` inside a loop body fails on the second iteration because the loop doesn't create a new scope per iteration.

## Files Changed
- lyric/interpreter.py — Removed `CompileErrorLyric` raises in `_evaluate_type_declaration()` and `_evaluate_multi_declaration()` for same-scope redeclarations; redeclaration now silently updates the variable's type and value
- lyric/tests/core-0.9.0/test_variable_redeclaration.py — 10 new tests covering simple redeclaration, loop redeclaration, type checking on redeclare, multi-declaration redeclare, and value preservation

## Reason
Declaring a variable inside a loop body (e.g., `var best_word = all_words[0]`) would fail on the second iteration with "Variable 'best_word' already declared" because loop bodies share the same scope frame across iterations. This was a common source of confusion. Allowing redeclaration as reassignment matches developer expectations without losing type safety (typed redeclarations still enforce type compatibility).

## Git Commit Hash
`TBD` - Adhoc Variable Redeclaration as Reassignment

## Status
✅ Completed
