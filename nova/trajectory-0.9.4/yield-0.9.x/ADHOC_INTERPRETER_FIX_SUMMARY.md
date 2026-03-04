# Adhoc Interpreter Fix Summary — Python Instance Method Dispatch & Try-Scope

## Task
Fix interpreter bugs exposed by the `core_datetime.ly` adhoc test. Two root causes were identified
and fixed so that every datetime test outputs PASS.

## Root Causes Fixed

### Bug 1 — `_evaluate_try_statement`: no scope push/pop
Sequential try blocks that reused the same variable name (e.g. `var dt = ...` in block 1, then
`var dt = ...` in block 2) triggered `CompileErrorLyric("Variable already declared")` because the
try body ran in the outer scope. The exception was silently caught by the catch clause and printed
as `ERROR`, masking nearly all tests.

**Fix:** Push a fresh scope before each try/catch/finally body and pop it in a Python `finally:`
block to guarantee cleanup even on exception.

### Bug 2 — `_evaluate_function_call`: missing generic Python instance handler
Raw Python instance objects (e.g. a `datetime.datetime` value stored in `var dt`) fell through all
specific-type checks (dict, PyModuleProxy, RexMatch, ArrObject, MapObject, DskObject) and reached
the `callable` check — which is False for instances — then fell to the `else` error branch.

**Fix:**
- Added `elif hasattr(current_obj, method_name)` branch before `elif callable` in the final
  method-dispatch block. Uses `getattr` + `callable(method)` to invoke the method.
- Added matching `elif hasattr(current_obj, member_name)` fallback in the member-path navigation
  loop, enabling chained access like `result.field` on Python-backed objects.

## Key Accomplishments
- All 130+ datetime tests in `core_datetime.ly` now output PASS
- Full coverage of `datetime.datetime`, `datetime.date`, `datetime.time`, `datetime.timedelta`,
  `datetime.timezone` — all constructors, instance methods, class methods, and constants
- 1112 pytest tests: 0 regressions

## Files Modified
- `lyric/interpreter.py` — `_evaluate_try_statement` (scope push/pop), `_evaluate_function_call`
  (hasattr fallback in member-path loop and final dispatch chain)

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260228/1024-CHANGELOG.md`
