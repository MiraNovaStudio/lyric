# Sprint 9 Task 11 Summary: Exec Chain Operators

**Status**: ✅ Complete  
**Date**: February 11, 2026  
**Version**: 0.8.3 (experimental branch)

## Task Overview

Implement command chaining operators for `exec()` built-in function:
- **Pipe operator (`|`)**: Pass output from one command to the next
- **Logical AND (`&&`)**: Execute next command only if previous succeeded
- **Logical OR (`||`)**: Execute next command only if previous failed

## Requirements

### Functional Requirements
1. **Pipe Operator (`|`)**
   - Pass stdout of one command as stdin to next command
   - Support chaining: `exec("cmd1") | exec("cmd2") | exec("cmd3")`
   - Allow `print` in chains: `exec("cmd") | print`
   - Support `print` as source: `print "text" | exec("cmd")`

2. **Logical AND (`&&`)**
   - Short-circuit on failure (non-zero exit code)
   - Execute next command only if previous succeeded
   - Example: `exec("test") && exec("build") && exec("deploy")`

3. **Logical OR (`||`)**
   - Short-circuit on success (zero exit code)
   - Execute next command only if previous failed
   - Example: `exec("try_A") || exec("try_B") || exec("fallback")`

4. **Return Code Handling**
   - Chains used as expressions return integer exit code
   - Return first non-zero exit code, or 0 if all succeed
   - Example: `int rc = exec("cmd1") && exec("cmd2")`

5. **File I/O Integration**
   - Support output redirection: `exec() | exec() -> var`
   - Support file append: `exec() | exec() ->> file`
   - Support input redirection: `exec() <- input | exec() -> output`

6. **Print Handling**
   - `print` without arguments receives piped input
   - `print "text"` can be source in pipe chain
   - `print` doesn't produce output for next command

### Non-Requirements (Deferred)
- Simultaneous I/O: `exec("cmd") <- input -> output` (both at once)
- Variable-only piping: `myvar | exec("cmd")` (must use `print myvar | exec()`)
- Advanced error recovery or retry logic

## Implementation

### 1. Lexer Changes (`lyric/lexer.py`)
**Additions:**
- Added `PIPE = '|'` token type
- Added `AND = '&&'` token type
- Added `OR = '||'` token type
- Updated `MULTI_CHARS` set to include `|`, `&&`, `||`
- Modified `_scan_multi_char_operator()` to recognize these operators
- Updated `_scan_token()` to trigger multi-char scanning for `&` and `|`

**Key Code:**
```python
MULTI_CHARS = {
    # ... existing ...
    '|': {'|'},     # | and ||
    '&': {'&'},     # &&
}

def _scan_multi_char_operator(self) -> Token:
    # ... existing checks ...
    if self.current_char == '|':
        if self._peek_next() == '|':
            self._advance()
            return Token('OR', '||', self.line, self.column)
        return Token('PIPE', '|', self.line, self.column)
    elif self.current_char == '&' and self._peek_next() == '&':
        self._advance()
        return Token('AND', '&&', self.line, self.column)
```

### 2. AST Node (`lyric/ast_nodes.py`)
**Additions:**
- Created `ExecChainNode` dataclass

**Structure:**
```python
@dataclass
class ExecChainNode:
    elements: List[Any]              # List of exec() or print CallNodes
    operators: List[str]             # List of '|', '&&', '||'
    input_source: Optional[Any]      # Optional <- input
    output_target: Optional[Any]     # Optional -> output or ->> file
    line: int
    column: int
```

### 3. Parser Changes (`lyric/parser.py`)
**Additions:**
- `_is_exec_chain_ahead()`: Lookahead to detect exec chains
- `_parse_exec_chain_stmt()`: Parse full chain statement with I/O
- `_parse_exec_chain_or_primary()`: Integrate chains into expressions
- `_parse_exec_chain_element()`: Parse individual chain elements

**Key Changes:**
- Modified `_parse_unary()` to call `_parse_exec_chain_or_primary()` instead of `_parse_primary()`
- Increased `_is_file_operator_ahead()` lookahead from 5 to 30 tokens

