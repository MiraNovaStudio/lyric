# Sprint 7 — Class System Implementation

**Target Version:** 0.7.0

## Sprint Goal

Implement the Lyric class system with constructor support, instance methods, and the `self` keyword.

**Additional Feature:** Add an alternative alias for the `god` type called `bin`.

**Scope:** This sprint will focus only on defining, instantiating, and using classes. Inheritance and access control (public/private/protected) will be handled in Sprint 8.

## Task 1 — Implement Class Definition Syntax

Classes begin with the keyword `class` and terminate with `+++`.

**Example syntax:**
```lyric
class Person:
    var name
    def Person() {
        print("Hello, I am ", self.name)
    }
+++
```

**Implementation:**
- The parser must recognize class blocks and store defined methods and attributes within a class object.
- Each class should have its own namespace for variables and methods.

### Acceptance Criteria:
- `class` keyword and `+++` terminator recognized.
- Parser correctly groups code between `class` and `+++`.
- Methods and variables defined inside class are attached to class scope.
- Nested or multiple class definitions in one file supported.

## Task 2 — Add Constructor Recognition

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

## Task 3 — Add Object Instantiation and Self Keyword

Add ability to create objects and call methods on them.

**Syntax:**
- Use standard function-call syntax for instantiation:
```lyric
var p = Person()
p.Person()
```

**Self Keyword:**
- The `self` keyword must automatically reference the instance object in all class methods.

**Example:**
```lyric
class Person:
    var name
    def Person() {
        self.name = "Unknown"
    }
    def greet() {
        print("Hello, I am ", self.name)
    }
+++

var user = Person()
user.greet()
```

### Acceptance Criteria:
- Objects can be instantiated with parentheses syntax.
- `self` references the instance correctly within all methods.
- Instance variables retain their values between method calls.
- Calling methods on object instances executes correctly.
- Error handling works if a method or property does not exist.

## Task 4 — Add Class Method and Property Access

Methods and variables inside classes should be accessible via dot notation.

**Example:**
```lyric
var p = Person()
p.name = "Michael"
p.greet()
```

### Acceptance Criteria:
- Dot notation works for property access and method calls.
- Assigning to an undeclared property raises an error.
- Properties persist across method calls for the same instance.
- Parser handles chained access correctly (`p.address.city`).

## Task 5 — Add Alternative Type Name Bin for God Type

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

## Task 6 — Documentation and Changelog Updates

Update `README.md` and `CHANGELOG.md` to describe:

**Content:**
- `class` definition and `+++` terminator.
- Constructor syntax (`def ClassName()`).
- `self` keyword behavior and usage examples.
- `bin` type alias for `god`.
- Include multiple examples of class creation, property assignment, and method calling.

### Acceptance Criteria:
- Documentation includes syntax and examples for `class`, `self`, and `bin`.
- CHANGELOG updated for version 0.2.2.

## Definition of Done

- Class syntax implemented and parser recognizes `class` and `+++`.
- Constructors function automatically when instances are created.
- `self` keyword works correctly inside all class methods.
- Dot notation works for accessing methods and variables.
- `bin` alias for `god` implemented and documented.
- All new features tested and verified through example programs.
- Documentation and CHANGELOG updated.
