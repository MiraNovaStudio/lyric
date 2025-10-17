PIVOT — Implement else if Conditional Syntax

Context:
During ongoing Sprint 9 planning and testing, it was determined that Lyric currently supports only basic if/else blocks.
We need to introduce support for 'else if' as a proper conditional construct that chains multiple comparisons within a single if statement sequence.

Objective:
Implement native support for the 'else if' keyword pair in the Lyric parser and interpreter, ensuring proper control flow and block resolution.

Implementation Details:
1. Update the parser to recognize 'else if' as a single combined clause, not as separate tokens.
2. Ensure that nested and chained conditions are parsed and executed in order.
3. Modify the block resolution logic so that only one branch executes per chain.
4. Verify compatibility with existing 'if' / 'else' / 'end' syntax and indentation-free structure.
5. Update the language grammar definition and syntax highlighting to include 'else if' as a control flow keyword.
6. Add a regression test file under /tests named test_conditionals.py covering:
   - Simple chained if / else if / else
   - Nested conditionals
   - Correct fall-through prevention (only one branch executes)
   - Mixed conditions using and/or operators

Acceptance Criteria:
- The interpreter correctly evaluates 'else if' chains and only executes the first matching condition.
- The 'else if' syntax parses without errors or ambiguity.
- Nested 'if' blocks remain unaffected by this change.
- All pytest cases under /tests/test_conditionals.py pass successfully.
- Highlighting and examples reflect the correct syntax in the Cursor extension.

Definition of Done:
- Code compiles and passes all tests.
- CHANGELOG.md updated noting Pivot implementation.
- Documentation and examples updated to show 'else if' usage.
- Sprint 9 tasks may resume once this Pivot is complete and verified.
