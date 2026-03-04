# SPRINT6_PIVOT_6.8.1_PRINT_DUAL_SYNTAX_SUPPORT.md

**Title:** Support Both Parenthesized and Bare Print Syntax  
**Date:** 2025-10-25  
**Authors:** Michael (Aeonath), ChatGPT, and Claude  
**Status:** Approved for Sprint 6 Integration (0.6.1)

## 🎯 Objective

Extend Lyric's print statement to support both modern function-style (`print(<expr>)`) and traditional bare (`print <expr>`) syntax forms. This enhances readability and flexibility while maintaining backward compatibility for developers who prefer the simpler statement form.

## 🧩 Background

Earlier builds allowed `print "Hello"` but failed to evaluate complex expressions in bare form (e.g., string concatenation or multi-variable output). Lyric 0.6.1 will expand the grammar to evaluate full expressions in both syntaxes, ensuring that:

```lyric
print("Hello " + name)
print "Hello " + name
```

are functionally identical.

## ⚙️ Implementation Tasks

### Task 1 — Parser Grammar Update

Modify parser rules for print to:

- Accept both `print(<expr>)` and `print <expr>`.
- Route both forms to the same expression evaluation logic.
- Ensure the bare form supports full expression parsing, including concatenation (`+`), arithmetic, and variable substitution.

### Task 2 — Interpreter Standardization

Consolidate handling for both syntaxes so they invoke a single print function internally.

Support multi-argument printing in both forms:

```lyric
print("a", "b")
print "a", "b"
```

Ensure identical spacing and formatting behavior between forms.

### Task 3 — Unit Testing

Add new test cases for:

- Single-expression prints.
- Concatenations (`"Hello " + name`).
- Multi-argument prints (`print "a", "b"`).
- Error handling for malformed syntax.
- Confirm that both forms produce identical output.

### Task 4 — Documentation & Examples

- Update `lyric_spec.md` to include both print forms.
- Add examples under `/studio` and `/tests` demonstrating both syntaxes.

**Note:** Both forms are equivalent and interchangeable.

## ✅ Acceptance Criteria

- ✅ `print(<expr>)` and `print <expr>` compile and execute correctly.
- ✅ Both forms support concatenation, multi-argument printing, and full expression evaluation.
- ✅ Unit tests cover all valid and invalid cases.
- ✅ Documentation and examples updated accordingly.
- ✅ No regressions introduced in interpreter or output logic.