**Parsing Logic:**
1. Check if current token is `exec` or `print`
2. Check if followed by `|`, `&&`, or `||`
3. Parse as `ExecChainNode` if pattern matches
4. Otherwise, parse as normal primary expression

### 4. Interpreter Changes (`lyric/interpreter.py`)
**Additions:**
- `_evaluate_exec_chain(node: ExecChainNode) -> int`
- `_evaluate_exec_chain_with_file_io(file_op_node: FileOpNode) -> None`

**Key Logic:**
```python
def _evaluate_exec_chain(self, node: ExecChainNode) -> int:
    current_output = ""
    first_nonzero_rc = 0
    exit_code = 0
    
    # Handle optional input source
    if node.input_source:
        # ... read input ...
    
    # Execute chain
    for i, element in enumerate(node.elements):
        # Short-circuit check BEFORE executing
        if i > 0:
            prev_operator = node.operators[i - 1]
            if prev_operator == '&&' and exit_code != 0:
                break  # AND: stop on failure
            elif prev_operator == '||' and exit_code == 0:
                break  # OR: stop on success
        
        # Determine if element receives piped input
        has_input = (i > 0 and node.operators[i-1] == '|')
        
        # Execute command
        if element.func_name == 'exec':
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                input=current_output if has_input else None,
                text=True
            )
            exit_code = result.returncode
            current_output = result.stdout
            
            if exit_code != 0 and first_nonzero_rc == 0:
                first_nonzero_rc = exit_code
        
        elif element.func_name == 'print':
            print(current_output if has_input else element.args)
            current_output = ""
    
    # Handle output_target if present
    # ...
    
    return first_nonzero_rc
```

**Integration:**
- Added `ExecChainNode` to `_evaluate_expression()` dispatcher
- Modified `_evaluate_file_op()` to detect `ExecChainNode` and route to `_evaluate_exec_chain_with_file_io()`

### 5. Test Suite (`lyric/tests/core-0.8.0/test_exit_exec.py`)
**Added 9 new tests:**
1. `test_exec_pipe_simple` - Basic `|` operator
2. `test_exec_pipe_to_print` - Piping to `print`
3. `test_exec_and_shortcircuit_success` - `&&` with success
4. `test_exec_and_shortcircuit_failure` - `&&` with failure
5. `test_exec_or_shortcircuit_success` - `||` with success
6. `test_exec_or_shortcircuit_failure` - `||` with failure
7. `test_exec_chain_return_code` - Exit code semantics
8. `test_exec_chain_file_append` - File I/O integration
9. `test_exec_chain_complex` - Multi-operator chains

**Test Results:**
- All 994 unit tests pass (100%)
- 23 total tests in `test_exit_exec.py`
- Full backward compatibility maintained

## Usage Examples

### Example 1: Simple Pipeline
```lyric
def main() {
    str result
    exec("echo hello world") | exec("cat") -> result
    print("Output:", result)
}
```

### Example 2: Build Chain with &&
```lyric
def main() {
    int rc = exec("make clean") && exec("make all") && exec("make test")
    if rc != 0
        print("Build failed with code:", rc)
        exit(rc)
    end
    print("Build successful!")
}
```

### Example 3: Fallback with ||
```lyric
def main() {
    exec("which python3") || exec("which python") || print("Python not found!")
}
```

### Example 4: Complex Pipeline
```lyric
def main() {
    var logfile = disk("pipeline.log")
    
    exec("git diff") | exec("grep +") | exec("wc -l") ->> logfile
    
    logfile.close()
}
```

### Example 5: Print in Chain
```lyric
def main() {
    exec("cat data.txt") | print
    
    print "test data" | exec("grep test")
}
```

## Design Decisions

### 1. Expression vs Statement
**Decision**: Exec chains can be both expressions and statements
- **As expression**: Returns exit code for assignment
- **As statement**: Can use file I/O operators

**Rationale**: Provides maximum flexibility for different use cases

### 2. Short-Circuit Evaluation
**Decision**: Check operator and previous exit code *before* executing next command

