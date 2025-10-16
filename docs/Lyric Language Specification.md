# Lyric Language Specification

**Version:** 0.1.3  
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

### Type Declarations

- Optional type declarations using C-style syntax
- Runtime type checking and inference
- Types are optional and can be omitted

```lyric
# Typed version
def int add_numbers(int a, int b) {
    return a + b
}

# Untyped version (also valid)
def greet(name) {
    print("Hello", name)
}

def main() {
    int x = 5          # Explicit type
    y = 10             # Type inferred as int
    str name = "Alice" # Explicit type
    result = add_numbers(x, y)
    greet(name)
}
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

## 🚫 Features Omitted in v0.1.3

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

### ✅ Implemented Features (v0.1.3)
- Core language constructs (functions, conditionals, loops)
- Class system with `+++` terminator
- Built-in data structures (lists, dictionaries)
- Type declarations and inference
- Return statements and function values
- Enhanced error handling with stack traces
- Runtime optimizations (constant folding, caching)
- Performance monitoring
- Comprehensive test suite (143+ tests)

### 🚧 Planned Features
- Import system
- Exception handling (try/catch/finally)
- File I/O operations
- Advanced type system features
- Module system
- Standard library expansion

## 💡 Example Program

```lyric
def float calculate_area(float radius) {
    return 3.14159 * radius * radius
}

def main() {
    float r = 5.0
    area = calculate_area(r)
    print("Area of circle with radius", r, "is:", area)
}
```

### Output
```
Area of circle with radius 5.0 is: 78.53975
```

## 🎵 Closing Thoughts

Lyric is designed to teach, inspire, and simplify.  
It's a bridge between thought and execution — a language that emphasizes intent, not ceremony.

> *"Code should not only work — it should sing."* 🎵

---

**Current Version:** 0.1.3 (Sprint 3 - Type System & Performance - 5/8 Tasks Complete)  
**Development Team:** Michael (Aeonath), ChatGPT, Claude  
**Project:** MiraNova Studios Initiative


