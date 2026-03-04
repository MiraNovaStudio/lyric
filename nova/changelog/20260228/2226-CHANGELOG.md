# Adhoc — Loop Variable Declaration Requirement — 20260228.2226

## Summary
Require loop variables to be declared before use in `given`/`for` iterator loops. This enforces Lyric's explicit-declaration language design for loop variables, adds type compatibility checking per iteration item, and converts Python tuples to lists for `arr`-declared loop variables.

## Files Changed
- lyric/interpreter.py — Added declaration check, type compatibility check, and tuple-to-list conversion in `_evaluate_iterator_loop`
- lyric/tests/core-0.9.0/test_loop_variable_declaration.py — New test file with 10 test cases
- lyric/tests/examples/nested_flow.ly — Added `int i`, `int j` declarations
- lyric/tests/core-0.1.0/test_interpreter.py — Added loop variable declarations in Lyric snippets
- lyric/tests/core-0.1.0/test_parser.py — Added loop variable declarations, updated assertion counts
- lyric/tests/core-0.2.0/test_boolean_operations.py — Added `int i` declarations
- lyric/tests/core-0.2.0/test_error_reporting.py — Added `int i` declarations
- lyric/tests/core-0.2.0/test_nested_control_flow.py — Added `int i`, `int j` declarations
- lyric/tests/core-0.2.0/test_builtins_integration.py — Added `int i` declarations
- lyric/tests/core-0.4.0/test_control_structure_syntax_simplification.py — Added `int i` declarations
- lyric/tests/core-0.6.0/test_for_keyword.py — Added `int i`, `int j` declarations
- lyric/tests/core-0.6.0/test_break_continue.py — Added `int i`, `int j` declarations (~13 snippets)
- lyric/tests/core-0.6.0/test_constructor_recognition.py — Added `int i` declaration
- lyric/tests/core-0.7.0/test_arr_methods.py — Added `var item` declaration
- lyric/tests/core-0.7.0/test_arr_type.py — Added `var color`, `var num`, `var item` declarations
- lyric/tests/core-0.7.0/test_map_methods.py — Added `var key` declaration
- lyric/tests/core-0.7.0/test_map_type.py — Added `var key` declarations
- lyric/tests/core-0.7.0/test_range_edge_cases.py — Added `int i` to all 15 test snippets
- lyric/tests/core-0.7.0/test_import_statement.py — Added `var item` declaration
- lyric/tests/core-0.8.0/test_dsk_type.py — Added `var line` declarations
- lyric/tests/core-0.8.0/test_cli_args.py — Added `var arg` declarations
- lyric/tests/core-0.9.0/test_tup_type.py — Added `var item` declaration
- studio/html_parser.ly — Added `var link`, `var heading` declarations
- studio/does_it_work.ly — Added `int num` declaration
- studio/http_fetch.ly — Added `var link` declaration
- studio/tutorial/6.2.loopy.ly — Added `int i`, `var color` declarations
- studio/tutorial/6.2.loopy2.ly — Added `int i` declaration
- studio/tutorial/6.4.breakcont.ly — Added `int i` declaration
- studio/tutorial/7.2.typedparam.ly — Added `int i` declaration
- studio/tutorial/8.3.iterloop.ly — Added `var score` declaration
- studio/tutorial/8.5.nested.ly — Added `var row`, `var val` declarations
- studio/tutorial/9.3.mapiter.ly — Added `var country` declaration
- studio/tutorial/9.3.1.items.ly — Added `arr pair` declaration

## Reason
Lyric requires variables to be declared with a type before use (e.g., `var x`, `int x`, `arr items`). However, `given`/`for` iterator loops previously bypassed this principle by implicitly creating and injecting the loop variable into `global_scope` without any declaration check. This violated Lyric's explicit-declaration language design.

## Git Commit Hash
`TBD` - Adhoc: Loop Variable Declaration Requirement

## Status
✅ Completed
