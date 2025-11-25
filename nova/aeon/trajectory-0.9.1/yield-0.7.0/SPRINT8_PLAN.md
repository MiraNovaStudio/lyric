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

### Task 8 – Implement and Test `arr` Methods (List API)

**Summary:**  
Expand Lyric’s `arr` type to support core list-style operations. These methods must behave consistently with Python list semantics where applicable, except that iterable-based operations are excluded. All built-in list functions are converted into instance methods (e.g., `mylist.len()`).

**Methods to Add (Unit Tests Required for Each):**

1. **append(element)** – Add a single element to the end of the list.  
2. **clear()** – Remove all elements, making the list empty.  
3. **copy()** – Return a shallow copy of the list.  
4. **count(value)** – Return number of occurrences of `value`.  
5. **index(value, start, end)** – Return index of first occurrence; raise `ValueError` if not found.  
6. **insert(index, element)** – Insert `element` at index, shifting items right.  
7. **pop(index)** – Remove and return item at index; default to last item; raise `IndexError` if invalid.  
8. **remove(value)** – Remove first occurrence of `value`; raise `ValueError` if missing.  
9. **reverse()** – Reverse list in place.  
10. **sort(key=None, reverse=False)** – Sort list in place; support optional key and reverse parameters.

**Built-In Functions Converted to Methods:**

11. **len()** – Return number of elements in the list.  
12. **max()** – Return largest element; error if list is empty.  
13. **min()** – Return smallest element; error if list is empty.  
14. **sum()** – Return sum of numeric elements; raise `TypeError` on non-numeric values.

**Acceptance Criteria:**  
- All above methods are implemented on the `arr` type.  
- Each method includes at least one unit test in `lyric/tests/core-0.7.0`.  
- Error conditions (`ValueError`, `IndexError`, `TypeError`) are fully tested.  
- Methods operate on the instance (`mylist.method()`), not as global built-ins.  
- All new tests pass in the Lyric test runner.


### Task 9 – Implement and Test `dict` Methods (Dictionary API)

**Summary:**  
Expand Lyric’s `dict` type to support core dictionary operations. Methods should follow Python-style semantics where applicable. Iterable-based updates (such as iterable of pairs) are excluded unless the source is another Lyric `dict`. Built-in functions like `len()` and `sorted()` are implemented as instance methods (`mydict.len()`, `mydict.sorted()`).  
Also add support for `key in dict` membership checks during iteration, and iteration over keys in `for` loops.

**Methods to Add (Unit Tests Required for Each):**

1. **clear()** – Remove all items from the dictionary.  
2. **copy()** – Return a shallow copy of the dictionary.  
3. **fromkeys(seq, value=None)** – Class method: create a new dictionary from a sequence of keys with an optional default value.  
4. **get(key, default=None)** – Return value for key; return default (or `None`) instead of raising a `KeyError`.  
5. **items()** – Return a view/list of `(key, value)` pairs.  
6. **keys()** – Return a view/list of all keys.  
7. **pop(key, default)** – Remove and return value for key; raise `KeyError` if missing and no default provided.  
8. **popitem()** – Remove and return the last inserted `(key, value)` pair.  
9. **setdefault(key, default=None)** – Return value for key; if missing, insert key with default value and return default.  
10. **update(other_dict)** – Update dictionary with key-value pairs from another dict.  
11. **values()** – Return a view/list of all values.

**Built-In Functions Converted to Methods:**

12. **len()** – Return number of items in the dictionary.  
13. **sorted()** – Return a sorted list of keys (ascending by default).

**Language Features to Add:**

14. **`key in dict` Membership Check** – Return `true` if the key exists, `false` otherwise.  
15. **Dictionary Iteration** – Iterating a dict in a `for` loop should yield keys in insertion order.

**Acceptance Criteria:**  
- All dictionary methods above are implemented on the `dict` type.  
- Each method includes at least one unit test in `lyric/tests/core-0.7.0`.  
- Error conditions (`KeyError`, type errors, missing defaults) are fully tested.  
- Built-in behaviors (`len()`, `sorted()`, membership checks, iteration) function correctly.  
- Iterating a dict produces keys in insertion order.  
- All new tests pass in the Lyric test runner.

