# Sprint9 Task8 — 20251202.2041

## Summary
Implemented auto-generated help functionality with the `-h` option in Lyric 0.8.0. When a user passes `-h` to a Lyric program, the CLI automatically generates and displays a help message showing available options and arguments, unless the program explicitly overrides `-h` by calling `getopts("h")` or `getopts('h')`.

## Files Changed
- lyric/cli.py — Added `_check_for_auto_help()` function to detect `-h` and generate help
- lyric/runtime.py — Added `get_command_line_options()` function to retrieve current CLI options
- lyric/tests/core-0.8.0/test_auto_help.py — Created 10 comprehensive tests for auto-help functionality

## Implementation Details

### Auto-Help Generation Logic
1. **Detection**: When `-h` is passed, `_check_for_auto_help()` is called before program execution
2. **Override Check**: Scans source code for `getopts("h")` or `getopts('h')` calls
3. **Help Display**: If no override found, generates help showing:
   - Program usage
   - Available options (extracted from getopts calls via regex)
   - Argument information (detected from main signature)
4. **Exit**: Returns exit code 0 after displaying help

### Features
- **Smart Override Detection**: Programs can override `-h` by using `getopts("h")` in their code
- **Option Discovery**: Automatically scans for all `getopts()` calls to list available options
- **Sorted Output**: Options are displayed in alphabetical order
- **Duplicate Removal**: Each option only appears once even if called multiple times
- **Argument Detection**: Recognizes `main(argc, argv)` signature to inform users about argument support
- **Both Quote Styles**: Detects both double quotes (`"h"`) and single quotes (`'h'`)

### Auto-Generated Help Format
```
Usage: lyric myprogram.ly [options] [arguments]

Auto-generated help (use -h in your program to override)

Available options:
  -a
  -b
  --debug
  --verbose
  --file

Arguments:
  This program accepts command-line arguments via main(argc, argv)
```

## Test Coverage
- 10 unit tests covering:
  - Auto-help when not overridden
  - Program override with getopts("h")
  - Programs with no options
  - Detection of main(argc, argv)
  - Normal execution without -h
  - Multiple options display
  - Double and single quote detection
  - Alphabetical sorting
  - Duplicate removal

## Reason
Implements Sprint 9 Task 8 requirements for auto-generated help. Provides users with immediate help about program usage without requiring manual documentation, while allowing programs to override this behavior when needed.

## Git Commit Hash
`TBD` - Sprint9 Task8 Implementation

## Status
✅ Completed - All 121 Sprint 8/9 tests passing (100% pass rate)

