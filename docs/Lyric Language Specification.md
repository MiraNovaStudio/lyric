# Lyric Language Specification

**Version:** 0.4.0  
**Authors:** Michael (Aeonath), ChatGPT, and Claude  
**Project:** MiraNova Studios Initiative  
**Date:** October 2025  

---

## 🌙 Overview

**Lyric** is a modern, beginner-friendly programming language designed for simplicity, readability, and elegance.
It blends Python’s clean structure with a clear, expressive syntax that emphasizes understanding over complexity.
Lyric is intended for use in introductory computer science courses, helping students learn core programming concepts through an approachable and consistent language design.

The language is implemented in Python and currently supports core programming constructs including functions, conditionals, loops, classes, and built-in data structures with comprehensive error handling and performance optimizations.  

---

## 🧭 Design Philosophy

> *Readable like pseudocode, structured like Python, expressive like poetry.*

1. **Clarity before cleverness** — syntax must express intent plainly.  
2. **Simplicity over completeness** — features exist only when they add clarity.  
3. **Visual harmony** — indentation and rhythm matter.  
4. **Consistency** — similar constructs end with parallel patterns (`end`, `done`, `fade`, `+++`).  
5. **Braces only where needed** — functions use braces; everything else uses natural terminators.

---

## 🧩 Syntax Summary
| **Construct**         | **Summary**                                                                                   |
| --------------------- | --------------------------------------------------------------------------------------------- |
| **Conditional**       | Opens with `if`, `else if`, or `else`; closes with `end`. Replaces Python’s `elif`.           |
| **Loop**              | Opens with `given`, closes with `done`. Unifies both `for` and `while` behavior.              |
| **Function**          | Defined with `def` and enclosed in `{ ... }`. Only construct using braces.                    |
| **Class**             | Declared with `class`, closed by symbolic `+++` marker. Adds the class to program scope.      |
| **Try / Except**      | Structured with `try`, `except`, `finally`, closed by `fade`. Handles exceptions inside `{}`. |
| **Import System**     | Uses `import` for Lyric modules and `importpy` for Python bridges. Single-line syntax.        |
| **Entry Point**       | Always begins with `def main()`. Acts as the mandatory starting function.                     |
| **Lists**             | Declared with `[ ... ]`. Built-in sequence type.                                              |
| **Dictionaries**      | Declared with `{ ... }`. Built-in key/value data type.                                        |
| **Type Declarations** | Supports `int`, `str`, `flt`, `var`, and `pyobject`. `var` enables dynamic typing.          |


## 🔹 Basic Structure

Every Lyric program starts execution in a **main function**.  
There is no `__name__` or hidden runtime boilerplate.

```lyric
def main() {
    print("Hello, world!")
}
```

## ⚙️ Core Constructs

### Conditionals

- Uses `else if` instead of `elif`
- Block introduced by `:` and closed by `end`

```lyric
if x > 0:
    print("positive")
else if x < 0:
    print("negative")
else:
    print("zero")
end
```

### Loops

- `given` replaces both `for` and `while`
- Ends with `done`

```lyric
# Iterator loop
given i in range(5):
    print(i)
done

# While loop
given n > 0:
    print(n)
    n -= 1
done
```


### Functions

- Braces used only for functions
- Indentation purely stylistic, not structural

```lyric
def greet(name) {
    print("Hello,", name)
}
```

### Classes

- `+++` closes a class, symbolizing addition of a structure to the program
- Classes are lightweight containers for variables and functions
- `+++` is supposed to symbolize attaching a data structure to a program

```lyric
class Player:
    name = "Guest"

    def greet() {
        print("Hello,", self.name)
    }
+++
```

### Data Structures

- Lists and dictionaries with indexing support
- Built-in functions for manipulation

```lyric
def main() {
    # Lists
    numbers = [1, 2, 3, 4, 5]
    print("First number:", numbers[0])
    
    # Dictionaries
    person = {"name": "Alice", "age": 30}
    print("Name:", person["name"])
}
```

