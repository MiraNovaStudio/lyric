# Sprint 7 — General Bugfixes to 0.6.0

**Target Version:** 0.7.0

## Sprint Goal

Fix bugs found from functional testing of Lyric 0.6.0 after sprint
6 completion

### Task 1: Remove parser ambiguity for rex literals

#### Summary

Replace Lyric’s ambiguous /pattern/ literal syntax with a new constructor-based form:

```
rex pattern = regex("/<pattern>/")
```

This resolves parser ambiguity between the division operator (/) and regex delimiters, while preserving all existing runtime behavior and the rex type interface.

The goal is to maintain feature parity with current functionality — only the syntax changes.

#### Implementation Tasks
Task 1 — Remove Direct Regex Literal Parsing

Remove the /pattern/ token rule from the grammar.

Ensure that / is used only for division and arithmetic expressions going forward.

2. — Implement regex() Constructor built-in function

Introduce a built-in function regex(str pattern, str flags="").

Return a rex type instance internally.

Compile the provided pattern string using Python’s re.compile() or Lyric’s equivalent.

3. — Update Parser and Runtime Integration

Adjust the parser so that regex("/pattern/") is treated as a normal function call expression.

Verify that regex objects created through this constructor still support the existing API methods (e.g. .search(), .match()).

4.  — Update Unit Tests

Modify all affected tests to use the new regex("/pattern/") syntax.

Add dedicated regression tests ensuring:

Division expressions (a / b) still parse and evaluate correctly.

Regex constructor patterns compile and function as before.

#### Acceptance Criteria

Acceptance Criteria

✅ Regex patterns are created using regex("/pattern/").

✅ /pattern/ literal syntax no longer parses or conflicts with division.

✅ Existing regex operations (.search(), .match(), etc.) continue functioning without modification.

✅ All updated unit tests pass.

✅ Documentation and examples reflect the new constructor syntax.

### Task 2: Implement Regex Match Group Handling

#### Summary

Fix the bug where Lyric cannot interpret or execute .group(n) calls on regex match objects.
Currently, expressions such as:

```
rex title_pattern = regex("<title>(.*?)<\/title>")
print title_pattern.group(1)
```

fail to parse or execute because Lyric does not recognize .group() as a valid method call on a regex object. also the parse of the title_pattern fails before it ever gets to pattern.group() method

#### Implementation Tasks

1. Parser Update

Extend grammar to allow method calls on regex match objects.

Ensure the parser correctly handles chained expressions like pattern.group(1) and match.group(0).

2. Interpreter Logic

Modify the runtime to support a RegexMatch object with callable methods:

.group(n) → return the nth capture group as a string.

If no match exists, .group() should raise a runtime error:
RuntimeError: No active regex match.

Regex Engine Integration

Hook into the existing Python re module or rex internal engine.

When a match is successful, wrap the Python match object inside Lyric’s RegexMatch type.

3. Unit Tests

Add tests under lyric/tests/core-0.6.4/test_regex_groups.py:

Single capture group ((.*?)) returns expected text.

Accessing a missing group raises an error.

Non-match returns handled gracefully.

Examples

Create a test example .ly script in tests/examples with the main body :

```
rex title = /<title>(.*?)<\/title>/
var match = title.match("<title>Hello</title>")
print match.group(1)
```

#### Acceptance Criteria

✅ Parser recognizes .group() syntax on regex match objects.

✅ .group(n) returns correct substring for valid matches.

✅ Nonexistent or failed matches raise clear runtime error.

✅ All new regex-related tests pass successfully.

✅ No regression in existing print or rex parsing behavior.


### Task 2. Ensure all Unit tests are passing 100%









## Definition of Done

