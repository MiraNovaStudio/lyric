# Changelog - Module-Level Restrictions and Variable Imports

**Date:** November 25, 2025  
**Time:** 00:30 UTC  
**Sprint:** 8 (yield-0.7.0)  
**Type:** Language Feature & Breaking Change

## Summary

Enforced module-level code restrictions: only variable declarations, functions, and classes are allowed at the top level. Control structures and function calls must be inside functions. Also updated the import system to support importing module-level variables.

## Changes Made

### 1. Parser Changes (`lyric/lyric/parser.py`)
- Added `is_top_level` flag to track when parsing module-level code
- Modified `_parse_statement()` to enforce top-level restrictions:
  - Control structures (`if`, `given`, `try`) not allowed at module level
  - `return` statements not allowed at module level
  - Function calls and expressions not allowed at module level
  - Only variable declarations, functions, classes, and imports allowed
- Updated `_parse_func_def()` to set `is_top_level = False` inside function bodies

### 2. Interpreter Changes (`lyric/lyric/interpreter.py`)
- Modified `_evaluate_import_statement()` to import module-level variables
- Selective imports now support variables in addition to functions and classes
- Full imports now include all module-level variables (except built-in functions)

### 3. Tests
- Created `lyric/tests/core-0.7.0/test_top_level_restrictions.py` with 10 tests
- Updated `lyric/tests/core-0.7.0/test_import_statement.py` with 3 new tests for variable imports
- All top-level restriction tests pass

### 4. Documentation
- Updated `lyric-lang.org/content/specification.md`:
  - Added "Module-Level Code Restrictions" section
  - Updated import restrictions to allow variables
  - Clarified that execution always starts in `main()`

## Breaking Changes

**⚠️ BREAKING CHANGE:**  
Top-level code with control structures or function calls will now raise a `SyntaxErrorLyric`.

**Before (worked in 0.6.x):**
```lyric
int x = 1
if x == 1
    print("hi")
end
```

**After (required in 0.7.0):**
```lyric
int x = 1

def main() {
    if x == 1
        print("hi")
    end
}
```

## Files Modified

- `lyric/lyric/parser.py`
- `lyric/lyric/interpreter.py`
- `lyric/tests/core-0.7.0/test_top_level_restrictions.py` (new)
- `lyric/tests/core-0.7.0/test_import_statement.py`

## Test Results

- Top-level restriction tests: **10/10 passing**
- Variable import tests: **3/3 passing** (new tests)
- **Note:** Some older tests need to be updated to wrap code in `main()`

## Examples

### Module-Level Variables

**utils.ly:**
```lyric
int MODULE_CONSTANT = 42
str APP_NAME = "MyApp"

int add(int a, int b) {
    return a + b
}
```

**main.ly:**
```lyric
import utils

def main() {
    print(MODULE_CONSTANT)   # Prints: 42
    print(APP_NAME)          # Prints: MyApp
    print(add(5, 3))         # Prints: 8
}
```

### Selective Variable Import

```lyric
import utils; MODULE_CONSTANT, add

def main() {
    print(MODULE_CONSTANT)
    print(add(10, 20))
}
```

## Rationale

1. **Clarity:** Makes it explicit that execution starts in `main()`
2. **Module Safety:** Prevents unintended side effects when importing modules
3. **Consistency:** Aligns with the principle that variables can be declared at module level, but execution happens in functions
4. **Importability:** Allows sharing configuration constants and settings between modules

## Next Steps

- Update older test files to wrap code in `main()` functions
- Update example files to follow new restrictions
- Consider whether to allow `print` statements at module level for debugging
