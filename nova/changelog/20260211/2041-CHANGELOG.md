# Sprint 9 Task 11: Exec Chain Operators (`|`, `&&`, `||`)

**Date**: February 11, 2026  
**Version**: 0.8.3 (experimental branch)  
**Task**: Implement command piping and short-circuit operators for `exec()` chains

## Summary

Added three new operators for chaining `exec()` commands:
- **Pipe operator (`|`)**: Passes stdout from one command to stdin of the next
- **Logical AND (`&&`)**: Short-circuits on failure (non-zero exit code)
- **Logical OR (`||`)**: Short-circuits on success (zero exit code)

These operators enable complex command workflows and can be combined with file I/O redirection (`->`, `->>`, `<-`).

## Changes

### Core Implementation Files
1. **lyric/lexer.py**
   - Added `PIPE`, `AND`, `OR` tokens to `MULTI_CHARS` set
   - Modified `_scan_multi_char_operator` to recognize `|`, `&&`, `||`
   - Updated `_scan_token` to trigger multi-char scanning for `&` and `|`

2. **lyric/ast_nodes.py**
   - Added `ExecChainNode` dataclass with:
     - `elements`: List of `exec()` or `print` calls
     - `operators`: List of chain operators (`|`, `&&`, `||`)
     - `input_source`: Optional input redirection (`<-`)
     - `output_target`: Optional output redirection (`->` or `->>`)

3. **lyric/parser.py**
   - Added `_is_exec_chain_ahead()` for lookahead detection
   - Added `_parse_exec_chain_stmt()` to parse full chains with I/O
   - Added `_parse_exec_chain_or_primary()` to integrate chains into expression parsing
   - Added `_parse_exec_chain_element()` to parse individual chain elements
   - Modified `_parse_unary()` to check for exec chains
   - Updated `_is_file_operator_ahead()` lookahead range from 5 to 30 tokens

4. **lyric/interpreter.py**
   - Added `ExecChainNode` to expression evaluation dispatcher
   - Added `_evaluate_exec_chain()` for standalone chain execution
   - Added `_evaluate_exec_chain_with_file_io()` for chains with file operators
   - Implemented pipe operator (passes stdout → stdin)
   - Implemented `&&` short-circuit (stops on non-zero exit code)
   - Implemented `||` short-circuit (stops on zero exit code)
   - Integrated with existing file operator system
   - Modified `_evaluate_file_op()` to detect and route `ExecChainNode`s

### Test Files
5. **lyric/tests/core-0.8.0/test_exit_exec.py**
   - Added 9 new tests for exec chains:
     - `test_exec_pipe_simple`: Basic pipe functionality
     - `test_exec_pipe_to_print`: Piping to print statement
     - `test_exec_and_shortcircuit_success`: `&&` with successful first command
     - `test_exec_and_shortcircuit_failure`: `&&` with failing first command
     - `test_exec_or_shortcircuit_success`: `||` with successful first command
     - `test_exec_or_shortcircuit_failure`: `||` with failing first command
     - `test_exec_chain_return_code`: Return code semantics
     - `test_exec_chain_file_append`: File I/O with chains
     - `test_exec_chain_complex`: Multiple operators in one chain

## Technical Details

### Operator Behavior

1. **Pipe (`|`)**:
   - Passes previous command's stdout as stdin to next command
   - Always continues to next command (no short-circuit)
   - Example: `exec("echo hello") | exec("cat")` → outputs "hello"

2. **Logical AND (`&&`)**:
   - Continues only if previous command succeeded (exit code 0)
   - Short-circuits on first failure
   - Example: `exec("exit 1") && exec("echo test")` → second doesn't run

3. **Logical OR (`||`)**:
   - Continues only if previous command failed (non-zero exit code)
   - Short-circuits on first success
   - Example: `exec("echo ok") || exec("echo backup")` → second doesn't run

### Return Code Handling
- Exec chains return the **first non-zero exit code** encountered
- If all commands succeed, returns 0
- Useful for error handling: `int rc = exec("cmd1") && exec("cmd2")`

### Integration with File Operators
Chains can be used with file I/O operators:
```lyric
exec("cat file.txt") | exec("grep test") -> results
exec("echo data") | exec("process") ->> outfile.txt
exec("filter") <- inputfile.txt | exec("sort") -> sorted
```

### Print in Chains
`print` can be used as a chain element:
- `exec("cmd") | print` → prints command output
- `print "data" | exec("cmd")` → pipes string to command

## Test Results

All 994 unit tests pass (100% pass rate), including:
- 9 new exec chain tests
- 14 existing `exec()` tests (backward compatible)
- All other Lyric language tests

### New Test Coverage
- Basic piping between commands
- Piping to `print` statement
- `&&` short-circuit on success and failure
- `||` short-circuit on success and failure
- Return code propagation
- File I/O integration (`->>` with chains)
- Complex multi-operator chains

## Usage Examples

### 1. Simple Pipe
```lyric
def main() {
    str output
    exec("echo hello world") | exec("cat") -> output
    print("Result:", output)
}
```

### 2. Conditional Execution (&&)
```lyric
def main() {
    exec("make clean") && exec("make all") && exec("make test")
}
```

### 3. Fallback Execution (||)
```lyric
def main() {
    exec("which python3") || exec("which python") || print("Python not found")
}
```

### 4. Complex Pipeline with File Output
```lyric
def main() {
    var logfile = disk("build.log")
    exec("git status") | exec("grep modified") ->> logfile
    logfile.close()
}
```

### 5. Error Handling
```lyric
def main() {
    int rc = exec("test -f config.txt") || exec("cp default.txt config.txt")
    if rc != 0
        print("Failed to ensure config file exists")
        exit(1)
    end
}
```

## Design Decisions

1. **Expression vs Statement**: Exec chains can be both expressions (return exit code) and statements (with I/O redirection)

2. **Short-Circuit Timing**: Short-circuit checks happen *before* executing the next command, not after

3. **Output Handling**: For pipe operator, only the final command's output is available. For `&&`/`||`, only the last executed command's output is kept

4. **Print Behavior**: `print` in a chain receives piped input but doesn't produce output for subsequent commands

5. **Lookahead Range**: Increased file operator lookahead from 5 to 30 tokens to accommodate long exec chains

## Deferred Features

The following features were discussed but not implemented:
1. **Simultaneous I/O**: `exec("cmd") <- input -> output` (both input and output in one chain)
2. **Variable piping**: Allowing standalone variables in chains (only `print expr` and `exec()` allowed)
3. **Mixed operator chains**: Currently all operators in a chain are evaluated, but could optimize to skip unnecessary evaluations

## Notes for Future Development

- The parser uses a specialized `_parse_exec_chain_or_primary()` method that checks for exec chains during expression parsing
- The interpreter has two separate evaluation paths:
  - `_evaluate_exec_chain()` for standalone chains (returns exit code)
  - `_evaluate_exec_chain_with_file_io()` for chains with file operators (handles I/O)
- Both paths share similar logic but differ in how they handle output
- Consider refactoring to unify these paths in future revisions
