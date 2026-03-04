# Sprint 10 Task 2 — Summary

## Task
Redirect and append stderr to stdout for exec() command output operators (`->`, `->>`)
and command pipelines (`|`). The entirety of stdout and stderr is treated as the
output of a command in all exec capturing paths.

## Key Accomplishments
- Confirmed `stderr=subprocess.STDOUT` was already present in all four exec paths:
  `exec_builtin`, `_evaluate_exec_with_io`, `_evaluate_exec_chain`, and
  `_evaluate_exec_chain_with_file_io`
- Updated docstrings and inline comments in `interpreter.py` and `runtime.py` to
  explicitly document the stderr merging contract
- Created `lyric/tests/core-0.9.0/test_stderr_merge.py` with 11 tests using a
  `py_script` pytest fixture that writes temporary Python scripts producing
  controlled stderr/stdout output — tests are fully cross-platform
- Identified and corrected a test logic error during development: a script that
  ignores its stdin cannot pass prior pipeline stderr through; fixed by using `cat`
  as the passthrough stage in the multi-stage pipeline test
- Full test suite: **1068/1068 passing**

## Tests Added (test_stderr_merge.py)
| Test | Covers |
|------|--------|
| `test_exec_redirect_captures_stderr_only` | `->` captures stderr-only |
| `test_exec_redirect_captures_stdout_and_stderr` | `->` captures both streams |
| `test_exec_redirect_captures_stderr_from_failing_command` | `->` captures stderr on non-zero exit |
| `test_exec_redirect_stderr_multiline` | `->` captures multi-line stderr |
| `test_pipeline_stderr_from_first_command_is_piped` | `\|` pipes stderr from first stage |
| `test_pipeline_stdout_and_stderr_from_first_command_are_piped` | `\|` pipes both streams |
| `test_pipeline_stderr_from_last_command_captured` | `\|` captures stderr from last stage |
| `test_pipeline_stderr_propagates_through_cat_stages` | stderr survives multi-stage pipeline |
| `test_append_to_file_captures_stderr` | `->>` appends stderr to file |
| `test_append_to_file_captures_stdout_and_stderr` | `->>` appends both streams to file |

## Files Modified / Created
- **Modified:** `lyric/interpreter.py` (docstrings only)
- **Modified:** `lyric/runtime.py` (docstring only)
- **Created:** `lyric/tests/core-0.9.0/test_stderr_merge.py`

## Status
✅ Completed

## Reference
Changelog: `nova/changelog/20260224/1855-CHANGELOG.md`
