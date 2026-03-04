# Adhoc — 20260228.1642

## Summary
Added selective import syntax to `importpy`: `importpy module; Name1, Name2`. Named attributes are bound directly into scope, wrapped in `PyCallableProxy` so Lyric-to-Python argument conversion still applies. Without the semicolon list, behavior is unchanged (whole-module proxy bound to the last dotted component).

## Files Changed
- `lyric/ast_nodes.py` — added `names: list = None` field to `ImportPyNode`
- `lyric/parser.py` — `_parse_importpy_stmt()` now parses optional `; Name1, Name2` list
- `lyric/interpreter.py` — `_evaluate_importpy_statement()` selectively binds named attributes when `node.names` is set; wraps raw callables/classes in `PyCallableProxy`
- `lyric/tests/core-0.9.0/test_importpy_selective.py` — 15 new tests

## Reason
Users need to call `HTTPServer(...)` and `partial(...)` directly without the `server.*` or `functools.*` prefix, mirroring Python's `from http.server import HTTPServer, SimpleHTTPRequestHandler` idiom.

## Git Commit Hash
`TBD` - Adhoc: Add selective importpy syntax

## Status
✅ Completed
