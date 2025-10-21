# Sprint 5 — Implement Rex Type and CLI Execution Command

**Target Version:** 0.5.0

## Sprint Goal

This sprint introduces a native regular expression type (`rex`) and adds proper command-line execution so users can run programs with `lyric run file_name.ly` or `lyric file_name.ly`. The default subcommand should be "run" if none is specified.

## Task 1 — Define Rex Type

Create a new built-in type called `rex`.

**Syntax:** Mirrors other built-ins like `int`, `str`, `var`.

**Example:**
```lyric
rex pattern
pattern = /^.*$/
```

The parser should recognize regex literals written between slashes (`/…/`) as valid `rex` objects.

### Acceptance Criteria:
- `rex` is a recognized native type keyword.
- `/…/` literals parse correctly without conflicting with division syntax.
- Invalid or unclosed regex literals raise syntax errors.

## Task 2 — Implement .match() Method

Add a `match(str)` method to `rex`.

**Implementation:** Internally call Python's `re.match` or equivalent.

**Return:** `True` if the string matches, `False` otherwise.

**Example:**
```lyric
rex pattern = /^abc/
pattern.match("abcdef") → True
pattern.match("xyz") → False
```

### Acceptance Criteria:
- `.match()` returns boolean `True`/`False`.
- Works on both string literals and variables.
- Raises a friendly error on non-string input.

## Task 3 — Implement .replace() Method

Add a `replace(source, replacement)` method.

**Implementation:** Internally use `re.sub` to replace all matches of the regex in the source string.

**Return:** The modified string; do not alter the original.

**Example:**
```lyric
rex pattern = /cat/
new_str = pattern.replace("the cat sat", "dog")
print(new_str)  # prints "the dog sat"
```

### Acceptance Criteria:
- Replaces all matches in the source string.
- Returns a new string.
- Works with string literals and variables.

## Task 4 — Search Method Decision

Decide whether to include a `.search()` method.

**Decision:** For this sprint, defer implementation.

**Action:** Leave a comment placeholder noting that `.search()` may be added later for mid-string matches.

### Acceptance Criteria:
- Comment or stub present noting deferred `.search()`.
- No runtime references to `.search()` for now.

## Task 5 — Add CLI Entrypoint

Allow running Lyric directly from the command line.

**Accept both forms:**
```bash
lyric run file_name.ly
lyric file_name.ly
```

If no subcommand is specified, assume "run" by default.

Update the CLI handler accordingly.

### Acceptance Criteria:
- Both commands successfully execute Lyric source files.
- Error messages appear when arguments are missing or invalid.
- Behavior matches `python -m lyric.cli run file_name.ly`.
- `lyric --help` and version flags still function.

## Task 6 — Pip/Packaging Integration

Ensure that once Lyric is installed with `pip install lyric-lang`, the `lyric` command is globally available.

**Add an entry_points block to setup.py or pyproject.toml:**
```python
entry_points={
    'console_scripts': [
        'lyric=lyric.cli:main',
    ],
}
```

Verify functionality on Windows and Unix.

### Acceptance Criteria:
- After `pip install -e .`, `lyric` is accessible globally.
- Both `lyric run file.ly` and `lyric file.ly` execute correctly.
- Help and version flags work as expected.

## Task 7 — Add God Type (Boolean Type)

Introduce a new built-in type named `god`, representing logical true/false values.

**Note:** This replaces the planned `bool` type. The name honors the logician Kurt Gödel, whose work on formal logic inspired the concept of truth values in computation.

### Implementation Requirements:
- `god` behaves as a boolean type.
- Literal values `true` and `false` are recognized by the interpreter.
- `god` variables can be used in conditional statements (`if`, `while`, etc.).
- `god` can be returned from functions and compared using logical operators (`and`, `or`, `not`).
- Internally it maps to a Python `bool` for now.
- Update documentation to include the origin of the name (referencing Gödel).

**Example usage:**
```lyric
god ready = true
if ready {
    print("System ready.")
} else {
    print("System not ready.")
}
```

### Acceptance Criteria:
- `god` is recognized as a native type keyword.
- `true` and `false` literals function correctly in conditionals.
- Logical operations and comparisons behave as expected.
- Documentation updated with a short note: "The `god` type (named in honor of logician Kurt Gödel) represents truth values."
- `README.md` and `CHANGELOG.md` updated accordingly.

## Definition of Done

- `rex` type implemented with `.match()` and `.replace()` fully working.
- Parser correctly handles `/…/` syntax.
- CLI accepts `lyric run file.ly` and `lyric file.ly` with default subcommand = run.
- Pip entry point configured for global `lyric` command.
- Unit tests created for `rex` functionality and CLI execution.
- `README.md` updated with new usage examples.
- `CHANGELOG.md` updated to include `rex` type and CLI improvements.
