# 🎵 Lyric — Sprint 4

**Target Version:** 0.4.0


**Goal:**  
Introduce improved variable handling and declaration syntax to make Lyric cleaner, more expressive, and optionally dynamic where appropriate.

---

## 🧩 Overview
This sprint focuses on enhancing Lyric’s variable system by adding dynamic typing with the `var` keyword, enforcing explicit declarations, and supporting multi-variable declarations. These updates improve language clarity, prevent silent variable creation, and align Lyric’s feel closer to Python while retaining structured control.

---

## 🧠 Sprint 4 Tasks



### **Task 1 — Multi-Variable Declarations**
**Description:**  
Support comma-separated variable declarations in a single line, e.g.:

var x, int y, str z

Each variable is declared but not initialized until later.

**Acceptance Criteria:**
- Multiple variables of mixed types can be declared on one line.  
- Each variable is added to the symbol table as uninitialized.  
- Assignments occur individually (`x = 3.1`, `y = 10`, `z = "Aeonath"`).  
- Parser correctly splits and handles each declaration segment.

---

### **Task 2 — Update Specification and Grammar**
**Description:**  
Extend the **Lyric Language Specification** to include:
- `var` keyword behavior  
- declaration and initialization rules  
- type enforcement logic  
- examples and sample error messages

**Acceptance Criteria:**
- Section “2.1 — Variable Declaration and Assignment” created/updated.  
- Grammar updated to parse multi-declaration syntax.  
- Internal docs regenerated.

---

### **Task 3 — Internal Validation & Testing**
**Description:**  
Verify correctness through dedicated test scripts covering:
- dynamic vs. static declarations  
- reassignment behavior  
- undeclared/unused variable errors  
- multi-declaration parsing

**Acceptance Criteria:**
- All tests pass without regression.  
- Manual and automated verification complete.


### **TASK 4 - AST Position Tracking & Structured Error Reporting**

**Goal:**  
Refactor `ast_node.py` and related parser components so each AST node stores `line` and `column` metadata, enabling precise source-level error reporting.

 Scope of Work

- Update `ASTNode` base class to include `line` and `column` attributes.  
- Modify the parser to attach position information during tokenization and node construction.  
- Update error and exception handling logic to use this metadata when displaying messages.  
- Ensure backward compatibility with existing interpreter behavior.  
- Add regression tests for error locations and messages.  


 Acceptance Criteria

- All syntax and runtime errors include **file, line, and column** in their output.  
- Existing tests pass with **no behavioral regressions**.  
- New test suite for **error positioning** passes.  
- Developer documentation updated (e.g., `/docs/errors.md`).  

Impact

This change requires a **major refactor** of the parser and AST node structures.  
While complex, it lays the foundation for advanced IDE integrations and precise debugging support in futu

### **Task 5 - Remove colon from class**


#### Instructions

- Update the parser to remove the required colon following class declarations.  
- The new valid syntax should be:

```
class Example

instead of 

class Example:
```
  
- When the colon form is used, emit a deprecation warning (e.g., “DeprecationWarning: Colons after class declarations will be removed in a future version.”).  
- Update all existing test cases and example programs to use the new syntax.  
- Add new tests to confirm that both forms currently parse successfully and that the deprecation warning appears.  


### Acceptance Criteria

- The following declaration compiles successfully:

```
class Example
+++
```

- The old form with a colon also compiles but produces a deprecation warning.  
- Removing the colon does not affect the class body or closing operator (`+++`).  
- All test cases in the Lyric suite pass without regressions.  
- At least one new test verifies that both syntaxes are accepted and warnings are properly displayed.  
- Documentation updated to reflect the new preferred syntax.  
- Parser changes are isolated and do not affect other constructs (`def`, `given/done`, etc.).

### **Task 6 - Control structure syntax simplification**

- Update the parser to remove the required colon (`:`) after control structure headers.
- The following constructs should no longer require colons:
  - `if condition`
  - `else if condition`
  - `else`
  - `given`

- Update all relevant parser functions (`parse_if_statement`, `parse_given_loop`, etc.) to reflect this rule.
- Adjust test suites and example files to use the new syntax.
- Add new tests ensuring both the old and new forms parse correctly and that warnings appear for the deprecated form.
- Update documentation to remove colons from all examples.

#### Acceptance Criteria

- The following code compiles and executes successfully:

```
if x > 0
print("positive")
else if x == 0
print("zero")
else
print("negative")
end

int x = 1
given x < 3 
print("looping")
x = x + 1
done
```


- All control structure tests pass without regression.
- All language examples and documentation are updated to reflect the new syntax style.
- The removal of colons does not affect unrelated constructs (`def`, `class`, etc.).

### **Task 7 - Exception Handling Syntax Simplification**

- Update the parser to remove the required colon (`:`) after `try`, `catch`, and `finally` statements.
- The new valid syntax should be:

```
try
...
catch 
...
finally
...
fade

instead of 

try:
...
catch:
...
finally:
...
fade
```


- Update all existing test files and example programs to use the colonless form.
- Add new tests verifying that both forms currently parse correctly and that the deprecation warning is displayed.
- Ensure this change does not affect the `fade` terminator or existing runtime behavior.
- Update documentation and example code accordingly.



#### Acceptance Criteria

- The following code executes successfully:
```
try
var x = items[5]
catch IndexError as e
print("Caught:", e)
finally
print("Always runs")
```


- The parser accepts both the colon and non-colon forms without syntax errors.
- Using a colon produces a deprecation warning.
- No regressions in existing exception-handling tests.
- All example programs and documentation updated to reflect the simplified syntax.
- Exception handling structure remains unchanged beyond syntax cleanup.


## 📅 Definition of Done
- All acceptance criteria met for each task.  
- `CHANGELOG.md` and `README.md` updated to reflect new syntax.  
- Sprint reviewed and merged to `main` branch.  


---

*End of Sprint 4 Specification*
