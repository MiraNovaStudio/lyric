# Sprint 6 Implementation Questions

**Target Version:** 0.6.0  
**Date:** October 22, 2025  
**Purpose:** Clarification questions for Sprint 6 implementation

## Task 1 - Scope Enforcement Questions

### Redeclaration Check Timing
- Should the redeclaration check happen during parsing (compile-time) or during interpretation (runtime)? The plan mentions "CompileError" but Lyric is interpreted.

  We will Detect at Runtime (Interpretation Phase) for now however we may change this behavior later

- For nested scopes, should we check all parent scopes or just immediate parent? (e.g., if we have 3 nested scopes, should we check all 3 levels up?)

Do Deep Check (No shadowing allowed)

### Scope Inheritance
- Should `try/catch/finally` blocks inherit their parent scope completely, or should they have their own scope for variables declared within them?

Shared Parent Scope (Inherited)

All three blocks share the enclosing scope, like Python’s try or if.

## Task 2 - Function Return Types Questions

### Void Keyword Inconsistency
- The example shows `def void greet(str name)` but the plan says "There is no void keyword." Should this be `def greet(str name)` with inferred NoneType?

yes there is no void type sorry

### Type Inference Scope
- For type inference, should we analyze all possible code paths or just the actual return statements? (e.g., if there's unreachable code)

Analyze All Possible Code Paths

- Should we consider implicit returns (functions that don't explicitly return) as returning None?

functions without a return always return None

### Return Type Storage
- Where should the inferred/declared return type be stored? In the AST node, symbol table, or both?

(Both AST + Symbol Table).

## Task 3 - `for` Keyword Questions

### Documentation Status
- I notice the plan was simplified from the original "Easter Egg" version. Should this be a documented feature or still hidden?

No this will be documented from now on

- Should error messages reference "for" or "given" when using the `for` keyword?

Use for it will be documented

### Implementation Approach
- Should `for` be treated as a direct alias in the lexer, or should it be handled in the parser?

handle for as an alias in the lexer, it will be functionally equivalent to given

## Task 4 - Error Hierarchy Questions

### Error Class Implementation
- Should the built-in error classes be actual Python classes or Lyric objects?
- For `raise "message"`, should this create a generic `Error` instance or a `RuntimeError`?

We will skip adding the raise keyword for now, skip this task but note that it was skippped int the changelog file for the task

## Task 5 - Exception Binding Questions

### Exception Variable Binding
- Should the exception variable (`e`) be bound as a string representation or as the actual exception object?

Each caught exception should be wrapped in a lightweight internal class like LyricError(type, message), giving it properties such as .type and .message.
In a catch e: block, e refers to this object, and print e should return a formatted string like "ErrorType: message".

- How should we handle `catch SomeType as e` when `SomeType` doesn't exist?

Treat as Compile/Parse Error

### String Conversion
- Should exception objects automatically convert to strings when used in string concatenation?
- What should the string representation look like for different error types?

Exception objects should automatically convert to strings when used in concatenation or interpolation.

Their __str__() method should return a consistent, readable format:
<Type>: <message> — for example, FileError: File not found.

If no message is provided, only the type name should be shown (e.g., RuntimeError).
This allows simple expressions like "Error: " + e to work naturally without requiring explicit conversion.

## Task 6 - Shebang Support Questions

### Implementation Location
- Should we modify the CLI or the interpreter itself to handle shebang detection?
- What should happen if the shebang path doesn't exist?

Handle shebang detection inside the interpreter, not the CLI.
The interpreter should ignore any first line beginning with #!, treating it as a comment.


### Cross-Platform Behavior
- Should we validate the shebang path exists before attempting execution?

if invoked with lyric file_name.ly do not check the shebang, if invoked as ./file_name.ly check the shebang path


- How should we handle relative paths in shebang lines?

require an absolute path



## Task 7 - `bin` Type Questions

### Type Interchangeability
- Should `bin` and `god` be completely interchangeable in all contexts, or should there be any differences?

they are identical bin is a lexer alias for god

- Should `isinstance(obj, "bin")` return true for `god` values and vice versa?

yes


### Future Deprecation
- Should we add any warnings or deprecation notices for `bin` usage?

No this is intential as some users may find the god variable offensive

## Task 8 - Constructor Recognition Questions

### Constructor Name Matching
- Should constructors be required to have the exact class name, or should we support variations?

must be exact class name

- What should happen if a constructor has a return statement?

Disallow return in Constructors


### Multiple Constructors
- Should we support method overloading for constructors, or only allow one constructor per class?

No

- How should we handle constructor parameters and type checking?

class User: 
    def User(str name, int age) { 
        self.name = name 
        self.age = age 
    } 
+++ 

var u1 = User("Alice", 30) # ✅ OK 
var u2 = User("Bob", "thirty") # ❌ TypeError

### Constructor Execution
- Should constructors be executed before or after instance variable initialization?
All var declarations at the class level are initialized before the constructor runs.

- What should happen if a constructor raises an exception?

We are skipping raise for this sprint

## General Implementation Questions

### Error Handling Strategy
- Should we implement a unified error handling system across all tasks?
- How should we ensure consistent error message formatting?

Implement a unified error handling system shared by all components (lexer, parser, interpreter, and CLI).
All errors should inherit from a single LyricError base class.
Adopt a consistent message format:
<ErrorType>: <message> [at line <line>, column <column>].
This ensures predictable, clean error output and simplifies future integration with Nova’s logging and debugging tools.

### Testing Strategy
- Should each task have its own test file, or should we group related tests together?

READ your CLAUDE_CONFIG.md to get our testing rules, tests for this sprint will go
into test/core-0.6.0

- How should we handle integration testing between tasks?

All functional testing will be handled by Michael, only worry about the unit tests

### Backward Compatibility
- Are there any existing features that might be affected by these changes?
No we are early in development and require no backwards compatibilty

- Should we maintain backward compatibility with existing code?

Existing .ly files in tests/ should be moified to to support the current implementation.  Any assciated unit tests which use those files should also 
be updated to the current syntax
