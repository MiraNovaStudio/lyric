SPRINT 6 — RUNTIME STABILITY AND ERROR HANDLING
Target Version: 0.2.1

Sprint Goal:
Improve Lyric’s runtime stability, finalize scope and type enforcement, and introduce the new exception-handling system using the keywords try, catch, finally, and fade.

TASK 1 — NESTED SCOPE RESOLUTION
Ensure variables declared inside inner blocks shadow outer ones correctly and restore the parent scope when the block exits.
Add lookup logic that searches local → enclosing → global scopes.
Confirm function scopes and nested try/catch scopes behave independently.

ACCEPTANCE CRITERIA:
• Inner-scope variables do not overwrite outer-scope values.
• Variables declared inside try/catch or functions are destroyed when the block closes.
• Variable lookups resolve in correct scope order.
• Shadowing confirmed through tests and printed output.

TASK 2 — TYPE ENFORCEMENT VERIFICATION
Verify that declared types (int, flt, str, rex, god, var) are enforced at runtime.
Assignments violating declared types must raise a TypeError.
Return types from functions must match declared type signatures.

ACCEPTANCE CRITERIA:
• Type errors produce clear messages showing variable name, expected type, and actual type.
• Return-type mismatches trigger errors.
• No silent type coercions unless explicitly handled.
• Unit tests pass for mixed type assignment and function returns.

TASK 3 — IMPLEMENT TRY / CATCH / FINALLY / FADE SYNTAX
Add structured exception handling using the following grammar:

try:
<code block>
catch:
<code block>
finally:
<code block>
fade

The fade keyword terminates the entire exception block.
Both catch and finally are optional.
The interpreter executes catch when an error occurs in try, then executes finally (if present), and ends the block on fade.

Example:
try:
int x = 10
x = "bad"
catch:
print("Type error caught")
finally:
print("Cleanup complete")
fade

ACCEPTANCE CRITERIA:
• Parser recognizes try, catch, finally, and fade as block keywords.
• Runtime correctly executes try, optional catch, optional finally, then resumes after fade.
• Nested try blocks handled correctly.
• Fade required to close any try/catch/finally sequence.
• Errors raised in catch or finally propagate outward unless handled.

TASK 4 — ADD RAISE KEYWORD AND ERROR HIERARCHY
Implement a raise keyword for throwing exceptions.
Create a minimal built-in hierarchy:
Error (base), TypeError, ValueError, NameError, RuntimeError.
Allow raise "message" for simple text errors or raise TypeError("message") for typed errors.
Unhandled errors should bubble up to CLI output.

ACCEPTANCE CRITERIA:
• raise keyword functional in any code block.
• Errors can be caught with catch or remain unhandled to top level.
• Error output includes error type, message, line number, and file.
• Built-in error classes available from the global scope.

TASK 5 — CLI ERROR INTEGRATION AND RUNTIME STABILITY
Integrate exception handling with the lyric run command.
Unhandled errors must display formatted output and exit with non-zero status.
Ensure interpreter never crashes with raw Python tracebacks.

ACCEPTANCE CRITERIA:
• CLI prints readable “Traceback” style messages for unhandled errors.
• Exit code ≠ 0 on unhandled error.
• All exceptions within CLI context handled gracefully.

TASK 6 — DOCUMENTATION AND CHANGELOG
Update README.md and CHANGELOG.md to document:
• New try / catch / finally / fade syntax.
• raise keyword and error hierarchy.
• Examples showing nested exception handling and fade terminator.
Include note that fade is used exclusively for error flow blocks.

ACCEPTANCE CRITERIA:
• All new keywords described with examples in README.
• CHANGELOG entry added for version 0.2.1.

DEFINITION OF DONE
• Nested scope resolution stable.
• Type enforcement confirmed.
• try / catch / finally / fade syntax fully implemented and tested.
• raise keyword and error hierarchy functional.
• CLI prints clean error output and handles exceptions gracefully.
• Documentation and CHANGELOG updated.
• Version bumped to 0.2.1 and committed.