# Bytecode Compiler (Phases 1-5) + Adhoc Changes — 20260314.0101

## Summary
Implemented a Lyric-to-Python AST transpiler (bytecode compiler) across 5 phases, enabling compiled execution via `--compile` flag. Also bumped version to 1.0.4, created Debian package build script, updated test subprocess calls to use system `lyric` command, and added Ruby/Perl performance benchmarks.

## Files Changed
- lyric/compiler.py — new: Lyric AST to Python AST transpiler (Phases 1-5)
- lyric/compiled_runtime.py — new: runtime support library for compiled code
- lyric/cli.py — added --compile flag, updated help text, version bump support
- lyric/__init__.py — version bumped to 1.0.4
- pyproject.toml — version bumped to 1.0.4
- build-deb.sh — new: Debian package build script
- lyric/tests/core-0.6.0/test_shebang_support.py — subprocess calls updated to use `lyric` command
- lyric/tests/core-0.8.0/test_auto_help.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_cli_args.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_dsk_type.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_exit_exec.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_file_operators.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_getopts.py — subprocess calls updated
- lyric/tests/core-0.8.0/test_print_file_redirect.py — subprocess calls updated
- lyric/tests/core-0.9.0/test_stderr_merge.py — subprocess calls updated
- lyric/tests/perftest/ruby_benchmark.rb — new: Ruby benchmark
- lyric/tests/perftest/ruby_benchmark_small.rb — new: Ruby small benchmark
- lyric/tests/perftest/perl_benchmark.pl — new: Perl benchmark
- lyric/tests/perftest/perl_benchmark_small.pl — new: Perl small benchmark
- nova/PYTHON_BYTECODE_PLAN.md — new: implementation plan
- nova/yield-1.1.x/BYTECODE_SUMMARY_PHASE1.md — new: Phase 1 summary
- nova/yield-1.1.x/BYTECODE_SUMMARY_PHASE2.md — new: Phase 2 summary
- nova/yield-1.1.x/BYTECODE_SUMMARY_PHASE3.md — new: Phase 3 summary
- nova/yield-1.1.x/BYTECODE_SUMMARY_PHASE4.md — new: Phase 4 summary
- nova/yield-1.1.x/BYTECODE_SUMMARY_PHASE5.md — new: Phase 5 summary

## Reason
Lyric's tree-walking interpreter runs ~74x slower than equivalent Python code on compute-heavy benchmarks. The transpiler compiles Lyric AST to Python AST, letting CPython's bytecode VM execute it natively. Result: ~5s vs ~74s on the full benchmark (14x speedup). Also needed Debian packaging to run tests against system-installed Lyric and benchmarks in other languages for comparison.

## Git Commit Hash
`TBD` - Bytecode Compiler Phases 1-5 + Adhoc Changes

## Status
✅ Completed