### Importing (Planned)
- `from … import …` replaced with direct or semicolon syntax

```lyric
import math
import random.randint
import random; randint, randrange
import os as system
```

### File I/O (Planned)
- `given` reads naturally with iterables
- Explicit and readable file handling

```lyric
def main() {
    total = 0
    given line in open("numbers.txt"):
        total += int(line.strip())
    done
    print("Total:", total)
}
```

### Error Handling (Planned)
- Uses familiar Python-style exception handling
- Syntax simplified: `except: ErrorType:`

```lyric
def main() {
    try:
        n = int(input("Enter a number: "))
        print("Half:", n / 2)
    except: ValueError:
        print("Invalid input")
    finally:
        print("Done")
    fade
}
```

### Variable Declaration and Assignment

Lyric supports both static and dynamic typing through explicit declarations.
All variables must be declared before use, preventing implicit variable creation or shadowing.

- Static typing is achieved by declaring a variable with a specific type (int, str, bool, etc.). Once declared, its type cannot change.

```
int count = 10
count = "ten"  # ❌ TypeError
```

- Dynamic typing is enabled through the var keyword, which allows the variable’s type to change at runtime.

```
var value = 10
value = "ten"  # ✅ Allowed
```


#### Declaration Syntax

**Dynamic Typing with `var`:**
```lyric
var x = 10           # Dynamic variable, can change type
var name = "Alice"   # Can be reassigned to different types
x = "hello"          # Type change allowed for var variables
```

**Static Type Declarations:**
```lyric
int count = 5        # Integer variable
str message = "Hi"   # String variable  
flt pi = 3.14        # Float variable
var dynamic = true   # Dynamic variable (can change type)
```

**Multi-Variable Declarations:**
```lyric
# Simple multi-declarations (same base type)
var x, y, z
int a, b, c
str name, message

# Mixed-type multi-declarations
var x, int y, str z
int count, var temp, flt pi
```

#### Declaration and Initialization Rules

1. **Declaration Before Use**: All variables must be explicitly declared before assignment or reference
2. **Initialization Tracking**: Variables are marked as declared but uninitialized until first assignment
3. **Type Enforcement**: Static types enforce type checking at runtime
4. **Dynamic Flexibility**: `var` variables can change type during reassignment

#### Error Handling

**Undeclared Variable Assignment:**
```lyric
def main() {
    x = 10  # Error: Variable 'x' used before declaration
}
```

**Referencing Uninitialized Variable:**
```lyric
def main() {
    var x    # Declared but uninitialized
    print(x) # Error: Variable 'x' referenced before assignment
    x = 10   # Now initialized
    print(x) # Works: prints 10
}
```

**Type Mismatch:**
```lyric
def main() {
    int x = 10
    x = "hello"  # Error: Type mismatch: cannot assign str to variable 'x' declared as int. Expected int, but got str. Use 'var x = ...' if you need dynamic typing.
}
```

**Invalid Type in Multi-Declaration:**
```lyric
def main() {
    invalid_type x, int y  # Error: Unknown type 'invalid_type' at line 1, column 1. Valid types are: int, str, flt, var
}
```

**PyObject Restriction:**
```lyric
def main() {
    pyobject x, int y  # Error: Type 'pyobject' is internal only and cannot be used in explicit declarations at line 1, column 1
}
```

#### Function Type Declarations

```lyric
# Typed function with parameters and return type
def int add_numbers(int a, int b) {
    return a + b
}

# Mixed typed and untyped parameters
def str format_greeting(str name, int age) {
    return "Hello " + name + ", age " + str(age)
}

# Dynamic function (no type declarations)
def greet(name) {
    print("Hello", name)
}

def main() {
    var result = add_numbers(5, 10)        # Dynamic variable
    int sum = add_numbers(20, 30)          # Static variable
    str greeting = format_greeting("Alice", 25)
    greet("World")
}
```

#### Grammar Rules

