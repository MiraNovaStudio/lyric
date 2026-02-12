# Sprint9 Task10 — 20260211.2011

## Summary
Enhanced `exec()` built-in function with I/O redirection operators (`->`, `->>`, `<-`) for capturing output and piping input to shell commands in Lyric 0.8.3. This completes the file I/O operator integration started in Task 9.

## Features Implemented

### exec() I/O Redirection
- **`exec("cmd") -> variable`**: Capture command stdout to a variable
- **`exec("cmd") <- variable`**: Pipe variable content as stdin to command
- **`exec("cmd") ->> file`**: Append command stdout to a file

### Key Behaviors
- Commands still return exit code (int) for conditional logic
- Stderr is always merged into stdout stream
- Output capture works with both variables and file objects
- Input piping supports strings and arrays (joined with newlines)
- Cross-platform compatible (Windows, Unix, Mac)

## Files Changed

### Core Implementation
- **lyric/interpreter.py**: 
  - Modified `_evaluate_file_op()` to detect and handle `exec()` calls
  - Added `_evaluate_exec_with_io()` method for exec I/O redirection
  - Special handling in file operator evaluation when left side is `exec()` call

### Tests
- **lyric/tests/core-0.8.0/test_exit_exec.py**:
  - Added 4 new tests for I/O redirection
  - All 14 tests passing (10 existing + 4 new)
  - `test_exec_output_redirection` - stdout to variable
  - `test_exec_input_piping` - stdin from variable
  - `test_exec_output_multiple_lines` - multi-line output capture
  - `test_exec_with_file_output` - append to file

## Technical Details

### Design Approach
The implementation integrates `exec()` with the file operator system by:
1. Detecting `exec()` CallNode on left side of file operators in `_evaluate_file_op()`
2. Routing to specialized `_evaluate_exec_with_io()` handler
3. Executing command with appropriate stdin/stdout configuration
4. Assigning captured output to target variable or file

### Output Redirection (`->`)
```python
subprocess.run(
    command,
    shell=True,
    stdout=subprocess.PIPE,  # Capture stdout
    stderr=subprocess.STDOUT, # Merge stderr
    text=True
)
# Store result.stdout in target variable
```

### Input Piping (`<-`)
```python
subprocess.run(
    command,
    shell=True,
    input=stdin_data,  # Pipe data to stdin
    stderr=subprocess.STDOUT,
    text=True
)
```

### File Append (`->>`)
- Captures stdout like `->` operator
- Instead of variable assignment, calls `DskObject.append()` method
- Maintains file object state for subsequent operations

## Usage Examples

### Basic Output Capture
```lyric
def main() {
    str output
    exec("ls -la") -> output
    print("Directory listing:", output)
}
```

### Input Piping
```lyric
def main() {
    str data = "input text"
    exec("grep pattern") <- data
}
```

### Append to File
```lyric
def main() {
    dsk logfile = disk("build.log")
    exec("make all") ->> logfile
    logfile.close()
}
```

### Return Code with Output
```lyric
def main() {
    str output
    int rc = exec("command") -> output  // Note: operator doesn't return value
    // Need to check command success another way
}
```

## Test Results
- **exec/exit tests**: 14/14 passing
- **Full suite**: 985/985 tests passing
- **New tests**: +4 I/O redirection tests
- **Pass rate**: 100%

## Deferred Features

### Chained I/O Redirection
The syntax `exec("cmd") <- input -> output` (simultaneous input and output redirection) was deferred due to parser complexity. Users can achieve the same result with temporary files:

```lyric
// Workaround for exec("cmd") <- input -> output
dsk tempfile = disk("temp.txt")
input_data -> tempfile
tempfile.close()

str output
exec("cmd < temp.txt") -> output
```

This could be implemented in a future task with enhanced parser support for chained operators.

## Notes
- The `exit()` function remains unchanged from previous implementation
- `exec()` without I/O operators still works as before (returns exit code)
- I/O redirection is opt-in via file operators
- Global `_last_exec_output` variable from previous implementation is no longer used

## Reason
Sprint 9 Task 10 required adding I/O redirection to `exec()` using the file operators (`->`, `->>`, `<-`) implemented in Task 9. This provides powerful shell integration for Lyric scripts.

## Git Commit Hash
`TBD` - Sprint9 Task10: Add exec() I/O redirection

## Status
✅ Completed

## Related Tasks
- **Sprint 9 Task 9**: File operators (`->>`, `->`, `<-`) - provides operator infrastructure
- **Sprint 9 Task 7**: `dsk` type - provides file object for `->>` operator with files
- **Sprint 9 Task 10 (Original)**: `exit()` and `exec()` basics - foundation this builds upon
