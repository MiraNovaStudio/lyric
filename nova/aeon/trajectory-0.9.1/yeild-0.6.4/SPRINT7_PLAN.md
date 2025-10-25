# Sprint 7 — General Bugfixes to 0.6.0

**Target Version:** 0.7.0

## Sprint Goal

Fix bugs found from functional testing of Lyric 0.6.0 after sprint
6 completion


### Task 1: Implement Regex Match Group Handling

#### Summary

Fix the bug where Lyric cannot interpret or execute .group(n) calls on regex match objects.
Currently, expressions such as:

```
rex title_pattern = /<title>(.*?)<\/title>/
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


### Task 2. 







## Definition of Done

