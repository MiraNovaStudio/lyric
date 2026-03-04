# Sprint10 Task5 Summary — obj Type

## Task
Add the `obj` type as a primitive type in Lyric for declaring class instance variables.

## Status
✅ Completed

## Key Accomplishments
- Confirmed that `obj` was already wired into the lexer (keyword), parser (valid_types), and interpreter (_is_type_compatible) from prior groundwork
- Verified that `obj account = BankAccount(100)` parses and executes correctly
- Verified that type enforcement correctly rejects non-instance values (int, str, arr, map, flt, bool)
- Verified that `var` continues to work unchanged for dynamic typing
- Wrote 17 unit tests covering all required scenarios

## Test Coverage
- `test_obj_declaration_and_method_call` — basic obj declaration and method invocation
- `test_obj_method_modifies_state` — state mutation via method calls
- `test_obj_instance_variable_access` — dot-notation access to instance fields
- `test_multiple_obj_variables` — multiple independent obj variables
- `test_obj_with_string_methods` — methods returning strings
- `test_obj_with_inheritance` — obj holds a subclass instance with overridden methods
- `test_obj_reassignment_to_new_instance` — reassigning obj to a new instance
- `test_obj_returned_from_function` — obj from a factory function
- `test_obj_in_main_function` — obj usage inside main()
- `test_var_still_holds_class_instance` — regression: var still works
- `test_var_holds_mixed_types` — regression: var accepts any type
- `test_obj_rejects_int` — type enforcement: int rejected
- `test_obj_rejects_str` — type enforcement: str rejected
- `test_obj_rejects_arr` — type enforcement: arr rejected
- `test_obj_rejects_map` — type enforcement: map rejected
- `test_obj_rejects_float` — type enforcement: float rejected
- `test_obj_rejects_bool` — type enforcement: bool rejected

## Files Created/Modified
- `lyric/tests/core-0.9.0/test_obj_type_sprint10.py` — new test file (17 tests)

## Full Test Suite
1131 tests passed, 0 failures.

## Changelog
See `nova/changelog/20260228/1412-CHANGELOG.md`
