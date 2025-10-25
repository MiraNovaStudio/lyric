# Sprint 6 — Runtime Stability and Error Handling

**Target Version:** 0.6.0

## Sprint Goal

Improve Lyric's runtime stability, finalize scope and type enforcement,

## Task 1 — Enforce No Redeclaration in Same or Nested Scope

### Goal
Prevent variable redeclaration within the same or any enclosing scope, ensuring Lyric remains simple, predictable, and strongly typed.  
Typed and untyped declarations (`int x = 1`, `var x = 1`, etc.) must not redeclare a variable name already in use in the current or parent scope.

### Steps to Implement
1. **Update Symbol Resolution Logic**
   - Modify the variable declaration handler in both the parser and interpreter.
   - When a new declaration (`int name = ...`, `str name = ...`, or `var name = ...`) is encountered:
     - Check if `name` exists in the **current** or **any parent scope**.
     - If it does, raise a `CompileError` before runtime.

2. **Modify Assignment Handling**
   - Ensure `name = expr` performs a lookup:
     - If variable exists, allow assignment.
     - If not, raise `NameError("Variable not declared")`.
   - Enforce strong type matching:
     - If types differ, raise `TypeError`.

3. **Adjust Scope Manager**
   - Ensure `try/catch/finally` (and any future block) inherits its parent scope.
   - Do **not** create isolated scopes for these constructs — variables within should reference the outer scope.

4. **Add Compiler Error Messaging**
   - Introduce standardized compiler messages:
     - `Variable 'name' already declared`
     - `Variable 'name' not declared`
     - `Type mismatch: expected int, got str`

5. **Update Unit Tests**
   - Add tests for valid and invalid redeclarations.
   - Confirm interpreter halts on compile errors before runtime execution.

**Example Behavior**

```lyric
int test = 1
try:
    int test = 5
catch:
    print("error")
fade
# → CompileError: Variable 'test' already declared

int test = 1
try:
    test = 5
fade
# → Passes, no error
```


### Acceptance Criteria
- ✅Declaring a variable twice — whether explicitly typed (int x = 1) or inferred via var x = 1 — in the same or any nested scope raises CompileError.
- ✅ Assigning to an existing variable (without `var` or type prefix) works normally.
- ✅ Type mismatches on assignment raise `TypeError`.
- ✅ Variables declared outside `try/catch/finally` are accessible within those blocks.
- ✅ All new behavior confirmed via unit tests under `tests/test_scope.py`.



## Task 2 — Implement Function Return Type Specification and Inference

### Tasks

1. **Parser Update**
   - Extend function declaration syntax to optionally include a return type before the function name.
     ```lyric
     def str hello() { ... }
     def int add(int a, int b) { ... }
     ```
   - If no return type is specified, the compiler must analyze all `return` statements within the function body to infer the type automatically.

   - If there are conflicting types in the return statements we should give a compiler error.

2. **Type Inference Rules**
   - If all `return` expressions produce the same type, infer that type.
   - If `return` statements produce different types, raise:
     ```
     CompileError: inconsistent return types
     ```
   - If some paths return a value and others do not, raise:
     ```
     CompileError: inconsistent return flow
     ```

3. **Functions without return or empty return**
   - If a function has no return statement → it implicitly returns None.

   - If a function has a bare return → it explicitly returns None.

    - The inferred return type for such functions is NoneType.

    -Any attempt to return a value in a function inferred as NoneType raises a CompileError.

    - There is no void keyword.
  
4. **Type Enforcement**
   - At runtime, the interpreter must verify that all returned values match the declared or inferred type.
   - If a mismatch occurs, raise:
     ```
     TypeError: return value does not match declared type
     ```

5. **Scope and Symbol Integration**
   - Ensure the declared return type is stored in the function’s symbol table entry.
   - Maintain compatibility with the existing type system for `int`, `str`, `god`, `bin`, etc.

---

#### Examples

