# Lyric

Lyric is a gradually typed, interpreted programming language built in Python, designed for clarity and expressive syntax. Type declarations are optional and enforced at runtime — variables declared with a type (`int`, `str`, `flt`, etc.) are strongly checked on assignment, while `var` opts into dynamic typing. It is developed and maintained by **MiraNova Studios**.

**Current version:** 0.8.4 (Pre-Alpha)
**Website:** [lyric-lang.org](https://lyric-lang.org)

---

## Installation

```bash
pip install lyric-lang
```

After installation the `lyric` command is available globally.

```bash
lyric run program.ly
# or
lyric program.ly
```

Lyric programs use the `.ly` file extension. Shebang lines (`#!/usr/bin/env lyric`) are supported.

---

## Architecture

The interpreter is implemented as a classical pipeline: source text flows through the lexer, parser, and interpreter in sequence. All stages are implemented from scratch in pure Python with no parser-generator dependencies.

```
lyric/
├── lexer.py          # Tokenizer — converts source text into a token stream
├── parser.py         # Recursive descent parser — produces an AST
├── ast_nodes.py      # AST node definitions
├── interpreter.py    # Tree-walking interpreter with lexical scoping
├── runtime.py        # Built-in functions and type coercions
├── pyproxy.py        # Python interoperability layer (importpy bridge)
├── errors.py         # Lexer, parser, and runtime error types
└── cli.py            # Command-line interface
```

### Lexer

The lexer performs single-pass tokenization with support for string literals (single and double quotes), regex literals (`/pattern/flags`), shebang lines, and inline comments (`#`). Tokens carry line and column positions used for error reporting.

### Parser

The parser is a hand-written recursive descent parser that produces a typed AST. It handles operator precedence, optional colon syntax across all control structures, and both `given`/`done` and `for`/`end` loop forms. The parser enforces top-level restrictions (e.g. bare expressions outside functions are rejected).

### Interpreter

The interpreter walks the AST directly. Scope is managed via a linked chain of environment frames — each function call and block pushes a new frame, and variable resolution walks the chain outward. Class instances are represented as environment frames with a `self` reference. Method resolution follows the inheritance chain at dispatch time.

### Type System

Lyric uses optional type declarations enforced at runtime. Variables declared with a specific type are strongly checked on every assignment and function call; `var` disables enforcement for that binding. The core types are:

| Type  | Description |
|-------|-------------|
| `int` | Integer |
| `flt` | Float |
| `str` | String |
| `var` | Dynamic (no enforcement) |
| `god` | Boolean (honoring Kurt Gödel) |
| `bin` | Boolean (alternative form) |
| `rex` | Regular expression literal (`/pattern/`) |
| `arr` | Array (ordered collection) |
| `map` | Dictionary / key-value map |
| `obj` | Generic object reference |
| `dsk` | Disk / file handle type |

Type coercion is available via casting functions (`int()`, `str()`, `flt()`, etc.) and explicit cast operators. The `var` type opts out of enforcement for dynamic use cases.

### Classes and Inheritance

Classes are defined with `class Name(Parent):` syntax. Constructors use `init()`. Constructor chaining (`super`) and single inheritance are supported. Access control is enforced via naming conventions. Method resolution walks the inheritance chain.

### Python Interoperability

The `importpy` keyword loads any installed Python package through `pyproxy.py`, which wraps Python objects for use inside the Lyric runtime. Return values are translated back to Lyric types where possible. This layer is intentionally kept separate from native `import`, which resolves Lyric modules.

### Error Reporting

All errors (lexer, parser, runtime) carry source position information. Error messages include file name, line number, and a formatted excerpt of the offending line.

---

## Language Features

- Typed variable declarations: `int x = 5`, `str name = "lyric"`, `var x = anything`
- Functions with typed parameters: `def greet(str name, int age) { ... }`
- Classes with `init()` constructors, inheritance, and access control
- Control flow: `if`/`elif`/`else`, `given`/`done` and `for`/`end` loops, `break`/`continue`, `case`
- Exception handling: `try`/`catch`/`finally`/`fade` with typed exception binding
- Regular expressions as first-class values with `rex` type and `/pattern/` literals
- `importpy` for Python library access; native `import` for Lyric modules
- `exec()` with I/O redirection via file operators
- `getopts` for CLI argument parsing within scripts
- Dual print syntax, mixed quote strings, multi-variable declarations

See the [language specification](https://lyric-lang.org) for full syntax reference.

---

## Module System

Lyric supports two import mechanisms. Native Lyric modules (`import name`) are resolved by a `ModuleLoader` that searches the runtime module path and caches loaded modules. Python packages (`importpy name`) are loaded through the `pyproxy` bridge as a secondary mechanism. Resolution order is: native Lyric module → built-in standard library → Python bridge → `ModuleNotFoundError`.

---

## Development

Requires Python 3.8 or newer.

```bash
pip install pytest flake8 build twine
pytest lyric/tests/
```

Tests are organized under `lyric/tests/` by version milestone (e.g. `core-0.8.0/`). Run the full suite with `pytest` from the project root.

---

## License and Credits

Lyric is developed by **MiraNova Studios**.

Licensed under the MiraNova Software License. See the `LICENSE` file for full terms. All rights reserved — © 2025–2026 MiraNova Studios.
