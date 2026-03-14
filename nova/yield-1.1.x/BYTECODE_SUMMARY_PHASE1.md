# Bytecode Compiler Phase 1 — Core Expressions and Statements

## Summary
Implemented the initial Lyric-to-Python AST transpiler. Lyric source code is parsed into a Lyric AST, then compiled into Python `ast` module nodes, which CPython compiles to bytecode and executes natively. This is the foundation of the `--compile` flag.

## What Was Built
- `lyric/compiler.py` — Main compiler class `LyricCompiler` with `compile()` and `compile_to_ast()` entry points
- `lyric/compiled_runtime.py` — Runtime support library with helpers for Lyric-specific semantics

## Constructs Supported
- `LiteralNode` → `ast.Constant`
- `IdentifierNode` → `ast.Name`
- `BinaryOpNode` (+, -, *, /, //, %, **, comparisons) → `ast.BinOp` / `ast.Compare`
- `UnaryOpNode` (-, not, +) → `ast.UnaryOp`
- `AssignNode` (simple + dotted) → `ast.Assign` / `ast.Attribute`
- `TypeDeclarationNode` (var only) → `ast.Assign`
- `IfNode` (if/elif/else) → `ast.If`
- `LoopNode` (while + iterator) → `ast.While` / `ast.For`
- `FunctionNode` → `ast.FunctionDef`
- `CallNode` (simple + dotted) → `ast.Call`
- `ReturnNode` → `ast.Return`
- `BreakNode` / `ContinueNode` → `ast.Break` / `ast.Continue`
- `ImportPyNode` (whole-module) → runtime `lyric_importpy()`
- `ProgramNode` → `ast.Module` with auto `main()` invocation

## Runtime Helpers
- `lyric_add()` — string auto-coercion for `+` operator
- `lyric_div()` / `lyric_floordiv()` — zero-division checking
- `lyric_mod()` — modulo/string format
- `lyric_importpy()` — Python module import via proxy

## CLI Integration
- Added `--compile` flag to `lyric` CLI (originally `--fast`, renamed in later phase)
- `_execute_file()` updated with `use_compiler` parameter

## Performance
- Full benchmark: ~74s (interpreted) → ~5.1s (compiled) — **14x speedup**
- Small benchmark: ~0.73s → ~0.055s

## Files Created/Modified
- `lyric/compiler.py` — new
- `lyric/compiled_runtime.py` — new
- `lyric/cli.py` — modified (added --compile flag)

## Status
✅ Completed
