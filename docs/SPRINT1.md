SPRINT 1 — LYRIC CORE FOUNDATIONS (PLAINTEXT SPEC FOR CLAUDE)

OBJECTIVE
Establish a minimal working Lyric interpreter that can read a .ly file, tokenize it, parse it into an AST, and execute a program that contains def, if/else end, given done, and print(), invoked via a CLI command.

SCOPE
Implement lexer, AST definitions, parser, interpreter core, minimal runtime, CLI entrypoint, and baseline tests and example programs.

DIRECTORY STRUCTURE (CREATE EXACTLY)
lyric/
init.py
lexer.py
parser.py
ast.py
interpreter.py
runtime.py
errors.py
cli.py
tests/
init.py
test_lexer.py
test_parser.py
test_interpreter.py
examples/
hello.ly
if_demo.ly
loop.ly
pyproject.toml or setup.py (choose one; prefer pyproject.toml with a console_script entry for "lyric")

TASK 1 — PROJECT SCAFFOLD
Work:

Create the directory structure listed above, with empty but importable modules.

Add pyproject.toml with project name "lyric", version "0.1.0", and a console_scripts entry: lyric = lyric.cli:main
If using setup.py instead, provide equivalent entry_points console_scripts.

Implement cli.py main() stub that supports:

"lyric --version" prints "Lyric 0.1"

"lyric run <path>" validates that file exists (no execution yet)

Add errors.py defining simple exception classes: LexError, ParseError, RuntimeErrorLyric.

Acceptance Criteria:
A1) Running "lyric --version" prints "Lyric 0.1".
A2) Running "lyric run tests/examples/hello.ly" prints an error like "execution not implemented" (placeholder ok).
A3) All modules import without error: python -c "import lyric, lyric.lexer, lyric.parser, lyric.ast, lyric.interpreter, lyric.runtime, lyric.errors, lyric.cli".

TASK 2 — LEXER
Work:

Implement a tokenizer in lexer.py that converts source text to a list (or generator) of tokens with type, value, line, col.

Recognize keywords: def, class, if, else, given, done, end, try, except, finally.

Recognize the symbolic class terminator: +++ as a single token CLASS_END.

Recognize identifiers, integers, floats, strings (double quotes), operators (+ - * / = == != < <= > >=), delimiters ( ( ) { } : , ; ), and newline handling.

Treat "else if" as two tokens ELSE and IF (parser will combine).

Ignore whitespace and comments (lines starting with #).

Provide a tokenize(source: str) -> List[Token] function and a Token dataclass or namedtuple.

Tests (tests/test_lexer.py):

Tokenize the sample:
if x > 0:
print("positive")
end

Expect sequence: IF, IDENT(x), GT, INT(0), COLON, NEWLINE, IDENT(print), LPAREN, STRING("positive"), RPAREN, NEWLINE, END, NEWLINE/EOF

Tokenize "class Player: +++" and detect CLASS, IDENT(Player), COLON, NEWLINE, CLASS_END.

Acceptance Criteria:
A4) All lexer tests pass with pytest, including the two samples above.
A5) Lexer attaches correct line and column numbers to tokens.

TASK 3 — AST DEFINITIONS
Work:

In ast.py, define lightweight node classes (dataclasses) for:
ProgramNode(statements)
FunctionNode(name, params, body_statements)
IfNode(condition, then_body, elifs:list, else_body or None)
LoopNode(condition_or_iter, loop_kind, body) // loop_kind: "iterator" or "while"
AssignNode(name, expr)
CallNode(func_name, args)
BinaryOpNode(op, left, right)
UnaryOpNode(op, operand)
LiteralNode(value)
IdentifierNode(name)
ClassNode(name, members_statements)
PrintNode(args) // optional convenience

Provide repr or to_dict methods for debugging.

Acceptance Criteria:
A6) Nodes can be instantiated and pretty-printed in a simple test in tests/test_parser.py setup code.

TASK 4 — PARSER (RECURSIVE DESCENT)
Work:

Implement a Parser class in parser.py that consumes tokens and produces ProgramNode.

Grammar to support in this sprint:
program := statement*
statement :=
func_def
| class_def
| if_block
| loop_block
| assignment_or_expr_stmt

func_def: "def" IDENT "(" param_list? ")" "{" statement* "}"

class_def: "class" IDENT ":" statement* CLASS_END

Members may be AssignNode or func_def only (no nested classes in v0.1).

