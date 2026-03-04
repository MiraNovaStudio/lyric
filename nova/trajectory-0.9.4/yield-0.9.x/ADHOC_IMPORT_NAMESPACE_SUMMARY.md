# Adhoc Task — Native Import Namespace Pattern

## Summary
Changed whole-module `import` to bind a `LyricModuleNamespace` object so callers access members via `module.func()` and `module.VAR` rather than having all names dumped into the calling scope.

## Syntax
```lyric
# Whole-module — accessible as mathutils.add(), mathutils.PI
import mathutils

# Selective — binds add() and PI directly into scope (unchanged)
import mathutils; add, PI
```

## Key Accomplishments
- Added `LyricModuleNamespace` class to `interpreter.py` (already existed from previous session)
- Added `_instantiate_class_by_name` helper — extracts duplicated class instantiation logic for reuse by both regular calls and namespace calls
- Refactored `elif node.func_name in self.classes:` block to use the helper
- Added `LyricModuleNamespace` case in `_evaluate_function_call` member-path navigation loop
- Added `LyricModuleNamespace` dispatch in `_evaluate_function_call` method dispatch section, supporting:
  - `module.func(args)` — calls via `_call_func_def` with module context
  - `module.Class(args)` — temporarily injects module scope/classes then instantiates
- Added `LyricModuleNamespace` case in `_evaluate_identifier` member-path loop for `module.VAR` access
- Changed `_evaluate_import_statement` else-branch to create `LyricModuleNamespace` instead of dumping names
- Fixed parser: added `_parse_indexing_chain` to member-access return path so `module.arr[0]` parses correctly
- Updated 8 existing tests in `test_import_statement.py` to use namespace syntax
- 1170 total tests pass

## Files Created/Modified
- `lyric/interpreter.py` — `LyricModuleNamespace`, `_instantiate_class_by_name`, dispatch wiring, import statement
- `lyric/parser.py` — indexing chain on member-access path
- `lyric/tests/core-0.7.0/test_import_statement.py` — 8 tests updated

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260228/1705-CHANGELOG.md`
