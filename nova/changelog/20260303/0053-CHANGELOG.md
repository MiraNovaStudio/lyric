# Adhoc: Widen importpy Support for Python Collection Types — 20260303.0053

## Summary
Extended Lyric's interpreter to support index access, index assignment, method calls, and `.len()` on Python objects that implement standard `collections.abc` protocols (Mapping, Sequence). This enables full interop with `collections.Counter`, `collections.deque`, `collections.OrderedDict`, `collections.namedtuple`, and `collections.ChainMap` via `importpy`. Also added a vet script for the `collections` module (50/50 PASS).

## Files Changed
- lyric/interpreter.py — Added `from collections.abc import Mapping, Sequence` import; widened `_evaluate_index()` to accept Mapping and Sequence types; widened index assignment in `_evaluate_assignment()` for both simple and member+index paths; added generic `.len()` support for any Python object with `__len__`; added `__missing__` check for dict subclasses (Counter, defaultdict) to allow native default-value behavior
- lyric/tests/python_modules/core_collections.ly — New vet script exercising Counter, defaultdict, deque, OrderedDict, namedtuple, and ChainMap (50 tests)

## Reason
The `importpy` bridge only recognized Lyric-native types (ArrObject, MapObject, dict, list) for indexing and assignment operations. Python collection types that implement standard protocols (Mapping, Sequence) were rejected with misleading type errors. This change uses protocol-based isinstance checks to support any conforming Python type, current and future.

## Known Limitation
`defaultdict` auto-creation on missing keys does not work because the factory function callback (e.g., `int()`, `list()`) executes in Python's runtime, which cannot call back into Lyric built-in functions. Explicit assignment and retrieval of existing keys works fine.

## Git Commit Hash
`TBD` - Adhoc importpy Protocol-Based Collection Support

## Status
✅ Completed
