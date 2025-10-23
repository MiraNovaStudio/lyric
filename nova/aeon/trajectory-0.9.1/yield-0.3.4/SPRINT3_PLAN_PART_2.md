# Sprint 3 — Type System Extension for importpy

**Project:** Lyric Programming Language  
**Version Target:** 0.3.0  
**Owner:** Michael (Aeonath)  
**Architect:** ChatGPT  
**Engineer:** Claude  
**Extension To:** Sprint 3 type system work (adds importpy + pyobject)

## Objective

Enable seamless interop with Python libraries using:

- `importpy <module>` (e.g., `importpy datetime`)
- Lazy proxy objects to avoid upfront wrapping/overhead
- A built-in `pyobject` type for values originating from Python
- Compatibility with `var` so this works immediately:

```lyric
importpy datetime

var now = datetime.datetime.now()
print(now.year)
```

## Scope & Non-Goals

### In-scope
- Parser support for `importpy`
- Runtime module binding via a lightweight proxy (`PyModuleProxy`)
- `pyobject` built-in type and minimal enforcement rules
- `var` accepts `pyobject` without errors
- Basic error messages for missing modules/attributes

### Not in this sprint
- Deep static analysis of Python signatures
- Autocomplete/type stubs for Python modules
- Packaging/external venv isolation

## Language & Runtime Design

### Task 1) Syntax

```lyric
importpy <identifier>
```

Examples:
```lyric
importpy math
importpy datetime
```

### Task 2) Semantics

On `importpy NAME`, Lyric binds `NAME` in the global environment to a module proxy that forwards attribute access and calls to the actual Python module.

Any object accessed through that proxy is treated as `pyobject` by the type system.

### 3) pyobject Type

Add `pyobject` as a built-in, internal type that is always represented as `var` in Lyric code.

- **Internal Type:** `pyobject` exists only internally, never in user syntax.
- **User Syntax:** Only `var x = value` is allowed, never `x:pyobject = value`.
- **Type System Integration:** `pyobject` values are always treated as `var` type in Lyric code.
- **Dynamic Behavior:** `var` can hold `pyobject` without type checking restrictions.
- **Syntax:** Only `var x = value` is allowed, never `x:pyobject = value`.

### 4) Minimal Overhead via Lazy Proxy

Python sketch:

```python
class PyModuleProxy:
    def __init__(self, module_name: str):
        self._module_name = module_name
        self._module = __import__(module_name)

    def __getattr__(self, name):
        # Forward attribute access: functions, classes, constants, submodules
        return getattr(self._module, name)

    def __repr__(self):
        return f"<PyModuleProxy {self._module_name}>"
```

```python
env.bind_symbol("datetime", PyModuleProxy("datetime"), type_name="pyobject")
```


## Type System Integration

Update type-checking helpers:

- **Registry:** Add `"pyobject"` to built-in types (internal only).
- **Assignment rule:** `pyobject` values are always assigned to `var` type in Lyric code.
- **Inference with var:** If the runtime value originates from a proxy (module, function, object), its inferred type is `pyobject` internally, but represented as `var` in Lyric.
- **Function calls:** Parameters declared as `var` can accept `pyobject` values without restrictions.
- **Syntax restriction:** Never allow explicit `x:pyobject = value` declarations - only `var x = value`.

Pseudo-code:

```python
def is_assignable(expected: str, actual: str) -> bool:
    # var can accept any type, including pyobject
    if expected == "var":
        return True
    # pyobject internally maps to var in Lyric syntax
    if actual == "pyobject":
        return expected == "var"
    return expected == actual
```

## Parser & CLI Changes

### Parser

Add a simple rule for `importpy`:

- **Token:** `IMPORTPY` followed by `IDENT`
- **AST node:** `ImportPy(module_name: str)`

### Interpreter Visitor

On `ImportPy(name)`: instantiate `PyModuleProxy(name)` and bind to the global env with type `pyobject`.

### Errors:

- **Module not found** → `ImportError: cannot import Python module '<name>'`
- **Attribute access error** → surface as Lyric `AttributeError` with file/line info.

## Error Handling & Messages

### Import error:

```
ImportError: cannot import Python module 'nonexistent'
at file.ly:Line 1
```

### Attribute error:

```
AttributeError: 'datetime' has no attribute 'nowz'
at file.ly:Line 3 -> datetime.nowz()
```

Follow Sprint 3's A17–A19 error formatting (filename, line, snippet).

## Tests

Create `tests/examples/importpy_tests.ly`:

```lyric
importpy math
importpy datetime

var r = math.sqrt(9)
print(r)        # expect 3.0 (pyobject okay with var)

var now = datetime.datetime.now()
print(now.year) # prints current year

# Explicit pyobject declaration is not allowed
var x = math.sin(0)
print(x)
```

```lyric
importpy datetime

var now = datetime.datetime.now()
print(now.year)
```

### Pytest expectations:

- Running through CLI prints values without type errors.
- No Python stack traces; errors (if any) show Lyric-formatted messages.

## Documentation

- **README.md** (or language spec): add `importpy` examples and describe `pyobject`.
- **CHANGELOG.md**: add entry for v0.3.0:
  - Added `importpy` statement
  - Added `pyobject` type (internal only, never explicit declarations)
  - `var` supports `pyobject` interop

## Acceptance Criteria (ImportPy)

- **I1** `importpy <module>` binds a working module proxy in the global env.
- **I2** Accessing attributes/functions via the proxy works (`math.sqrt`, `datetime.datetime.now`).
- **I3** Values from Python land are typed as `pyobject` internally, but represented as `var` in Lyric code; `var` accepts them without error.
- **I4** Assignments to explicitly declared `pyobject` variables are **never allowed** - only `var` assignments work.
- **I5** `tests/examples/importpy_tests.ly` runs via CLI; outputs are correct; no Python tracebacks.
- **I6** Errors (missing module/attribute) show Lyric-style messages with file/line (consistent with A17–A19).

## Mapping to Sprint 3 Tasks

- **Task 1** — Type Declaration and Inference: add `pyobject` to registry (internal only), adjust `is_assignable` to map `pyobject` to `var`, allow `var` inference to `pyobject`.
- **Task 2** — Return Statements: functions may return `pyobject` values (represented as `var`) without strict checks.
- **Task 6** — Runtime Safety & Error Messages: ensure import/attr errors use consistent formatting.
- **Task 7** — Test Suite Expansion: add `importpy_tests.ly` + related pytest.
- **Task 8** — Docs & Version: update README/CHANGELOG; version remains 0.3.0 target.

## Definition of Done (Extension)

- Parser accepts `importpy`.
- Runtime binds a module proxy.
- `pyobject` type present and enforced per rules above.
- Tests pass for `importpy` scenarios.
- Docs & changelog updated accordingly.

## Example (End-to-End)

```lyric
importpy datetime

var now = datetime.datetime.now()
print(now.year)
```

This should execute without any type complaints, printing the current year.