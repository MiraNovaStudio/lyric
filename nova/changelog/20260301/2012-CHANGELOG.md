# Adhoc — 20260301.2012

## Summary
Fixed a bug where selectively imported Python classes via `importpy` could not have their attributes accessed (e.g., `datetime.now()` failed after `importpy datetime; datetime`). The `PyCallableProxy` wrapper was missing a `__getattr__` method, so attribute access on wrapped classes was blocked.

## Files Changed
- lyric/pyproxy.py — Added `__getattr__` to `PyCallableProxy` to forward attribute access to the underlying callable, enabling class method access (e.g., `datetime.now()`) on selectively imported classes.

## Reason
When using `importpy datetime; datetime`, the `datetime` class was wrapped in `PyCallableProxy` for argument conversion. However, `PyCallableProxy` only implemented `__call__` and `__repr__`, so attribute access like `.now()` raised `AttributeError`. Adding `__getattr__` allows the proxy to forward attribute lookups to the wrapped object while preserving argument conversion on calls.

## Git Commit Hash
`TBD` - Adhoc fix for PyCallableProxy attribute access

## Status
Completed
