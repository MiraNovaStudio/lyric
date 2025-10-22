# 🎵 Lyric — Sprint 4

**Target Version:** 0.4.0


**Goal:**  
Introduce improved variable handling and declaration syntax to make Lyric cleaner, more expressive, and optionally dynamic where appropriate.

---

## 🧩 Overview
This sprint focuses on enhancing Lyric’s variable system by adding dynamic typing with the `var` keyword, enforcing explicit declarations, and supporting multi-variable declarations. These updates improve language clarity, prevent silent variable creation, and align Lyric’s feel closer to Python while retaining structured control.

---

## 🧠 Sprint 4 Tasks

### **Task 1 — Implement `var` Keyword (Dynamic Typing)**
**Description:**  
Add support for `var` as a declaration keyword for dynamically typed variables.
- Behaves like Python variables (`x = 10`, `x = "hello"`, etc.).
- Fully dynamic: type can change at runtime.
- Declaring with `var` is required before first assignment.
- Update interpreter and symbol table to handle `dynamic = True`.

**Acceptance Criteria:**
- `var x = 10` works as expected.  
- `x = 10` without prior declaration throws an error.  
- Type reassignment is allowed for `var` variables.  
- `CHANGELOG.md` and `README.md` updated.

---

### **Task 2 — Enforce Declaration Before Assignment**
**Description:**  
All variables must be explicitly declared before use (`var`, `int`, `str`, etc.) to prevent implicit variable creation.

**Acceptance Criteria:**
- Assigning to undeclared variable → `RuntimeError: Variable 'x' used before declaration`.  
- Referencing declared but uninitialized variable → `RuntimeError: Variable 'x' referenced before assignment`.

---

### **Task 3 — Multi-Variable Declarations**
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

### **Task 4 — Update Specification and Grammar**
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

### **Task 5 — Internal Validation & Testing**
**Description:**  
Verify correctness through dedicated test scripts covering:
- dynamic vs. static declarations  
- reassignment behavior  
- undeclared/unused variable errors  
- multi-declaration parsing

**Acceptance Criteria:**
- All tests pass without regression.  
- Manual and automated verification complete.


### **TASK 6 - AST Position Tracking & Structured Error Reporting**

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


## 📅 Definition of Done
- All acceptance criteria met for each task.  
- `CHANGELOG.md` and `README.md` updated to reflect new syntax.  
- Sprint reviewed and merged to `main` branch.  


---

*End of Sprint 4 Specification*
