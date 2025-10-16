# Lyric Language

Lyric is a lightweight interpreted programming language designed for simplicity, readability, and elegant syntax. It is implemented in Python and currently supports basic constructs such as def, if, else, end, given, done, and the class terminator +++.

## How to Run

Lyric programs use the `.ly` file extension and are executed through the command line interface.

To execute a Lyric program, open a terminal and run the command:
```
lyric run path_to_file.ly
```

For example:
```
lyric run tests/examples/hello.ly
```

This command runs the program's main function automatically if it exists. You can also check the current interpreter version with:
```
lyric --version
```

### Example Programs

The project includes several example programs that demonstrate core language features:

- **hello.ly** - Basic function definition and print statement
- **if_demo.ly** - Conditional logic with if/else statements  
- **loop.ly** - Iterator loops using the given/done construct
- **class_test.ly** - Class definition and instantiation
- **nested_flow.ly** - Nested control flow structures
- **boolean_test.ly** - Boolean and comparison operations
- **runtime_test.ly** - Runtime enhancements (isinstance, type, enhanced print)

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
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install pytest flake8
   ```

3. **Run tests**
   ```bash
   pytest tests/
   ```

4. **Check code formatting**
   ```bash
   flake8 lyric/ tests/
   ```

### Development Commands

- `pytest` runs the comprehensive test suite (88 tests covering all components)
- `flake8` enforces coding style and identifies potential issues
- `python -m lyric.cli run tests/examples/hello.ly` runs the interpreter directly if the project hasn't been installed as a package

## Project Layout

```
lyric/
├── lyric/                    # Main source code for the language
│   ├── lexer.py             # Converts source code into tokens
│   ├── parser.py            # Builds the abstract syntax tree
│   ├── ast.py               # Defines node types for syntax trees
│   ├── interpreter.py       # Executes parsed programs
│   ├── runtime.py           # Provides built-in functions like print, input, and range
│   ├── errors.py            # Defines exceptions for lexing, parsing, and runtime
│   └── cli.py               # Command line interface for running Lyric programs
├── tests/                   # Contains automated test files and example programs
│   ├── examples/            # Sample Lyric programs
│   │   ├── hello.ly         # Basic hello world program
│   │   ├── if_demo.ly       # Conditional logic demonstration
│   │   ├── loop.ly          # Iterator loop demonstration
│   │   ├── class_test.ly    # Class definition and instantiation
│   │   ├── nested_flow.ly   # Nested control flow structures
│   │   ├── boolean_test.ly  # Boolean and comparison operations
│   │   └── runtime_test.ly  # Runtime enhancements demonstration
│   ├── test_lexer.py        # Lexer test suite (22 tests)
│   ├── test_parser.py       # Parser test suite (28 tests)
│   ├── test_interpreter.py  # Interpreter test suite (26 tests)
│   └── test_cli_integration.py # CLI integration test suite (12 tests)
├── examples/                # Additional example programs
│   ├── hello.ly
│   ├── if_demo.ly
│   └── loop.ly
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

### Core Constructs

- **Functions**: `def name(params) { body }`
- **Conditionals**: `if condition: ... else: ... end`
- **Loops**: `given variable in iterable: ... done` or `given condition: ... done`
- **Classes**: `class Name: ... +++` (full implementation with instantiation and methods)
- **Variables**: Dynamic typing with assignment `name = value`
- **Comments**: `# comment text` (full-line and inline comments)

### Built-in Functions

- `print(*args)` — Multi-argument printing with space separation and None handling
- `input(prompt?)` — Read from stdin with optional prompt
- `int(value)`, `float(value)`, `str(value)` — Type conversions
- `range(start?, stop, step?)` — Integer sequence generation
- `len(sequence)` — Length calculation
- `open(path)` — File iteration over lines
- `isinstance(obj, type_name)` — Type checking for objects and class instances
- `type(obj)` — Type introspection returning string type names

### Example Syntax

```lyric
# Class definition with methods and attributes
class Player:
    name = "Guest"
    score = 0
    
    def greet() {
        print("Hello,", self.name)
    }
    
    def add_score(points) {
        self.score = self.score + points
    }
+++

def main() {
    print("Hello, Lyric!")
    
    # Conditional logic
    if 5 > 3:
        print("Math works!")
    else:
        print("Something's wrong")
    end
    
    # Iterator loops
    given i in range(3):
        print("Count:", i)
    done
    
    # Class instantiation and method calls
    player = Player()
    player.name = "Alice"
    player.greet()
    player.add_score(100)
    
    # Type checking and introspection
    print("Player type:", type(player))
    print("Is Player:", isinstance(player, "Player"))
    
    # Enhanced print with None handling
    print("Value:", None)
}
```

## License and Credits

The Lyric language is developed by **Michael (Aeonath)**, **ChatGPT**, and **Claude** as part of the **MiraNova Studios** initiative. This project represents a collaborative effort to create a clean, educational programming language implementation.

The project is currently **pre-release** and version **0.1.3** corresponds to the partial completion of Sprint 3 (Type System, Data Structures, Error Handling, and Performance). This milestone includes type declarations and inference, built-in data structures (lists and dictionaries), enhanced error handling with stack traces, runtime optimizations, and comprehensive test coverage with 143+ passing tests. Sprint 3 is currently 5/8 tasks complete with 3 additional tasks remaining.

## Contributing

This project is part of an ongoing development sprint. Future versions will include additional language features, enhanced type system, and extended runtime capabilities.

For development questions or contributions, please refer to the project's development workflow outlined above.
