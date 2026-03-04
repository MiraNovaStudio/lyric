# Adhoc — 20260228.1616

## Summary
Added native `tup` (tuple) type to the Lyric language. Tuples are immutable sequences created with parenthesis syntax `(elem1, elem2, ...)`. They pass through the `importpy` bridge as proper Python `tuple` objects, fixing the `AF_INET address must be tuple, not list` error when using `http.server.HTTPServer`. Also removed the old array-to-tuple workaround in `tup_builtin()`, replacing it with a proper `TupObject`-returning converter.

## Files Changed
- `lyric/lexer.py` — added `'tup'` to KEYWORDS and TYPE_OR_IDENT set
- `lyric/ast_nodes.py` — added `TupleLiteralNode` dataclass
- `lyric/parser.py` — imported `TupleLiteralNode`; rewrote LPAREN handler to distinguish grouping `(expr)` vs tuple `(expr, ...)`; added `'tup'` to all 4 `valid_types` sets
- `lyric/interpreter.py` — imported `TupleLiteralNode`; added `TupObject` class (immutable, read-only methods: count, index, len, min, max, sum); added `_evaluate_tuple_literal()`; wired dispatch, indexing, for-loop, `in` operator, and method calls; updated `_lyric_to_python()` to convert `TupObject` → Python `tuple`
- `lyric/pyproxy.py` — updated `_lyric_to_python()` to handle `TupObject` → `tuple` for importpy callables
- `lyric/runtime.py` — updated `tup_builtin()` to return `TupObject` instead of raw Python `tuple`
- `lyric/tests/core-0.9.0/test_tup_type.py` — 24 new tests covering all tup features

## Reason
`server.HTTPServer(["0.0.0.0", PORT], ...)` failed with `AF_INET address must be tuple, not list` because Lyric arrays are lists. Native tuples allow users to write `server.HTTPServer(("0.0.0.0", PORT), ...)` directly. The `TupObject` is automatically converted to a Python `tuple` when passed through the `importpy` bridge.

## Git Commit Hash
`TBD` - Adhoc: Add native tup type to Lyric language

## Status
✅ Completed
