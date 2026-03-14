# Lyric Python Bytecode Compilation Backend — Implementation Plan

**Date:** 2026-03-13
**Status:** Draft
**Author:** MiraNova Studios / Architecture Review

---

## 1. Executive Summary

The Lyric interpreter is a tree-walking interpreter written in Python. On a benchmark
that calls simple functions 10 million times with arithmetic loops, it runs in ~74
seconds vs ~1-3 seconds for Python/Ruby/Perl. The overhead comes from:

- Repeated `isinstance` dispatch on every AST node visit
- Dictionary-based scope lookup instead of local variable slots
- Function calls that copy/restore `global_scope` dicts on every invocation
- Python method call overhead on every single Lyric operation

This plan describes a new compilation pipeline that translates Lyric AST into Python
`ast` module nodes, compiles them with `compile()`, and executes via `exec()`/`eval()`.
This approach reuses CPython's own bytecode compiler and achieves near-native Python
speed for arithmetic, loops, and function calls.

**Recommended approach:** Generate Python `ast` module nodes (not raw bytecode).
Rationale:

- Python's `ast` module is a stable public API; bytecode opcodes change every minor
  CPython release.
- The `ast` module handles all the complex bytecode generation (local variable
  slots, jump targets, exception tables, etc.).
- The performance difference between `ast`-compiled code and hand-rolled bytecode is
  negligible for Lyric's use cases — the bottleneck is the tree-walking, not the
  code generation.
- `compile(ast_node, ..., 'exec')` produces the same bytecode that CPython uses for
  `.py` files.

**Expected speedup:** 20-50x for compute-heavy loops and function calls (bringing
the 74-second benchmark to ~2-4 seconds, comparable to equivalent Python code).

---

## 2. Architecture Overview

### 2.1 Current Pipeline

```
Source (.ly) --> Lexer --> Parser --> Lyric AST --> Tree-Walking Interpreter
                                     (ast_nodes.py)    (interpreter.py)
```

### 2.2 New Pipeline (Added, Not Replaced)

```
Source (.ly) --> Lexer --> Parser --> Lyric AST --> Compiler ──> Python AST
                                     (ast_nodes.py)  (compiler.py)     |
                                                                  compile()
                                                                       |
                                                                  Code Object
                                                                       |
                                                                   exec()
                                                              (with runtime lib)
```

The tree-walking interpreter (`interpreter.py`) is preserved as a fallback and
reference implementation. A new `--compile` or `--fast` CLI flag selects the
bytecode path. Eventually, the compiled path can become the default.

### 2.3 New Files

| File | Role |
|------|------|
| `lyric/compiler.py` | Main compiler: walks Lyric AST, emits Python `ast` nodes |
| `lyric/compiled_runtime.py` | Runtime support library called by compiled code |
| `lyric/tests/core-X.X.X/test_compiler_*.py` | Compiler-specific tests |

### 2.4 Key Design Principle: Runtime Helper Functions

Many Lyric features have no direct Python equivalent. The compiler emits calls to
runtime helper functions in `compiled_runtime.py` rather than trying to inline
everything. This keeps the compiler simple and the emitted AST readable.

Example: Lyric's typed variable declarations become:
```python
# Lyric: int x = 42
x = _lyric_rt.check_type('int', 42, 'x')  # returns 42 or raises
```

---

## 3. Mapping of Lyric Constructs to Python

### 3.1 Direct Mappings (No Runtime Helpers Needed)

| Lyric Construct | AST Node | Python Equivalent |
|----------------|----------|-------------------|
| `LiteralNode` (int, float, str, bool, None) | `ast.Constant` | Identical |
| `IdentifierNode` (simple) | `ast.Name` | Identical |
| `BinaryOpNode` (+, -, *, /, <, >, <=, >=, ==, !=) | `ast.BinOp` / `ast.Compare` | Identical |
| `UnaryOpNode` (-, not) | `ast.UnaryOp` | Identical |
| `ListLiteralNode` | `ast.List` | `[e1, e2, ...]` |
| `DictLiteralNode` | `ast.Dict` | `{k1: v1, ...}` |
| `TupleLiteralNode` | `ast.Tuple` | `(e1, e2, ...)` |
| `IndexNode` | `ast.Subscript` | `obj[index]` |
| `SliceNode` | `ast.Subscript` + `ast.Slice` | `obj[start:end:step]` |
| `AssignNode` (simple) | `ast.Assign` | `x = expr` |
| `IfNode` | `ast.If` | `if/elif/else` |
| `ReturnNode` | `ast.Return` | `return expr` |
| `BreakNode` | `ast.Break` | `break` |
| `ContinueNode` | `ast.Continue` | `continue` |
| `FunctionNode` | `ast.FunctionDef` | `def func(params): ...` |
| `TryNode` | `ast.Try` | `try/except/finally` |
| `RaiseNode` | `ast.Raise` | `raise ExceptionType(msg)` |
| `ImportPyNode` | `ast.Import` / `ast.ImportFrom` | `import module` |

