# Lyric Language

Lyric is a lightweight interpreted programming language designed for simplicity, readability, and elegant syntax. This project is being developed from scratch to test our development processes and create a clean, educational programming language implementation.

**Status**: Active Development - Version 0.7.4 (Pre-Alpha)

## Project Goals

This iteration of Lyric is being built from the ground up to:
- Test and refine our development processes
- Create a clean, minimal language implementation
- Establish proper testing and documentation practices
- Build a solid foundation for future language features

## Current State

The project has completed Sprint 1, Sprint 2, Sprint 3, Sprint 4, and Sprint 5 with:
- ✅ Complete lexer implementation with tokenization
- ✅ Recursive descent parser with AST generation
- ✅ Interpreter with scope management and built-in functions
- ✅ CLI interface for running Lyric programs
- ✅ Comprehensive test suite (436 tests)
- ✅ Class definitions and instantiation
- ✅ Nested control flow (if/else, given/done)
- ✅ Error reporting with line numbers
- ✅ Built-in functions (print, input, int, float, str, range, len, isinstance, type)
- ✅ List literals and None support
- ✅ Typed variable declarations (int, str, flt, var)
- ✅ Dictionary literals and indexing
- ✅ Class constructors with init() methods
- ✅ Exception handling (try/catch/finally)
- ✅ Return statements and function parameters
- ✅ Python interoperability with `importpy` statement
- ✅ `pyobject` type system integration
- ✅ Multi-variable declarations with mixed types (`var x, int y, str z`)
- ✅ Dynamic typing with `var` keyword
- ✅ AST position tracking for precise error reporting
- ✅ Optional colon syntax across all core constructs
- ✅ Native regular expression support with `rex` type and `/pattern/` literals
- ✅ Boolean types (`god` and `bin`) with `true`/`false` literals
- ✅ Enhanced CLI with `lyric run file.ly` and `lyric file.ly` commands
- ✅ Global `lyric` command availability after `pip install`

## How to Run

Lyric programs use the `.ly` file extension and are executed through the command line interface:

```bash
lyric run path_to_file.ly
# or simply:
lyric path_to_file.ly
```

For example:
```bash
lyric run lyric/tests/examples/hello.ly
lyric run lyric/tests/examples/class_test.ly
```

### Example Programs

**Hello World** (`lyric/tests/examples/hello.ly`):
```lyric
def main() {
    print("Hello, Lyric!")
}
```

**Typed Variables** (`lyric/tests/examples/type_tests.ly`):
```lyric
# Type declarations with enforcement
int age = 25
str name = "Alice"
flt pi = 3.14159
var dynamic = "anything"

# Type enforcement prevents mismatches
# int count = "hello"  # This would cause a type error

print("Name:", name, "Age:", age, "PI:", pi)
```

**Lists and Dictionaries** (`lyric/tests/examples/list_dict_tests.ly`):
```lyric
# List literals and operations
var numbers = [1, 2, 3, 4, 5]
var fruits = ["apple", "banana", "cherry"]

# Dictionary literals and access
var person = {"name": "Alice", "age": 30, "city": "New York"}
var settings = {"theme": "dark", "language": "en"}

# Indexing and modification
numbers[0] = 10
person["age"] = 31

print("First number:", numbers[0])
print("Person name:", person["name"])
print("List length:", len(numbers))
```

**Class with Constructor** (`lyric/tests/examples/class_init_tests.ly`):
```lyric
class Person:
    def init(str name, int age) {
        self.name = name
        self.age = age
        self.greeting = "Hello, I'm " + name
    }
    
    def greet() {
        print(self.greeting)
        print("I am", self.age, "years old")
    }
+++

def main() {
    var person = Person("Alice", 30)
    person.greet()
    
    # Access instance variables
    print("Name:", person.name)
    print("Age:", person.age)
}
```

**Regular Expressions** (`lyric/tests/examples/regex_demo.ly`):
```lyric
# Regular expression literals with /pattern/ syntax
rex email_pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
rex phone_pattern = /^\d{3}-\d{3}-\d{4}$/

# Test email validation
var email = "user@example.com"
if email_pattern.match(email):
    print("Valid email address")
else:
    print("Invalid email address")

# Replace operations
rex space_pattern = /\s+/
var text = "hello    world   with   spaces"
var cleaned = space_pattern.replace(text, " ")
print(cleaned)  # prints "hello world with spaces"

# Multiple replacements
rex vowel_pattern = /[aeiou]/i
var message = "Hello World"
var result = vowel_pattern.replace(message, "*")
print(result)  # prints "H*ll* W*rld"
```

