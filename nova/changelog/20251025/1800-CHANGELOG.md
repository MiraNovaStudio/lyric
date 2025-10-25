# Changelog

## 2025-10-25

### Added
- **Sprint 6 Pivot 6.5.1: Break and Continue Keywords**
  - **Lexer Updates**: Added `break` and `continue` as reserved keywords
  - **AST Nodes**: Created `BreakNode` and `ContinueNode` to represent loop control statements
  - **Parser Enhancements**:
    - Added parsing logic for `break` and `continue` statements
    - Implemented compile-time validation using `loop_depth` tracking
    - Raises `ParseError` if `break` or `continue` is used outside of loop context
    - Loop depth increments/decrements properly for nested loops
  - **Control Flow Signals**:
    - Created `BreakSignal` and `ContinueSignal` classes (subclass `BaseException`, not `Exception`)
    - Signals bypass user-level `try/catch` blocks entirely
    - Only loop-level handlers recognize and process these signals
  - **Interpreter Loop Handling**:
    - Updated `_evaluate_iterator_loop` to catch `BreakSignal` and `ContinueSignal`
    - Updated `_evaluate_while_loop` to catch loop control signals
    - Implemented `_evaluate_break_statement` to raise `BreakSignal`
    - Implemented `_evaluate_continue_statement` to raise `ContinueSignal`
    - Implemented `_evaluate_return_statement` for proper return value handling
  - **Loop Control Behavior**:
    - `break`: Immediately exits the nearest enclosing loop
    - `continue`: Skips remainder of current iteration, proceeds to next
    - Nested loops: Inner `break`/`continue` only affects inner loop
    - Works with both `given` (while-style) and `for` (iterator-style) loops
  - **Comprehensive Test Coverage**:
    - Created `tests/core-0.6.0/test_break_continue.py` with 17 new tests
    - Tests cover: basic break/continue, nested loops, while loops, try/catch interaction, edge cases
    - Previously skipped test `test_for_keyword_with_break_continue` now passes
    - All 476 tests passing (100% pass rate)
  
  **Example Usage**:
  ```lyric
  # Break example
  for i in range(10):
      if i == 5:
          break
      end
      print(i)
  done
  
  # Continue example
  for i in range(10):
      if i == 5:
          continue
      end
      print(i)
  done
  ```

### Technical Implementation Details
- **Signal Design**: Used `BaseException` instead of `Exception` to ensure loop control signals never interfere with user-level exception handling
- **Scope Validation**: Parser tracks loop depth (`loop_depth`) and validates `break`/`continue` can only appear within loops
- **Clean Separation**: Loop control flow is completely separate from error handling flow
- **No Breaking Changes**: All existing code continues to work with full backward compatibility

### Files Modified
- `lyric/lexer.py` - Added `break` and `continue` keywords
- `lyric/parser.py` - Added loop depth tracking and statement parsing
- `lyric/ast_nodes.py` - Added `BreakNode` and `ContinueNode`
- `lyric/errors.py` - Added `BreakSignal` and `ContinueSignal`
- `lyric/interpreter.py` - Added loop control signal handling
- `lyric/tests/core-0.6.0/test_break_continue.py` - Added 17 comprehensive tests

### Test Results
- **Total Tests**: 476
- **Passed**: 476 (100%)
- **Failed**: 0
- **Skipped**: 0 (previously skipped test now passes)

### Status
✅ **COMPLETED** - Break and continue keywords fully implemented and tested