### 3.2 Mappings Requiring Runtime Helpers

| Lyric Construct | AST Node | Compiled Form | Runtime Helper |
|----------------|----------|---------------|----------------|
| `TypeDeclarationNode` | `int x = 5` | `x = _rt.typed_assign('int', 5, 'x')` | `typed_assign()` |
| `MultiDeclarationNode` | `int a, b, c` | Multiple `_rt.typed_declare(...)` calls | `typed_declare()` |
| `LoopNode` (while / `given...done`) | `given x > 0:` | `while x > 0:` | Direct mapping |
| `LoopNode` (iterator / `given i in`) | `given i in range(n):` | `for i in range(n):` | With type check wrapper |
| `CallNode` (print) | `print(args)` | `print(args)` | Direct (Python builtin) |
| `CallNode` (user func) | `func(args)` | `func(args)` | Direct (Python function) |
| `CallNode` (type-checked) | `func(int x)` | `func(_rt.check_param('int', x, 'x'))` | `check_param()` |
| `ClassNode` | class definition | Native Python `class` | Direct mapping |
| `AssignNode` (dotted: `self.x = v`) | Member assignment | `self.x = v` | Direct |
| `AssignNode` (indexed: `a[i] = v`) | Index assignment | `a[i] = v` | Direct |
| `BinaryOpNode` (+, string auto-coerce) | `str + int` | `_rt.add(left, right)` | `add()` with str coercion |
| `BinaryOpNode` (%) | String format or modulus | `_rt.mod(left, right)` | `mod()` |
| `BinaryOpNode` (`in`) | Membership test | `left in right` | May need `MapObject` check |
| `BinaryOpNode` (`and`, `or`) | Logical ops | `_rt.truthy(left) and _rt.truthy(right)` | `truthy()` |
| `FileOpNode` | `expr -> dsk` | `_rt.file_op(op, left, right)` | `file_op()` |
| `ExecChainNode` | `exec('cmd') \| exec('cmd2')` | `_rt.exec_chain(...)` | `exec_chain()` |
| `RexNode` | `/pattern/` | `_rt.rex('pattern')` | `rex()` |
| `ImportNode` | `import mymodule` | `_rt.import_lyric('mymodule', ...)` | `import_lyric()` |

### 3.3 Lyric-Specific Features Requiring Special Handling

#### 3.3.1 Typed Variables (`int x = 5`)

Lyric enforces types at assignment time. In the compiled backend:

```python
# Lyric: int x = 5
x = _rt.typed_assign('int', 5, 'x')  # returns 5

# Lyric: x = "hello"  (if x was declared as int, this raises)
x = _rt.reassign('x', "hello", _type_registry)
```

A `_type_registry` dict tracks which variables have declared types. The runtime
helpers check against it. For `var` declarations, no check is needed.

**Optimization:** In a second pass, if all assignments to a variable are
type-consistent (statically determinable), the type checks can be elided entirely.

#### 3.3.2 `given`/`done` Loops

Lyric's `given` is syntactic sugar for `while` or `for`:

```python
# Lyric: given i <= n: ... done  (while loop)
while i <= n:
    ...

# Lyric: given var i in range(10): ... done  (iterator loop)
for i in range(10):
    ...
```

The `LoopNode.loop_kind` field (`"iterator"` or `"while"`) determines which Python
construct to emit. Iterator loops with type annotations need a runtime type check
wrapper around the iterable.

#### 3.3.3 Class System (Native Python Classes)

Lyric classes compile directly to native Python classes. The interpreter's dict-based
instance model (`__instance_class__`, `__visibility_*` keys, etc.) is being retired
in favor of a clean, idiomatic Python class mapping.

```python
# Lyric:
# class Animal {
#     constructor(str name) {
#         self.name = name
#     }
#     def speak() {
#         return self.name + " speaks"
#     }
# }

class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return self.name + " speaks"

# Lyric: class Dog extends Animal { ... }
class Dog(Animal):
    ...
```

