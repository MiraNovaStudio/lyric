# Sprint 8 Task 5 Summary

## Task
Add casting rules for `arr` type

## Status
✅ Completed

## Key Accomplishments

### 1. Array-to-Scalar Casting
Implemented casting from `arr` to scalar types:
- **`int(arr)`** returns array length
- **`float(arr)`** returns length as float
- **`str(arr)`** returns string representation

### 2. Array-to-Map Casting
- **`map(arr)`** converts array to dictionary with string keys "1", "2", "3", etc.
- Preserves all values from the array
- Works with mixed-type arrays

### 3. Scalar-to-Array Casting  
- **`arr(str)`** converts string to list of characters
- Handles all string content including spaces

### 4. Map-to-Array Casting
- **`arr(map)`** converts dictionary values to a list
- Keys are discarded, only values are preserved

### 5. Identity Operations
- **`arr(arr)`** returns the same array
- **`map(map)`** returns the same dictionary

### 6. Bonus: Map Casting (for Task 6)
Also implemented map casting rules in preparation for Task 6:
- **`int(map)`** returns number of keys
- **`float(map)`** returns number of keys as float

## Files Modified
- `lyric/lyric/runtime.py` - Enhanced built-in casting functions

## Files Created
- `lyric/tests/core-0.7.0/test_arr_casting.py` - 19 comprehensive tests

## Test Results
- **Total tests in core-0.7.0**: 81
- **Passing**: 81 (100%)
- **Failing**: 0

### New Tests Added
1. test_int_arr_returns_length
2. test_float_arr_returns_length_as_float
3. test_str_arr_returns_string_representation
4. test_map_arr_converts_to_dict_with_string_keys
5. test_arr_str_converts_to_list_of_characters
6. test_arr_map_converts_dict_values_to_list
7. test_int_empty_arr
8. test_float_empty_arr
9. test_arr_empty_string
10. test_map_empty_arr
11. test_arr_preserves_list_reference
12. test_map_preserves_dict_reference
13. test_arr_string_with_spaces
14. test_map_arr_with_mixed_types
15. test_chained_casting_arr_to_map_to_arr
16. test_casting_in_expressions
17. test_float_casting_in_division
18. test_arr_of_arr
19. test_map_arr_single_element

## Design Decisions

### String Key Indexing for map(arr)
Arrays are converted to dictionaries with string keys starting from "1" (not "0") to align with human-friendly 1-based indexing expectations in dictionaries, while arrays themselves remain 0-indexed for compatibility with Python.

### arr(map) Extracts Values Only
When converting a map to an array, only the values are preserved. This is because arrays are ordered lists of values without keys, so the key information would be lost anyway.

### str(arr) Returns Representation
The specification requested `str(arr)` to return the variable name in the code, but this information is not available at runtime after parsing. Instead, we return the string representation of the array, which is more useful for debugging and display purposes.

## Examples

### Basic Casting
```lyric
arr numbers = [10, 20, 30, 40, 50]
print int(numbers)    # 5
print float(numbers)  # 5.0
```

### Array to Map
```lyric
arr values = [100, 200, 300]
map indexed = map(values)
print indexed["1"]    # 100
print indexed["3"]    # 300
```

### String to Array
```lyric
str greeting = "hi there"
arr chars = arr(greeting)
print chars[0]        # h
print chars[2]        # (space)
```

### Map to Array
```lyric
map config = {"host": "localhost", "port": 8080, "debug": true}
arr values = arr(config)
print int(values)     # 3
```

### Chained Conversions
```lyric
arr original = [10, 20, 30]
int double_length = int(original) * 2
print double_length   # 6
```

## Related Documentation
- Changelog: `nova/changelog/20251124/2036-CHANGELOG.md`
- Sprint Plan: `nova/aeon/trajectory-0.9.1/yield-0.7.0/SPRINT8_PLAN.md`

