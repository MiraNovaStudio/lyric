# Sprint 5 Implementation Plan — Rex Type and CLI Execution Command

**Target Version:** 0.5.0  
**Sprint Goal:** Introduce native regular expression type (`rex`) and enhance CLI execution

## 🎯 **Sprint Overview**

Sprint 5 focuses on adding powerful text processing capabilities through a native `rex` type and improving the developer experience with enhanced CLI functionality. This sprint also introduces the `god` and `bin` boolean types, honoring logician Kurt Gödel.

## 📋 **Task Breakdown**

### **Task 1 — Define Rex Type**
**Objective:** Create a new built-in `rex` type with `/.../` literal syntax

**Implementation Details:**
- **Lexer Changes:**
  - Add `REGEX_LITERAL` token type
  - Handle `/.../` syntax without conflicting with division
  - Validate regex patterns at tokenization time
  - Raise parse-time errors for malformed regex

- **Parser Changes:**
  - Create `RexNode` AST node class
  - Handle `REGEX_LITERAL` tokens in `_parse_primary()`
  - Add regex compilation and validation
  - Store compiled regex pattern for runtime use

- **Interpreter Changes:**
  - Add `RexNode` to evaluation dispatch
  - Implement `_evaluate_rex_literal()` method
  - Store compiled regex objects in runtime

- **Test Coverage:**
  - Valid regex patterns (`/^abc/`, `/cat/`, `/\\d+/`)
  - Invalid regex patterns (malformed, unclosed)
  - Edge cases (empty patterns, special characters)
  - Integration with existing type system

### **Task 2 — Implement .match() Method**
**Objective:** Add `match(str)` method to rex objects

**Implementation Details:**
- **Method Implementation:**
  - Use Python's `re.match()` internally
  - Return boolean `True`/`False`
  - Handle non-string input with friendly errors
  - Support both string literals and variables

- **Error Handling:**
  - Type checking for input parameters
  - Clear error messages for invalid inputs
  - Graceful handling of regex compilation errors

- **Test Coverage:**
  - Basic matching (`/^abc/` vs `"abcdef"`)
  - Non-matching patterns (`/^abc/` vs `"xyz"`)
  - Edge cases (empty strings, special characters)
  - Error cases (non-string input)

### **Task 3 — Implement .replace() Method**
**Objective:** Add `replace(source, replacement)` method to rex objects

**Implementation Details:**
- **Method Implementation:**
  - Use Python's `re.sub()` internally
  - Replace all matches in source string
  - Return new string without modifying original
  - Support both string literals and variables

- **Error Handling:**
  - Type checking for both parameters
  - Clear error messages for invalid inputs
  - Handle edge cases (empty strings, no matches)

- **Test Coverage:**
  - Basic replacement (`/cat/` → `"dog"`)
  - Multiple matches replacement
  - No matches scenarios
  - Edge cases (empty patterns, special characters)

### **Task 4 — Search Method Decision**
**Objective:** Defer `.search()` method implementation

**Implementation Details:**
- Add comment placeholder in rex implementation
- Note that `.search()` may be added in future sprints
- Ensure no runtime references to `.search()`

### **Task 5 — Add CLI Entrypoint**
**Objective:** Support both `lyric run file.ly` and `lyric file.ly` commands

**Implementation Details:**
- **CLI Parser Changes:**
  - Modify argument parsing to handle missing subcommand
  - Default to "run" when no subcommand specified
  - Maintain backward compatibility with existing commands

- **Command Handling:**
  - `lyric file.ly` → automatically assume "run" subcommand
  - `lyric run file.ly` → explicit run command
  - Preserve help and version flags functionality

- **Test Coverage:**
  - Both command formats execute correctly
  - Error messages for missing/invalid arguments
  - Help and version flags still work
  - Integration with existing CLI functionality

### **Task 6 — Pip/Packaging Integration**
**Objective:** Ensure global `lyric` command availability after pip install

**Implementation Details:**
- **Package Configuration:**
  - Verify `entry_points` in `pyproject.toml`
  - Ensure `lyric=lyric.cli:main` console script
  - Test installation with `pip install -e .`

- **Cross-Platform Testing:**
  - Verify functionality on Windows PowerShell
  - Test Unix compatibility
  - Ensure global command availability

### **Task 7 — Add God Type (Boolean Type)**
**Objective:** Introduce `god` type honoring logician Kurt Gödel

**Implementation Details:**
- **Lexer Changes:**
  - Add `god` keyword to `KEYWORDS`
  - Add `true` and `false` literals
  - Handle boolean tokenization

- **Parser Changes:**
  - Add `god` to type parsing
  - Handle `true`/`false` literals
  - Create `BooleanNode` AST node

