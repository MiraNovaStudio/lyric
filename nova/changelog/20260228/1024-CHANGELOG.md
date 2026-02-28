# Adhoc Interpreter Fix — 20260228.1024

## Summary
Fixed two root-cause bugs in the Lyric interpreter that caused nearly all Python instance method calls
to fail when tested via `core_datetime.ly`. After the fix every datetime test outputs PASS.

## Files Changed
- `lyric/interpreter.py` — Two targeted fixes:
  1. `_evaluate_try_statement`: each try/catch/finally body now pushes a fresh scope and pops it in
     a Python `finally:` block. This prevents `CompileErrorLyric("Variable already declared")` when
     sequential try blocks reuse the same variable name (e.g. `var dt = ...` across multiple blocks).
  2. `_evaluate_function_call`: added `elif hasattr(current_obj, method_name)` handler before the
     `elif callable` branch in the final method-dispatch chain, and a matching `elif hasattr` fallback
     in the member-path navigation loop. This enables instance method calls on arbitrary Python objects
     such as `datetime.datetime` instances (e.g. `dt.isoformat()`, `dt.weekday()`).

## Reason
The `core_datetime.ly` adhoc test revealed two systematic failures:
- Sequential try blocks sharing the same variable name triggered a `CompileErrorLyric` that was
  silently caught by the catch clause, masking the real test intent.
- Raw Python instance objects (returned from e.g. `datetime.datetime.now()`) fell through all
  specific-type checks (dict, PyModuleProxy, RexMatch, ArrObject, etc.) to the final `else` error
  branch because Python instances are not callable and do not define `__getattr__` explicitly.

## Git Commit Hash
`TBD` - Adhoc Interpreter Fix Implementation

## Status
✅ Completed
