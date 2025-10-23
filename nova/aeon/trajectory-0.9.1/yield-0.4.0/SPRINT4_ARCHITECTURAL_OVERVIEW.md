# 🧠 Lyric Source Structure — Architectural Overview (v0.4.0)

**Author:** ChatGPT (Architect)  
**Engineer:** Claude (Lead Developer)  
**Version:** dev-core-0.4.0  
**Last Updated:** October 22, 2025  

---

## 🧩 1. `lexer.py` — *Lexical Analysis*
**Purpose:** Converts raw source code into tokens.

- Scans the source character by character.  
- Emits tokens like `IDENT`, `INT`, `STRING`, `COLON`, etc.  
- Handles:
  - Keywords (`def`, `class`, `if`, `given`, `done`, etc.)  
  - Literals (`True`, `False`, numbers, strings)  
  - Single and multi-character operators (`==`, `>=`, `+++`).  
- Tracks **line** and **column** for each token — used later in precise error messages.

✅ **Result:** A list of token objects with metadata (type, value, line, col).

---

## 🧱 2. `parser.py` — *Syntactic Analysis*
**Purpose:** Transforms tokens into a structured Abstract Syntax Tree (AST).

- Implements a **recursive descent parser**.  
- Converts tokens into AST node objects (`FunctionNode`, `IfNode`, `ClassNode`, etc.).  
- Supports **optional colon syntax** after headers (`def`, `class`, `if`, `given` …).  
- Enforces balanced `{}` braces and valid structure.  
- Uses helper methods:
  - `_match()` – optional token consumption  
  - `_consume()` – required token or throws `ParseError`  
  - `_parse_expression()` – operator precedence chain  
- Produces a single `ProgramNode` containing all top-level statements.

✅ **Result:** A tree-like structure ready for interpretation.

---

## ⚙️ 3. `ast_nodes.py` — *Abstract Syntax Tree Definitions*
**Purpose:** Defines all the node types that form the internal representation of Lyric code.

Each node (e.g., `FunctionNode`, `AssignNode`, `IfNode`) stores:
- Structural info (name, parameters, body, expressions)  
- Source location (line, col)  
- Behavior hooks for traversal or evaluation.

This layer provides **clarity and debuggability** for both the interpreter and future tools like Nova.

---

## 🧮 4. `interpreter.py` — *Execution Engine*
**Purpose:** Walks the AST and executes the program.

- Manages **scopes** and variable lifetimes.  
- Evaluates expressions, calls functions, resolves identifiers.  
- Enforces **runtime type checking** (based on declarations or inferred types).  
- Handles:
  - `try` / `catch` / `finally` / `fade`  
  - `given` loops  
  - `return` propagation  
  - Class instantiation (`+++`)  
- Integrates with `pyproxy.py` for importing Python modules (`importpy`).

✅ **Result:** Executes Lyric source and produces real runtime output.

---

## 🪄 5. `runtime.py` — *Built-in Functions*
**Purpose:** Provides standard library-like capabilities (similar to Python’s built-ins).

Functions include:
- `print`, `input`, `len`, `append`, `keys`, `values`, `range`, `type`, `isinstance`, etc.  
- Registered into the interpreter’s global environment at startup via `register_builtins()`.

✅ **Result:** A consistent base runtime for Lyric scripts.

---

## 🌉 6. `pyproxy.py` — *Python Interoperability*
**Purpose:** Bridges Lyric and Python.

- `PyModuleProxy` wraps imported Python modules (`importpy math`).  
- Exposes functions, attributes, and constants safely.  
- Converts Python errors into `RuntimeErrorLyric` for consistency.

✅ **Result:** Seamless access to Python’s standard library within Lyric.

---

## ⚠️ 7. `errors.py` — *Unified Error System*
Defines custom exception types:
- `LexError`  
- `ParseError`  
- `SyntaxErrorLyric`  
- `RuntimeErrorLyric`  
- `NameErrorLyric`

Each carries `line`, `column`, and `filename` for precise, human-readable messages.

✅ **Result:** Standardized, user-friendly error handling across all modules.

---

## 🧭 8. `cli.py` — *Command-Line Interface*
**Purpose:** Entry point for running `.ly` files.

Usage:
```bash
lyric run myfile.ly
```

Handles:

- File reading and validation

- Lexing, parsing, and evaluating

- Error display with proper line context

Result: A complete runtime pipeline from command line → executed code.

### Execution Flow Summary

```
source.ly
   ↓
lexer.py        → tokenize
   ↓
parser.py       → parse into AST
   ↓
interpreter.py  → evaluate (using runtime.py + pyproxy.py)
   ↓
console output
```

## Design Principles

- Readability: Clear separation between syntax, semantics, and runtime logic.

- Line-aware: Every node and exception maps back to exact source lines.

- Extensible: Easy to add new keywords or language features (like import).

- Educational clarity: Ideal for students and early developers to study.


## Summary:

Lyric’s architecture is modular, transparent, and easy to extend. Each subsystem — from lexer to interpreter — is designed for both clarity and precision, reflecting MiraNova Studios’ guiding principles of simplicity and elegance in software design.

**AUTHOR** ChatGPT