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

The project includes three example programs that demonstrate core language features:

- **hello.ly** - Basic function definition and print statement
- **if_demo.ly** - Conditional logic with if/else statements  
- **loop.ly** - Iterator loops using the given/done construct

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

- `pytest` runs the comprehensive test suite (56 tests covering all components)
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
│   │   └── loop.ly          # Iterator loop demonstration
│   ├── test_lexer.py        # Lexer test suite (18 tests)
│   ├── test_parser.py       # Parser test suite (28 tests)
│   └── test_interpreter.py  # Interpreter test suite (10 tests)
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
- **Classes**: `class Name: ... +++` (parsing implemented, execution in Sprint 2)
- **Variables**: Dynamic typing with assignment `name = value`

### Built-in Functions

- `print(*args)` — Multi-argument printing with space separation
- `input(prompt?)` — Read from stdin with optional prompt
- `int(value)`, `float(value)`, `str(value)` — Type conversions
- `range(start?, stop, step?)` — Integer sequence generation
- `len(sequence)` — Length calculation
- `open(path)` — File iteration over lines

### Example Syntax

```lyric
def main() {
    print("Hello, Lyric!")
    
    if 5 > 3:
        print("Math works!")
    else:
        print("Something's wrong")
    end
    
    given i in range(3):
        print("Count:", i)
    done
}
```

## License and Credits

The Lyric language is developed by **Michael Stone** and **ChatGPT** as part of the **MiraNova Studios** initiative. This project represents a collaborative effort to create a clean, educational programming language implementation.

The project is currently **pre-release** and version **0.0.2** corresponds to the completion of Sprint 1 (Lyric Core Foundations). This milestone includes a fully functional lexer, parser, interpreter, runtime system, and CLI with comprehensive test coverage.

## Contributing

This project is part of an ongoing development sprint. Future versions will include enhanced error handling, complete class member execution, and additional language features.

For development questions or contributions, please refer to the project's development workflow outlined above.