**Boolean Types** (`lyric/tests/examples/boolean_demo.ly`):
```lyric
# God type (honoring Kurt Gödel)
god is_valid = true
god is_complete = false

# Bin type (alternative boolean type)
bin is_active = true
bin is_pending = false

# Both types work identically
if is_valid and is_active:
    print("Both conditions are true")

# Type checking
print(type(is_valid))  # prints "god"
print(type(is_active)) # prints "bin"

# Logical operations
var result = is_valid or is_complete
print(result)  # prints true

# Comparisons
var comparison = 5 > 3
print(comparison)  # prints true
print(type(comparison))  # prints "god"
```

**Python Interoperability** (`lyric/tests/examples/importpy_tests.ly`):
```lyric
# Import Python modules using importpy
importpy math
importpy datetime

# Use Python functions and constants
var result = math.sqrt(16)
print(result)  # prints 4.0

var pi = math.pi
print(pi)      # prints 3.141592653589793

# Access Python classes and methods
var now = datetime.datetime.now()
print(now.year)  # prints current year

# Chained member access works
var today = datetime.date.today()
print(today)

# Multiple modules
importpy os
var current_dir = os.getcwd()
print(current_dir)

# pyobject values work seamlessly with var type
var math_obj = math
var sqrt_func = math_obj.sqrt
var result2 = sqrt_func(25)
print(result2)  # prints 5.0
```

**Exception Handling** (`lyric/tests/examples/exception_tests.ly`):
```lyric
# Basic try/catch/finally
try:
    var result = 10 / 0
    print("Result:", result)
catch:
    print("Division by zero caught!")
finally:
    print("Cleanup completed")
fade

# Exception handling in functions
def safe_divide(int a, int b) {
    try:
        return a / b
    catch:
        print("Division failed, returning 0")
        return 0
    finally:
        print("Division attempt completed")
    fade
}

var result = safe_divide(10, 0)
print("Safe result:", result)
```

**Complex Example** (combining all features):
```lyric
class BankAccount:
    def init(str owner, flt initial_balance) {
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []
    }
    
    def deposit(flt amount) {
        self.balance = self.balance + amount
        append(self.transactions, "Deposit: " + str(amount))
    }
    
    def withdraw(flt amount) {
        try:
            if self.balance >= amount:
                self.balance = self.balance - amount
                append(self.transactions, "Withdrawal: " + str(amount))
            else:
                raise ValueErrorLyric
        catch:
            print("Insufficient funds!")
        finally:
            print("Transaction attempt completed")
        end
    }
+++

def main() {
    var account = BankAccount("Alice", 1000.0)
    account.deposit(500.0)
    account.withdraw(200.0)
    
    print("Account owner:", account.owner)
    print("Current balance:", account.balance)
    print("Transaction count:", len(account.transactions))
}
```

## How to Develop

Development requires Python 3.8 or newer.

