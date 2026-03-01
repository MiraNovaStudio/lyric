# Adhoc — 20260228.1705

## Summary
Changed `import module` (whole-module form) from dumping all names into the calling scope to binding a `LyricModuleNamespace` object, so callers use `module.func()` and `module.VAR` syntax — mirroring Python's `import math` vs `from math import sqrt`. Selective import (`import module; sym1, sym2`) is unchanged.

Also fixed the parser so `module.member[index]` (e.g., `vars_module.MODULE_LIST[0]`) is parsed correctly by adding `_parse_indexing_chain` to the member-access return path.

## Files Changed
- `lyric/interpreter.py` — Added `LyricModuleNamespace` class (bound by whole-module import), `_instantiate_class_by_name` helper (extracts class instantiation logic), `LyricModuleNamespace` dispatch in `_evaluate_function_call` member-path loop and method dispatch section, `LyricModuleNamespace` in `_evaluate_identifier` member-path loop, refactored `_evaluate_import_statement` whole-module branch to create namespace
- `lyric/parser.py` — Added `_parse_indexing_chain` to member-access return path so `module.arr[0]` parses correctly
- `lyric/tests/core-0.7.0/test_import_statement.py` — Updated 8 whole-module import tests to use namespace syntax (`mathutils.add()`, `classes.Person()`, etc.)

## Reason
User requested that `import module` follow the same namespace pattern as `importpy module` — binding the module as a namespace object rather than polluting the calling scope, consistent with Python's `import math` idiom.

## Git Commit Hash
`TBD` - Adhoc: Namespace pattern for whole-module import

## Status
✅ Completed
