# Sprint9 Task5 — 20251202.1952

## Summary
Implemented `getopts()` built-in function to provide convenient command-line option parsing in Lyric programs.

## Key Accomplishments
1. **getopts() Built-in Function**:
   - Added `getopts_builtin()` function to `lyric/runtime.py`
   - Returns option value for options with values (e.g., `--file=myfile` returns `"myfile"`)
   - Returns `True` for flags without values (e.g., `-a` or `--verbose` returns `True`)
   - Returns `False` for options that weren't provided

2. **CLI Option Parsing**:
   - Added `_parse_options()` function to parse command-line arguments
   - Supports short options with single dash: `-a`, `-b`, `-c`
   - Supports long options with double dash: `--verbose`, `--debug`
   - Supports options with values: `--file=myfile`, `--output=result.txt`
   - Options can be mixed with file arguments: `lyric myfile.ly -a --verbose --file=test.txt`

3. **Global Option Storage**:
   - Added `set_command_line_options()` function to store parsed options
   - Options are stored globally and accessible via `getopts()` from Lyric code
   - Works with both `lyric run <file.ly>` and `lyric <file.ly>` commands

4. **Comprehensive Testing**:
   - Created 10 unit tests in `lyric/tests/core-0.8.0/test_getopts.py`
   - Tests cover all option types: short flags, long flags, options with values
   - Tests verify correct behavior for missing options (returns `False`)
   - Tests verify mixed options and values work correctly
   - All 10 tests passing ✅

## Files Changed
- `lyric/runtime.py` — added `getopts_builtin()`, `set_command_line_options()`, global option storage
- `lyric/cli.py` — added `_parse_options()` function, updated `main()` to parse and store options
- `lyric/tests/core-0.8.0/test_getopts.py` — created 10 comprehensive tests

## Example Usage
```lyric
def main() {
    god a = getopts("a")
    god verbose = getopts("verbose")
    var filename = getopts("file")
    god x = getopts("x")
    
    print("a:", a)              # True if -a was provided, False otherwise
    print("verbose:", verbose)  # True if --verbose was provided, False otherwise
    print("file:", filename)    # File value if --file=value was provided, False otherwise
    print("x:", x)              # False if -x was not provided
}
```

Command line:
```bash
lyric myProgram.ly -a --verbose --file=myfile
# Output:
# a: True
# verbose: True
# file: myfile
# x: False
```

## Reason
Provides convenient built-in command-line option parsing for Lyric programs, as specified in Sprint 9 Task 5. This allows Lyric programs to easily handle command-line flags and options without requiring external Python libraries.

## Git Commit Hash
`TBD` - Sprint9 Task5: Implement getopts support

## Status
✅ Completed

## Sprint Reference
- Sprint 9 Plan: `nova/aeon/trajectory-0.9.1/yield-0.8.0/SPRINT9_PLAN.md`
- Task: Task 5 — getopts support

