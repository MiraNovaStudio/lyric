# Adhoc: getopts Colon Convention — Task Summary

## Summary
Added `:` suffix convention to `getopts()` for options that expect a value, enabling space-separated CLI syntax (`-f value`, `--file value`).

## Usage
```
# Script:
var config = getopts("f:", "file:")

# CLI:
lyric script.ly -f config.txt
lyric script.ly --file config.txt
lyric script.ly -f=config.txt       # also still works
```

## Files Modified
- lyric/runtime.py — getopts colon handling + raw args storage
- lyric/cli.py — Pass raw args to runtime

## Status
✅ Completed
