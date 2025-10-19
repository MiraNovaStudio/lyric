# Sprint2 Bug Fix — 20251019.1050

## Summary
Fixed lexer comment handling to properly consume newlines after comments. The lexer was encountering unexpected newline characters after comment lines because the comment pattern didn't include the newline.

## Files Changed
- lyric/lexer.py — Updated comment pattern to include newline: `r'#.*(?:\n|$)'`

## Reason
The original comment pattern `r'#.*'` only matched the comment text but not the trailing newline, causing the lexer to encounter unexpected newline characters on subsequent iterations. This fix ensures comments are properly consumed including their trailing newlines.

## Git Commit Hash
`[commit_hash]` - Sprint2: Fix lexer comment handling

## Status
✅ Completed
