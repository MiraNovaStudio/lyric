# DEBUG PLAN — Lyric `given` Infinite Loop Fix

**Goal:**  
Fix the infinite loop behavior in the `given` construct so that the loop condition variable (like `keep_going`) is re-evaluated on each iteration using the live updated environment, not a stale snapshot.

---

## 🧩 Observed Behavior

When running:


python -m lyric.cli run tests/examples/does_it_work.ly


…the interpreter enters an infinite loop even after `keep_going` is set to `false`.

Changing the starting value of `count` alters the first few lines of output, but the loop still repeats indefinitely.

This indicates that the `given` condition is only evaluated once or that the loop executes in an isolated environment that never sees updates from inside the block.

---

## ⚙️ Root Cause Hypothesis

The interpreter or evaluator currently does one of the following:
1. Evaluates the `given` condition once before entering the loop and never re-evaluates it.
2. Executes the `given` block in a cloned or isolated environment that prevents variable changes from propagating.
3. Both of the above.

---

## ✅ Expected Behavior

For a construct like:



given keep_going:
...
done


…the interpreter should perform logic equivalent to:

while evaluate(keep_going) == True:
execute(block) in the SAME environment

Loop continues until `evaluate(keep_going)` returns `False`.

---

## 🔍 Steps to Fix

1. **Locate Implementation**
   - Find the section of code handling the `given` statement, likely in `interpreter.py` or a similar module.
   - Search for `Given`, `GivenNode`, or `GivenStatement` in the interpreter.

2. **Inspect Condition Evaluation**
   - Confirm where `keep_going` is evaluated.
   - If it’s evaluated once before entering a loop, move it *inside* the loop.

3. **Verify Environment Handling**
   - Ensure the block executes in the **same environment object**.
   - Do **not** create or clone new scopes per iteration.
   - The interpreter should re-evaluate and execute using the live variable bindings.

4. **Modify Loop Logic**
   - Use logic equivalent to:
     ```
     while evaluate(condition_expr, env):
         execute(block, env)
     ```
   - Re-use the same environment each pass.

5. **Check Scope Management**
   - If there’s a `push_scope()` or `new_scope()` call before executing the `given` block, determine if it’s necessary.
   - If it isolates variable updates, remove or adjust it.

6. **Add Debug Logging**
   - Print `keep_going` value before each iteration to verify that it changes when set inside the block.

7. **Test the Fix**
   - Run:
     ```
     python -m lyric.cli run tests/examples/does_it_work.ly
     ```
   - Expected correct output:
     ```
     Count: 0
     count assignment:  1
     Count: 1
     count assignment:  2
     Count: 2
     count assignment:  3
     count:  3
     keep_going:  False
     Final count: 3
     ```

8. **Regression Testing**
   - Execute:
     ```
     pytest -v
     ```
   - Confirm all other control flow constructs (`if`, `else`, `when`, etc.) continue to pass.

---

**End of Plan**
