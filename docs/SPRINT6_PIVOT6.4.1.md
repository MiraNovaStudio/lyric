PIVOT — Implement Logical Operators and Boolean Literals

Context:
While working through conditional flow and boolean type (god), we identified the need for logical operators and boolean literals.
These are fundamental to making Lyric’s conditionals expressive, readable, and complete.
This pivot will add 'and', 'or', and 'not' operators and the lowercase literals 'true' and 'false' as native language elements.

Objective:
Implement full support for boolean literals (true/false) and logical operators (and/or/not) in the Lyric parser, interpreter, and syntax highlighter.

Implementation Details:
1. Lexer:
   - Add new tokens for 'and', 'or', 'not', 'true', and 'false'.
   - Ensure these are treated as reserved keywords, not identifiers.

2. Parser:
   - Extend the expression grammar to recognize 'and', 'or', and 'not' with correct operator precedence.
     - Precedence order: not > and > or
   - Ensure 'true' and 'false' are parsed as boolean literal values of type god.
   - Support short-circuit evaluation for 'and' and 'or':
     - 'and' should stop evaluating if the left operand is false.
     - 'or' should stop evaluating if the left operand is true.
   - 'not' applies only to a single operand and inverts its boolean value.

3. Interpreter:
   - Map 'true' to Python True and 'false' to Python False internally.
   - Implement evaluation logic for 'and', 'or', and 'not' using short-circuit behavior.
   - Ensure type enforcement:
     - god variables must hold only boolean literals.
     - Arithmetic or string coercion is not allowed for god type.
   - Handle mixed expressions (e.g., x > 0 and ready) safely and predictably.

4. Syntax Highlighter:
   - Add 'and', 'or', 'not', 'true', and 'false' to the grammar’s keyword lists for colorization.

5. Testing:
   - Create /tests/test_logic.py with the following coverage:
     a. Simple and compound conditions using and/or/not
     b. Nested expressions
     c. Short-circuit behavior correctness
     d. Interaction with god type variables
     e. Mixed expressions (numeric + boolean)
     f. Error cases (unsupported operations)

Acceptance Criteria:
- The interpreter correctly evaluates boolean expressions with and/or/not.
- Short-circuit behavior functions as expected.
- god type variables accept only true/false literals.
- The syntax highlighter and examples display the correct colors for new keywords.
- All tests in /tests/test_logic.py pass successfully.

Definition of Done:
- Code compiles and passes all pytest tests.
- CHANGELOG.md updated noting Pivot implementation.
- Documentation and examples updated to reflect boolean literals and logical operators.
- Once this pivot is complete and verified, the current sprint may resume.
