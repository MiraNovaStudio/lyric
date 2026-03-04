# Sprint 9 Task 6 Summary: Script Arguments

## Task Overview
Implemented command-line arguments support allowing Lyric programs to receive arguments via `main(int argc, arr argv)` parameters.

## Status
✅ **Completed**

## Key Accomplishments

### 1. CLI Argument Parsing
- Updated `_parse_options()` function in `lyric/cli.py` to separate options from arguments
- Options (starting with `-` or `--`) are collected separately
- Arguments (non-option values) are collected in order
- Example: `lyric myprogram.ly -a --file=x.txt arg1 arg2`
  - Options: `{a: None, file: 'x.txt'}`
  - Arguments: `['arg1', 'arg2']`

### 2. Main Function Signature Support
- Interpreter now supports three main() signatures:
  1. `def main()` — no parameters (legacy support)
  2. `def main(int argc, arr argv)` — standard argc/argv pattern
  3. `def main(int argc)` — only argc (uncommon but supported)
- Parameters are automatically detected and provided based on function signature

### 3. Interpreter Integration
- Added `cli_args` field to `Interpreter` class to store command-line arguments
- Modified `evaluate()` function to accept `cli_args` parameter from CLI
- Updated `evaluate()` method to:
  - Detect main() function parameters
  - Create `argc` (integer count) and `argv` (ArrObject array)
  - Call main() with appropriate parameters

### 4. CLI Updates
- Modified `_execute_file()` to accept and pass `arguments` parameter
- Updated both command formats:
  - `lyric run <file.ly> [options] [arguments]`
  - `lyric <file.ly> [options] [arguments]`
- Arguments can be mixed with options: `lyric myprogram.ly -a arg1 --verbose arg2`
- Updated `--help` text to document arguments

### 5. ArrObject Integration
- Arguments are passed as `ArrObject` (not plain Python list)
- This provides full Lyric array functionality:
  - Indexing: `argv[0]`, `argv[1]`
  - Iteration: `for arg in argv`
  - Methods: `argv.len()`, `argv.sorted()`, etc.

### 6. Comprehensive Testing
- Created 10 unit tests in `lyric/tests/core-0.8.0/test_cli_args.py`
- **Test Coverage**:
  1. `test_main_with_no_arguments` — main() with no params, no args
  2. `test_main_with_argc_argv` — main(argc, argv) receives args
  3. `test_main_with_options_and_arguments` — options and args separation
  4. `test_main_accessing_argv_elements` — array indexing
  5. `test_main_with_zero_arguments` — argc=0 when no args
  6. `test_spec_example` — exact example from Sprint 9 Plan
  7. `test_arguments_with_run_command` — works with `lyric run`
  8. `test_mixed_options_values_and_arguments` — complex mixing
  9. `test_argv_len_method` — argv.len() method works
  10. `test_numeric_string_arguments` — numeric args stay as strings
- **All 10 tests passing** ✅

## Implementation Details

### Argument Type
- All arguments are strings (type `str`)
- Even numeric-looking arguments like `"123"` remain strings
- Programs can convert using `int()` or `flt()` if needed

### Backwards Compatibility
- Programs with `def main()` (no parameters) continue to work
- Arguments are available but not passed if main() doesn't request them
- This ensures existing programs don't break

### Integration with getopts()
- Options (via `getopts()`) and arguments (via `argc`/`argv`) work together
- Options are extracted first, remaining values become arguments
- Example:
  ```bash
  lyric prog.ly -a --file=x.txt arg1 arg2
  ```
  - `getopts("a")` → `True`
  - `getopts("file")` → `"x.txt"`
  - `argc` → `2`
  - `argv` → `["arg1", "arg2"]`

## Example Usage

### Basic Usage
```lyric
def main(int argc, arr argv) {
    print("Arguments received:", argc)
    for arg in argv
        print("  -", arg)
    done
}
```

```bash
$ lyric myprogram.ly hello world test
Arguments received: 3
  - hello
  - world
  - test
```

### With Options
```lyric
def main(int argc, arr argv) {
    god verbose = getopts("verbose")
    
    if verbose
        print("Verbose mode enabled")
    end
    
    print("Processing", argc, "files:")
    for file in argv
        print("  File:", file)
    done
}
```

```bash
$ lyric myprogram.ly --verbose file1.txt file2.txt
Verbose mode enabled
Processing 2 files:
  File: file1.txt
  File: file2.txt
```

### Array Access
```lyric
def main(int argc, arr argv) {
    if argc >= 2
        str input = argv[0]
        str output = argv[1]
        print("Input:", input)
        print("Output:", output)
    else
        print("Usage: program <input> <output>")
    end
}
```

```bash
$ lyric myprogram.ly data.txt result.txt
Input: data.txt
Output: result.txt
```

## Files Created/Modified

### Modified
- `lyric/cli.py` — updated argument parsing, `_execute_file()` signature, help text
- `lyric/interpreter.py` — added cli_args storage, main() parameter detection, argc/argv passing

### Created
- `lyric/tests/core-0.8.0/test_cli_args.py` — 10 comprehensive unit tests

## Acceptance Criteria ✅

From Sprint 9 Task 6:
- ✅ Arguments are processed and passed when command-line arguments are present
- ✅ Arguments are passed to main() via user-defined parameters (argc, argv)
- ✅ Unit tests present to test arguments, argc, argv parameters, and corner cases
- ✅ Works with both `lyric run` and `lyric <file.ly>` commands
- ✅ Integrates seamlessly with getopts() from Task 5

## Technical Notes

### Parameter Type Enforcement
- The interpreter enforces parameter types if declared:
  - `int argc` — enforced as integer
  - `arr argv` — enforced as array (ArrObject)
- Using `var` would also work: `def main(var argc, var argv)`

### Empty Arguments
- When no arguments provided: `argc = 0`, `argv = []` (empty array)
- Empty array is falsy in Lyric conditionals
- Can check: `if argc == 0` or `if argv.len() == 0`

## References
- Sprint Plan: `nova/aeon/trajectory-0.9.1/yield-0.8.0/SPRINT9_PLAN.md` Task 6
- Changelog: `nova/changelog/20251202/2008-CHANGELOG.md`
- Related: Sprint 9 Task 5 (getopts support)