if_block:
"if" expression ":" statement* ("else" "if" expression ":" statement*)* ("else" ":" statement*)? "end"

loop_block:
"given" expression ":" statement* "done"
Note: expression can be "i in range(5)" (parse as a specific iterator loop form) OR a boolean expression for while-like loops.

assignment_or_expr_stmt:
IDENT "=" expression
OR expression where expression can be:
call, identifier, literal, parenthesized, binary/unary ops
Calls: IDENT "(" arg_list? ")"

Expressions:
Standard precedence: unary (!, -), multiplicative (*,/), additive (+,-), comparisons (==, !=, <, <=, >, >=), logical (and, or) if used.

Provide parse(source: str) -> ProgramNode function.

Tests (tests/test_parser.py):

Parse the following source and assert AST shapes:
def main() { print("Hello, Lyric!") }

If/else example from spec.

given i in range(3): print(i) done

class Player: name = "Guest" def greet() { print("Hello,", self.name) } +++

Acceptance Criteria:
A7) Parser builds the expected ASTs for the test samples without raising errors.
A8) Else-if sequences using "else if" are parsed into IfNode with elifs list populated.

TASK 5 — INTERPRETER CORE
Work:

Implement an Interpreter class in interpreter.py with:

Global environment (dict) and a call stack of local environments.

A function registry for user-defined functions.

Evaluation methods for expressions and statement execution.

Implement:

Execution of ProgramNode

Function definition and invocation (def … { … })

Variable assignment and lookup (locals shadow globals)

If/else end

given done:
a) Iterator form: "i in range(N)" iterates
b) While form: any boolean expression (non-zero/non-empty truthiness)

print() as a built-in call routed via runtime

After loading a ProgramNode, automatically call main() if defined when invoked via CLI.

Acceptance Criteria:
A9) Running tests/examples/hello.ly produces "Hello, Lyric!" exactly.
A10) If/else demo prints "positive" when x=5.
A11) Loop demo prints 0, 1, 2 on separate lines.

TASK 6 — RUNTIME AND BUILT-INS
Work:

In runtime.py implement built-ins:
print(*args) // writes to stdout with single space joining
input(prompt?) // reads from stdin (can be stubbed or injectable for tests)
int, float, str
range(N) // yields 0..N-1
len
open(path) // return an iterable over lines (text mode) for simple demos

Provide a function register_builtins(env: dict) to populate the global environment.

Acceptance Criteria:
A12) print, int, float, str, range, len are callable from Lyric programs.
A13) File I/O example using "given line in open("numbers.txt")" can iterate lines in a test (you can simulate a small temp file in the test).

TASK 7 — CLI INTEGRATION
Work:

Implement lyric/cli.py main() to:

Parse argv

Handle "--version"

Handle "run <file.ly>": read file, tokenize, parse, interpret, auto-call main()

Add helpful error messages with file name and line number on LexError, ParseError, RuntimeErrorLyric.

Acceptance Criteria:
A14) "lyric run tests/examples/hello.ly" runs end-to-end without Python tracebacks (unless a bug is present), printing user-friendly messages on errors.
A15) "--version" prints "Lyric 0.1".

TASK 8 — TESTS AND EXAMPLES
Work:

Populate tests/examples/hello.ly:
def main() {
print("Hello, Lyric!")
}

Populate tests/examples/if_demo.ly:
def main() {
x = 5
if x > 0:
print("positive")
else:
print("non-positive")
end
}

Populate tests/examples/loop.ly:
def main() {
given i in range(3):
print(i)
done
}

Implement pytest tests:

tests/test_lexer.py: at least 3 cases including class terminator +++.

tests/test_parser.py: build ASTs for the three examples and one class sample.

tests/test_interpreter.py: run the three examples; capture stdout and assert exact output.

Acceptance Criteria:
A16) All tests pass: pytest -q returns success.
A17) No flake8 or ruff critical errors (basic style clean).

DEFINITION OF DONE (SPRINT)

CLI "lyric run <file.ly>" executes a Lyric program that uses def, if/else end, given done, and print().

Lexer, Parser, Interpreter, Runtime, and CLI implemented and covered by baseline tests.

Examples run and produce expected output.

Clear error messages with file and line number for lexing/parsing/runtime errors.

Code scaffold ready for Sprint 2 (adding richer errors, class member execution rules, and the +++ class structure semantics beyond parsing).