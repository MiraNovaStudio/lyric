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

### Task 2: Investigatge Regex Match Group Handling

#### Summary

Fix the bug where Lyric cannot interpret or execute .group(n) calls on regex match objects.
Currently, expressions such as:

```
rex title_pattern = regex("<title>(.*?)<\/title>")
print title_pattern.group(1)
```

May fail to parse or execute because Lyric does not recognize .group() as a valid method call on a regex object. 

#### Implementation Tasks

1. Investigate that pattern.group(1) is functioning properly

2. Verify that pattern.group(2) is also functioning

3. Unit Tests

Add tests under lyric/tests/core-0.6.4/test_regex_groups.py:

Single capture group ((.*?)) returns expected text.

Accessing a missing group raises an error.

Non-match returns handled gracefully.

#### Examples

Create a test example .ly script in tests/examples with the main body :

```
rex title = regex("<title>(.*?)<\/title>")
var match = title.match("<title>Hello</title>")
print match.group(1)
```

#### Acceptance Criteria

✅ Parser recognizes .group() syntax on regex match objects.

✅ .group(n) returns correct substring for valid matches.

✅ Nonexistent or failed matches raise clear runtime error.

✅ All new regex-related tests pass successfully.

✅ No regression in existing print or rex parsing behavior.


### Task 3. Resolve issue with line number


Error: Lexical error at line 0, column 0: Unexpected character '^' at line 75, column 26

The line 0 and column 0 are incorrect in the beginning and we do not need
this information displayed twice.

#### Implementation steps (for Claude):

Locate Error Formatting Function

Identify where lexical and syntax errors are formatted into final user-facing strings.

Confirm that both the leading “line 0, column 0” and trailing “at line …, column …” values are generated in the same function or context.

Determine Accurate Source Position

Retrieve the actual token or character position that triggered the error (token.line, token.column, or lexer cursor state).

Ensure these values are accessible when constructing the error message.

Choose and Implement One of Two Output Formats:

Option A: Remove the incorrect prefix entirely, keeping only the final “at line X, column Y” (the correct values).

Option B: Replace the prefix’s zeroes with the actual values and remove the redundant trailing position reference.

Ensure the message reads cleanly and includes only one accurate position reference.

Update Error Templates

Modify any global error template or exception class that automatically includes both prefixes.

Verify that runtime and compile-time errors remain consistent in their output format.

Add Targeted Unit Tests

Create tests that intentionally trigger lexical and syntax errors at known line/column positions.

Confirm that the resulting error message contains:

Only one line/column reference.

Correct coordinates matching the offending character.

#### Acceptance Criteria

✅ Only one instance of line/column information appears in error messages.

✅ Reported line and column values correctly match the position of the offending token.

✅ “line 0, column 0” never appears in any error output.

✅ Format of error messages is consistent across lexical and syntax errors.

✅ All new error-handling tests pass successfully.

### Task 4: 

Add elif as an Alternative to else if

#### Summary
Re-enable the elif keyword in Lyric as a direct alternative to else if. Both forms should function identically in syntax and behavior. This allows developers coming from Python or C-style backgrounds to use their preferred conditional style without altering control-flow semantics.

#### Implementation Tasks

Update the lexer to recognize elif as a valid token mapped to the same internal construct as else if.

Adjust the parser’s conditional rule to accept either else if or elif in chained conditions.

Ensure code generation or interpreter evaluation treats both forms equivalently.

Add new unit tests validating correct behavior, including mixed usage (if … elif … else and if … else if … else).


#### Acceptance Criteria

✅ elif executes correctly and produces identical logic flow to else if.

✅ Mixed constructs (if … elif … else and if … else if … else) parse and run successfully.

✅ No regressions or syntax conflicts occur with existing if/else blocks.


### Task 5: Remove else if Constructs, Standardize on elif

#### Summary:
We have decided to deprecate and remove all else if constructs from Lyric. The language will now exclusively use elif for conditional chaining. This change eliminates a persistent grammar ambiguity and simplifies both parsing and readability. The update will require a full parser cleanup and a very significant unit test refactor since many test scripts currently use else if.

#### Implementation Tasks:

Remove else if handling entirely from the parser and grammar definitions.

Delete or comment out any lexer rules recognizing else if as a valid control-flow token.

Ensure elif remains fully supported and properly mapped to the conditional continuation logic.

Refactor all unit tests to replace else if occurrences with elif. This includes:

Parser tests

Interpreter logic tests

Example and demo scripts under /tests and /examples

Re-run all test suites and confirm 100% pass rate.

Note: this is a major unit test refactor and we are not in a hurry so 
take your time.


Validate that mixed constructs like if … elif … else parse and execute correctly.

#### Acceptance Criteria:

✅ elif is the only valid form of conditional continuation.

✅ Any use of else if now triggers a parser or syntax error.

✅ All unit and integration tests updated and passing.

✅ Syntax highlighting and tokenization correctly identify elif only.

✅ No remaining references to else if anywhere in source, grammar, or documentation.


### Task 6 - Add case as Syntactic Sugar for elif (in Lexer Only)

#### Summary:
Introduce the case keyword as an alternate form of elif for readability and future expansion. At this stage it should function only as a token alias—no parser or interpreter logic changes. The goal is to reserve case as a stylistic synonym while preserving full backward compatibility with existing elif behavior.

#### Implementation Tasks:

Update the lexer to recognize case as a valid keyword.

Map case internally to the same token type as elif (e.g., TOKEN_ELIF).

Do not introduce separate grammar or execution logic; this is lexer-level only.

Confirm the parser continues to handle all conditional flow exactly as if elif were used.

Add a few new unit tests under lyric/tests/core-0.6.4 to verify tokenization consistency:

if … case … else … end parses without error.

Mixed usage (if … elif … case … else … end) is accepted.

Run the full test suite to ensure no regressions.

#### Acceptance Criteria:

✅ case is accepted and internally treated as elif.

✅ No syntax, parsing, or runtime changes occur.

✅ Existing elif tests remain valid and passing.

✅ New tokenization tests for case pass successfully.

✅ No other language behavior or grammar is affected.


### Task 7 - Ensure Proper Handling of Escape Strings in Regex Literals

#### Summary:
We need to verify and fix Lyric’s handling of escaped sequences inside string literals used in regular expressions. The goal is to ensure constructs like regex("/<title>something<\/title>/") are correctly parsed, tokenized, and executed — preserving backslashes and special characters exactly as written.

#### Implementation Tasks:

Review the string literal parsing logic to confirm escape sequences (e.g. \", \\, \/, \n, \t) are preserved correctly through the lexer and parser.

Specifically test regex patterns wrapped in quotes (e.g. regex("/pattern/")) to ensure escaped slashes \/ are not stripped or misinterpreted.

Confirm that Lyric does not attempt to interpret regex delimiters or backslashes as syntax — they should remain raw inside the string.

Update or extend lexer rules if necessary to distinguish between Lyric escape sequences and regex literal escapes.

Add comprehensive unit tests under lyric/tests covering cases such as:

regex("/<title>something<\/title>/")

regex("/\\d+/")

regex("/foo\\//")

regex("/\\w+\\s\\w+/")

Run the full test suite and confirm all string and regex handling tests pass.

#### Acceptance Criteria:

✅ Escaped characters within string literals are preserved correctly.

✅ Regex patterns with backslashes and escaped slashes work exactly as in Python.

✅ No parsing or tokenization errors occur when using regex(...).

✅ Unit tests demonstrate correct matching behavior.

✅ No regressions in general string literal parsing.


## Definition of Done

