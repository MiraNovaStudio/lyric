SPRINT6_PIVOT6.5.1_PLAN.md

Title: Introduce break and continue keywords into Lyric
Date: 2025-10-25
Author: Michael (Aeonath)
Sprint: 6 (Pivot 6.5.1)
Status: Planned

Objective

Enhance Lyric’s loop control flow with break and continue statements to improve expressiveness and align Lyric more closely with common structured programming conventions.
This pivot adds targeted functionality without destabilizing the current interpreter architecture.

Background

Lyric currently supports given and done constructs for iteration and block control but lacks fine-grained loop interruption mechanisms.
Introducing break and continue will allow developers to exit loops early or skip the remainder of a loop iteration, increasing flexibility and readability in control structures.

Design Overview
break Keyword

Immediately exits the nearest enclosing loop (given, while, or future for loops).

Control transfers to the first statement after the loop block.

Example:
given x < 10:
if x == 5:
break
print x
x = x + 1
done

Result: loop stops once x == 5.

continue Keyword

Skips the remainder of the current iteration and proceeds to the loop’s next iteration.

Example:
given x < 10:
x = x + 1
if x % 2 == 0:
continue
print x
done

Result: prints only odd numbers.

Implementation Plan

Lexer Updates

Add break and continue as new reserved keywords.

Ensure they are tokenized distinctly from identifiers.

Parser Modifications

Extend loop grammar to recognize break and continue statements.

Enforce positional validation: they must occur within loop contexts.

Invalid usage should raise CompileError: 'break' used outside of loop' or 'continue' used outside of loop'.

AST Nodes

Introduce new node types: BreakNode and ContinueNode.

Both nodes require minimal payload (no child expressions).

Interpreter Logic

Modify loop execution handlers to detect these nodes:

BreakNode: raise internal signal or flag to terminate loop execution.

ContinueNode: raise internal signal or skip directly to loop’s next iteration boundary.

Use internal exceptions or structured control signals rather than raw Python exceptions for clarity.

Unit Tests

Create test cases validating:

Correct loop termination with break.

Correct iteration skipping with continue.

Error handling for out-of-context usage.

Nested loops with inner break or continue only affecting nearest loop.

Documentation Update

Update language specification and website:

Add break and continue entries under “Control Flow.”

Include examples demonstrating nested and conditional use.

Acceptance Criteria

✅ break cleanly exits current loop level.

✅ continue correctly skips to the next iteration.

✅ Both keywords raise compile-time errors if used outside of loops.

✅ Unit tests cover all valid and invalid usage scenarios.

✅ Documentation and examples updated.

Risk & Mitigation

Parser Conflicts: Ensure token priority does not interfere with existing done or return parsing.

Runtime Signals: Internal loop control should use a lightweight mechanism distinct from error handling to avoid unintended catch interactions.

Testing Overlap: Validate interactions with try/catch within loops to ensure consistent break behavior.

Notes

This pivot should be implemented after Task 5 stabilizes.
No core interpreter redesign is required—only incremental additions to parser and loop handling logic.
Target inclusion in Lyric 0.6.0 release if testing remains stable by Sunday evening.