# Bytecode Compiler Phase 2 — Collections, Strings, and Type System

## Summary
Added support for Lyric's collection types (arr, map, tup), indexing, slicing, typed variable declarations with enforcement, multi-declarations, and the `in` operator.

## Constructs Added
- `ListLiteralNode` → `_rt.make_arr([...])`
- `DictLiteralNode` → `_rt.make_map({...})`
- `TupleLiteralNode` → `_rt.make_tup([...])`
- `IndexNode` → `ast.Subscript` (obj[index])
- `SliceNode` → `ast.Subscript` + `ast.Slice` (obj[start:end:step])
- `MultiDeclarationNode` → multiple `x = None` assignments
- `TypeDeclarationNode` with type enforcement → `_rt.typed_assign('type', value, 'name')`
- `BinaryOpNode` with `in` operator → `ast.Compare` with `ast.In()`

## Runtime Helpers Added
- `make_arr()` — construct ArrObject from Python list
- `make_map()` — construct MapObject from Python dict
- `make_tup()` — construct TupObject from Python list
- `typed_assign()` — enforce type on typed variable declarations
- `_is_type_compatible()` — type checking logic matching the interpreter

## Files Modified
- `lyric/compiler.py` — added collection/index/slice/type compilation
- `lyric/compiled_runtime.py` — added container constructors and type checking

## Status
✅ Completed
