Here are the plain-text Sprint 5 instructions for Claude — no Markdown or formatting characters, ready to paste directly into Cursor:

SPRINT 5 — IMPLEMENT REX TYPE AND CLI EXECUTION COMMAND
Target Version: 0.1.9

Sprint Goal:
This sprint introduces a native regular expression type (rex) and adds proper command-line execution so users can run programs with “lyric run file_name.ly” or “lyric file_name.ly”. The default subcommand should be “run” if none is specified.

TASK 1 — DEFINE REX TYPE
Create a new built-in type called rex.
Syntax mirrors other built-ins like int, str, var.
Example:
rex pattern
pattern = /^.*$/

The parser should recognize regex literals written between slashes (/…/) as valid rex objects.

ACCEPTANCE CRITERIA:
• rex is a recognized native type keyword.
• /…/ literals parse correctly without conflicting with division syntax.
• Invalid or unclosed regex literals raise syntax errors.

TASK 2 — IMPLEMENT .MATCH() METHOD
Add a match(str) method to rex.
Internally call Python’s re.match or equivalent.
Return True if the string matches, False otherwise.

Example:
rex pattern = /^abc/
pattern.match("abcdef") → True
pattern.match("xyz") → False

ACCEPTANCE CRITERIA:
• .match() returns boolean True/False.
• Works on both string literals and variables.
• Raises a friendly error on non-string input.

TASK 3 — IMPLEMENT .REPLACE() METHOD
Add a replace(source, replacement) method.
Internally use re.sub to replace all matches of the regex in the source string.
Return the modified string; do not alter the original.

Example:
rex pattern = /cat/
new_str = pattern.replace("the cat sat", "dog")
prints “the dog sat”

ACCEPTANCE CRITERIA:
• Replaces all matches in the source string.
• Returns a new string.
• Works with string literals and variables.

TASK 4 — SEARCH METHOD DECISION
Decide whether to include a .search() method.
For this sprint, defer implementation.
Leave a comment placeholder noting that .search() may be added later for mid-string matches.

ACCEPTANCE CRITERIA:
• Comment or stub present noting deferred .search().
• No runtime references to .search() for now.

TASK 5 — ADD CLI ENTRYPOINT
Allow running Lyric directly from the command line.
Accept both forms:

lyric run file_name.ly

lyric file_name.ly

If no subcommand is specified, assume “run” by default.
Update the CLI handler accordingly.

ACCEPTANCE CRITERIA:
• Both commands successfully execute Lyric source files.
• Error messages appear when arguments are missing or invalid.
• Behavior matches “python -m lyric.cli run file_name.ly”.
• “lyric --help” and version flags still function.

TASK 6 — PIP/PACKAGING INTEGRATION
Ensure that once Lyric is installed with pip install lyric-lang, the lyric command is globally available.
Add an entry_points block to setup.py or pyproject.toml:
entry_points={
'console_scripts': [
'lyric=lyric.cli:main',
],
}

Verify functionality on Windows and Unix.

ACCEPTANCE CRITERIA:
• After pip install -e ., “lyric” is accessible globally.
• Both “lyric run file.ly” and “lyric file.ly” execute correctly.
• Help and version flags work as expected.


TASK 7 — ADD GOD TYPE (BOOLEAN TYPE)
Introduce a new built-in type named god, representing logical true/false values.
This replaces the planned bool type. The name honors the logician Kurt Gödel, whose work on formal logic inspired the concept of truth values in computation.

Implementation requirements:
• god behaves as a boolean type.
• Literal values true and false are recognized by the interpreter.
• god variables can be used in conditional statements (if, while, etc.).
• god can be returned from functions and compared using logical operators (and, or, not).
• Internally it maps to a Python bool for now.
• Update documentation to include the origin of the name (referencing Gödel).

Example usage:
god ready = true
if ready {
 print("System ready.")
} else {
 print("System not ready.")
}

ACCEPTANCE CRITERIA:
• god is recognized as a native type keyword.
• true and false literals function correctly in conditionals.
• Logical operations and comparisons behave as expected.
• Documentation updated with a short note:
 “The god type (named in honor of logician Kurt Gödel) represents truth values.”
• README.md and CHANGELOG.md updated accordingly.


DEFINITION OF DONE
• rex type implemented with .match() and .replace() fully working.
• Parser correctly handles /…/ syntax.
• CLI accepts “lyric run file.ly” and “lyric file.ly” with default subcommand = run.
• Pip entry point configured for global lyric command.
• Unit tests created for rex functionality and CLI execution.
• README.md updated with new usage examples.
• CHANGELOG.md updated to include rex type and CLI improvements.
• Version bumped to 0.1.9 and committed.