**Rationale**: Prevents unnecessary command execution and matches shell behavior

### 3. Output Handling
**Decision**: For `|`, pass output between commands. For `&&`/`||`, only last command's output is kept.

**Rationale**: 
- Pipe needs output passing for functionality
- `&&`/`||` are about control flow, not data flow
- Keeps implementation simpler

### 4. Print Behavior
**Decision**: `print` can receive piped input but doesn't produce output for next command

**Rationale**:
- `print` is a display operation, not a data transformation
- Prevents confusion about what gets piped
- User can still use `exec("cat")` if they need to capture print output

### 5. Lookahead Range
**Decision**: Increased file operator lookahead from 5 to 30 tokens

**Rationale**: Exec chains like `exec("cmd") | exec("cmd2") | exec("cmd3") ->> file` can exceed 5 tokens

### 6. Parser Integration
**Decision**: Integrate exec chain parsing into expression parsing layer (via `_parse_unary()`)

**Rationale**:
- Allows chains to be used in assignments
- Maintains clean separation between statement and expression parsing
- Avoids duplicating parsing logic

## Challenges and Solutions

### Challenge 1: Parsing Ambiguity
**Problem**: `|` and `||` look similar, need to distinguish in lexer  
**Solution**: Multi-character operator scanning with lookahead

### Challenge 2: Expression vs Statement Parsing
**Problem**: Chains need to work in both contexts  
**Solution**: Parse as expression first, wrap in FileOpNode if followed by file operator

### Challenge 3: Short-Circuit Timing
**Problem**: Initial implementation checked short-circuit *after* executing command  
**Solution**: Moved check to *before* execution, preventing unwanted command runs

### Challenge 4: Output Management
**Problem**: Each command's output needs to be tracked differently for `|` vs `&&`/`||`  
**Solution**: Unified execution loop with `has_input` flag based on previous operator type

### Challenge 5: File I/O Integration
**Problem**: Exec chains with file operators create nested AST structures  
**Solution**: Added `_evaluate_exec_chain_with_file_io()` to handle `FileOpNode(left=ExecChainNode)`

## Performance Considerations

- **Subprocess Overhead**: Each `exec()` spawns a subprocess, so long chains may be slow
- **Output Buffering**: All command output is buffered in memory
- **Lookahead Cost**: 30-token lookahead may slow parsing for deeply nested structures

**Mitigation**:
- Subprocess overhead is inherent to `exec()` design
- Output buffering is unavoidable for pipe functionality
- Lookahead only happens at statement boundaries, not in inner loops

## Future Enhancements

1. **Simultaneous I/O**: Support `exec("cmd") <- input -> output`
2. **Stream Processing**: Option to process output line-by-line instead of buffering
3. **Parallel Execution**: For independent commands (not in same chain)
4. **Timeout Support**: `exec("cmd", timeout=5)` to prevent hanging
5. **Signal Handling**: Better control over subprocess signals
6. **Environment Variables**: `exec("cmd", env={...})` for custom environment

## Documentation Impact

### User-Facing Documentation
- Add section on exec chains to language reference
- Add examples to cookbook/tutorials
- Update `exec()` built-in function documentation

### Developer Documentation
- Document `ExecChainNode` AST structure
- Explain short-circuit evaluation semantics
- Add notes on subprocess management

## Backward Compatibility

**Status**: ✅ Full backward compatibility maintained

- All existing `exec()` uses continue to work
- No breaking changes to syntax or semantics
- New operators are additive only
- All 994 existing tests pass

## Conclusion

Sprint 9 Task 11 successfully implements command chaining operators for Lyric's `exec()` built-in. The implementation:
- ✅ Supports all three operators (`|`, `&&`, `||`)
- ✅ Integrates with file I/O system
- ✅ Handles `print` in chains
- ✅ Returns appropriate exit codes
- ✅ Maintains 100% test pass rate
- ✅ Preserves backward compatibility

The feature enables powerful shell-like scripting capabilities while maintaining Lyric's type safety and error handling.
