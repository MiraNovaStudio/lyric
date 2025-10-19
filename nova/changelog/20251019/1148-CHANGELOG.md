# Sprint2 Keyword Recognition — 20251019.1055

## Summary
Added proper keyword recognition to the lexer and updated parser to use keyword tokens instead of string matching. The lexer now properly recognizes all core Lyric keywords as distinct tokens.

## Files Changed
- lyric/lexer.py — Added keyword dictionary and keyword recognition logic
- lyric/parser.py — Updated all parsing methods to use keyword tokens (DEF, IF, ELSE, GIVEN, DONE, END, IN, AND, OR, NOT)

## Keywords Recognized
- def, class, if, else, given, done, end, try, except, finally
- in, and, or, not

## Reason
The lexer was treating keywords as regular identifiers instead of recognizing them as special language constructs. This fix ensures proper tokenization and parsing of Lyric language keywords, making the parser more robust and accurate.

## Git Commit Hash
`[commit_hash]` - Sprint2: Add keyword recognition

## Status
✅ Completed
