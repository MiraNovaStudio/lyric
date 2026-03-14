# Bytecode Compiler Phase 4 — Classes and Inheritance

## Summary
Lyric classes compile directly to native Python classes. No runtime helpers needed — method dispatch, isinstance(), and attribute access all run at C speed. The interpreter's dict-based instance model is not preserved; this is a deliberate architectural simplification.

## Constructs Added
- `ClassNode` → Python `ast.ClassDef`
- Constructor (`def ClassName(...)`) → `__init__(self, ...)`
- Methods → Python instance methods with `self` prepended as first param
- `based on` inheritance → Python class inheritance via base classes
- Dotted identifiers (`self.name`) → proper `ast.Attribute` chains (read + write)
- Member variables (`var name`) → class-level attributes
- `isinstance(obj, ClassName)` → works natively via Python inheritance

## Key Design Decisions
- **No super().__init__() auto-call** — Lyric constructors typically set all fields directly. Auto-calling super with no args would fail when base constructors require parameters.
- **No access control enforcement** — private/protected deferred to a future optimization pass.
- **Dotted identifier fix** — `IdentifierNode` with dots (e.g., `self.name`) now compiles to proper `Attribute` node chains instead of a single `Name` node.

## Files Modified
- `lyric/compiler.py` — added `_compile_class()`, `_compile_constructor()`, `_compile_method()`, fixed dotted identifier compilation

## Status
✅ Completed