**Variable Declaration Grammar:**
```
variable_declaration := 
    | single_declaration
    | multi_declaration

single_declaration :=
    | type_annotation identifier '=' expression
    | 'var' identifier '=' expression

multi_declaration :=
    | base_type identifier (',' declaration_item)*

declaration_item :=
    | identifier                    # Uses base_type
    | type_annotation identifier    # Overrides base_type

base_type :=
    | 'var'
    | 'int'
    | 'str'
    | 'flt'
    | 'pyobject'

type_annotation :=
    | 'int'
    | 'str'
    | 'flt'
    | 'var'

identifier := [a-zA-Z_][a-zA-Z0-9_]*
```

**Examples of Valid Grammar:**
```lyric
# Single declarations
var x = 10
int count = 5
str name = "Alice"

# Multi-declarations (simple)
var x, y, z
int a, b, c

# Multi-declarations (mixed types)
var x, int y, str z
int count, var temp, flt pi
```

### Advanced Class Example

```lyric
class Counter
    value = 0

    def Counter(start) {
        self.value = start
    }

    def increment() {
        self.value += 1
    }

    def get_string() {
        return str(self.value)
    }
+++

def main() {
    c = Counter()
    given i in range(3)
        c.increment()
    done
    print("Count:", c)
}
```

## 🚫 Features Omitted in v0.1.6

To maintain simplicity and focus on core concepts:

- **No comprehensions** (`[x for x in y]`)
- **No lambdas** (anonymous functions)
- **No decorators** (function modifiers)
- **No context managers** (`with` statements)
- **No async/await** (asynchronous programming)
- **No complex imports** (module system)
- **No exception handling** (try/catch blocks)

Lyric is about learning and clarity, not syntax density.

## 📋 Current Implementation Status

### ✅ Implemented Features (v0.4.0)
- Core language constructs (functions, conditionals, loops)
- Class system with `+++` terminator
- Built-in data structures (lists, dictionaries)
- Type declarations and inference
- Return statements and function values
- Enhanced error handling with stack traces
- Runtime optimizations (constant folding, caching)
- Performance monitoring
- **Dynamic typing with `var` keyword**
- **Declaration enforcement (all variables must be declared)**
- **Multi-variable declarations with comma-separated syntax**
- **Mixed-type multi-declarations support**
- Comprehensive test suite (334+ tests)

### 🚧 Planned Features
- Advanced exception handling enhancements
- File I/O operations
- Advanced type system features
- Module system expansion
- Standard library expansion

## 💡 Example Program

```lyric
# Multi-variable declarations with mixed types
var x, int y, str name

# Static type declarations
flt pi = 3.14159
var active = true

def flt calculate_area(flt radius) {
    return pi * radius * radius
}

def str format_result(flt area, str shape) {
    return "Area of " + shape + ": " + str(area)
}

def main() {
    # Initialize multi-declared variables
    x = 10
    y = 5
    name = "Circle"
    
    # Calculate area using typed function
    var area = calculate_area(5.0)  # Dynamic variable
    str result = format_result(area, name)  # Static variable
    
    print(result)
    print("Dynamic x:", x, "type:", type(x))
    print("Static y:", y, "type:", type(y))
    
    # Demonstrate type flexibility with var
    x = "Hello"
    print("Now x is:", x, "type:", type(x))
}
```

### Output
```
Area of Circle: 78.53975
Dynamic x: 10 type: int
Static y: 5 type: int
Now x is: Hello type: str
```

## 🎵 Closing Thoughts

Lyric is designed to teach, inspire, and simplify.  
It's a bridge between thought and execution — a language that emphasizes intent, not ceremony.

> *"Code should not only work — it should sing."* 🎵

---

**Current Version:** 0.1.6 (Sprint 4 - Variable Handling & Declaration Syntax - COMPLETE)  
**Development Team:** Michael (Aeonath), ChatGPT, Claude  
**Project:** MiraNova Studios Initiative


