## Sprint 8 Plan — Lyric 0.7.0 Iteration

### Summary
This sprint expands Lyric’s core type system and import features to strengthen modularity and data handling.  
We’ll introduce the new `arr` and `map` collection types, implement the `import` statement for module management, and refine function declaration syntax for improved readability.  
This iteration lays the groundwork for module organization and type interoperability ahead of the 0.7.0 release.

---

### Task 1 – Add `arr` type for Python lists
**Summary:**  
Introduce a dedicated `arr` type mapped to Python’s native `list`, giving Lyric consistent array behavior and better parity with other typed languages.

**Implementation Items:**  
- Add `arr` token to the type registry.  
- Map internally to Python’s `list` object.  
- Support indexing, slicing, and iteration.

**Acceptance Criteria:**  
- `arr` behaves as a list equivalent in all basic operations.  
- Indexing, slicing, and iteration validated by unit tests.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 2 – Add `map` type for Python dictionaries
**Summary:**  
Add a native `map` type to represent key/value collections, aligning Lyric more closely with common language standards for associative arrays.

**Implementation Items:**  
- Add `map` token to the type registry.  
- Map internally to Python’s `dict`.  
- Enable key/value access, updates, and iteration.

**Acceptance Criteria:**  
- `map` supports standard dictionary operations.  
- Key/value types enforced during assignment and casting.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 3 – Add basic `import` statement
**Summary:**  
Implement foundational module import capability to allow structured program organization and external module usage within Lyric scripts.

**Implementation Items:**  
- Create parser rule for `import module_name`.  
- Resolve modules via Lyric search paths or Python `importlib`.

**Acceptance Criteria:**  
- Imported module symbols accessible in global scope.  
- Import failures produce clear diagnostic errors.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 4 – Add method import syntax
**Summary:**  
Expand import behavior to allow selective symbol imports using the form `import module; func1, func2`, giving developers finer control over namespace exposure.

**Implementation Items:**  
- Extend grammar to handle multiple symbol imports.  
- Inject imported functions or variables into current scope.

**Acceptance Criteria:**  
- Multiple imports resolve and bind successfully.  
- Duplicate imports or undefined symbols handled gracefully.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 5 – Add casting rules for `arr`
**Summary:**  
Define conversion rules between `arr` and other compatible types to ensure consistent and predictable behavior during type casting.

**Implementation Items:**  
- Implement `arr(str)` and `arr(map)` constructors.  
- Support conversions where element coercion is valid.

**Acceptance Criteria:**  
- Valid casts succeed with correct data conversion.  
- Invalid casts raise a standardized `TypeError`.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 6 – Add casting rules for `map`
**Summary:**  
Extend Lyric’s type interoperability by supporting conversions to and from `map`, including array and string conversions when possible.

**Implementation Items:**  
- Implement `map(arr)` and `map(str)` conversion rules.  
- Enforce proper type inference for keys and values.

**Acceptance Criteria:**  
- `map` conversions yield correctly typed dictionary objects.  
- Casting behavior verified across unit tests.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.

---

### Task 7 – Change function return-type declaration
**Summary:**  
Simplify function declaration syntax by removing redundant keyword combinations and enabling both explicit typing and automatic type inference.

**Implementation Items:**  
- Remove `str def func()` form.  
- Support:
  - `str funcname()` → explicit typed return  
  - `def funcname()` → inferred or void return  
- Update parser logic and documentation accordingly.

**Acceptance Criteria:**  
- New syntax compiles and executes correctly.  
- Functions infer return type automatically or default to `None`.  
- Add and update related unit tests in `lyric/tests/core-0.7.0`.
