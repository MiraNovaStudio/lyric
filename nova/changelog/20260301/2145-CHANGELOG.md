# Adhoc — 20260301.2145

## Summary
Added print statement file redirection support. `print "text" ->> file` and `print "text" -> file` now work, appending/overwriting with an automatic newline — matching print's behavior on stdout. This enables natural multi-line file building like `print "---" ->> journal_file`.

## Files Changed
- lyric/parser.py — Updated `_parse_statement()` routing to let print statements handle their own file operators; added file operator detection after print argument parsing in `_parse_assignment_or_expr_stmt()`, wrapping the result in a `FileOpNode` when `->>`, `->`, or `<-` follows
- lyric/interpreter.py — Added print redirect handling at the top of `_evaluate_file_op()`: when left side is a `CallNode('print', ...)`, evaluates args, joins with spaces, appends newline, and writes to dsk object
- lyric/tests/core-0.8.0/test_print_file_redirect.py — 8 new tests: append, overwrite, multi-arg, expression, multiline file building, no-echo-to-stdout, function-call print still works, statement print still works

## Reason
Enable `print "text" ->> file` syntax so Lyric programs can build multi-line files with automatic newlines, matching the intuitive behavior of shell `echo "text" >> file`.

## Git Commit Hash
`TBD` - Adhoc print file redirection

## Status
✅ Completed
