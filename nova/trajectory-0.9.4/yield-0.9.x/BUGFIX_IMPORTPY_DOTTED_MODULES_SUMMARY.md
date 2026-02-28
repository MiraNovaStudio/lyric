# Bugfix Summary — importpy Dotted Modules + Python Type Conversion

## Status
✅ Completed

## Problems Fixed

### 1. Parser: dotted module names
`importpy http.server` caused "Only variable declarations..." because the
parser consumed only one `IDENT` token. Fixed to consume `IDENT(.IDENT)*`.

### 2. PyModuleProxy: wrong module object for submodules
`__import__('http.server')` returns the `http` package, not `http.server`.
Replaced with `importlib.import_module(module_name)` which always returns
the exact module requested.

### 3. Interpreter: binding name for dotted imports
The module is now bound to the **last component** of the dotted name:
- `importpy math` → `math`
- `importpy http.server` → `server`
- `importpy os.path` → `path`

### 4. ArrObject/MapObject not accepted by Python APIs (the tuple problem)
Python C-extensions reject Lyric's `ArrObject` wrapper. Fixed by adding
`_lyric_to_python()` conversion at every point where Lyric values are passed
to external Python callables:
- In `PyCallableProxy.__call__` (Python functions via importpy)
- In the interpreter's PyModuleProxy call path (Python class constructors)
- In the interpreter's arbitrary-Python-instance call path (methods on
  Python objects returned from importpy)
Conversion: `ArrObject` → Python `list`, `MapObject` → Python `dict`,
recursively. This is transparent — most Python APIs accept lists wherever
they accept tuples.

### 5. `tup()` built-in added
For the rare case where a Python API uses `isinstance(x, tuple)` rather than
accepting any sequence, `tup(arr)` converts a Lyric `arr` to a Python tuple.

### 6. `http.server` whitelisted
Added to `WHITELISTED_MODULES`. Safe: pure network I/O, no CPython internals.

## Corrected test.ly
```lyric
importpy http.server

def main() {
    int PORT = 8000
    var httpd = server.HTTPServer(["0.0.0.0", PORT], server.SimpleHTTPRequestHandler)
    print("Serving on port", PORT)
    httpd.serve_forever()
}
```

## Files Changed
- `lyric/parser.py`
- `lyric/pyproxy.py`
- `lyric/interpreter.py`
- `lyric/runtime.py`
- `lyric-lang.org/test.ly`

## Test Suite
1131 tests passed, 0 failures.

## Changelog
See `nova/changelog/20260228/1434-CHANGELOG.md`
