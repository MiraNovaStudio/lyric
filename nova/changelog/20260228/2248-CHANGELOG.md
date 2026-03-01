# Adhoc Bugfix: isinstance inheritance — 20260228.2248

## Summary
Fixed `isinstance()` returning `False` for parent classes in inheritance chains. `isinstance(dog, Animal)` now correctly returns `True` when `Dog` inherits from `Animal`.

## Files Changed
- lyric/interpreter.py — Added `_isinstance_with_inheritance` override in `__init__` that walks the `__base_class__` chain via the class registry instead of only checking direct class name match

## Reason
The original `isinstance_builtin` in `runtime.py` only performed a direct class name comparison (`instance_class == target_name`), never walking the inheritance chain. This caused `isinstance(dog, Animal)` to return `False` even though `Dog based on Animal`. The fix overrides `isinstance` in the interpreter with a closure that has access to `self.classes`, walking up `__base_class__` links until a match is found or the chain is exhausted. Supports multi-level inheritance (e.g., Puppy → Dog → Animal).

## Git Commit Hash
`TBD` - Adhoc Bugfix: isinstance inheritance

## Status
✅ Completed
