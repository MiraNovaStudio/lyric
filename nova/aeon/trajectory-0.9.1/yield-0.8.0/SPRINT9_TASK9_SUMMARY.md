# Sprint 9 Task 9 — File Operators (PARTIALLY COMPLETED)

**Date:** December 2, 2025  
**Task:** Sprint 9 Task 9 - File Operators  
**Status:** ⚠️ Partially Completed (Lexer Only)

## Summary

Sprint 9 Task 9 aimed to implement file I/O operators (`>>`, `>`, `<`) for convenient file operations in Lyric 0.8.0. The task was started but **not completed** before moving to Task 10 (`exit()` and `exec()`). Only the lexer changes were implemented.

## What Was Implemented

### 1. Lexer Changes (`lyric/lexer.py`)

**Added Token Support for Shift Operators:**
- Added `>>` and `<<` to `MULTI_CHARS` set
- Implemented `RSHIFT` token for `>>` operator (append/right-shift)
- Implemented `LSHIFT` token for `<<` operator (left-shift)
- Updated `_scan_multi_char_operator()` to recognize these operators

```python
# In MULTI_CHARS
MULTI_CHARS = {
    '==', '!=', '<', '<=', '>', '>=', '+++', '>>', '<<'
}

# In _scan_multi_char_operator()
elif first_char == '>' and self._peek() == '>':
    # Handle >> (RSHIFT / append operator)
    self._advance()  # consume second >
    self.tokens.append(Token('RSHIFT', '>>', start_line, start_col))
elif first_char == '<' and self._peek() == '<':
    # Handle << (LSHIFT operator)
    self._advance()  # consume second <
    self.tokens.append(Token('LSHIFT', '<<', start_line, start_col))
```

### 2. AST Node Definition (`lyric/ast_nodes.py`)

**Created `FileOpNode` AST Node:**
- Represents file I/O operations: `var > file`, `var >> file`, `var < file`
- Fields: `operator` (str), `left` (ASTNode), `right` (ASTNode)
- Included in the `ASTNode` Union type
- Added to parser imports

```python
@dataclass
class FileOpNode(ASTNode):
    """Represents a file I/O operation: var > file, var >> file, var < file."""
    operator: str  # '>', '>>', or '<'
    left: 'ASTNode'  # Source variable or expression
    right: 'ASTNode'  # Target variable (usually a DskObject)
    line: int = 0
    column: int = 0
```

## What Was NOT Implemented

### 1. Parser Changes (NOT DONE)
- ❌ No parsing logic for `FileOpNode` statements
- ❌ No recognition of file operator patterns in `_parse_statement()`
- ❌ Cannot parse `str >> dsk`, `str > dsk`, or `str < dsk` syntax

### 2. Interpreter Support (NOT DONE)
- ❌ No evaluation logic for `FileOpNode` operations
- ❌ No type checking for file operator operands
- ❌ No runtime implementation of file I/O operations

### 3. File Operator Operations (NOT DONE)
- ❌ `str >> dsk` - Append string to file
- ❌ `str > dsk` - Overwrite file with string
- ❌ `str < dsk` - Read file into string
- ❌ `arr >> dsk` - Write array lines to file (append)
- ❌ `arr < dsk` - Read file lines into array
- ❌ `print("text") >> myfile` - Append print output to file

### 4. Tests (NOT DONE)
- ❌ No unit tests for file operators
- ❌ No test coverage for any file operator functionality

### 5. Documentation (NOT DONE)
- ❌ No changelog entry created
- ❌ No usage examples documented

## Architectural Decision Made

During implementation, an important architectural decision was made:

**Statement-Level Operations vs Expression-Level Operations:**

The file operators (`>>`, `>`, `<`) were initially considered as binary expression operators, but this approach was deemed too complex due to:
1. Context-sensitive parsing (operators mean different things with different types)
2. Conflict with existing comparison operators (`<`, `>`)
3. Complex type-dependent evaluation in the interpreter

**Decision:** Treat file operators as **statement-level operations** rather than binary expressions. This means:
- `text >> myfile` is parsed as a special file I/O statement, not a binary expression
- Creates `FileOpNode` AST nodes specifically for file operations
- Simpler to implement and maintain
- Clearer semantics for file I/O operations

## Intended Functionality (Per SPRINT9_PLAN.md)

The task was meant to enable:

```lyric
# File I/O with operators
dsk myfile = disk("test.txt")

# Append string to file
print("test") >> myfile
str test = "test"
test >> myfile

# Overwrite file
print("Test") > myfile

# Read file to string
str myvar < myfile

# Read file to array (line by line)
arr myarr < myfile

# Write array to file (line by line)
arr myarr = [1, 2, 3]
myarr >> myfile  # Creates file with:
                 # 1
                 # 2
                 # 3
```

