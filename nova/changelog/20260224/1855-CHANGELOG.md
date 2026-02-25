# Sprint10 Task2 — 20260224.1855

## Summary
Formalised and tested the stderr-to-stdout merge behaviour for exec() output
operators and pipelines. The code already used `stderr=subprocess.STDOUT` in all
subprocess calls; this task adds explicit documentation and a comprehensive test
suite proving the behaviour is correct for every exec path.

## Files Changed
- `lyric/interpreter.py` — Updated docstrings for `_evaluate_exec_with_io` and
  `_evaluate_exec_chain` to explicitly state that stderr is merged with stdout
  (`stderr=subprocess.STDOUT`) in all output-capturing and pipeline paths.
  Updated inline comment for the `->` operator case.
- `lyric/runtime.py` — Updated docstring for `exec_builtin` to document stderr
  merging.
- `lyric/tests/core-0.9.0/test_stderr_merge.py` — New test file (11 tests)
  covering:
  - `exec() -> var` captures stderr-only output
  - `exec() -> var` captures both stdout and stderr together
  - `exec() -> var` captures stderr from a failing (non-zero exit) command
  - `exec() -> var` captures multi-line stderr
  - `exec() | exec()` pipes stderr from first command onward
  - `exec() | exec()` pipes both stdout and stderr from first command
  - `exec() | exec()` captures stderr from the last command in the pipeline
  - Stderr propagates through multiple `cat` stages in a three-command pipeline
  - `exec() ->> file` appends stderr to file
  - `exec() ->> file` appends both stdout and stderr to file

## Reason
The sprint plan specifies that the entirety of a command's output (stdout + stderr)
is the output of the program for `->`, `->>`, and `|` operators. The behaviour was
already implemented via `stderr=subprocess.STDOUT` but was undocumented and had no
test coverage. This task closes that gap.

## Git Commit Hash
`TBD` - Sprint10 Task2 Implementation

## Status
✅ Completed
