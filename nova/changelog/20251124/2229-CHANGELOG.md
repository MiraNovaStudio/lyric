# Changelog - Sprint 8 Task 11: Add bin() and god() Casting Functions

**Date:** November 24, 2025  
**Time:** 22:29  
**Sprint:** 8  
**Task:** 11  
**Version:** 0.7.0

## Summary

Implemented `bin()` and `god()` casting functions to convert values to boolean types following Python's truthiness rules. Both functions are aliases and behave identically, providing boolean casting for all Lyric types.

## Changes Made

### 1. Runtime Changes (`lyric/lyric/runtime.py`)

Added two new built-in functions:

**bin_builtin()**
- Converts any value to boolean using Python's `bool()` function
- Follows standard truthiness rules:
  - `0`, `0.0`, empty string `""`, empty collections `[]`, `{}` → `False`
  - Non-zero numbers, non-empty strings/collections → `True`

**god_builtin()**
- Identical to `bin_builtin()` - alias for consistency with Lyric's `god` type
- Uses same conversion logic as `bin()`

Both functions registered in `register_builtins()`:
```python
env['bin'] = bin_builtin
env['god'] = god_builtin
```

### 2. Test Suite (`lyric/tests/core-0.7.0/test_bin_god_casting.py`)

Created comprehensive test suite with 26 tests covering:

**TestBinCasting** (13 tests):
- Non-zero integers → `True`
- Zero integers → `False`
- Negative integers → `True`
- Non-zero floats → `True`
- Zero floats → `False`
- Non-empty strings → `True`
- Empty strings → `False`
- Non-empty arrays → `True`
- Empty arrays → `False`
- Non-empty maps → `True`
- Empty maps → `False`
- Boolean values (`True`/`False`)

**TestGodCasting** (13 tests):
- Identical test coverage as `TestBinCasting`
- Validates that `god()` behaves exactly like `bin()`

## Test Results

```
============================= 26 passed in 0.12s ==============================
```

**Test Pass Rate:** 100% (26/26)

## Usage Examples

### Example 1: Integer Casting
```lyric
int x = 5
god result1 = bin(x)  # True
print result1

int y = 0
god result2 = god(y)  # False
print result2
```

### Example 2: String Casting
```lyric
str name = "Alice"
god has_name = bin(name)  # True

str empty = ""
god is_empty = god(empty)  # False (empty string is falsy)
```

### Example 3: Collection Casting
```lyric
arr items = [1, 2, 3]
god has_items = bin(items)  # True

arr empty_list = []
god is_empty = god(empty_list)  # False
```

### Example 4: Map Casting
```lyric
map data = {"key": "value"}
god has_data = bin(data)  # True

map empty_dict = {}
god is_empty = god(empty_dict)  # False
```

## Truthiness Rules

The casting functions follow Python's truthiness rules:

| Value Type | Example | Result |
|-----------|---------|--------|
| Non-zero int | `5`, `-10` | `True` |
| Zero int | `0` | `False` |
| Non-zero float | `3.14`, `-0.1` | `True` |
| Zero float | `0.0` | `False` |
| Non-empty string | `"hello"` | `True` |
| Empty string | `""` | `False` |
| Non-empty arr | `[1, 2]` | `True` |
| Empty arr | `[]` | `False` |
| Non-empty map | `{"a": 1}` | `True` |
| Empty map | `{}` | `False` |
| Boolean | `True`, `False` | Same value |

## Benefits

1. **Explicit Boolean Conversion**: Clear way to convert values to boolean
2. **Type Consistency**: Both `bin` and `god` available for user preference
3. **Standard Behavior**: Follows Python's well-understood truthiness rules
4. **Universal**: Works with all Lyric types (int, flt, str, arr, map, god/bin)

## Technical Notes

- Both functions internally call Python's `bool()` for conversion
- `bin()` and `god()` are completely equivalent - choice is stylistic
- Maintains consistency with Lyric's dual naming: `god`/`bin` for boolean type
- No special handling needed - Python's truthiness rules apply universally

## Files Modified

- `lyric/lyric/runtime.py` - Added `bin_builtin` and `god_builtin` functions and registered them
- `lyric/tests/core-0.7.0/test_bin_god_casting.py` - New comprehensive test suite

## Status

✅ **Implementation Complete**  
✅ **All Tests Passing (26/26)**  
✅ **Ready for Commit**