## Why Task Was Not Completed

Based on the conversation transcript:
1. Task 9 was identified as "a big lift" by the user
2. Implementation began with lexer and AST changes
3. Parser complexity was encountered
4. User requested moving to Task 10 (`exit()` and `exec()`) before completing Task 9
5. Task 10 was described as "the last task for the night"
6. Task 9 was never resumed

## Files Modified

### Completed:
- ✅ `lyric/lexer.py` - Added `RSHIFT` and `LSHIFT` token support
- ✅ `lyric/ast_nodes.py` - Added `FileOpNode` class definition
- ✅ `lyric/parser.py` - Imported `FileOpNode` (but not used)

### Not Modified (Needed):
- ❌ `lyric/parser.py` - No parsing logic added
- ❌ `lyric/interpreter.py` - No evaluation logic added
- ❌ `lyric/tests/core-0.8.0/test_file_operators.py` - Not created

## Current Status

**Tokens:** ✅ Lexer can tokenize `>>` and `<<`  
**AST:** ✅ `FileOpNode` exists  
**Parser:** ❌ Cannot parse file operator statements  
**Interpreter:** ❌ Cannot execute file operations  
**Tests:** ❌ No test coverage  
**Overall:** ⚠️ ~10% complete (infrastructure only)

## To Complete This Task

To finish Sprint 9 Task 9, the following work is needed:

### 1. Parser Implementation
```python
# In parser.py _parse_statement()
# After checking for assignments, check for file operators
if self._peek_ahead(1).type in ('GT', 'RSHIFT') and self._peek_ahead(2):
    # Parse as FileOpNode
    left = self._parse_expression()
    operator = self._advance().value  # '>' or '>>'
    right = self._parse_expression()
    return FileOpNode(operator=operator, left=left, right=right)

# Also handle '<' operator similarly
```

### 2. Interpreter Evaluation
```python
# In interpreter.py
def _evaluate_file_op(self, node: FileOpNode) -> None:
    left_val = self._evaluate(node.left)
    right_val = self._evaluate(node.right)
    
    if not isinstance(right_val, DskObject):
        raise RuntimeErrorLyric(f"File operators require dsk type on right side")
    
    if node.operator == '>>':
        # Append operation
        if isinstance(left_val, str):
            right_val.append(left_val)
        elif isinstance(left_val, ArrObject):
            for item in left_val.elements:
                right_val.append(str(item) + '\n')
    elif node.operator == '>':
        # Overwrite operation
        if isinstance(left_val, str):
            right_val.write(left_val)
        elif isinstance(left_val, ArrObject):
            content = '\n'.join(str(item) for item in left_val.elements)
            right_val.write(content)
    elif node.operator == '<':
        # Read operation - handled differently (assigns to left)
        content = right_val.read()
        if isinstance(left_val, str):
            # Assign content to string variable
            pass  # Need variable name, not value
        elif isinstance(left_val, ArrObject):
            # Read lines into array
            pass
```

### 3. Comprehensive Tests
- Test `str >> dsk` (append string)
- Test `str > dsk` (overwrite with string)
- Test `str < dsk` (read to string)
- Test `arr >> dsk` (write array lines)
- Test `arr < dsk` (read lines to array)
- Test print redirection: `print("text") >> myfile`
- Test error cases (wrong types, file not found, etc.)
- Test with existing vs new files

### 4. Documentation
- Update changelog
- Document operator precedence
- Provide usage examples
- Document type requirements

## Reason

Sprint 9 Task 9 was started but left incomplete when the user requested to proceed with Task 10 instead. The foundational work (lexer tokens and AST nodes) was completed, but the core functionality (parsing and evaluation) was never implemented.

## Related Tasks

- **Task 7 (Completed):** `dsk` type and file object methods - provides the underlying file I/O functionality that Task 9 operators would use
- **Task 10 (Completed):** `exit()` and `exec()` built-ins - implemented after Task 9 was paused
- **Task 10 Deferred Features:** The specification mentioned `exec()` with I/O redirection operators, which were deferred to Task 9 but Task 9 was never completed

## Notes

- The `FileOpNode` import exists in `parser.py` but is never instantiated
- The lexer recognizes `>>` as `RSHIFT` but this token is never consumed by the parser
- The `<<` operator (LSHIFT) was added but has no defined purpose in Lyric
- Completing this task would significantly improve file I/O ergonomics in Lyric

## Recommendation

To complete Sprint 9 Task 9:
1. Implement parser logic to recognize file operator patterns
2. Implement interpreter evaluation for `FileOpNode`
3. Handle the `<` operator special case (assigns to left-hand side, not right)
4. Consider whether `<<` has a purpose or should be removed
5. Create comprehensive test suite
6. Update this summary with completion status
