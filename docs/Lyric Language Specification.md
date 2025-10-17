# Lyric Language Specification

**Version:** 0.1.6  
**Authors:** Michael (Aeonath), ChatGPT, and Claude  
**Project:** MiraNova Studios Initiative  
**Date:** December 2024  

---

## 🌙 Overview

**Lyric** is a modern, beginner-friendly programming language designed for simplicity, readability, and elegance.  
It blends Python's clean structure with a touch of natural language rhythm — code that reads like thought and feels like poetry.  

Lyric minimizes syntax noise, avoids redundant symbols, and introduces symbolic elegance (`+++`, `done`, `end`) to clarify program flow.

The language is implemented in Python and currently supports core programming constructs including functions, conditionals, loops, classes, and built-in data structures with comprehensive error handling and performance optimizations.  

---

## 🧭 Design Philosophy

> *Readable like pseudocode, structured like Python, expressive like poetry.*

1. **Clarity before cleverness** — syntax must express intent plainly.  
2. **Simplicity over completeness** — features exist only when they add clarity.  
3. **Visual harmony** — indentation and rhythm matter.  
4. **Consistency** — similar constructs end with parallel patterns (`end`, `done`, `+++`).  
5. **Braces only where needed** — functions use braces; everything else uses natural terminators.

---

## 🧩 Syntax Summary

| Construct | Open | Close | Status | Notes |
|------------|-------|--------|--------|-------|
| Conditional | `if`, `else if`, `else` | `end` | ✅ Implemented | Replaces `elif` with `else if` |
| Loop | `given` | `done` | ✅ Implemented | Unifies `for` and `while` |
| Function | `def` | `{ ... }` | ✅ Implemented | Only construct using braces |
| Class | `class` | `+++` | ✅ Implemented | Symbolic closure (adds class to program) |
| Try/Except | `try`, `except`, `finally` | implicit | 🚧 Planned | Structured inside `{}` |
| Import | `import` | — | 🚧 Planned | Simplified single-line import |
| Entry Point | `main()` | — | ✅ Implemented | Required start of every program |
| Lists | `[ ... ]` | `[ ... ]` | ✅ Implemented | Built-in data structures |
| Dictionaries | `{ ... }` | `{ ... }` | ✅ Implemented | Built-in data structures |
| Type Declarations | `int name` | — | ✅ Implemented | Optional C-style type declarations |

---

## 🔹 Basic Structure

Every Lyric program starts execution in a **main function**.  
There is no `__name__` or hidden runtime boilerplate.

```lyric
def main() {
    print("Hello, world!")
}


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
}
```

### Variable Declaration and Assignment

Lyric supports both dynamic and static typing with strict declaration enforcement. All variables must be explicitly declared before use to prevent implicit variable creation.

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
god active = true   # Boolean variable (named in honor of logician Kurt Gödel)
float pi = 3.14      # Float variable
None value = None    # None variable
```

**Multi-Variable Declarations:**
```lyric
# Simple multi-declarations (same base type)
var x, y, z
int a, b, c
str name, message

# Mixed-type multi-declarations
var x, int y, str z
int count, var temp, god flag
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
    x = "hello"  # Error: Type mismatch for variable 'x': expected int, got str
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
    | 'god'
    | 'float'
    | 'None'

type_annotation :=
    | 'int'
    | 'str'
    | 'god'
    | 'float'
    | 'None'

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
int count, var temp, god flag
```

### Advanced Class Example

```lyric
class Counter:
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
    given i in range(3):
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

### ✅ Implemented Features (v0.1.6)
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
- Comprehensive test suite (226+ tests)

### 🚧 Planned Features
- Import system
- Exception handling (try/catch/finally)
- File I/O operations
- Advanced type system features
- Module system
- Standard library expansion

## 💡 Example Program

```lyric
# Multi-variable declarations with mixed types
var x, int y, str name

# Static type declarations
float pi = 3.14159
god active = true

def float calculate_area(float radius) {
    return pi * radius * radius
}

def str format_result(float area, str shape) {
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


