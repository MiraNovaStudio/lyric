# Changelog Entry - Version 0.5.0 Release

**Date:** 2025-01-22  
**Time:** 21:32  
**Type:** Version Release  
**Sprint:** Sprint 5 Complete  

---

## 🚀 Version 0.5.0 Release

### **Major Features Added**

#### **Rex Type (Regular Expressions)**
- ✅ Native `rex` type with `/pattern/` literal syntax
- ✅ `.match(str)` method for pattern matching
- ✅ `.replace(source, replacement)` method for string replacement
- ✅ Comprehensive error handling for invalid regex patterns
- ✅ Disambiguation from division operator (`/` vs `/pattern/`)

#### **Boolean Types**
- ✅ `god` type honoring Kurt Gödel's contributions to logic
- ✅ `bin` type as alternative boolean type name
- ✅ `true` and `false` literals (lowercase)
- ✅ Full compatibility with logical operations and comparisons
- ✅ Interchangeable `god` and `bin` types

#### **Enhanced CLI**
- ✅ `lyric run file.ly` command for explicit execution
- ✅ `lyric file.ly` shorthand command (defaults to run)
- ✅ `lyric --help` and `lyric --version` flags
- ✅ Global `lyric` command availability after `pip install`
- ✅ Proper error messages for missing/invalid arguments

### **Technical Improvements**

#### **Error Handling**
- ✅ Fixed AST position tracking in binary operations
- ✅ Accurate line and column numbers in error messages
- ✅ Better debugging experience for developers

#### **Type System**
- ✅ Enhanced `type()` and `isinstance()` built-ins
- ✅ Support for new `rex`, `god`, and `bin` types
- ✅ Improved type compatibility checking

### **Documentation Updates**
- ✅ Updated `README.md` with version 0.5.0
- ✅ Added examples for regex and boolean types
- ✅ Updated CLI usage documentation
- ✅ Updated `Lyric Language Specification.md` to version 0.5.0
- ✅ Comprehensive changelog entries for all Sprint 5 tasks

### **Test Coverage**
- ✅ **436 total tests** (100% passing)
- ✅ **76 new tests** for Sprint 5 features
- ✅ **24 tests** for `rex` type functionality
- ✅ **24 tests** for `god` type functionality
- ✅ **28 tests** for `bin` type functionality

### **Files Modified**
- `pyproject.toml` - Version updated to 0.5.0
- `README.md` - Updated version and added Sprint 5 features
- `docs/Lyric Language Specification.md` - Updated to version 0.5.0
- `lyric/cli.py` - Enhanced CLI with new commands
- `lyric/lexer.py` - Added regex literal scanning and new keywords
- `lyric/parser.py` - Added regex parsing and type validation
- `lyric/interpreter.py` - Added rex object handling and type compatibility
- `lyric/runtime.py` - Updated built-in functions for new types

### **New Test Files**
- `lyric/tests/core-0.5.0/test_rex_type.py` - 24 comprehensive tests
- `lyric/tests/core-0.5.0/test_god_type.py` - 24 comprehensive tests
- `lyric/tests/core-0.5.0/test_bin_type.py` - 28 comprehensive tests

### **Sprint 5 Summary**
- ✅ **All 8 tasks completed** successfully
- ✅ **1 critical bug fix** (PIVOT 8.1) for AST position tracking
- ✅ **100% test pass rate** maintained
- ✅ **Comprehensive documentation** with changelogs and summaries
- ✅ **Ready for production** tagging and release

---

## 🎯 Version 0.5.0 Status

**Status:** ✅ **COMPLETE**  
**Ready for:** Tagging, Release, and Sprint 6 Planning  
**Test Status:** 436/436 tests passing (100%)  
**Documentation:** Complete with examples and specifications  

**Version 0.5.0 represents a significant milestone in Lyric's development with native regex support, enhanced boolean types, and improved CLI experience.**
