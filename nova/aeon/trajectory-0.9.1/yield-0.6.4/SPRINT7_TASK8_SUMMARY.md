# Sprint 7 Task 8 — Validate Handling of Single Quotes in Regex String Literals

## Summary
Implemented support for both single-quoted and double-quoted string literals in Lyric, enabling regex patterns to contain mixed quotes without premature string termination.

## Problem Statement
Previously, regex patterns with mixed quotes like `regex("<a href=[\"']([^\"']+)[\"']>")` would fail because the lexer would terminate the string prematurely when encountering the opposite quote character. This prevented developers from creating robust regex patterns that need to match HTML attributes that can use either single or double quotes.

## Solution
Modified the lexer to:
1. Recognize both single (`'`) and double (`"`) quotes as string delimiters
2. Track which quote character started a string
3. Only terminate the string when the matching closing quote is encountered
4. Handle escaped quotes correctly in both single and double-quoted strings

## Implementation Details

### Files Modified
- `lyric/lexer.py`:
  - Updated `_scan_token()` to recognize both quote types
  - Modified `_scan_string()` to accept and use a `quote_char` parameter
  - Added support for escaped single quotes in escape sequence handling

### Test Coverage
Created `lyric/tests/core-0.6.4/test_mixed_quotes.py` with 10 comprehensive tests:
- Basic single-quoted strings
- Mixed quotes in various configurations
- Escaped quotes in both string types
- Regex patterns with mixed quotes
- Full end-to-end regex execution test

## Results

### Test Results
- ✅ All 10 new tests pass (100%)
- ✅ All 567 existing tests pass (100%)
- ✅ No regressions

### Acceptance Criteria
✅ Mixed quote characters within regex strings are parsed correctly  
✅ No premature string termination occurs  
✅ All new regex string tests pass successfully  
✅ Existing regex-related tests remain green  
✅ Regex behavior is identical to equivalent Python code  

## Technical Changes

### Lexer Changes
```python
# Before
if char == '"':
    self._scan_string()
    return

def _scan_string(self):
    while self._peek() != '"' and not self._is_at_end():
        # ...

# After
if char == '"' or char == "'":
    self._scan_string(char)
    return

def _scan_string(self, quote_char):
    while self._peek() != quote_char and not self._is_at_end():
        # ... handle escaped quotes for both types
```

## Impact
This change enables more robust regex patterns for HTML parsing and text extraction, allowing developers to create patterns that handle both single and double quotes in HTML attributes without needing complex workarounds.

## Reference
See changelog: `nova/changelog/20251025/2120-CHANGELOG.md`
