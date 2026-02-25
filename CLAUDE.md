# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Lyric** is an experimental interpreted programming language written in Python, developed by MiraNova Studios. Current version: 0.8.4 (Pre-Alpha). Website: https://lyric-lang.org

## Commands

```bash
# Run tests
pytest lyric/tests/

# Run tests for a specific version milestone
pytest lyric/tests/core-0.8.0/

# Run a single test file
pytest lyric/tests/core-0.8.0/test_foo.py -q

# Run a Lyric program
lyric run program.ly
lyric program.ly

# Install dev dependencies
pip install pytest flake8 build twine

# Release to PyPI
./release.sh [version]
```

## Shell Environment

**Running Git Bash, NOT PowerShell.** Always use Unix/Bash syntax:
- `date +"%Y%m%d/%H%M"` — NOT `Get-Date -Format "yyyyMMdd/HHmm"`
- Forward slashes in paths, Unix shell constructs throughout

## Critical Workflow Rules

**These rules are mandatory for every task — no exceptions:**

1. **One task at a time.** After completing any task, STOP execution. Do NOT proceed to the next task. Wait for explicit user instruction before starting anything new.

2. **Changelog file before commit.** NEVER commit without first creating a new changelog file (see format below). Mandatory order: changelog file → task summary → (DOD summary if sprint complete) → commit.

3. **All tests must pass 100%.** Run `pytest lyric/tests/ -q` and confirm zero failures before marking any task complete. If 100% pass rate cannot be achieved in 3–5 attempts, pause and ask the user what to do next.

4. **Do not modify `/studio/`.** That directory contains example scripts and must remain unchanged unless explicitly instructed otherwise. Development work goes in `/lyric/`, `/lyric/tests/`, and `/lyric/tests/examples/` only.

5. **Work on `dev-core` branch.** Verify this before starting any task.

6. **Git Commit Toggle = YES, Deployment Toggle = NO.** Lyric is interpreted; there are no build or deployment steps.

7. **Implement only the task specified.** When given a sprint task (e.g., "SPRINT10_PLAN.md Task 1"), implement only that task. Do not implement other tasks from the sprint unless explicitly told to.

## Safety & Validation Rules

- **Never delete directories without explicit user confirmation.**
- All generated Python files must be syntactically valid and importable.
- Unit tests must run via `pytest -q` without fatal errors.
- After any Sprint 1 or later completion: `lyric run examples/hello.ly` must work.

## Git Commit Format

```bash
git add .
git commit -a -m "SprintX TaskY: brief description"
```

- **`git add .`** is required first to stage any newly created files (changelog files, summaries, etc.).
- **`git commit -a -m`** stages and commits all modifications to tracked files.
- Commit message must be **one line only**, concise. All details belong in the changelog file.
- **Only one commit per user prompt — no exceptions.** Do NOT create a second commit to update the changelog hash.

**Correct:**
```
git commit -m "Sprint10 Task1: Blacklist unsafe Python modules"
```

**Wrong — too detailed, multi-line:**
```
git commit -m "Sprint10 Task1: Blacklist unsafe Python modules

- Added blacklist check to importpy handler
- Added 30+ modules to blacklist
..."
```

## Documentation Files to Create After Each Task

Each of these is a **separate file created fresh** for each task. Do not append entries to any existing file.

---

### 1. Changelog File (REQUIRED — create BEFORE commit)

**Always get the current date and time before creating this file.**

Path format:
```
nova/changelog/YYYYMMDD/HHMM-CHANGELOG.md
```

- Use 24-hour time: `1430` for 2:30 PM, `0915` for 9:15 AM.
- If a file already exists at that timestamp, append a decimal suffix:
  - `1430-CHANGELOG.md` → `1430.1-CHANGELOG.md` → `1430.2-CHANGELOG.md`

**Content format:**
```markdown
# SprintX TaskY — YYYYMMDD.HHMM

## Summary
Short explanation of what was implemented or fixed.

## Files Changed
- lyric/foo.py — description of change
- lyric/tests/core-0.x.x/test_foo.py — description of change

## Reason
Why this change was made.

## Git Commit Hash
`TBD` - SprintX TaskY Implementation

## Status
✅ Completed
```

Use `TBD` as the commit hash placeholder. Do NOT create a second commit to fill it in.

---

### 2. Sprint Task Summary (REQUIRED — create BEFORE commit)

Path format:
```
nova/aeon/trajectory-0.9.1/yield-0.x.x/SPRINTX_TASKX_SUMMARY.md
```

Example: `SPRINT10_TASK1_SUMMARY.md`

**Include:**
- Brief task completion summary
- Key accomplishments
- Files created/modified
- Status: `✅ Completed`
- Reference to the changelog file for full details

---

### 3. Sprint DOD Summary (REQUIRED only when all sprint tasks are complete)

Path format:
```
nova/aeon/trajectory-0.9.1/yield-0.x.x/SPRINTX_DOD_SUMMARY.md
```

**Include:**
- Sprint objective summary
- Completion status for all tasks
- Definition of done criteria verification
- Overall sprint status: `✅ Completed`
- References to all task summaries and changelog files

---

## License Header

Every Python source file in `/lyric/` and every test file in `/lyric/tests/` must begin with this exact header:

```python
# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.
```

This project is licensed under the **MiraNova Software License** (see `LICENSE`). Do not use GPL, MIT, or any other license header.

## Architecture

The interpreter is a classical 4-stage pipeline: **Lexer → Parser → AST → Interpreter**. All stages are hand-written in pure Python with no parser-generator dependencies.

| File | Role |
|------|------|
| `lyric/lexer.py` | Tokenizer — single-pass, produces token stream with line/col position info |
| `lyric/parser.py` | Recursive descent parser — produces a typed AST (~69 KB) |
| `lyric/ast_nodes.py` | ~50+ AST node type definitions |
| `lyric/interpreter.py` | Tree-walking executor with lexical scope via linked environment frames (~133 KB) |
| `lyric/runtime.py` | Built-in functions, type coercions |
| `lyric/pyproxy.py` | `importpy` bridge — wraps Python objects for use inside the Lyric runtime |
| `lyric/errors.py` | `LexError`, `ParseError`, `RuntimeErrorLyric` — all carry source position |
| `lyric/cli.py` | `main()` entry point, argument parsing, file execution |

**Scope management:** Linked chain of environment frames. Each function call/block pushes a new frame; variable resolution walks outward. Class instances are environment frames with a `self` reference. Method resolution walks the inheritance chain at dispatch time.

**Module resolution order:** native Lyric module → built-in stdlib → Python bridge (`importpy`) → `ModuleNotFoundError`.

## Test Organization

Tests live under `lyric/tests/core-0.x.x/` organized by version milestone. New tests for a sprint go in the directory matching the target version (e.g., `lyric/tests/core-0.9.x/` for Sprint 10). Follow the structure in `nova/aeon/trajectory-0.9.1/TEST_STRUCTURE.md`.

## Sprint Planning

Active sprint plans:
```
nova/aeon/trajectory-0.9.1/yield-0.x.x/SPRINT_PLAN.md
```

Implement only tasks listed in the active sprint plan, and only the specific task given. Do not read ahead and implement future tasks.

## Language Specification

The Lyric language specification is maintained manually at the external `lyric-lang.org` repository. Do not update the specification here.
