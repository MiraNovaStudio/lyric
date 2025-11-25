# Sprint8 Task6 — 20251124.2045

## Summary
Completed comprehensive casting rules for the `map` type by creating thorough test coverage. The actual implementation was completed as part of Task 5, which included all necessary map casting functionality. Task 6 focuses on validating and documenting these capabilities.

## Files Changed
- `lyric/tests/core-0.7.0/test_map_casting.py` — Created comprehensive test suite with 21 tests covering all map casting scenarios

## Implementation Details

### Casting TO Other Types (from map)
All implementations were completed in Task 5:

1. **`int(map)`** — Returns the number of keys in the dictionary
   - Example: `int({"a": 1, "b": 2, "c": 3})` → `3`
   - Works with empty maps: `int({})` → `0`

2. **`float(map)`** — Returns the number of keys as a float
   - Example: `float({"x": 10, "y": 20})` → `2.0`
   - Works with empty maps: `float({})` → `0.0`

3. **`str(map)`** — Returns string representation of the dictionary
   - Example: `str({"a": 1})` → `"{'a': 1}"`
   - Note: Does not return variable name (would require interpreter-level tracking)

4. **`arr(map)`** — Converts dictionary values to a list
   - Example: `arr({"a": 1, "b": 2, "c": 3})` → `[1, 2, 3]`
   - Only extracts values, keys are discarded
   - Empty dict converts to empty list

### Casting FROM Other Types (to map)

1. **`map(arr)`** — Converts array to dictionary with string keys "1", "2", "3", etc.
   - Example: `map([100, 200, 300])` → `{"1": 100, "2": 200, "3": 300}`
   - Works with mixed-type arrays
   - Empty array converts to empty dict

2. **`map(str)`** — Not supported, raises clear error
   - Throws `RuntimeErrorLyric` with helpful message
   - Error: "Cannot directly convert str to map"

3. **`map(map)`** — Returns the same dictionary (identity operation)
   - Preserves reference to original dict

### Design Decisions

#### Why `arr(map)` Extracts Values Only
Dictionaries contain both keys and values, but arrays are ordered lists without keys. When converting a map to an array, only the values are preserved because:
1. Arrays cannot store key-value associations
2. Value preservation is more useful for data processing
3. Keys can be retrieved separately if needed via `keys()` function

#### String Key Indexing for `map(arr)`
Arrays are converted to dictionaries with string keys starting from "1" (not "0") to provide human-friendly 1-based indexing in dictionaries while maintaining 0-based array indexing.

## Reason
Completes the type interoperability system for the `map` type, enabling flexible data transformations between dictionaries and other Lyric types. This allows developers to easily convert between collection types for different use cases.

## Git Commit Hash
`TBD` - Sprint8 Task6 Implementation

## Status
✅ Completed

## Test Results
All 102 tests in core-0.7.0 pass (100% pass rate)
- 21 new map casting tests
- All previous tests still passing

## Examples

### Length Conversions
```lyric
map config = {"host": "localhost", "port": 8080, "debug": true}
int count = int(config)          # 3
flt count_float = float(config)  # 3.0
```

### Map to Array Conversion
```lyric
map scores = {"alice": 95, "bob": 87, "charlie": 92}
arr values = arr(scores)
print int(values)  # 3
```

### Array to Map Conversion
```lyric
arr data = [10, 20, 30, 40]
map indexed = map(data)
print indexed["1"]  # 10
print indexed["4"]  # 40
```

### Chained Conversions
```lyric
map original = {"a": 10, "b": 20, "c": 30}
arr values = arr(original)
map reconstructed = map(values)
print int(reconstructed)  # 3
```

### Casting in Expressions
```lyric
map items = {"x": 1, "y": 2, "z": 3, "w": 4}
flt result = 10 / float(items)
print result  # 2.5
```