```lyric
# Inferred str
def hello() {
    return "hello"
}

# Explicit int
def int add(int a, int b) {
    return a + b
}

# Explicit god (boolean-like)
def god is_even(int n) {
    if n % 2 == 0 {
        return true
    } else {
        return false
    }
}

# Explicit bin (binary 0/1)
def bin flag(int n) {
    if n > 10 {
        return 1
    } else {
        return 0
    }
}

# CompileError: inconsistent return types
def mystery(int n) {
    if n > 0 {
        return "positive"
    } else {
        return 0
    }
}

# Returns None
def void greet(str name) {
    print("Hello " + name)
    return
}

### Acceptance Criteria

Functions may optionally declare a return type before the function name.

✅ If no return type is declared, Lyric infers the type from all return expressions.

✅ Mixed-type or partial-return functions produce a compile error.

✅ Functions with no value-returning statements return NoneType

✅ Returned values are verified at runtime to match the declared or inferred type.

✅ All behavior confirmed via new unit tests under tests/test_functions.py


## Task 3 — Add the for keyword

### Goal  
The `for` keyword should function identically to Lyric’s existing `given/done` loop construct

### Steps to Implement
1. **Parser Update**
   - Modify the parser to recognize the keyword `for` as a valid alias for `given`.
   - Internally, treat `for` as syntactic sugar — it should map directly to the same AST node used by `given`.
   - Ensure there is no difference in behavior, performance, or scope handling between `for` and `given`.

2. **Interpreter Support**
   - The interpreter should execute `for` blocks identically to `given` loops.
   - Ensure any errors or tracebacks still reference the internal node type (e.g., “Loop”) rather than the literal `for`.

3. **Error Handling**
   - Ensure that using `for` incorrectly produces the same compile/runtime errors as `given`.
   

### Acceptance Criteria
- ✅ `for` loops parse and execute identically to `given` loops.  
 above.  

## Task 4 — Add Raise Keyword and Error Hierarchy

Implement a `raise` keyword for throwing exceptions.

**Implementation:**
- Create a minimal built-in hierarchy: `Error` (base), `TypeError`, `ValueError`, `NameError`, `RuntimeError`.
- Allow `raise "message"` for simple text errors or `raise TypeError("message")` for typed errors.
- Unhandled errors should bubble up to CLI output.

### Acceptance Criteria:
- `raise` keyword functional in any code block.
- Errors can be caught with `catch` or remain unhandled to top level.
- Error output includes error type, message, line number, and file.
- Built-in error classes available from the global scope.

## Task 5 — Implement Exception Type Binding in `catch` Clauses

### Goal
Extend Lyric’s exception handling system to support typed exception capture using `catch <ExceptionType> as <var>`.  
This allows developers to catch specific errors and access the raised exception’s message or value.

### Tasks

1. **Parser Update**
   - Extend the existing `catch` grammar to support the following optional form:
     ```
     catch <ExceptionType> as <identifier>:
     ```
     Examples:
     ```lyric
     catch IndexError as e:
         print("Caught IndexError: " + e)
     catch TypeError as err:
         print(err)
     ```
   - Both `catch <Type>:` and plain `catch:` must remain valid.
   - Store the exception type (`IndexError`) and variable name (`e`) in the AST node for this block.

2. **Interpreter Update**
   - When executing a `try` block:
     1. Capture runtime exceptions.
     2. For each `catch` clause:
        - If the clause specifies an exception type, only execute it when the caught error’s type matches.
        - If it uses `as <var>`, bind the error message or object to that variable in the current scope.
        - If no type is specified, it should match all exceptions.
   - The following cases must all behave correctly:
     ```lyric
     catch IndexError:
         ...
     catch IndexError as e:
         ...
     catch:
         ...
     ```

3. **Error Propagation**
   - If no matching `catch` block is found, propagate the exception up to the caller.
   - Support nesting:
     ```lyric
     try:
         try:
             ...
         catch IndexError as e:
             ...
     catch:
         ...
     ```

4. **String Concatenation Behavior**
   - When printing an exception variable (e.g., `"Caught IndexError: " + e`), ensure that `e` is automatically converted to a string if needed.
   - Implement `__str__` or equivalent conversion for all Lyric exception objects.

5. **Testing Requirements**
   - Add runtime tests for:
     - Matching and non-matching exception types.
     - Bare `catch` fallback behavior.
     - `catch ... as e` variable binding.
     - String concatenation using the caught exception variable.
   - Example test:
     ```lyric
     def main() {
         var items = [1, 2, 3]
         try:
             var x = items[5]
         catch IndexError as e:
             print("Caught IndexError: " + e)
         fade
     }
     # Expected output: Caught IndexError: list index out of range
     ```

### Acceptance Criteria

- ✅ `catch <Type> as <var>` syntax is parsed correctly and recognized in the AST.
- ✅ Exceptions are matched by type at runtime.
- ✅ Variable `e` (or any identifier) is properly bound to the caught exception.
- ✅ Bare `catch:` remains functional as a generic fallback.
- ✅ String concatenation with the bound exception variable works automatically via implicit string conversion.
- ✅ Nested try/catch blocks behave correctly without scope leaks.
- ✅ All behavior confirmed by unit tests under `tests/test_exceptions.py`.


## Task 6 - Add Shebang Support (`#!/usr/bin/lyric`)

