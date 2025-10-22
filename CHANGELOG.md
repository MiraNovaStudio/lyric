# Changelog

All notable changes to the Lyric Programming Language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-10-22

### Added
- **Python Interoperability**: Added `importpy` statement for seamless Python library access
  - `importpy math` - Import Python modules directly into Lyric
  - `importpy datetime` - Access Python standard library modules
  - `importpy os` - Import any available Python module
- **pyobject Type System**: Internal type system integration for Python objects
  - `pyobject` type for values originating from Python (internal only)
  - `var` type accepts `pyobject` values without restrictions
  - Seamless integration between Lyric and Python type systems
- **Chained Member Access**: Support for complex Python object navigation
  - `datetime.datetime.now()` - Access nested Python classes and methods
  - `math.sqrt(16)` - Call Python functions directly
  - `obj.member.method()` - Chain member access and method calls
- **Proxy Objects**: Lightweight Python object wrappers
  - `PyModuleProxy` for Python module access
  - `PyCallableProxy` for Python function/method calls
  - Runtime safety with Lyric-style error handling
- **Enhanced Error Messages**: Consistent error formatting for Python interop
  - `ImportError: cannot import Python module 'module_name'`
  - `AttributeError: 'module' has no attribute 'attribute'`
  - A17-A19 standard error formatting maintained
- **Comprehensive Test Suite**: Added extensive testing for Python interoperability
  - `tests/examples/importpy_tests.ly` - Complete example file
  - `tests/core-0.3.4/test_importpy_integration.py` - Integration tests
  - `tests/core-0.3.4/test_pyobject_integration.py` - Type system tests

### Changed
- **Type System**: Enhanced `var` type to seamlessly handle `pyobject` values
- **Runtime Safety**: Improved error handling for Python attribute access
- **Parser**: Added support for `importpy` statement parsing
- **Lexer**: Added `IMPORTPY` token recognition
- **Interpreter**: Enhanced member access and function call handling for Python objects

### Technical Details
- **Files Modified**: `lexer.py`, `parser.py`, `interpreter.py`, `runtime.py`, `ast_nodes.py`
- **Files Added**: `pyproxy.py` (Python proxy implementation)
- **Test Coverage**: 100% pass rate maintained with 310+ tests
- **Backward Compatibility**: All existing Lyric code continues to work unchanged

### Examples
```lyric
# Basic Python module import
importpy math
var result = math.sqrt(16)  # prints 4.0

# Complex Python object access
importpy datetime
var now = datetime.datetime.now()
print(now.year)  # prints current year

# Multiple modules
importpy os
var current_dir = os.getcwd()
print(current_dir)
```

## [0.2.0] - 2025-10-21

### Added
- **Exception Handling**: Complete try/catch/finally system
- **Return Statements**: Function return value support
- **Enhanced Type System**: Improved type declarations and inference
- **Data Structures**: List and dictionary literals with indexing
- **Class Constructors**: `init()` method support for class instantiation

## [0.1.0] - 2025-10-20

### Added
- **Core Language Features**: Functions, conditionals, loops, classes
- **Type System**: Basic type declarations (int, str, flt, var)
- **Built-in Functions**: print, input, type conversions, collections
- **CLI Interface**: Command-line program execution
- **Comprehensive Testing**: Full test suite with 200+ tests
- **Error Reporting**: Line-numbered error messages
- **Documentation**: Complete language specification and examples
