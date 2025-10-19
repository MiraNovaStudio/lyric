# Lyric Language

Lyric is a lightweight interpreted programming language designed for simplicity, readability, and elegant syntax. This project is being developed from scratch to test our development processes and create a clean, educational programming language implementation.

**Status**: Starting Fresh - Version 0.0.1 (Pre-Alpha)

## Project Goals

This iteration of Lyric is being built from the ground up to:
- Test and refine our development processes
- Create a clean, minimal language implementation
- Establish proper testing and documentation practices
- Build a solid foundation for future language features

## Current State

The project is currently in its initial phase with:
- Basic project structure established
- Development environment configured
- Sprint-based development process ready to begin

## How to Run (Future)

Once implemented, Lyric programs will use the `.ly` file extension and be executed through the command line interface:

```bash
lyric run path_to_file.ly
```

For example:
```bash
lyric run examples/hello.ly
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

## Planned Language Features

### Core Constructs (To Be Implemented)

- **Functions**: `def name(params) { body }` with optional return statements
- **Conditionals**: `if condition: ... else: ... end`
- **Loops**: `given variable in iterable: ... done` or `given condition: ... done`
- **Classes**: `class Name: ... +++` (full implementation with instantiation, methods, and init())
- **Variables**: Dynamic typing `var name = value` or static type declarations `type name = value`
- **Data Structures**: `[item1, item2, ...]` for lists, `{"key": value, ...}` for dictionaries
- **Exception Handling**: `try: ... except: ... finally: ... end`
- **Comments**: `# comment text` (full-line and inline comments)

### Planned Built-in Functions

- `print(*args)` — Multi-argument printing
- `input(prompt?)` — Read from stdin with optional prompt
- `int(value)`, `float(value)`, `str(value)` — Type conversions
- `range(start?, stop, step?)` — Integer sequence generation
- `len(sequence)` — Length calculation for strings, lists, and dictionaries
- And more as the language develops...

## Development Process

This project follows a structured sprint-based development approach:

1. **Sprint Planning**: Each sprint has defined tasks and goals
2. **Implementation**: Code is developed incrementally with tests
3. **Documentation**: Changes are documented in changelog entries
4. **Version Control**: Structured commits with clear messages
5. **Testing**: Comprehensive test coverage for all components

## License and Credits

The Lyric language is developed by **Michael (Aeonath)**, **ChatGPT**, and **Claude** as part of the **MiraNova Studios** initiative. This project represents a collaborative effort to create a clean, educational programming language implementation.

## Contributing

This project is currently in active development following a structured sprint methodology. The development process emphasizes:

- Clean, readable code
- Comprehensive testing
- Clear documentation
- Incremental feature development
- Proper version control practices

For development questions or contributions, please refer to the project's development workflow and sprint documentation.
