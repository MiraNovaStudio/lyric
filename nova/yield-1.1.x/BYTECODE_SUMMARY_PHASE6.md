# Bytecode Compiler Phase 6 — I/O, Exec, and Edge Cases

## Summary
Final phase: added try/catch/finally, raise, file I/O operators (->, ->>, <-), and exec chain support. This completes feature coverage for the bytecode compiler. All 6 phases are now implemented.

## Constructs Added
- `TryNode` → Python `ast.Try` with `ast.ExceptHandler` for each catch clause
- `RaiseNode` → `_rt.lyric_raise('ExceptionName')`
- `FileOpNode` (->>, ->, <-) → `_rt.lyric_file_op(operator, left, right)`
- `ExecChainNode` → `_rt.lyric_exec_chain(elements, operators, input, output)`
- `CatchClauseNode` → exception type mapping via `_rt.get_exception_type()`

## Runtime Helpers Added
- `get_exception_type()` — maps Lyric exception names to Python exception classes
- `lyric_raise()` — raises an exception by name
- `lyric_file_op()` — file write/append/read operations via DskObject
- `lyric_exec_chain()` — shell command chains with pipe (|), and (&&), or (||) operators

## Compiler Utility
- `_compile_body()` — shared helper to compile statement lists, reducing code duplication

## Files Modified
- `lyric/compiler.py` — added Phase 6 statement/expression compilation
- `lyric/compiled_runtime.py` — added Phase 6 runtime helpers

## Status
✅ Completed — All 6 phases implemented
