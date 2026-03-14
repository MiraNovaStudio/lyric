# Bytecode Compiler Phase 5 — Module System and Imports

## Summary
Added full module import support for both Lyric modules (.ly files) and selective Python imports. Imported Lyric modules are themselves compiled by the same transpiler — modules are not interpreted, they're also transpiled.

## Constructs Added
- `ImportNode` (whole-module) → `_rt.lyric_import('module', __file__, globals())`
- `ImportNode` (selective) → `_rt.lyric_import_selective('module', [('sym', 'alias')], __file__, globals())`
- `ImportPyNode` (selective) → `_rt.lyric_importpy_selective('module', ['name1', 'name2'], globals())`

## Module Resolution
- Reserved prefixes (`lyric`, `lyrical`) resolve from stdlib `lib/` directory only
- `ly` namespace is hard-blocked (reserved for future use)
- User modules searched in: cwd, source file directory, LYRIC_PATH
- File resolution: `module.ly` file, then `module/module.ly` directory-as-package

## Selective Imports
- `import mymodule; func1, func2 as alias` — pulls specific symbols with optional aliases
- `importpy math; sin, cos` — imports specific Python names via PyModuleProxy

## Runtime Helpers Added
- `lyric_importpy_selective()` — selective Python module import
- `lyric_import()` — find, compile, execute a .ly module, bind as namespace
- `lyric_import_selective()` — same but pull specific symbols with alias support
- `_compile_and_exec_module()` — shared helper that compiles .ly files using the same compiler
- `_ModuleNamespace` — simple namespace class for dotted access (e.g., `lyric.pwd()`)

## Files Modified
- `lyric/compiler.py` — added ImportNode compilation, updated ImportPyNode for selective imports
- `lyric/compiled_runtime.py` — added module import runtime helpers

## Status
✅ Completed
