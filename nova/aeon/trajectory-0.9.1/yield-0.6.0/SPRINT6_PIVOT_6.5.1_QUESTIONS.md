# Sprint 6 Pivot 6.5.1 Questions - Break and Continue Keywords

## Plan Review Summary ✅

The Sprint 6 Pivot 6.5.1 plan for implementing `break` and `continue` keywords is well-structured and addresses the exact gap identified in our unit tests. The plan provides clear implementation guidance across all components (lexer, parser, AST, interpreter) with proper error handling and testing requirements.

## Clarifying Questions

### 1. Control Signal Implementation Approach
**Question**: The plan mentions "internal exceptions or structured control signals." Do you have a preference for the implementation approach?

**Proposed Approach**: Use custom exception classes like `BreakSignal` and `ContinueSignal` that are caught by loop handlers. This would be clean and avoid confusion with error handling.

**Example**:
```python
# In errors.py
class BreakSignal(Exception):
    """Internal signal for break statement."""
    pass

class ContinueSignal(Exception):
    """Internal signal for continue statement."""
    pass

# In interpreter.py loop handling
try:
    # loop body execution
except BreakSignal:
    break  # Exit loop
except ContinueSignal:
    continue  # Skip to next iteration
```

#### 1. Answer: yes use Control Signals

### 2. Loop Context Detection Scope
**Question**: For compile-time validation, should I check that `break`/`continue` are within any loop construct (`given`, `for`, future `while`), or are there specific loop types where they should/shouldn't be allowed?

**Current Understanding**: All loop constructs should support `break`/`continue` since they're fundamental control flow operations.

#### 2. ANSWER: Yes — check for any active loop context.
If loop_depth > 0, break and continue are valid.
If not, raise a compile-time error.

### 3. Nested Loop Behavior Implementation
**Question**: The plan mentions "inner break or continue only affecting nearest loop." Should I implement this by having each loop level catch and re-raise the signal if it's not meant for that level?

**Proposed Approach**: Each loop level catches the signal and handles it appropriately. Inner loops don't re-raise - they handle the signal locally.

#### 3. ANSWER: Yes — implement your proposed model:

Use internal signals (BreakSignal, ContinueSignal).

Each loop execution block catches and handles its own signal.

Inner loops handle locally and do not re-raise.

Signals never reach user-level catch blocks.

### 4. Integration with Exception Handling (Task 5)
**Question**: Since we just implemented exception type binding, should `break`/`continue` signals be designed to work cleanly with `try/catch` blocks within loops?

**Specific Scenario**: If `break` is inside a `try` block, should it still exit the loop, or should it be caught by the `catch` clause?

**Proposed Behavior**: `break`/`continue` should bypass `try/catch` blocks and directly affect loop control, as they are control flow statements, not exceptions.

#### 4. ANSWER: Summary Decision

break and continue are control signals, not exceptions.

They bypass user-level catch blocks entirely.

Only loop-level handlers recognize and process them.

Interpreter must ensure the try/catch layer never intercepts these signals.


### 5. Implementation Timeline and Priority
**Question**: You mentioned "Target inclusion in Lyric 0.6.0 release if testing remains stable by Sunday evening." Should I prioritize getting this implemented quickly, or focus on thorough testing?

**Current Status**: The skipped test `test_for_keyword_with_break_continue` is ready to pass once these keywords are implemented.

## Implementation Sequence Proposal

1. **Lexer Updates**: Add `break` and `continue` to keywords
2. **AST Nodes**: Create `BreakNode` and `ContinueNode`
3. **Parser**: Add parsing logic with context validation
4. **Interpreter**: Implement loop control signal handling
5. **Tests**: Comprehensive test coverage including the skipped test
6. **Documentation**: Update language specification

#### 5. ANSWER: We are not in a rush at all, we have all day.  We want to 
get this right from the beginning so focus on doing thorough testing.

## Risk Mitigation Questions

### Parser Conflicts
**Question**: The plan mentions ensuring token priority doesn't interfere with existing `done` or `return` parsing. Are there any specific parsing edge cases I should be aware of?

#### Answer: 

1   break and continue are statements only, never expressions.
2	They must appear only within loop context.
3	return is valid only in function context.
4	done parsing must remain context-aware (loop vs try vs function).
5	break/continue must not absorb following tokens — always standalone statements.
6	Indentation or explicit done pairing ensures no ambiguity between control and closure.

### Runtime Signal Design
**Question**: Should the internal loop control mechanism be completely separate from the exception hierarchy we just implemented, or can it leverage some of the same infrastructure?

#### Answer: Use separate signal classes, not part of LyricError.

Subclass BaseException, not Exception.

Share infrastructure pattern (raise/catch mechanics, file structure) for consistency, but maintain logical separation.

This keeps control flow and error flow clean, predictable, and debuggable.

### Testing Integration
**Question**: Should I create new test files specifically for `break`/`continue`, or integrate them into existing loop test files?


#### Answer: Create new test cases for break and continue as part of tests/core-0.6.0

## Expected Outcomes

Once implemented, this will:
- ✅ Enable the currently skipped `test_for_keyword_with_break_continue` test
- ✅ Provide fine-grained loop control for Lyric developers
- ✅ Align Lyric with common structured programming conventions
- ✅ Complete the loop control flow functionality for Lyric 0.6.0

## Ready to Proceed

The plan is clear and comprehensive. I'm confident this can be implemented cleanly without destabilizing the current architecture. The implementation approach using internal control signals is elegant and will integrate well with the existing interpreter design.

**Awaiting your guidance on the questions above before beginning implementation.**
