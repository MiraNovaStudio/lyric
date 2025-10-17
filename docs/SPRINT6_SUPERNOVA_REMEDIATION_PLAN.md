SUPERNOVA_REMEDIATION — Declaration Enforcement Plan

Project: Lyric Language
Phase: SUPERNOVA Remediation
Objective: Implement strict declaration enforcement for variables (static typing model)
Author: Aeonath
Engineer: Claude
Sprint: 6

Overview:
Following the SUPERNOVA regression, we determined that Lyric’s intended design philosophy aligns with explicit variable declaration similar to C and JavaScript.

This means:

Every variable must be declared before it is used.

Declarations specify a type (int, string, bool, var, etc.).

The special keyword var allows type inference or generic type holding.

Assignments to undeclared variables are illegal and must throw an error.

Examples:
int x
x = 10 Valid
x = 10 Error: Variable 'x' used before declaration
var name
name = "Aeonath" Valid
var count = 5 Valid (immediate declaration with assignment)

This design makes Lyric an educational, statically typed language with a readable syntax and clear memory model.

Implementation Plan:

Interpreter Updates
Files: interpreter.py, environment.py

Enforce variable existence on assignment.
When executing x = 10, check if x exists in the current scope.
If not declared, raise error: Variable 'x' used before declaration.

Implement methods:
env.declare_variable(name, type, value=None)
env.assign_variable(name, value)

Ensure that type enforcement occurs at assignment (except for var).

Allow declaration with or without initialization:
int x
int x = 10
var y
var y = 20

Parser Enhancements
Files: parser.py, grammar.py

Ensure syntax rules support:
int x
int x = 10
var y
var y = "Hello"

Disallow bare assignments to undeclared variables:
x = 10 should raise DeclarationError.

Update AST nodes:
Add new node type: DeclarationStatement
Fields: type_name, var_name, initializer

Type Enforcement Rules

Type Behavior Summary:
int allows integer assignments only
string allows string assignments only
bool allows True/False assignments only
var allows any type and acts as generic type

Examples:
int x = 10 Valid
x = "Hello" TypeError
var y = "Aeonath" Valid
y = 25 Valid

Error Handling

Add new error classes if not present:
DeclarationError("Variable 'x' used before declaration")
TypeError("Cannot assign string to int variable 'x'")

Ensure these propagate cleanly to CLI and test output.

Testing Strategy

Tests to update or re-enable:
test_declaration_enforcement.py
test_scope_resolution.py
test_variable_assignment.py

Expected passing cases:
int x
x = 10
print(x)

Expected failing cases:
x = 10
Error: Variable 'x' used before declaration

Run sequence:
pytest -v > tests/TEST_REPORT_SUPERNOVA_REMEDIATION.txt

Goal: Zero declaration enforcement failures.

Validation via CLI

After successful test pass, verify manually:
python -m lyric_lang.cli run tests/examples/does_it_work.ly
python -m lyric_lang.cli run tests/examples/nested_flow.ly

Expected: Proper declaration behavior, no implicit creation.

Documentation Update

File: docs/LANGUAGE_DESIGN_DECISIONS.md

Add section:
Declaration Enforcement:
Lyric now enforces explicit variable declarations before use.
All variables must be declared with a type prior to assignment.
var provides a flexible generic type supporting type inference.
This design enhances educational value by reinforcing type and memory fundamentals.