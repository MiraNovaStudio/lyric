# SPRINT5 Task 3 — Implement .REPLACE() Method — COMPLETED ✅

## Summary

Successfully implemented the `.replace()` method for the `rex` type, enabling regex-based string replacement functionality. The implementation uses Python's `re.sub()` internally and provides comprehensive string manipulation capabilities with proper error handling and type safety.

## Implementation Details

### 1. RexObject Class Updates (`lyric/interpreter.py`)
- ✅ Added `.replace(source, replacement)` method to `RexObject` class
- ✅ Implemented using Python's `re.sub()` for pattern replacement
- ✅ Added comprehensive parameter validation for both source and replacement strings
- ✅ Proper error handling for non-string input parameters
- ✅ Returns new string without modifying the original

### 2. Method Signature and Behavior
```python
def replace(self, source: str, replacement: str) -> str:
    """Replace all matches of the regex pattern in the source string."""
```

### 3. Test Coverage
- ✅ Created comprehensive test suite (`tests/test_rex_replace.py`) with 15 tests
- ✅ Created example program (`tests/examples/rex_replace_tests.ly`)

## Features Implemented

### ✅ Basic Replacement Functionality
```lyric
rex pattern = /cat/
var result = pattern.replace("the cat sat", "dog")  # Returns "the dog sat"
```

### ✅ Multiple Match Replacement
```lyric
rex pattern = /cat/
var result = pattern.replace("cat cat cat", "dog")  # Returns "dog dog dog"
```

### ✅ String Variable Support
```lyric
rex pattern = /hello/
var source_text = "hello world hello"
var replacement = "hi"
var result = pattern.replace(source_text, replacement)  # Works with variables
```

### ✅ Complex Pattern Replacement
```lyric
rex digit_pattern = /\d+/
var result = digit_pattern.replace("I have 5 cats and 3 dogs", "many")
# Returns "I have many cats and many dogs"
```

### ✅ Word Boundary Patterns
```lyric
rex word_pattern = /\bcat\b/
var result = word_pattern.replace("cat in the catalog", "dog")
# Returns "dog in the catalog" (preserves "catalog")
```

### ✅ Whitespace Normalization
```lyric
rex space_pattern = /\s+/
var result = space_pattern.replace("hello    world", " ")
# Returns "hello world"
```

### ✅ Email Pattern Replacement
```lyric
rex email_pattern = /[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}/
var result = email_pattern.replace("Contact user@example.com for help", "admin@company.com")
# Returns "Contact admin@company.com for help"
```

### ✅ Error Handling
```lyric
rex pattern = /cat/
var number = 123
var result = pattern.replace(number, "dog")  # Raises RuntimeErrorLyric
```

## Test Results

All 15 tests pass successfully:

1. ✅ `test_rex_replace_basic_functionality` - Basic replacement operations
2. ✅ `test_rex_replace_multiple_matches` - Multiple match replacement
3. ✅ `test_rex_replace_with_string_variables` - String variable support
4. ✅ `test_rex_replace_complex_patterns` - Complex regex patterns
5. ✅ `test_rex_replace_whitespace_pattern` - Whitespace pattern replacement
6. ✅ `test_rex_replace_email_pattern` - Email pattern replacement
7. ✅ `test_rex_replace_empty_string` - Empty string handling
8. ✅ `test_rex_replace_no_matches` - No match scenarios
9. ✅ `test_rex_replace_case_sensitive` - Case sensitivity verification
10. ✅ `test_rex_replace_error_non_string_source` - Error handling for non-string source
11. ✅ `test_rex_replace_error_non_string_replacement` - Error handling for non-string replacement
12. ✅ `test_rex_replace_error_boolean_parameters` - Error handling for boolean parameters
13. ✅ `test_rex_replace_returns_string_type` - Return type verification
14. ✅ `test_rex_replace_preserves_original_string` - Original string preservation
15. ✅ `test_rex_replace_special_characters` - Special character handling

## Acceptance Criteria Verification

### ✅ Replaces all matches in the source string
- Method correctly replaces all occurrences of the pattern in the source string
- Multiple matches are all replaced in a single operation
- Works with complex patterns including word boundaries, digits, and whitespace

### ✅ Returns a new string
- Method returns a new string object without modifying the original
- Return type is properly recognized as `str` in Lyric
- Original source string remains unchanged

### ✅ Works with string literals and variables
- Method accepts string literals: `pattern.replace("text", "replacement")`
- Method accepts string variables: `pattern.replace(source_var, replacement_var)`
- Both usage patterns work identically

## Technical Implementation Notes

### Python Integration
- Uses Python's `re.sub()` method for efficient regex-based replacement
- Leverages the compiled regex pattern stored in `RexObject` for performance
- Handles all Python regex features including word boundaries, character classes, and quantifiers

### Parameter Validation
- Validates that both `source` and `replacement` parameters are strings
- Provides clear error messages for invalid parameter types
- Different error messages for source vs replacement parameter validation

### String Immutability
- Original source string is never modified
- Method returns a completely new string with replacements applied
- Follows functional programming principles for string operations

### Performance Considerations
- Regex patterns are compiled once during `RexObject` creation
- `re.sub()` is highly optimized for string replacement operations
- No unnecessary string copying or intermediate operations

## Example Usage

```lyric
def main() {
    # Basic usage
    rex pattern = /cat/
    var result = pattern.replace("the cat sat", "dog")     # "the dog sat"
    
    # Multiple matches
    var result2 = pattern.replace("cat cat cat", "dog")    # "dog dog dog"
    
    # With variables
    var source = "hello world"
    var replacement = "hi"
    rex hello_pattern = /hello/
    var result3 = hello_pattern.replace(source, replacement)  # "hi world"
    
    # Complex patterns
    rex digit_pattern = /\d+/
    var result4 = digit_pattern.replace("I have 5 cats", "many")  # "I have many cats"
    
    # Word boundaries
    rex word_pattern = /\bcat\b/
    var result5 = word_pattern.replace("cat in catalog", "dog")   # "dog in catalog"
    
    # Whitespace normalization
    rex space_pattern = /\s+/
    var result6 = space_pattern.replace("hello    world", " ")    # "hello world"
}
```

## Integration with Existing Features

### Method Call System
- Fully integrated with Lyric's method call infrastructure
- Uses the same method resolution as `.match()` and other object methods
- Consistent error handling and parameter validation

### Type System
- Return values are properly typed as `str`
- Method parameters are validated for correct types
- Integrates seamlessly with Lyric's type checking system

### Error Handling
- Consistent error message format with other Lyric methods
- Clear indication of expected vs actual parameter types
- Graceful failure with informative error messages

## Next Steps

Task 3 is complete and ready for Task 4 (Search Method Decision). The `.replace()` method provides comprehensive string replacement functionality with proper error handling, type safety, and integration with the existing Lyric language infrastructure.

---

**Status:** ✅ COMPLETED  
**Tests:** 15/15 passing  
**Ready for:** SPRINT5 Task 4
