# Bugfix — importpy dotted modules + Python type conversion — 20260228.1434

## Summary
Fixed three interconnected problems that blocked using Python submodules (e.g.
`http.server`) from Lyric via `importpy`, and solved the recurring "tuple
argument" problem that would have hit every Python API expecting a sequence
for a constructor or function call.

## Files Changed
- `lyric/parser.py` — `_parse_importpy_stmt`: consume `IDENT(.IDENT)*` so
  dotted module names like `importpy http.server` parse correctly
- `lyric/pyproxy.py` — use `importlib.import_module` instead of `__import__`
  (which returns the top-level package for dotted names, not the submodule);
  add `http.server` to WHITELISTED_MODULES; add `_lyric_to_python()` helper
  and apply it in `PyCallableProxy.__call__`
- `lyric/interpreter.py` — bind dotted imports to last component
  (`http.server` → `server`); add `_lyric_to_python()` instance helper;
  apply at PyModuleProxy, arbitrary-Python-instance, and callable-class
  call sites
- `lyric/runtime.py` — add `tup()` built-in that converts an `arr` to a
  Python tuple for APIs that specifically require `tuple` rather than a list
- `lyric-lang.org/test.ly` — rewritten to use correct Lyric syntax

## Reason
`importpy http.server` failed with a parse error because the parser only
accepted a single identifier after `importpy`. Even after fixing parsing,
`PyModuleProxy` used `__import__` which returned the `http` package rather
than the `http.server` submodule. The binding name would have been the full
dotted string, inaccessible as a Lyric identifier. Additionally, passing a
Lyric `arr` (ArrObject) to a Python function that expects a list or tuple
caused failures at the C-extension level; auto-conversion to Python list at
all Python call boundaries fixes this permanently.

## Git Commit Hash
`TBD` - Bugfix implementation

## Status
✅ Completed
