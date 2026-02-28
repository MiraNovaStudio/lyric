# Adhoc Task — Native tup Type

## Summary
Added `tup` as a native immutable tuple type in Lyric, solving the `AF_INET address must be tuple, not list` error when passing server address arguments to Python APIs via `importpy`.

## Key Accomplishments
- `tup` is now a first-class keyword and type in Lyric
- Tuple literal syntax: `(elem1, elem2, ...)` — distinguished from grouping `(expr)` by presence of a comma
- Single-element tuples: `(elem,)` with trailing comma
- Empty tuple: `()`
- `TupObject` wrapper class: immutable backing store (`tuple`), read-only methods (`count`, `index`, `len`, `min`, `max`, `sum`)
- `TupObject` → Python `tuple` conversion in both `interpreter._lyric_to_python()` and `pyproxy._lyric_to_python()` so that tuples pass correctly to Python APIs
- `tup()` builtin now returns `TupObject` (was returning raw Python `tuple`)
- 24 new tests, all passing; 1155 total tests pass

## Files Created/Modified
- `lyric/lexer.py` — `tup` in KEYWORDS + TYPE_OR_IDENT
- `lyric/ast_nodes.py` — `TupleLiteralNode`
- `lyric/parser.py` — LPAREN disambiguation + valid_types updated
- `lyric/interpreter.py` — `TupObject` class + full runtime wiring
- `lyric/pyproxy.py` — `TupObject` → tuple in `_lyric_to_python()`
- `lyric/runtime.py` — `tup_builtin()` returns `TupObject`
- `lyric/tests/core-0.9.0/test_tup_type.py` — 24 new tests

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260228/1616-CHANGELOG.md`