### Objective
Enable Lyric scripts to be executed directly from the command line on Unix-like systems using a shebang line, allowing developers to run Lyric files without explicitly invoking the interpreter.

**Example:**
```bash
#!/usr/bin/lyric
print "Hello from Lyric!"
```

Run

```
$ chmod +x hello.ly
$ ./hello.ly
Hello from Lyric!
```

### Implementation Plan

- Interpreter Invocation

Modify the main entry script (lyric.py or CLI wrapper) to detect and skip the shebang line if present.

Ensure that Lyric can handle direct execution through the OS shell.

- Path Resolution

Verify Lyric can be installed or symlinked to /usr/bin/lyric, or an equivalent directory within $PATH.

- Cross-Platform Behavior

On Windows, ensure the shebang line is safely ignored and does not affect parsing.

On Unix-like systems, verify full compatibility with executable permissions.

- Testing

Create a test script with a shebang line and ensure it executes both via lyric file.ly and ./file.ly.

Confirm error reporting and exit codes behave identically between both execution paths.

### Acceptance Criteria

✅ Lyric correctly ignores the #! line when present at the start of a file.

✅ Scripts can be executed directly from the shell with a valid shebang line.

✅ Execution behavior is identical between lyric file.ly and ./file.ly.

✅ Compatible with both absolute and relative interpreter paths (e.g., /usr/bin/lyric, /usr/local/bin/lyric).

✅ No adverse behavior on Windows platforms.

✅ Includes a new automated unit test validating shebang execution.

✅ Documentation updated in the “Command Line Usage” section of the Lyric specification.

## Task 7 — Add Alternative Type Name Bin for God Type

Introduce `bin` as an alias for `god`.

**Behavior:**
- Both types represent true/false values.
- Internally, both map to the same boolean implementation.
- If `god` becomes widely accepted, `bin` may be deprecated in a future release.

**Example:**
```lyric
god flag1 = true
bin flag2 = false
print(flag1, flag2)
```

### Acceptance Criteria:
- `bin` recognized as a valid type keyword.
- `bin` and `god` behave identically.
- Type enforcement and logical operations work with both.
- Documentation updated noting `bin` is an alias for `god`.

## Task 8 — Add Constructor Recognition

If a method name matches the class name, it is treated as the constructor.

**Behavior:**
- Constructors run automatically on object instantiation.
- The interpreter should translate `def ClassName()` to Python's `__init__()` under the hood.

**Example:**
```lyric
class Person:
    var name
    def Person() {
        self.name = "Unknown"
        print("Person created")
    }
+++
```

### Acceptance Criteria:
- Constructor executes automatically upon object creation.
- Constructor can access and modify instance variables through `self`.
- Only one constructor allowed per class (raise error if multiple found).
- Constructor can accept parameters (`def Person(str name)`, etc.).



## Definition of Done (Updated)

- ✅ **Scope Stability:** Variable and type resolution confirmed across all nested scopes, including within `try`, `catch`, and `fade` blocks.  
- ✅ **Type Enforcement:** Strict type enforcement validated for variable declarations, assignments, and function return types (including inferred `NoneType`).  
- ✅ **Function Returns:** Function return type inference and validation working for explicit and inferred types, with consistent behavior across all code paths.  
- ✅ **Exception System:** `try`, `catch`, and `fade` syntax fully implemented and tested with support for typed exception capture via `catch <Type> as <var>`.  
- ✅ **Raise Keyword:** `raise` keyword fully functional, with a complete built-in error hierarchy (`Error`, `TypeError`, `ValueError`, `NameError`, `RuntimeError`).  
- ✅ **Error Output:** CLI displays clear and structured error output including type, message, line, and file information.  
- ✅ **Easter Egg Compliance:** Hidden `for` keyword functions as alias for `given`, excluded from all documentation and tests, and enforced by Claude’s configuration.  
- ✅ **Documentation and Configuration:** Documentation, `CLAUDE_CONFIG.md`, and `CHANGELOG` updated to reflect all new features and restrictions.  
- ✅ **Testing Coverage:** New and existing unit tests pass under `tests/test_scope.py`, `tests/test_functions.py`, and `tests/test_exceptions.py`.  
- ✅ **Version Bump:** Lyric version updated to `0.6.0` and committed to repository with verified build integrity.