This gives us:
- Native Python attribute access (`self.x`) — no dict lookups or runtime helpers
- Native Python inheritance and `super()` — MRO handled by Python
- Native `isinstance()` — works automatically
- Method dispatch at C speed — no interpreter-level resolution

#### 3.3.4 Access Control (public/private/protected)

Access control compiles to Python's name-mangling convention:

```python
# Lyric: private str _secret = "hidden"
# Compiled: self.__secret = "hidden"  (Python name-mangling)

# Lyric: protected int _count = 0
# Compiled: self._count = 0  (single underscore convention)
```

For strict enforcement beyond Python's conventions, the compiler can emit a
simple check at the call site:

```python
# External access to private member -> compile-time error
# (the compiler knows the caller context statically)
```

This moves access control from runtime overhead to compile-time validation, which
is both faster and catches errors earlier.

#### 3.3.5 `importpy` (Python Module Bridge)

`importpy` can be compiled almost directly to Python `import` statements:

```python
# Lyric: importpy math
import math as _py_math
math = _rt.wrap_py_module(_py_math, 'math')  # applies whitelist/blacklist

# Lyric: importpy http.server; HTTPServer
from http.server import HTTPServer as _raw_HTTPServer
HTTPServer = _rt.wrap_py_callable(_raw_HTTPServer, 'http.server.HTTPServer')
```

#### 3.3.6 `import` (Lyric Module System)

Lyric module imports execute a `.ly` file and inject its definitions into the
caller's scope. The compiled backend:

1. Compiles the imported module using the same compiler
2. Executes it in a separate namespace
3. Binds the results into the caller's compiled scope

```python
_mod = _rt.import_lyric_module('mymodule', source_file=__file__)
mymodule = _mod  # LyricModuleNamespace
```

#### 3.3.7 `dsk` Type and File Operations

`dsk` objects and file operators (`->`, `->>`, `<-`) compile to runtime helper calls:

```python
# Lyric: var f = disk("file.txt")
f = _rt.disk("file.txt")  # returns DskObject

# Lyric: data -> f
_rt.file_write(data, f)

# Lyric: data ->> f
_rt.file_append(data, f)
```

The existing `DskObject` class can be reused directly.

#### 3.3.8 `exec()` and Exec Chains

Shell execution compiles to runtime helper calls:

```python
# Lyric: exec("ls -la")
_rt.exec_cmd("ls -la")

# Lyric: exec("ls") | exec("grep test")
_rt.exec_chain([("ls",), ("grep", "test")], operators=['|'])
```

#### 3.3.9 String `+` Auto-Coercion

Lyric's `+` operator auto-converts to string if either operand is a string. The
compiler must wrap `+` operations in a helper when operand types are unknown:

```python
# If either side could be a string:
result = _rt.add(left, right)

# If both sides are known to be numeric (optimization):
result = left + right  # direct Python add
```

#### 3.3.10 `ArrObject` / `MapObject` / `TupObject`

The existing container wrapper classes are reused directly in compiled code:

```python
# Lyric: arr x = [1, 2, 3]
x = ArrObject([1, 2, 3])

# Lyric: x.append(4)
x.append(4)  # ArrObject.append() works directly

# Lyric: map m = {"a": 1}
m = MapObject({"a": 1})
```

---

## 4. Phased Implementation Plan

### Phase 1: Core Expressions and Statements (MVP)

**Goal:** Compile and execute a program with variables, arithmetic, print, if/else,
and while loops. The benchmark's inner arithmetic loop should run at near-Python
speed.

**Scope:**
- `LiteralNode` -> `ast.Constant`
- `IdentifierNode` (simple, no dots) -> `ast.Name`
- `BinaryOpNode` (arithmetic: +, -, *, /, comparisons) -> `ast.BinOp` / `ast.Compare`
- `UnaryOpNode` -> `ast.UnaryOp`
- `AssignNode` (simple) -> `ast.Assign`
- `TypeDeclarationNode` (var only, no type checking) -> `ast.Assign`
- `IfNode` -> `ast.If`
- `LoopNode` (while) -> `ast.While`
- `LoopNode` (iterator with range) -> `ast.For`
- `CallNode` (print) -> `ast.Call` to `print`
- `ReturnNode` -> `ast.Return`
- `BreakNode` -> `ast.Break`
- `ContinueNode` -> `ast.Continue`
- `FunctionNode` -> `ast.FunctionDef`
- `ProgramNode` -> `ast.Module`

