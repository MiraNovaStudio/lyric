# Adhoc Task — Selective importpy Syntax

## Summary
Extended `importpy` to support `from X import Y, Z` style selective imports via semicolon syntax.

## Syntax
```lyric
# Selective — binds HTTPServer and SimpleHTTPRequestHandler directly into scope
importpy http.server; HTTPServer, SimpleHTTPRequestHandler

# Selective — partial callable bound directly
importpy functools; partial

# Whole-module (unchanged) — accessible as math.*
importpy math
```

## Key Accomplishments
- `ImportPyNode` has new optional `names: list` field (defaults to `None` → whole module)
- Parser detects `;` after module name and collects comma-separated identifiers
- Both `IDENT` and `TYPE_OR_IDENT` tokens accepted in name list
- Interpreter selectively binds each attribute; classes (types) are wrapped in `PyCallableProxy` so Lyric-to-Python arg conversion applies on call
- Blacklist/whitelist checks still enforced (module creation raises before attribute lookup)
- Both forms can coexist in the same program
- 15 new tests, all passing; 1170 total tests pass

## Files Created/Modified
- `lyric/ast_nodes.py` — `names` field on `ImportPyNode`
- `lyric/parser.py` — `;` name list parsing
- `lyric/interpreter.py` — selective binding logic
- `lyric/tests/core-0.9.0/test_importpy_selective.py` — 15 new tests

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260228/1642-CHANGELOG.md`