- **Interpreter Changes:**
  - Implement boolean evaluation
  - Handle logical operations (`and`, `or`, `not`)
  - Support conditional statements

- **Type System:**
  - Replace existing `bool` type entirely
  - Map internally to Python `bool`
  - Update type compatibility checking

- **Documentation:**
  - Add note about Gödel reference
  - Update language specification
  - Include usage examples

### **Task 8 — Add Bin Type Alias**
**Objective:** Introduce `bin` as alias for `god` type

**Implementation Details:**
- **Lexer Changes:**
  - Add `bin` keyword to `KEYWORDS`
  - Handle `bin` type parsing

- **Parser Changes:**
  - Add `bin` to type parsing
  - Map to same boolean implementation

- **Interpreter Changes:**
  - Handle `bin` type identically to `god`
  - Same logical operations support

- **Documentation:**
  - Note that `bin` is alias for `god`
  - Include usage examples

## 🧪 **Test Strategy**

### **Test Directory Structure:**
```
lyric/tests/core-0.5.0/
├── __init__.py
├── test_rex_type.py          # Task 1: Rex type definition
├── test_rex_match_method.py # Task 2: .match() method
├── test_rex_replace_method.py # Task 3: .replace() method
├── test_cli_enhancements.py  # Task 5: CLI improvements
├── test_god_type.py          # Task 7: God type
└── test_bin_type.py          # Task 8: Bin type alias
```

### **Test Coverage Requirements:**
- **100% Test Pass Rate:** All tests must pass before task completion
- **Comprehensive Coverage:** Edge cases, error conditions, integration
- **Regression Testing:** Ensure existing functionality remains intact
- **Cross-Platform:** Test on Windows PowerShell environment

## 📁 **File Modifications**

### **Core Language Files:**
- `lyric/lexer.py` — Add regex literals, god/bin keywords, true/false literals
- `lyric/parser.py` — Handle rex parsing, god/bin types, boolean literals
- `lyric/ast_nodes.py` — Add RexNode, BooleanNode
- `lyric/interpreter.py` — Implement rex evaluation, god/bin type handling
- `lyric/runtime.py` — Update type system for god/bin types

### **CLI Files:**
- `lyric/cli.py` — Enhance argument parsing for default subcommand

### **Configuration Files:**
- `pyproject.toml` — Verify entry_points configuration

### **Documentation Files:**
- `docs/Lyric Language Specification.md` — Update with rex, god/bin types
- `README.md` — Add usage examples and feature descriptions

## 🔄 **Implementation Order**

1. **Task 1:** Define Rex Type (foundation for Tasks 2-3)
2. **Task 2:** Implement .match() Method (depends on Task 1)
3. **Task 3:** Implement .replace() Method (depends on Task 1)
4. **Task 4:** Search Method Decision (documentation only)
5. **Task 5:** Add CLI Entrypoint (independent)
6. **Task 6:** Pip/Packaging Integration (depends on Task 5)
7. **Task 7:** Add God Type (independent)
8. **Task 8:** Add Bin Type Alias (depends on Task 7)

## 🎯 **Success Criteria**

### **Technical Requirements:**
- ✅ `rex` type fully functional with `.match()` and `.replace()` methods
- ✅ `/.../` regex literals parse correctly without division conflicts
- ✅ CLI supports both `lyric run file.ly` and `lyric file.ly` commands
- ✅ Global `lyric` command available after pip install
- ✅ `god` and `bin` types work identically for boolean operations
- ✅ 100% test pass rate maintained

### **Quality Requirements:**
- ✅ Comprehensive test coverage for all new features
- ✅ Clear error messages for invalid inputs
- ✅ Backward compatibility maintained
- ✅ Documentation updated with examples
- ✅ Cross-platform compatibility verified

## 📝 **Documentation Requirements**

### **Changelog Entries:**
- Create changelog for each task in `nova/changelog/20251022/`
- Include implementation details, files changed, status
- Use placeholder commit hash format

### **Task Summaries:**
- Create `SPRINT5_TASKX_SUMMARY.md` for each completed task
- Include brief completion summary, key accomplishments, status
- Reference changelog for detailed information

### **DOD Summary:**
- Create `SPRINT5_DOD_SUMMARY.md` upon sprint completion
- Verify all definition of done criteria met
- Include overall sprint status and achievements

## 🚀 **Ready for Implementation**

This implementation plan provides a comprehensive roadmap for Sprint 5, ensuring:
- **Clear Task Dependencies:** Logical implementation order
- **Comprehensive Testing:** 100% test coverage requirement
- **Quality Assurance:** Error handling and edge case coverage
- **Documentation:** Complete changelog and summary requirements
- **Cross-Platform:** Windows PowerShell environment compatibility

**Status:** Ready for user confirmation to begin Task 1 implementation.