**Files to create:**
- `lyric/compiler.py` (~400-600 lines)
- `lyric/compiled_runtime.py` (~100 lines, minimal)
- `lyric/tests/core-X.X.X/test_compiler_phase1.py`

**CLI integration:** Add `--fast` flag to `cli.py`:
```python
if '--fast' in options or '--compile' in options:
    from lyric.compiler import compile_lyric
    code_obj = compile_lyric(ast)
    exec(code_obj, {'_rt': compiled_runtime})
```

**Deliverable:** The arithmetic benchmark runs in ~2-4 seconds instead of ~74 seconds.

### Phase 2: Collections, Strings, and Type System

**Goal:** Support `arr`, `map`, `tup`, typed declarations, string operations.

**Scope:**
- `ListLiteralNode` -> `ArrObject(ast.List)` constructor call
- `DictLiteralNode` -> `MapObject(ast.Dict)` constructor call
- `TupleLiteralNode` -> `TupObject(ast.Tuple)` constructor call
- `IndexNode` -> `ast.Subscript`
- `SliceNode` -> `ast.Subscript` + `ast.Slice`
- `TypeDeclarationNode` with type enforcement -> runtime `typed_assign()`
- `MultiDeclarationNode` -> multiple assignments
- `BinaryOpNode` with string auto-coercion in `+`
- `BinaryOpNode` `in` operator
- `BinaryOpNode` `and`/`or` with truthy semantics
- `BinaryOpNode` `%` (modulus vs string format)
- Method calls on `ArrObject`, `MapObject`, `TupObject`, `str`

### Phase 3: Functions with Type Checking and Builtins

**Goal:** Full function support including parameter types, return types, and all
builtin functions.

**Scope:**
- Parameter type checking in compiled functions
- Return type checking
- All builtin functions: `int()`, `flt()`, `str()`, `bin()`, `god()`, `arr()`,
  `map()`, `tup()`, `range()`, `isinstance()`, `type()`, `regex()`, `getopts()`,
  `exit()`, `exec()`, `disk()`, `input()`
- `RexNode` -> runtime `regex()` call
- Closures and lexical scoping

### Phase 4: Classes and Inheritance

**Goal:** Compile Lyric classes, constructors, methods, inheritance, and access
control using native Python classes.

**Scope:**
- `ClassNode` -> native Python `class` definition
- `constructor()` -> `__init__()` with parameter compilation
- Methods -> Python instance methods with `self`
- `extends` -> Python class inheritance (single inheritance via parentheses)
- `super()` calls in constructor chains
- Access control -> compile-time validation + Python naming conventions
- `isinstance()` -> native Python `isinstance()` (works automatically)
- Member access -> native `self.x` attribute access

**Simplified by decision to not preserve dict-based instance model.** Lyric classes
map almost 1:1 to Python classes. The interpreter's class system will be refactored
to match.

### Phase 5: Module System and Imports

**Goal:** Support `import` (Lyric modules) and `importpy` (Python modules).

**Scope:**
- `ImportNode` -> compile and execute imported `.ly` files
- `ImportPyNode` -> Python `import` with whitelist/blacklist
- `LyricModuleNamespace` binding
- Selective imports with aliases
- Dotted module paths
- Stdlib loading (`lyric.math`, etc.)
- Module scope isolation

### Phase 6: I/O, Exec, and Edge Cases

**Goal:** Complete feature parity with the tree-walking interpreter.

**Scope:**
- `FileOpNode` (file I/O operators `->`, `->>`, `<-`)
- `ExecChainNode` (shell command chains with `|`, `&&`, `||`)
- `DskObject` operations
- `RaiseNode` with full exception type mapping
- `TryNode` with typed catch clauses and Python exception conversion
- Error line/column reporting in compiled code
- REPL support with compiled execution

---

## 5. Compiler Architecture (`lyric/compiler.py`)

### 5.1 Core Class Structure

```python
class LyricCompiler:
    """Compiles Lyric AST to Python ast module nodes."""

    def __init__(self, source_file=None):
        self.source_file = source_file
        self._type_registry = {}  # var_name -> declared_type
        self._function_registry = {}  # func_name -> return_type, param_types
        self._class_registry = {}  # class_name -> class_def

    def compile(self, program: ProgramNode) -> ast.Module:
        """Compile a ProgramNode to a Python ast.Module."""
        body = []
        # Emit runtime import:
        # import lyric.compiled_runtime as _rt
        body.append(self._emit_runtime_import())

        for stmt in program.statements:
            body.extend(self._compile_statement(stmt))

        # If main() was defined, emit a call to it
        if 'main' in self._function_registry:
            body.append(self._emit_main_call())

        module = ast.Module(body=body, type_ignores=[])
        ast.fix_missing_locations(module)
        return module

    def _compile_statement(self, node) -> list[ast.stmt]:
        """Compile a Lyric statement node to Python AST statements."""
        ...

    def _compile_expression(self, node) -> ast.expr:
        """Compile a Lyric expression node to a Python AST expression."""
        ...
```

