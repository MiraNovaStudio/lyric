# Changelog - Sprint 8 Task 9: Implement `map` Methods (Dictionary API)

**Date:** November 24, 2025  
**Time:** 21:39  
**Task:** Sprint 8 Task 9 - Implement `map` Methods (Dictionary API)  
**Status:** ✅ Complete

## Summary

Implemented a comprehensive method-based API for the `map` type (dictionaries) by creating the `MapObject` wrapper class. Added 14 dictionary methods covering mutation, query, and utility operations. Implemented support for the `in` operator for membership checks. Updated the parser to recognize `in` as a comparison operator. All 182 Sprint 8 tests now pass with 100% success rate.

## Changes Made

### 1. Core Implementation (`lyric/lyric/interpreter.py`)

#### Created `MapObject` Class
- Wrapper class for Python dictionaries with method-based API
- Internal storage using `self.elements` attribute
- Implements `__getitem__`, `__setitem__`, `__iter__`, `__contains__` for native Python operations

#### Mutation Methods (7)
1. **`clear()`** - Remove all items from the dictionary
2. **`update(other: MapObject)`** - Merge another map into current map
3. **`pop(key, default=None)`** - Remove and return value for key
4. **`popitem()`** - Remove and return last key-value pair as `ArrObject`
5. **`setdefault(key, default=None)`** - Get value or set default if missing

#### Query Methods (5)
1. **`get(key, default=None)`** - Return value for key with optional default
2. **`keys()`** - Return `ArrObject` of all keys
3. **`values()`** - Return `ArrObject` of all values
4. **`items()`** - Return `ArrObject` of (key, value) pairs
5. **`copy()`** - Return shallow copy of the map

#### Built-in Functions as Methods (2)
1. **`len()`** - Return number of items in the dictionary
2. **`sorted(reverse=False)`** - Return `ArrObject` of sorted keys

#### Static Methods (1)
1. **`fromkeys(seq, value=None)`** - Create new map from sequence of keys

### 2. Parser Changes (`lyric/lyric/parser.py`)

- **Added `in` operator support** in `_parse_comparison()`
  - Recognizes `IN` token as a comparison operator
  - Enables syntax: `"key" in map_obj`

### 3. Interpreter Updates (`lyric/lyric/interpreter.py`)

- **Updated `_evaluate_dict_literal()`** - Returns `MapObject` instead of plain `dict`
- **Updated `_evaluate_function_call()`** - Handles `MapObject` method calls
- **Updated `_evaluate_index()`** - Supports `MapObject` indexing
- **Updated `_evaluate_assignment()`** - Supports `MapObject` indexed assignment
- **Updated `_evaluate_iterator_loop()`** - Iterates over `MapObject` keys
- **Updated `_is_type_compatible()`** - Checks for `MapObject` for `map` type
- **Updated `_evaluate_binary_operation()`** - Implements `in` operator for membership checks

### 4. Runtime Function Updates (`lyric/lyric/runtime.py`)

Updated all casting functions to handle `MapObject`:
- **`int_builtin()`** - Returns `len(value.elements)` for `MapObject`
- **`float_builtin()`** - Returns `float(len(value.elements))` for `MapObject`
- **`str_builtin()`** - Returns string representation of `MapObject`
- **`arr_builtin()`** - Converts `MapObject` to `ArrObject` of values
- **`map_builtin()`** - Returns `MapObject` wrapper for dictionaries

### 5. Test Suite (`lyric/tests/core-0.7.0/test_map_methods.py`)

Created comprehensive test suite with 25 tests covering:
- **Mutation methods:** `clear`, `update`, `pop`, `popitem`, `setdefault`
- **Query methods:** `get`, `keys`, `values`, `items`, `copy`
- **Built-in methods:** `len`, `sorted`
- **`in` operator:** membership checks in standalone expressions and conditionals
- **Iteration:** looping over map keys
- **Indexing:** accessing and assigning values by key
- **Error handling:** missing keys, empty maps

## Files Modified

- `lyric/lyric/interpreter.py` - Added `MapObject` class, updated evaluation methods
- `lyric/lyric/parser.py` - Added `in` operator to comparison parsing
- `lyric/lyric/runtime.py` - Updated casting functions for `MapObject`
- `lyric/lyric/lexer.py` - Confirmed `in` keyword already present
- `lyric/tests/core-0.7.0/test_map_methods.py` - Created (25 tests)

## Test Results

```
============================= 182 passed in 0.22s =============================
```

- **All Sprint 8 tests passing:** ✅ 182/182 (100%)
- **New map methods tests:** ✅ 25/25 (100%)
- **No regressions:** All existing tests continue to pass

## Breaking Changes

None. This is an additive change that enhances the `map` type with a method-based API while maintaining backward compatibility.

## Implementation Details

### Internal Attribute Naming
- Used `self.elements` instead of `self.items` to avoid conflict with the `items()` method
- This matches the pattern used in `ArrObject` for consistency

### Method Return Types
- Methods that return collections (keys, values, items, sorted) return `ArrObject` instances
- This allows chaining method calls and maintaining type consistency
- Example: `data.keys().len()` works seamlessly

### `in` Operator Implementation
- Added to `_parse_comparison()` at the same precedence level as other comparison operators
- Evaluates using Python's built-in `in` operator via `__contains__` method
- Works with conditionals, assignments, and expressions

### Error Handling
- Uses `KeyErrorLyric` for missing key errors (not `RuntimeErrorLyric`)
- Uses `TypeErrorLyric` for type mismatches in method arguments
- Provides clear, descriptive error messages

## Next Steps

Sprint 8 Task 9 is complete. All tasks in Sprint 8 (yield-0.7.0) are now complete.

