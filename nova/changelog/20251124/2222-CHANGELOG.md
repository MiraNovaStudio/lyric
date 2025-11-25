# Changelog - Sprint 8 Task 10: Add obj Type for Class Instances

**Date:** November 24, 2025  
**Time:** 22:22  
**Sprint:** 8  
**Task:** 10  
**Version:** 0.7.0

## Summary

Implemented the `obj` keyword as a type declaration for class instances. The `obj` type provides explicit typing for class instances, complementing the existing type system with support for object-oriented programming patterns.

## Changes Made

### 1. Lexer Changes (`lyric/lyric/lexer.py`)
- Added `'obj'` to the `KEYWORDS` set
- Added `'obj'` to the `TYPE_OR_IDENT` token list (line 261)
- The lexer now recognizes `obj` as both a type keyword and allows it in expression contexts

### 2. Parser Changes (`lyric/lyric/parser.py`)
- Added `'obj'` to the `valid_types` set in `_parse_type_declaration` (line 929)
- Added `'obj'` to the `valid_types` set in `_parse_multi_declaration` (line 962)
- The parser now accepts `obj` in all type declaration contexts

### 3. Interpreter Changes (`lyric/lyric/interpreter.py`)
- Added `obj` type compatibility check in `_is_type_compatible` method (lines 924-925)
- The `obj` type checks if a value is a dictionary with `'__instance_class__'` marker
- This ensures only actual class instances can be assigned to `obj`-typed variables

### 4. Test Suite (`lyric/tests/core-0.7.0/test_obj_type.py`)
Created comprehensive test suite with 11 tests covering:
- Basic class instance declaration with `obj` type
- Method calls on `obj` instances
- Multiple instances of the same class
- Reassignment of `obj` variables
- Interchangeability with `var` type (backward compatibility)
- Type safety: rejection of non-class values (integers, strings, lists, dicts)
- Function parameters typed as `obj`
- Function return type as `obj`
- Storing `obj` instances in `arr` collections

## Test Results

```
============================= test session starts =============================
collected 11 items

lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_declaration_with_class_instance PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_with_methods PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_multiple_instances PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_reassignment PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_with_var_interchangeable PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_error_when_not_class PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_error_with_string PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_error_with_list PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_in_function_parameter PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_function_return_type PASSED
lyric/tests/core-0.7.0/test_obj_type.py::TestObjType::test_obj_type_in_arr PASSED

============================== 11 passed in 0.09s ==============================
```

**Test Pass Rate:** 100% (11/11)

## Usage Examples

### Basic obj Declaration
```lyric
class Person
    def init(str name) {
        self.name = name
    }
+++

obj person = Person("Alice")
var name_value = person.name
```

### obj in Functions
```lyric
class Point
    def init(int x, int y) {
        self.x = x
        self.y = y
    }
+++

def get_x(obj point) {
    return point.x
}

obj create_item(str item_name) {
    return Item(item_name)
}
```

### obj with Collections
```lyric
obj book1 = Book("Book1")
obj book2 = Book("Book2")
arr books = [book1, book2]
```

## Benefits

1. **Type Safety**: Provides explicit type checking for class instances
2. **Code Clarity**: Makes it clear when a variable should hold a class instance
3. **Backward Compatible**: `var` can still be used for class instances
4. **Composable**: Works seamlessly with functions, arrays, and other language features

## Technical Notes

- The `obj` type uses the internal `'__instance_class__'` marker to identify valid class instances
- Type checking happens at assignment time through `_is_type_compatible`
- The implementation maintains full backward compatibility with existing code using `var` for objects

## Files Modified

- `lyric/lyric/lexer.py` - Added `obj` keyword
- `lyric/lyric/parser.py` - Added `obj` to valid types
- `lyric/lyric/interpreter.py` - Added `obj` type compatibility check
- `lyric/tests/core-0.7.0/test_obj_type.py` - New comprehensive test suite

## Status

✅ **Implementation Complete**  
✅ **All Tests Passing (11/11)**  
✅ **Ready for Commit**