### 5.2 Dispatch Pattern

Use a dispatch dict (mirroring the interpreter's pattern):

```python
self._stmt_compilers = {
    AssignNode: self._compile_assign,
    TypeDeclarationNode: self._compile_type_decl,
    FunctionNode: self._compile_function_def,
    IfNode: self._compile_if,
    LoopNode: self._compile_loop,
    # ...
}

self._expr_compilers = {
    LiteralNode: self._compile_literal,
    IdentifierNode: self._compile_identifier,
    BinaryOpNode: self._compile_binary_op,
    CallNode: self._compile_call,
    # ...
}
```

### 5.3 Line Number Propagation

Every Lyric AST node carries `line` and `column`. The compiler must set these on
the generated Python AST nodes so that Python tracebacks point to the correct
Lyric source line:

```python
def _loc(self, py_node, lyric_node):
    """Copy source location from Lyric node to Python AST node."""
    py_node.lineno = lyric_node.line
    py_node.col_offset = lyric_node.column
    py_node.end_lineno = lyric_node.line
    py_node.end_col_offset = lyric_node.column
    return py_node
```

---

## 6. Runtime Support Library (`lyric/compiled_runtime.py`)

### 6.1 Core Functions

```python
# Type checking
def typed_assign(type_name: str, value, var_name: str) -> Any
def check_param(type_name: str, value, param_name: str) -> Any
def check_return(type_name: str, value, func_name: str) -> Any

# Lyric-specific operators
def add(left, right)  # string auto-coercion
def mod(left, right)  # string format vs integer modulus
def truthy(value) -> bool  # Lyric truthiness rules

# Container constructors
def make_arr(elements: list) -> ArrObject
def make_map(pairs: dict) -> MapObject
def make_tup(elements: list) -> TupObject

# Module system
def import_lyric_module(module_name, source_file, compiler) -> dict
def import_py_module(module_name, names, unsafe_mode) -> Any

# File I/O
def file_op(operator, left, right) -> None

# Shell execution
def exec_cmd(command) -> int
def exec_chain(elements, operators, input_source, output_target) -> int

# Regex
def rex(pattern) -> RexObject
```

### 6.2 Re-use Strategy

Many runtime objects can be imported directly from the existing codebase:

```python
from lyric.interpreter import ArrObject, MapObject, TupObject, DskObject, RexObject
from lyric.interpreter import LyricModuleNamespace, ReturnValue
from lyric.errors import *
from lyric.pyproxy import PyModuleProxy, PyCallableProxy
from lyric.runtime import *  # all builtins
```

---

## 7. Testing Strategy

### 7.1 Dual-Execution Testing

Every existing test should pass under both the tree-walking interpreter and the
compiled backend. Create a pytest fixture or parametrize decorator:

```python
@pytest.fixture(params=['interpret', 'compile'])
def execute_lyric(request):
    if request.param == 'interpret':
        return run_interpreted
    else:
        return run_compiled
```

### 7.2 Phase-Specific Tests

Each phase adds tests for the constructs it compiles:

- Phase 1: arithmetic, variables, if/else, while/for loops, functions, print
- Phase 2: collections, slicing, type enforcement, string ops
- Phase 3: builtins, regex, parameter/return type checks
- Phase 4: classes, inheritance, access control, isinstance
- Phase 5: import, importpy, module namespaces
- Phase 6: file I/O, exec chains, error reporting

### 7.3 Benchmark Regression Tests

The `lyric/tests/perftest/lyric_benchmark.ly` must produce identical output under
both backends. Timing tests verify the compiled backend is at least 10x faster.

### 7.4 AST Dump Tests

For debugging, add a `--dump-ast` flag that prints the generated Python AST before
compilation. This helps verify correct translation.

---

## 8. Risk Assessment

### 8.1 High Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Scope model mismatch** | Lyric uses a flat `global_scope` dict that gets copied/restored on every function call. Python uses proper lexical scoping with LEGB resolution. Compiled code must match Lyric's scoping behavior exactly. | Phase 1 functions compile to Python functions with explicit parameter passing. Closures may need to use `nonlocal` or cell variables. Extensive scoping tests. The interpreter's scoping model may also be refactored to align with Python's natural scoping. |

### 8.2 Medium Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| **String `+` auto-coercion** | Lyric's `+` does `str(left) + str(right)` if either operand is a string. Python's `+` raises TypeError. Every `+` with unknown types must go through the runtime helper. | Use the runtime helper for `+` when types are unknown. Add a simple type inference pass that avoids the helper when both operands are provably numeric. |
| **Module import side effects** | Lyric's `import` executes a `.ly` file and injects symbols. The compiled backend must compile the imported file too, or fall back to the interpreter. | Phase 5 recursively compiles imported modules. If compilation fails, fall back to interpreted execution for that module. |
| **Error reporting fidelity** | Python tracebacks from compiled code will reference Lyric line numbers but the traceback format will look different. | Wrap `exec()` in a try/except that reformats errors to match the interpreter's error output format. |

### 8.3 Low Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| **CPython version coupling** | The `ast` module API is stable across Python 3.8+. Minor changes occur. | Target Python 3.10+ (which Lyric already requires). Use `ast.Constant` instead of deprecated nodes. |
| **Performance not meeting targets** | If runtime helpers are called too frequently, overhead may prevent reaching near-Python speed. | Profile after Phase 1. Inline common operations directly in the AST without runtime helpers. |

---

## 9. Migration and Compatibility

### 9.1 Backward Compatibility

- The tree-walking interpreter remains the default execution mode.
- The compiled backend is opt-in via `--fast` or `--compile` CLI flag.
- Both backends must produce identical output for all valid Lyric programs.
- When the compiled backend reaches full feature parity and passes all tests,
  it can become the default (with `--interpret` as the fallback flag).

### 9.2 Semantic Differences to Document

1. **Scoping:** Functions have true local scope (Python semantics) rather than
   copy/restore of a global dict. This is more correct behavior.
2. **Performance characteristics:** Compiled code has lower per-operation overhead
   but higher startup cost (compilation step).
3. **Error messages:** Stack traces will include Python-style tracebacks rather than
   the interpreter's custom error formatting.

### 9.3 Incremental Adoption

If the compiler encounters an unsupported construct, it raises a `CompileErrorLyric`
and suggests using `--interpret`. Fail fast with a clear message.

---

## 10. Future Optimizations (Post-MVP)

1. **Type inference pass:** Analyze the AST to determine variable types statically.
   Elide runtime type checks for provably type-safe variables.

2. **Native Python classes:** For Lyric classes without access control or complex
   inheritance, compile directly to Python classes.

3. **Inline caching:** Cache compiled code objects for imported modules.

4. **Constant folding:** Evaluate constant expressions at compile time.

5. **Loop optimization:** Bare `for i in range(n):` without wrapper overhead.

6. **Cython extension:** Compile critical runtime helpers with Cython.

---

## 11. Effort Estimate

| Phase | Estimated Lines | Complexity |
|-------|----------------|------------|
| Phase 1: Core MVP | ~600 | Medium |
| Phase 2: Collections + Types | ~400 | Medium |
| Phase 3: Functions + Builtins | ~300 | Medium |
| Phase 4: Classes | ~250 | Low-Medium |
| Phase 5: Module System | ~400 | High |
| Phase 6: I/O + Edge Cases | ~300 | Medium |
| Testing (ongoing) | ~800 | Low |
| **Total** | **~3300** | |

---

## 12. Success Criteria

1. **Performance:** The `lyric_benchmark.ly` benchmark runs in under 5 seconds
   (from 74 seconds) on the compiled backend.
2. **Correctness:** 100% of existing tests pass under both backends.
3. **Feature parity:** All Lyric language features work identically in both backends.
4. **Maintainability:** The compiler is well-structured with clear mapping between
   Lyric and Python AST nodes.
5. **Graceful degradation:** Unsupported features produce clear error messages
   directing users to the interpreter fallback.

---

## 13. Critical Files Reference

| File | Relevance |
|------|-----------|
| `lyric/ast_nodes.py` | All AST node types the compiler must handle |
| `lyric/interpreter.py` | Reference implementation — every `_evaluate_*` method defines exact semantics |
| `lyric/runtime.py` | Built-in functions available in the compiled runtime |
| `lyric/cli.py` | Entry point where `--fast`/`--compile` flag is added |
| `lyric/pyproxy.py` | Python module proxy system preserved in compiled import path |