### Basic Workflow

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lyric
   ```

2. **Install dependencies**
   ```bash
   pip install pytest flake8 setuptools
   ```

3. **Run tests** (once implemented)
   ```bash
   pytest tests/
   ```

4. **Check code formatting**
   ```bash
   flake8 lyric/ tests/
   ```

### Development Commands (Future)

- `pytest` will run the comprehensive test suite
- `flake8` enforces coding style and identifies potential issues
- `python -m lyric.cli run examples/hello.ly` will run the interpreter directly

## Planned Project Layout

```
lyric/
├── lyric/                    # Main source code for the language
│   ├── lexer.py             # Converts source code into tokens
│   ├── parser.py            # Builds the abstract syntax tree
│   ├── ast.py               # Defines node types for syntax trees
│   ├── interpreter.py       # Executes parsed programs
│   ├── runtime.py           # Provides built-in functions
│   ├── errors.py            # Defines exceptions for lexing, parsing, and runtime
│   └── cli.py               # Command line interface for running Lyric programs
├── tests/                   # Contains automated test files and example programs
│   ├── examples/            # Sample Lyric programs
│   ├── test_lexer.py        # Lexer test suite
│   ├── test_parser.py       # Parser test suite
│   ├── test_interpreter.py  # Interpreter test suite
│   └── test_cli_integration.py # CLI integration test suite
├── examples/                # Additional example programs
├── README.md                # Project overview and setup instructions
├── CHANGELOG.md             # Version history and release notes
└── pyproject.toml           # Build configuration and CLI entry point
```

## Dependencies

The following Python packages are required for development:

- **pytest** — for comprehensive testing of all language components
- **flake8** — for linting and style checking
- **setuptools** — for package building and CLI entry point configuration

All dependencies can be installed with pip:
```bash
pip install pytest flake8 setuptools
```

## Language Features

### Core Constructs (Implemented)

- **Functions**: `def name(params) { body }` with optional return statements ✅
- **Conditionals**: `if condition: ... else: ... end` with nested support ✅
- **Loops**: `given variable in iterable: ... done` or `given condition: ... done` ✅
- **Classes**: `class Name: ... +++` with instantiation, methods, and member access ✅
- **Variables**: Dynamic typing with `name = value` assignment ✅
- **Typed Variables**: `int name = value`, `str name = value`, `flt name = value`, `var name = value` ✅
- **Boolean Types**: `god name = true/false` and `bin name = true/false` (honoring Kurt Gödel) ✅
- **Regular Expressions**: `rex name = /pattern/` with `.match()` and `.replace()` methods ✅
- **Data Structures**: `[item1, item2, ...]` for lists and `{"key": value}` for dictionaries ✅
- **Exception Handling**: `try: ... catch: ... finally: ... fade` with error propagation ✅
- **Comments**: `# comment text` (full-line and inline comments) ✅
- **Python Interoperability**: `importpy module` for seamless Python library access ✅

### Built-in Functions (Implemented)

- `print(*args)` — Multi-argument printing ✅
- `input(prompt?)` — Read from stdin with optional prompt ✅
- `int(value)`, `float(value)`, `str(value)` — Type conversions ✅
- `range(start?, stop, step?)` — Integer sequence generation ✅
- `len(sequence)` — Length calculation for strings, lists, dictionaries ✅
- `isinstance(obj, type)` — Type checking for classes and built-in types ✅
- `type(obj)` — Get type name of objects ✅
- `append(list, item)` — Add items to lists ✅
- `keys(dict)` — Get dictionary keys ✅
- `values(dict)` — Get dictionary values ✅

### Planned Features (Future Sprints)

- **Modules**: Import/export system
- **File I/O**: Enhanced file operations
- **Advanced Type System**: Generic types and type inference
- **Standard Library**: Extended built-in functions and utilities

### Module System

Lyric's upcoming module system is designed around two complementary import mechanisms. Native Lyric modules — written in `.ly` files — will be resolved and cached by a `ModuleLoader` at runtime, keeping programs fully self-contained with no Python dependency. These modules will form the basis of a growing standard library covering areas such as math, I/O, string handling, and JSON. The import syntax is clean and familiar: `import mathutils` loads a native module, and the runtime searches a configurable module path before falling back to built-ins.

For interoperability with the broader Python ecosystem, Lyric retains its existing `importpy` bridge, which uses Python's `importlib` to load packages like `numpy` or `requests` and wraps their return values into Lyric types. This is intentionally kept as a secondary mechanism — users are aware when they cross the Python boundary, and the long-term goal is for native Lyric modules to replace most such dependencies. The full hybrid module system is targeted for stabilization in version 1.0.0.

## Development Process

This project follows a structured sprint-based development approach:

1. **Sprint Planning**: Each sprint has defined tasks and goals
2. **Implementation**: Code is developed incrementally with tests
3. **Documentation**: Changes are documented in changelog entries
4. **Version Control**: Structured commits with clear messages
5. **Testing**: Comprehensive test coverage for all components

## License and Credits

The Lyric language is developed by **Michael (Aeonath)**, **ChatGPT**, and **Claude** as part of the **MiraNova Studios** initiative. This project represents a collaborative effort to create a clean, educational programming language implementation.

Licensed under the MiraNova Software License. See the `LICENSE` file for full terms. All rights reserved — © 2025–2026 MiraNova Studios.

## Contributing

This project is currently in active development following a structured sprint methodology. The development process emphasizes:

- Clean, readable code
- Comprehensive testing
- Clear documentation
- Incremental feature development
- Proper version control practices

For development questions or contributions, please refer to the project's development workflow and sprint documentation.
