# Module-Level Restrictions Implementation Summary

**Date:** November 25, 2025  
**Sprint:** 8 (yield-0.7.0)  
**Breaking Change:** Yes

## Overview

Implemented strict module-level code restrictions to enforce that execution always starts in `main()`. Only variable declarations, functions, classes, and imports are now allowed at the module (top) level. Control structures and executable statements must be inside functions.

## Motivation

From user requirements:
> "control structures should never be allowed outside of a function and execution always starts in the main function. We allow variable declaration and definition only."

This aligns with Lyric's design philosophy that execution is explicit and predictable.

## Changes Implemented

### 1. Parser Enforcement (`lyric/lyric/parser.py`)

- Added `is_top_level` flag to track parsing context
- Modified `_parse_statement()` to check `is_top_level` and raise `SyntaxErrorLyric` for:
  - Control structures: `if`, `elif`, `else`, `for`, `given`, `try`, `catch`, `finally`
  - `return` statements
  - Function calls and expressions
- Updated `_parse_func_def()` to set `is_top_level = False` inside function bodies

**Allowed at module level:**
- Variable declarations: `int x = 10`, `str name = "test"`, `arr items = [1, 2, 3]`
- Function definitions: `def funcname()`, `int funcname()`
- Class definitions: `class ClassName ...`
- Import statements: `import module`, `importpy library`

### 2. Import Variable Support (`lyric/lyric/interpreter.py`)

- Modified `_evaluate_import_statement()` to import module-level variables
- Full imports (`import module`) now include:
  - All functions (with module scope preserved)
  - All classes
  - All module-level variables (excluding built-in functions)
- Selective imports (`import module; sym1, sym2`) now support variables

### 3. Test Coverage

**New Tests:**
- `lyric/tests/core-0.7.0/test_top_level_restrictions.py` - 10 tests, all passing
  - Tests for allowed constructs (variables, functions, classes, imports)
  - Tests for disallowed constructs (if, loops, try, return, function calls)
  - Tests that all constructs work inside functions

**Updated Tests:**
- `lyric/tests/core-0.7.0/test_import_statement.py` - 12 tests, all passing
  - Added 3 new tests for variable imports
  - Wrapped all test code in `main()` functions

### 4. Documentation

Updated `lyric-lang.org/content/specification.md`:
- Added "Module-Level Code Restrictions" section with examples
- Updated import documentation to reflect variable support
- Clarified that execution always starts in `main()`

## Breaking Changes

### Before (0.6.x)

```lyric
int x = 1
if x == 1
    print("hi")
end
```

This code would execute immediately.

### After (0.7.0)

```lyric
int x = 1

def main() {
    if x == 1
        print("hi")
    end
}
```

Executable code must be inside `main()`.

## Error Messages

**Top-level control structure:**
```
Error [line 2]: Control structures not allowed at module level. Only variable declarations, functions, and classes are allowed at the top level.
```

**Top-level return:**
```
Error [line 3]: 'return' statement not allowed at module level. Execution starts in main().
```

**Top-level expression:**
```
Error [line 4]: Only variable declarations, functions, and classes are allowed at module level. Execution starts in main().
```

## Examples

### Module-Level Variables (Now Importable)

**utils.ly:**
```lyric
int MODULE_CONSTANT = 42
str APP_NAME = "MyApp"
arr DEFAULT_VALUES = [1, 2, 3]

int add(int a, int b) {
    return a + b
}

class Calculator
    int value
    
    def Calculator(int v) {
        self.value = v
    }
+++
```

**main.ly:**
```lyric
import utils

def main() {
    print(MODULE_CONSTANT)    # 42
    print(APP_NAME)           # MyApp
    print(DEFAULT_VALUES[0])  # 1
    print(add(5, 3))          # 8
    obj calc = Calculator(100)
}
```

### Selective Import with Variables

```lyric
import utils; MODULE_CONSTANT, add, Calculator

def main() {
    print(MODULE_CONSTANT)
    int result = add(10, 20)
    obj calc = Calculator(result)
}
```

## Test Status

✅ **Passing:**
- `test_top_level_restrictions.py` - 10/10
- `test_import_statement.py` - 12/12

⚠️ **Needs Manual Update:**
- Many older test files (core-0.1.0 through core-0.6.0) use top-level code
- Approximately 266 tests need to be updated to wrap code in `main()`
- This is a significant but necessary refactoring task

## Files Modified

- `lyric/lyric/parser.py`
- `lyric/lyric/interpreter.py`
- `lyric/tests/core-0.7.0/test_top_level_restrictions.py` (new)
- `lyric/tests/core-0.7.0/test_import_statement.py`
- `lyric/tests/examples/*.ly`
- `lyric-lang.org/content/specification.md`

## Rationale

1. **Explicit Execution:** Makes it crystal clear that execution starts in `main()`
2. **Module Safety:** Prevents unintended side effects when importing modules
3. **Teaching Tool:** Reinforces good programming practices for beginners
4. **Consistency:** Aligns with the language's design philosophy
5. **Importability:** Allows sharing constants and configuration between modules

## Next Steps

1. **Update Remaining Tests:** Systematically update older test files to wrap code in `main()`
2. **Update Examples:** Ensure all example files follow new restrictions
3. **User Communication:** Document breaking change in release notes
4. **Migration Guide:** Create guide for users migrating from 0.6.x to 0.7.0

## Impact Assessment

- **High Impact:** This is a breaking change affecting all Lyric code
- **Easy to Fix:** Simply wrap executable code in `def main() { ... }`
- **Better Design:** Aligns with language philosophy and improves code clarity
- **Worth It:** The benefits far outweigh the migration effort

## Conclusion

This is a significant but essential improvement to the Lyric language. It makes execution explicit, prevents surprising behavior, and sets a strong foundation for future language features.
