
---

## 🧱 Revised `SPRINT1_PLAN.md`
> Adds environment setup tasks, ensures `lyric/` directory creation, and readies Claude to bootstrap the interpreter cleanly.

```markdown
# Sprint 1 — Lyric Core Foundations (dev-core)

## Objective
Bootstrap the Lyric project from scratch by creating the directory structure, baseline modules, and command-line entry point for an interpreted language.  
By the end of this sprint, the project should import cleanly, provide a functioning CLI (`lyric run <file.ly>`), and execute placeholder code paths.

---

## Scope
- Establish initial `lyric/` source tree
- Add pyproject configuration for CLI entry
- Implement CLI stubs and error classes
- Verify imports and baseline test scaffolding
- Prepare for Lexer, Parser, and Interpreter work in Sprint 2+

---

## Directory Structure
```
lyric/
 init.py
 cli.py
 errors.py
 lexer.py
 parser.py
 ast.py
 interpreter.py
 runtime.py
 tests/
  init.py
```


---

## Task 1 — Project Scaffold

**Work**

1. Create all directories and files listed above.
2. Add `pyproject.toml` with:
   - `project.name = "lyric"`
   - `project.version = "0.1.0"`
   - `[project.scripts] lyric = "lyric.cli:main"`
3. Implement `cli.py` with `main()` supporting:
   - `--version` → prints `Lyric 0.1`
   - `run <file.ly>` → validates file path, prints “execution not implemented”
4. Define `errors.py` with exception classes:
   - `LexError`
   - `ParseError`
   - `RuntimeErrorLyric`
5. Ensure `__init__.py` exists in both `lyric/` and `tests/` so imports succeed.

**Acceptance Criteria**
- `lyric --version` prints `Lyric 0.1`.
- `lyric run examples/hello.ly` prints “execution not implemented”.
- All modules import without Python errors:
  ```bash
  python -c "import lyric, lyric.cli, lyric.errors, lyric.lexer, lyric.parser, lyric.ast, lyric.interpreter, lyric.runtime"
```

## Task 2 — Test Environment Setup

Work

Add pytest as a development dependency.

Create placeholder test files:

tests/test_cli.py

tests/test_imports.py

Validate that pytest discovers and runs the test suite:

pytest -q

Confirm all tests pass (even if only placeholders).

### Acceptance Criteria

Test discovery works.

Imports verified via unit test.

No tracebacks or missing module errors.

## Task 3 — Example Programs

create the lyric/examples directory

Populate lyric/examples/hello.ly with:

```
def main() {
    print("Hello, Lyric!")
}
```

## Definition of Done

✅ Lyric project initialized and functional at the CLI level.
✅ All files import successfully and pass pytest -q.
✅ Ready for Sprint 2 — Lexer Implementation.


