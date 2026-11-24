---
title: Lyric Tutorial
---
# The Lyric Tutorial

Lyric is a modern interpreted programming language designed for clarity and expressiveness.
This tutorial walks you through the language from the ground up — starting with your first program,
moving through types, control flow, functions, classes, and finishing with Lyric's unique
system integration features.

Install Lyric using the instructions in the README, then come back here.
This tutorial is written for complete
beginners as well as developers coming from other languages. If you have never written
a line of code before, start from section 1 and work your way through — every concept
is explained from scratch with examples you can run immediately.

---

## Table of Contents

1. [Your First Program](#1-your-first-program)
2. [Comments](#2-comments)
3. [Variables and Types](#3-variables-and-types)
4. [Operators](#4-operators)
5. [Control Flow](#5-control-flow)
6. [Functions](#6-functions)
7. [Arrays](#7-arrays)
8. [Tuples](#8-tuples)
9. [Maps](#9-maps)
10. [Strings](#10-strings)
11. [Classes and Inheritance](#11-classes-and-inheritance)
12. [Exception Handling](#12-exception-handling)
13. [Regular Expressions](#13-regular-expressions)
14. [File I/O](#14-file-io)
15. [Shell Execution](#15-shell-execution)
16. [Importing Lyric Modules](#16-importing-lyric-modules)
17. [Importing Python Modules](#17-importing-python-modules)
18. [Command-Line Arguments](#18-command-line-arguments)
19. [Putting It All Together](#19-putting-it-all-together)
20. [Standard Library](#20-standard-library)
21. [Next Steps](#21-next-steps)

---

## 1. Your First Program

Create a file called `hello.ly`:

```lyric
def main() {
    print("Hello from Lyric!")
}
```

Run it:

```bash
lyric hello.ly
```

```output
Hello from Lyric!
```

**Key points:**
- Every Lyric program needs a `main()` function as its entry point.
- Functions are defined with `def`, followed by the name and a parameter list.
- The body is enclosed in `{ }`.
- `print()` outputs text. You can also write `print` without parentheses.

---

## 2. Comments

Comments let you leave notes in your code that the interpreter ignores completely.  They are a common way for programmers to explain what the program does — both for other people reading it and for your future self.

In Lyric, a comment starts with `#` and runs to the end of the line:

```lyric
def main() {
    # This is a full-line comment — the interpreter skips it entirely
    int x = 42   # This is an inline comment after a statement

    # You can use comments to explain why you wrote something a certain way,
    # or to temporarily disable a line of code while you are debugging.
    # print("This line is commented out and will not run")
    print("x =", x)
}
```

```output
x = 42
```

Lyric does not have multi-line block comments. Just start each line with `#`.

---

## 3. Variables and Types

A **variable** is a named container that holds a value your program can read and change.  A **type** tells the program what kind of data that container is allowed to hold.  Types matter because a number and a piece of text behave very differently — you can multiply two numbers, but multiplying two names doesn't make sense.  By knowing the type of each variable, Lyric can catch mistakes early and handle your data correctly.

Lyric is **statically typed at declaration time** but allows dynamic typing with `var`.  Every variable declaration begins with a type keyword.

### 3.1 Primitive Types

A **primitive type** is the simplest kind of data a programming language understands — a single, indivisible value rather than something built out of smaller parts. Think of primitives as the atoms of your program: a whole number, a decimal number, a piece of text, or a simple yes/no answer. Everything else you will encounter later (arrays, objects, classes) is assembled from these basic building blocks.

Lyric provides the following primitive types:

| Type keyword | Meaning                    | Example value          |
|--------------|----------------------------|------------------------|
| `int`        | Integer number             | `42`, `-7`             |
| `flt`        | Floating-point             | `3.14`, `-0.5`         |
| `str`        | String (text)              | `"hello"`              |
| `god`        | Boolean                    | `True`, `False`        |
| `bin`        | Boolean (alias)            | `True`, `False`        |
| `obj`        | Class instance             | `Person("Alice")`      |
| `var`        | Dynamic (any type)         | anything               |

`god` is Lyric's primary boolean type — named in honor of the logician Kurt Gödel.
`bin` is a convenient alias for the same type.
`obj` is the type for holding class instances — see [section 3.4](#34-the-obj-type) and [section 11](#11-classes).

```lyric
def main() {
    int age = 30
    flt price = 9.99
    str greeting = "Hello"
    god active = True
    bin flag = False
    var anything = 42

    print("age is an integer:", age)
    print("price is a floating-point number:", price)
    print("greeting is a string:", greeting)
    print("active is a boolean (god):", active)
    print("flag is a boolean (bin):", flag)

    anything = "now I'm a string"
    print("var can change type — anything is now:", anything)
}
```

```output
age is an integer: 30
price is a floating-point number: 9.99
greeting is a string: Hello
active is a boolean (god): True
flag is a boolean (bin): False
var can change type — anything is now: now I'm a string
```

### 3.2 The `var` Type

Most of the types you have seen so far are **static** — once you declare a variable as `int`, it can only ever hold an integer. If you tried to store a string in an `int` variable, Lyric would report an error. This safety net is useful because it catches mistakes before your program runs.

`var` works differently. It is a **dynamic** type, meaning the variable is free to hold any kind of value and can even switch between types as your program runs. An `int` box only fits integers; a `var` box can be reshaped on the fly to fit whatever you put in it.

Use `var` when you need that flexibility — for example, when a value could reasonably be a number or a string depending on the situation, or when you are not sure what a function will return. In most cases, prefer a specific type so Lyric can catch errors for you; reach for `var` only when you genuinely need it.

```lyric
def main() {
    var result = 10
    print("result starts as an integer:", result)

    result = "changed to string"
    print("result is now a string:", result)

    result = True
    print("result is now a boolean:", result)
}
```

```output
result starts as an integer: 10
result is now a string: changed to string
result is now a boolean: True
```

### 3.3 Collection Types

So far every variable you have seen holds a single value — one number, one string, one boolean. A **collection type** is a variable that holds multiple values grouped together. Collections let you work with lists of items, fixed groups of related values, or lookups that pair a key with a value, all inside a single variable.

Lyric provides three built-in collection types:

| Type keyword | Meaning                        | Example              |
|--------------|--------------------------------|----------------------|
| `arr`        | Array (ordered, mutable list)  | `[1, 2, 3]`          |
| `tup`        | Tuple (ordered, immutable)     | `(1, 2, 3)`          |
| `map`        | Map (key-value pairs)          | `{"name": "Alice"}`  |

Arrays, tuples, and maps are covered in detail in [section 7](#7-arrays), [section 8](#8-tuples), and [section 9](#9-maps).

### 3.4 The `obj` Type

An **object** is a value that bundles together its own data and behavior. You define the blueprint for an object by writing a **class** (covered in detail in [section 11](#11-classes)), and when you create a concrete value from that blueprint — for example `Point(3, 7)` — you **instantiate** the class, and the result is an object.

Use `obj` to declare a variable that holds one of these objects. It is a typed alternative to `var` that enforces that the variable can only hold a Lyric object — not a plain integer, string, or array.

```lyric
class Point:
    def Point(x, y) {
        self.x = x
        self.y = y
    }
    def to_string() {
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    }
+++

def main() {
    obj p = Point(3, 7)      # p must hold a class instance
    print(p.to_string())     # (3, 7)
}
```

```output
(3, 7)
```

`obj` is preferred over `var` when you know the variable will always hold a class instance, because it makes the code's intent explicit and catches accidental type errors early:

```lyric
def main() {
    obj x = 42       # TypeError — 42 is not a class instance
}
```

`var` remains valid and is still the right choice when you need a variable that can hold different types at different times. Both are fully supported.

Classes are covered in detail in [section 11](#11-classes).

### 3.5 Type Conversion

Sometimes a value is the right data but the wrong type. For example, a user might type `"42"` into a text field — that is a string, not a number, so you cannot do math with it until you convert it. **Type conversion** (also called **casting**) transforms a value from one type into another. In Lyric you convert a value by calling the target type as a function — `int("42")` turns the string `"42"` into the integer `42`.

Lyric provides built-in functions to convert between types:

```lyric
def main() {
    str s = "42"
    int n = int(s)       # "42" (string) becomes 42 (integer)
    flt f = flt(n)       # 42 (integer) becomes 42.0 (float)
    str back = str(f)    # 42.0 (float) becomes "42.0" (string)

    print("string \"42\" converted to int:", n)
    print("int 42 converted to float:", f)
    print("float 42.0 converted back to string:", back)

    god truth = god(1)
    print("god(1) — non-zero numbers are True:", truth)

    god empty = god("")
    print("god(\"\") — empty string is False:", empty)
}
```

```output
string "42" converted to int: 42
int 42 converted to float: 42.0
float 42.0 converted back to string: 42.0
god(1) — non-zero numbers are True: True
god("") — empty string is False: False
```

### 3.6 Checking Types

As your programs grow, you will sometimes need to find out what type a value is at runtime — especially when working with `var` variables or data that comes from outside your program. Lyric's built-in `type()` function returns the type name of any value as a string, so you can inspect it or print it out for debugging:

```lyric
def main() {
    int x = 5
    str s = "hello"
    arr items = [1, 2, 3]

    print("type of x (which is 5):", type(x))
    print("type of s (which is \"hello\"):", type(s))
    print("type of items (which is [1,2,3]):", type(items))
}
```

```output
type of x (which is 5): int
type of s (which is "hello"): str
type of items (which is [1,2,3]): arr
```

### 3.7 None

`None` represents the absence of a value. Functions that do not explicitly
return a value return `None`.

```lyric
def do_nothing() {
    # no return statement
}

def main() {
    var result = do_nothing()
    print("Return value of a function with no return statement:", result)
}
```

```output
Return value of a function with no return statement: None
```

---

## 4. Operators

An **operator** is a symbol that performs an action on one or more values — things like `+` to add, `==` to compare, or `and` to combine conditions. When you combine values and operators together, you get an **expression**: something the program evaluates to produce a result, such as `age >= 18 and has_id`. Lyric supports arithmetic, comparison, logical, and membership operators, as well as rules for how non-boolean values behave in conditions.

### 4.1 Arithmetic Operators

Arithmetic operators are the basic math symbols you already know from school. They work on numbers and produce a new number as the result. One thing to note: division with `/` always returns a floating-point number, even if both sides are integers.

```lyric
def main() {
    int a = 10
    int b = 3

    print("10 + 3 =", a + b)   # addition
    print("10 - 3 =", a - b)   # subtraction
    print("10 * 3 =", a * b)   # multiplication
    print("10 / 3 =", a / b)   # division (always returns a float)
    print("10 % 3 =", a % b)   # modulus (remainder)
}
```

```output
10 + 3 = 13
10 - 3 = 7
10 * 3 = 30
10 / 3 = 3.3333333333333335
10 % 3 = 1
```

String concatenation uses `+`, and repetition uses `*`:

```lyric
def main() {
    str word = "hello"
    str twice = word + " " + word
    str dashes = "-" * 20
    print("Joining a string with itself:", twice)
    print("Repeating \"-\" 20 times:", dashes)
}
```

```output
Joining a string with itself: hello hello
Repeating "-" 20 times: --------------------
```

### 4.2 Comparison Operators

Comparison operators ask a yes-or-no question about two values — is one bigger, smaller, or equal to the other? The answer is always a boolean: `True` or `False`. You will use these constantly in `if` statements and loops to make your program choose what to do next.

```lyric
def main() {
    int x = 5
    int y = 10

    print("5 == 10 (are they equal?):", x == y)
    print("5 != 10 (are they not equal?):", x != y)
    print("5 < 10 (is 5 less than 10?):", x < y)
    print("5 <= 5 (is 5 less than or equal to 5?):", x <= 5)
    print("10 > 5 (is 10 greater than 5?):", y > x)
    print("10 >= 10 (is 10 greater than or equal to 10?):", y >= 10)
}
```

```output
5 == 10 (are they equal?): False
5 != 10 (are they not equal?): True
5 < 10 (is 5 less than 10?): True
5 <= 5 (is 5 less than or equal to 5?): True
10 > 5 (is 10 greater than 5?): True
10 >= 10 (is 10 greater than or equal to 10?): True
```

### 4.3 Logical Operators

Logical operators let you combine multiple conditions into one. Use `and` when every condition must be true, `or` when at least one must be true, and `not` to flip a condition from true to false or vice versa. These are the glue that lets you build more complex decisions out of simple comparisons.

```lyric
def main() {
    int age = 25
    god has_id = True

    if age >= 18 and has_id        # True — age is 25 AND has_id is True
        print("Entry permitted")
    end

    if age < 13 or age > 65        # False — 25 is neither under 13 nor over 65
        print("Discount applies")  # this line will not print
    end

    if not has_id                  # False — has_id is True, so not has_id is False
        print("ID required")       # this line will not print
    end
}
```

```output
Entry permitted
```

### 4.4 Membership Operator

Sometimes you need to know whether a specific item exists inside a collection or a piece of text before you do something with it. The `in` operator answers that question — it checks whether a value appears in an array, whether a key exists in a map, or whether a substring is found inside a string, and returns `True` or `False`.

```lyric
def main() {
    arr fruits = ["apple", "banana", "cherry"]

    if "banana" in fruits          # True — "banana" is in the array
        print("Found it!")
    end

    map person = {"name": "Alice", "age": 30}

    if "name" in person            # True — "name" is a key in the map
        print(person["name"])      # prints the value stored under "name"
    end

    str text = "Hello, World!"

    if "World" in text             # True — the substring "World" appears in text
        print("World is in there")
    end
}
```

```output
Found it!
Alice
World is in there
```

### 4.5 Truthiness

In Lyric, you can use any value — not just booleans — where a condition is expected, like in an `if` statement. When this happens, Lyric decides whether to treat the value as `True` or `False` based on a simple idea: empty or zero values are **falsy** (treated as `False`), and everything else is **truthy** (treated as `True`). The full rules are listed below.

| Value                  | Truthiness |
|------------------------|------------|
| `0`, `0.0`             | `False`    |
| Any other number       | `True`     |
| `""` (empty string)    | `False`    |
| Any non-empty string   | `True`     |
| `[]` (empty array)     | `False`    |
| Any non-empty array    | `True`     |
| `None`                 | `False`    |
| `True`                 | `True`     |
| `False`                | `False`    |

```lyric
def main() {
    if 5
        print("5 is truthy — any non-zero number counts as True")
    end

    if not 0
        print("0 is falsy — zero counts as False")
    end

    if "hello"
        print("\"hello\" is truthy — non-empty strings count as True")
    end

    if not ""
        print("\"\" is falsy — empty strings count as False")
    end
}
```

```output
5 is truthy — any non-zero number counts as True
0 is falsy — zero counts as False
"hello" is truthy — non-empty strings count as True
"" is falsy — empty strings count as False
```

### 4.6 Compound Assignment Operators

Writing `total = total + score` works, but you will find yourself doing it so often that it gets tedious. A **compound assignment operator** is a shorthand that combines an arithmetic operation with assignment in one step. Instead of `total = total + score` you can write `total += score` — it means the same thing but is shorter and easier to read. Lyric supports compound assignment for all five arithmetic operators:

| Operator | Longhand form    | What it does        |
|----------|------------------|---------------------|
| `+=`     | `x = x + value`  | Add and assign      |
| `-=`     | `x = x - value`  | Subtract and assign |
| `*=`     | `x = x * value`  | Multiply and assign |
| `/=`     | `x = x / value`  | Divide and assign   |
| `%=`     | `x = x % value`  | Modulo and assign   |

One thing to watch out for: `/=` always produces a floating-point result, even when both sides are integers. That means using `/=` on an `int` variable will cause a type mismatch error, because you would be trying to store a `flt` value in an `int` container. If you need to divide and reassign, declare the variable as `flt` or `var` instead.

```lyric
def main() {
    int score = 10

    score += 5
    print("After += 5:", score)

    score -= 3
    print("After -= 3:", score)

    score *= 2
    print("After *= 2:", score)

    score /= 4
    print("After /= 4:", score)
}
```

```output
After += 5: 15
After -= 3: 12
After *= 2: 24
Runtime error [line 13]: Type mismatch: cannot assign float to variable 'score' declared as int. Expected int, but got float. Use 'var score = ...' if you need dynamic typing.
```

These operators also work with strings — `+=` appends text to the end of a string, and `*=` repeats it:

```lyric
def main() {
    str greeting = "Hello"
    greeting += " World"
    print(greeting)

    str dash = "-"
    dash *= 10
    print(dash)
}
```

```output
Hello World
----------
```

---

## 5. Control Flow

So far every program we've written runs straight through from top to bottom, executing every line exactly once. **Control flow** is how you change that — making your program ask questions, skip over code it shouldn't run, or repeat actions until some condition is met. This is what lets a program actually make decisions and respond to different situations.

### 5.1 If / Elif / Else

An `if` statement is the most basic way to make a decision in your program. You give it a condition, and the code indented beneath it only runs when that condition is `True`. If you need to check multiple possibilities, add `elif` (short for "else if") branches — Lyric tests them one by one from top to bottom and runs the first one that matches. An optional `else` at the end catches everything that didn't match any earlier branch. The whole block is closed with `end`.

```lyric
def main() {
    int score = 91
    print("Score:", score)

    if score >= 90
        print("Grade: A — excellent work!")
    elif score >= 80
        print("Grade: B — good job")
    elif score >= 70
        print("Grade: C — passing")
    else
        print("Grade: F — needs improvement")
    end
}
```

```output
Score: 91
Grade: A — excellent work!
```

The condition does not need parentheses. You may add a colon (`:`) after the
condition — it is optional:

```lyric
def main() {
    int x = 10

    if x > 0:
        print(x, "is positive")
    else:
        print(x, "is zero or negative")
    end
}
```

```output
10 is positive
```

### 5.2 For Loops

A **for loop** lets you repeat a block of code once for every item in a sequence — whether that is a range of numbers, an array, or any other collection. Instead of writing the same operation over and over, you describe what to do with one item and the loop handles the rest. The loop variable (like `i` or `color` below) automatically takes on the next value each time through. The block is closed with `done`.

```lyric
def main() {
    # Count from 0 to 4
    print("Counting from 0 to 4:")
    for int i in range(5)
        print(" ", i)
    done

    # Iterate over an array
    arr colors = ["red", "green", "blue"]
    print("Available colors:")
    for str color in colors
        print(" -", color)
    done
}
```

```output
Counting from 0 to 4:
  0
  1
  2
  3
  4
Available colors:
 - red
 - green
 - blue
```

`range(n)` produces numbers from `0` up to (but not including) `n`.
You can also call `range(start, stop)` or `range(start, stop, step)`:

```lyric
def main() {
    print("range(1, 6) — from 1 up to (but not including) 6:")
    for int i in range(1, 6)
        print(" ", i)
    done

    print("range(0, 10, 2) — even numbers from 0 to 8:")
    for int i in range(0, 10, 2)
        print(" ", i)
    done
}
```

```output
range(1, 6) — from 1 up to (but not including) 6:
  1
  2
  3
  4
  5
range(0, 10, 2) — even numbers from 0 to 8:
  0
  2
  4
  6
  8
```

### 5.3 Given Loops (While)

A `for` loop is great when you know exactly what items to loop over, but sometimes you need to keep repeating until a condition changes — and you don't know in advance how many times that will be. That is what `given` is for. It checks a condition before each pass: if the condition is `True`, the body runs; if it is `False`, the loop stops. Because there is no built-in counter moving forward for you, you must make sure something inside the loop eventually makes the condition `False` — otherwise it will run forever.

```lyric
def main() {
    int count = 0

    print("Counting up while count is less than 5:")
    given count < 5:
        print(" count =", count)
        count = count + 1
    done
    print("Loop finished. Final count:", count)
}
```

```output
Counting up while count is less than 5:
 count = 0
 count = 1
 count = 2
 count = 3
 count = 4
Loop finished. Final count: 5
```

### 5.4 Break and Continue

Use `break` to exit a loop early and `continue` to skip to the next iteration:

```lyric
def main() {
    # Find the first even number greater than 5
    print("Searching for the first even number greater than 5:")
    for int i in range(20)
        if i <= 5
            continue   # skip anything 5 or under
        end
        if i % 2 == 0
            print("Found it:", i)
            break      # stop as soon as we find one
        end
    done
}
```

```output
Searching for the first even number greater than 5:
Found it: 6
```

> **Note:** The modulo operator `%` gives the remainder of integer division.

---

## 6. Functions

A **function** is a named, reusable block of code that you define once and can run as many times as you need. Think of it like a recipe — you write the steps down under a name, and then anywhere in your program you can say "go run that recipe" just by using its name. Functions can accept **inputs** (called parameters) that let you pass different values in each time you call them, and they can **return** a result back to the code that called them. Breaking your program into functions keeps it organized, avoids repeating yourself, and makes each piece easier to read and test on its own.

### 6.1 Defining Functions

To create a function you use the `def` keyword, give it a name, list any parameters it accepts inside parentheses, and then write the body between curly braces `{ }`. The name is how you will call the function later, the parameters are the inputs it expects, and the body is the code that runs each time you call it. If your function produces a result, use `return` to send that value back to the caller. If there is no `return`, the function simply does its work and returns `None`.

```lyric
def greet(name) {
    print("Hello,", name + "!")
}

def add(a, b) {
    return a + b
}

def main() {
    greet("Alice")
    int result = add(3, 4)
    print("3 + 4 =", result)
}
```

```output
Hello, Alice!
3 + 4 = 7
```

### 6.2 Typed Parameters

In section 3 you learned that every variable in Lyric has a type. The same idea applies to function parameters — you can place a type keyword like `int` or `str` before a parameter name to declare what kind of value it expects. This serves two purposes: it makes your code self-documenting so anyone reading the function signature immediately knows what to pass in, and it lets the interpreter catch mistakes at runtime if someone accidentally passes the wrong type. You are not required to type every parameter, but doing so is good practice, especially as your programs grow.

```lyric
def square(int n) {
    return n * n
}

def greet_user(str name, int times) {
    for int i in range(times)
        print("Hello,", name)
    done
}

def main() {
    print("5 squared =", square(5))
    print("Greeting Bob 3 times:")
    greet_user("Bob", 3)
}
```

```output
5 squared = 25
Greeting Bob 3 times:
Hello, Bob
Hello, Bob
Hello, Bob
```

### 6.3 Typed Return Values

Just as you can type a function's parameters, you can also declare the type of value a function returns. Instead of writing `def` before the function name, you replace it with the return type — for example `int get_max(...)` tells the reader (and the interpreter) that this function will always hand back an integer. This makes your code easier to reason about: when you see a typed return, you know exactly what kind of value to expect without having to read the function body. If the function accidentally returns the wrong type, the interpreter will catch it.

```lyric
int get_max(int a, int b) {
    if a > b
        return a
    else
        return b
    end
}

str make_label(str key, str value) {
    return key + ": " + value
}

def main() {
    int m = get_max(8, 13)
    print("The larger of 8 and 13 is:", m)
    print(make_label("Name", "Alice"))
}
```

```output
The larger of 8 and 13 is: 13
Name: Alice
```

### 6.4 The `main()` Function

`main()` is Lyric's program entry point — it is where execution always begins. At the top level of a Lyric file (outside any function), only variable declarations, function definitions, and class definitions are allowed. Statements like `print()` must live inside a function. When you run a Lyric program, the interpreter processes all top-level declarations first and then calls `main()` automatically.

```lyric
int GLOBAL_MAX = 100   # top-level variable declaration — allowed

def main() {
    print("GLOBAL_MAX is:", GLOBAL_MAX)
}
```

```output
GLOBAL_MAX is: 100
```

### 6.5 Recursion

A function is allowed to call itself — this is called **recursion**. It's useful when a problem can be broken down into a smaller version of the same problem. The key is always having a **base case**: a condition that stops the function from calling itself again, otherwise it would repeat forever. In the example below, `factorial` computes the product of all whole numbers from 1 up to `n` — the base case is when `n` reaches 1, at which point it stops and returns.

Functions can call themselves:

```lyric
int factorial(int n) {
    if n <= 1
        return 1
    end
    return n * factorial(n - 1)
}

def main() {
    print("5! (5 factorial) =", factorial(5))
    print("10! (10 factorial) =", factorial(10))
}
```

```output
5! (5 factorial) = 120
10! (10 factorial) = 3628800
```

---

## 7. Arrays

So far every variable we've used has held exactly one value — one number, one string, one boolean. But what if you need to work with a whole list of things? A shopping list, a set of test scores, a collection of names? That's what an **array** is for.

An array is an ordered list of values stored together under a single variable name. You can put as many items in it as you need, access them one at a time or all at once, add new items, remove old ones, and loop through the whole list with a `given` loop. In Lyric, arrays use the type keyword `arr` and are written with square brackets: `[1, 2, 3]`. Each item in the list is called an **element**, and each element has a numbered position called an **index**, starting at `0`.

### 7.1 Creating Arrays

```lyric
def main() {
    arr numbers = [1, 2, 3, 4, 5]
    arr words   = ["hello", "world", "lyric"]
    arr mixed   = [1, "two", 3.0, True]
    arr empty   = []

    print("numbers:", numbers)
    print("words:", words)
    print("mixed types:", mixed)
    print("empty array:", empty)
}
```

```output
numbers: [1, 2, 3, 4, 5]
words: ['hello', 'world', 'lyric']
mixed types: [1, 'two', 3.0, True]
empty array: []
```

### 7.2 Indexing and Slicing

You access a single element from an array by writing its index in square brackets: `items[0]` gives you the first element, `items[1]` the second, and so on. Remember indexes start at `0`, so a five-element array has indexes `0` through `4`.

**Slicing** lets you pull out a chunk of the array in one go. Instead of a single number you write a range inside the brackets: `items[1:3]` means "give me the elements starting at index 1, up to but not including index 3." You can leave either side blank — `items[:3]` means "from the start up to index 3", and `items[2:]` means "from index 2 to the end." Adding a second colon lets you set a step: `items[::2]` means "every other element."

```lyric
def main() {
    arr items = [10, 20, 30, 40, 50]

    print("First element (index 0):", items[0])
    print("Second element (index 1):", items[1])

    items[0] = 99
    print("After setting index 0 to 99:", items[0])

    # Slicing: items[start:stop]
    print("Slice [1:3] — elements at index 1 and 2:", items[1:3])
    print("Slice [:3] — first three elements:", items[:3])
    print("Slice [2:] — from index 2 to the end:", items[2:])
    print("Slice [::2] — every other element:", items[::2])
}
```

```output
First element (index 0): 10
Second element (index 1): 20
After setting index 0 to 99: 99
Slice [1:3] — elements at index 1 and 2: [20, 30]
Slice [:3] — first three elements: [99, 20, 30]
Slice [2:] — from index 2 to the end: [30, 40, 50]
Slice [::2] — every other element: [99, 30, 50]
```

### 7.3 Iterating

Working with an array usually means doing something with each element inside it. A `for` loop is the natural way to do that — it walks through the array from the first element to the last, assigning each one to the loop variable so you can use it in the body. Notice that the loop variable (`score` below) must be declared before the loop, just like any other variable. In this example we use the loop to add up every score into a running total, then call `.len()` to find out how many elements the array contains.

```lyric
def main() {
    arr scores = [85, 92, 78, 95, 88]
    int total = 0

    for int score in scores
        total = total + score
    done

    print("Total:", total)
    print("Count:", scores.len())
}
```

```output
Total: 438
Count: 5
```

### 7.4 Array Methods

Arrays come with a set of built-in **methods** — functions that belong to the array itself. You call a method by writing a dot after the array's name followed by the method name, for example `nums.append(7)`. Some methods change the array in place (like `.sort()` and `.reverse()`), some return a value without changing anything (like `.len()` and `.sum()`), and some do both (like `.pop()`, which removes the last element and gives it back to you). The table below lists the most useful ones, and the code example that follows shows each one in action.

| Method | What it does |
|---|---|
| `.len()` | Returns the number of elements in the array |
| `.append(x)` | Adds `x` to the end of the array |
| `.pop()` | Removes and returns the last element |
| `.remove(x)` | Removes the first occurrence of value `x` |
| `.sort()` | Sorts the array in place, smallest to largest |
| `.reverse()` | Reverses the order of elements in place |
| `.count(x)` | Returns how many times value `x` appears |
| `.index(x)` | Returns the index of the first occurrence of `x` |
| `.insert(i, x)` | Inserts value `x` at position `i` |
| `.min()` | Returns the smallest value |
| `.max()` | Returns the largest value |
| `.sum()` | Returns the sum of all values |
| `.copy()` | Returns a new independent copy of the array |
| `.clear()` | Removes all elements, leaving an empty array |

```lyric
def main() {
    arr nums = [3, 1, 4, 1, 5, 9, 2, 6]
    print("Starting array:", nums)
    print("Length:", nums.len())

    nums.append(7)
    print("After append(7):", nums)

    int last = nums.pop()
    print("Popped last element:", last)
    print("Array after pop:", nums)

    nums.remove(1)
    print("After removing first 1:", nums)

    nums.sort()
    print("After sort:", nums)

    nums.reverse()
    print("After reverse:", nums)

    print("Count of value 1 in array:", nums.count(1))
    print("Index of value 5:", nums.index(5))

    nums.insert(0, 0)
    print("After insert(0, 0) — added 0 at the front:", nums)

    print("Minimum value:", nums.min())
    print("Maximum value:", nums.max())
    print("Sum of all values:", nums.sum())

    arr copy = nums.copy()
    copy.clear()
    print("Cleared copy — length is now:", copy.len())
}
```

### 7.5 Nested Arrays

An array can contain other arrays as its elements — this is called a **nested array**. It's useful any time your data is naturally two-dimensional: a grid, a game board, a table of rows and columns, or a list of records where each record is itself a list of values. You access elements by chaining two indexes together — the first selects the inner array (the row), and the second selects the element within it (the column).

```lyric
def main() {
    arr matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    print("Full matrix:", matrix)
    print("Row at index 1:", matrix[1])
    print("Element at row 1, column 2:", matrix[1][2])

    print("All values one by one:")
    for arr row in matrix
        for int val in row
            print(" ", val)
        done
    done
}
```

```output
Full matrix: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
Row at index 1: [4, 5, 6]
Element at row 1, column 2: 6
All values one by one:
  1
  2
  3
  4
  5
  6
  7
  8
  9
```

---

## 8. Tuples

A **tuple** is an ordered sequence of values, just like an array, but with one
key difference: a tuple is **immutable** — once you create it, its contents
cannot change. You cannot add, remove, or replace elements.

This makes tuples useful when you want a sequence to stay fixed — a set of
coordinates, a configuration pair, or any group of values that must not be
modified. Tuples are also required when passing sequences to certain Python APIs
that expect a native Python `tuple` rather than a list (for example,
`HTTPServer(("0.0.0.0", 8080), handler)`).

In Lyric, tuples use the type keyword `tup` and are written with parentheses:
`(10, 20, 30)`.

### 8.1 Creating Tuples

```lyric
def main() {
    tup coords  = (10, 20)
    tup mixed   = (1, "hello", 3.14)
    tup empty   = ()
    tup single  = (42,)    # trailing comma required for a one-element tuple

    print("coordinates:", coords)
    print("mixed types:", mixed)
    print("empty tuple:", empty)
    print("single element:", single)
}
```

```output
coordinates: (10, 20)
mixed types: (1, 'hello', 3.14)
empty tuple: ()
single element: (42,)
```

**Key rules:**
- Written with parentheses `( )`, not square brackets.
- A single-element tuple must end with a trailing comma: `(42,)`.
  Without the comma, `(42)` is just the number `42` in parentheses, not a tuple.
- Values are separated by commas.

### 8.2 Indexing and Iteration

Access elements by index just like an array, starting at `0`:

```lyric
def main() {
    tup t = (10, 11, 12)

    print("First element:", t[0])
    print("Third element:", t[2])

    print("Iterating over the tuple:")
    for var item in t:
        print(" ", item)
    done
}
```

```output
First element: 10
Third element: 12
Iterating over the tuple:
  10
  11
  12
```

The `in` operator also works for membership tests:

```lyric
def main() {
    tup nums = (5, 10, 15, 20)

    if 10 in nums
        print("10 is in the tuple")
    end

    if 7 in nums
        print("7 is in the tuple")
    else
        print("7 is not in the tuple")
    end
}
```

```output
10 is in the tuple
7 is not in the tuple
```

### 8.3 Tuple Methods

Tuples have a set of **read-only** methods. There are no mutation methods —
you cannot sort, append to, or remove from a tuple.

| Method | What it does |
|---|---|
| `.len()` | Returns the number of elements |
| `.count(x)` | Returns how many times value `x` appears |
| `.index(x)` | Returns the index of the first occurrence of `x` |
| `.min()` | Returns the smallest value |
| `.max()` | Returns the largest value |
| `.sum()` | Returns the sum of all numeric values |

```lyric
def main() {
    tup scores = (85, 92, 78, 92, 100)

    print("Length:", scores.len())
    print("Min:", scores.min())
    print("Max:", scores.max())
    print("Sum:", scores.sum())
    print("Count of 92:", scores.count(92))
    print("Index of 78:", scores.index(78))
}
```

```output
Length: 5
Min: 78
Max: 100
Sum: 447
Count of 92: 2
Index of 78: 2
```

### 8.4 Converting Between arr and tup

Use the built-in `tup()` function to convert an `arr` to a `tup`:

```lyric
def main() {
    arr numbers = [1, 2, 3, 4, 5]
    tup fixed = tup(numbers)

    print("Original array:", numbers)
    print("Converted tuple:", fixed)
    print("Length of tuple:", fixed.len())
}
```

```output
Original array: [1, 2, 3, 4, 5]
Converted tuple: (1, 2, 3, 4, 5)
Length of tuple: 5
```

### 8.5 Immutability

Tuples cannot be modified after creation. Attempting to assign to an index
raises a `TypeError`:

```lyric
def main() {
    tup t = (1, 2, 3)
    t[0] = 99    # TypeError — tuples are immutable
}
```

There are also no methods like `append`, `remove`, or `sort` on a tuple —
only the read-only methods listed above exist.

---

## 9. Maps

A **map** (`map`) stores key-value pairs. If you know Python, a Lyric map is
very similar to a Python **dictionary** (`dict`).

Think of it like a labeled container:
- the **key** is the label (for example `"name"` or `"age"`)
- the **value** is the data stored under that label (for example `"Alice"` or `30`)

In Lyric maps, keys must be strings, and values can be of any type.

### 9.1 Creating Maps

This example shows how to create maps using `{}` and how to read values by key
with `map["key"]` syntax.

```lyric
def main() {
    map person = {"name": "Alice", "age": 30, "city": "Boston"}
    map scores = {"math": 95, "english": 88}
    map config = {"debug": True, "version": "0.8.4"}
    map empty  = {}

    print("person's name:", person["name"])
    print("person's city:", person["city"])
    print("math score:", scores["math"])
    print("debug mode:", config["debug"])
}
```

```output
person's name: Alice
person's city: Boston
math score: 95
debug mode: True
```

### 9.2 Adding and Modifying Entries

This example shows that assigning to a key does two different things depending
on whether the key already exists:
- if the key is new, it is added
- if the key already exists, its value is replaced

```lyric
def main() {
    map info = {"language": "Lyric"}
    print("Before changes:", info)

    info["version"] = "0.8.4"      # add a new key
    info["language"] = "Lyric 2"   # update existing key

    print("After adding 'version' and updating 'language':", info)
}
```

```output
Before changes: {'language': 'Lyric'}
After adding 'version' and updating 'language': {'language': 'Lyric 2', 'version': '0.8.4'}
```

### 9.3 Iterating

This section shows two ways to loop through map data:
- loop over the map directly to get keys
- use `.items()` to get key-value pairs together

Iterating over a map directly yields its **keys**:

```lyric
def main() {
    map capitals = {"France": "Paris", "Japan": "Tokyo", "Brazil": "Brasília"}
    for str country in capitals
        print(country, "->", capitals[country])
    done
}
```

```output
France -> Paris
Japan -> Tokyo
Brazil -> Brasília
```

Use `.items()` to get key-value pairs as an array of two-element arrays:

```lyric
def main() {
    map prices = {"apple": 1.20, "banana": 0.50, "cherry": 2.99}

    for arr pair in prices.items()
        print(pair[0], "costs", pair[1])
    done
}
```

### 9.4 Map Methods

This example demonstrates a common workflow when working with maps:
1. Inspect what is inside a map (`keys()` and `values()`).
2. Safely read a value that might not exist (`get()`).
3. Remove one entry (`pop()`).
4. Merge in new entries (`update()`).
5. Duplicate a map (`copy()`) and then empty that duplicate (`clear()`).

In other words, it shows how to **look at**, **read**, **change**, **combine**, and **reset** map data.

```lyric
def main() {
    map data = {"a": 1, "b": 2, "c": 3}

    arr keys = data.keys()
    print("Keys:", keys)

    arr vals = data.values()
    print("Values:", vals)

    var x = data.get("z", 0)
    print("get(\"z\", 0) — key doesn't exist, so default is returned:", x)

    int removed = data.pop("b")
    print("Removed key \"b\", its value was:", removed)
    print("Map after pop:", data)

    map extra = {"d": 4, "e": 5}
    data.update(extra)
    print("After merging {d:4, e:5}, total keys:", data.len())

    map copy = data.copy()
    copy.clear()
    print("After clearing the copy, its length is:", copy.len())
}
```

Method-by-method explanation:

- `data.keys()`: Returns an array of all keys in the map.  
  Here it returns `["a", "b", "c"]`. Use this when you need to loop over or inspect key names.

- `data.values()`: Returns an array of all values in the map.  
  Here it returns `[1, 2, 3]`. Use this when you care about stored data but not key names.

- `data.get("z", 0)`: Tries to read key `"z"`.  
  If `"z"` exists, its value is returned. If it does not exist, the default value (`0`) is returned instead.  
  This is safer than `data["z"]` when a key might be missing.

- `data.pop("b")`: Removes key `"b"` from the map and returns the removed value.  
  In this example, it returns `2`, and `data` becomes `{"a": 1, "c": 3}`.

- `data.update(extra)`: Adds entries from `extra` into `data`.  
  New keys are inserted. If a key already exists, its value is overwritten by the value from `extra`.

- `data.len()`: Returns how many key-value pairs are currently in the map.  
  After update, the map has 4 keys in this example.

- `data.copy()`: Creates a new map with the same key-value pairs.  
  This lets you modify the copy without changing the original map.

- `copy.clear()`: Removes all entries from `copy`, leaving it empty (`{}`).

- `copy.len()`: Confirms the copy is empty by returning `0`.

```output
Keys: ['a', 'b', 'c']
Values: [1, 2, 3]
get("z", 0) — key doesn't exist, so default is returned: 0
Removed key "b", its value was: 2
Map after pop: {'a': 1, 'c': 3}
After merging {d:4, e:5}, total keys: 4
After clearing the copy, its length is: 0
```

### 9.5 Nested Maps

So far you've used maps with simple values like numbers or strings. A **nested map**
means a map that stores another map (or an array of maps) inside it. This is useful
for representing structured data, like an app configuration, a user profile, or API data.
You access each level one step at a time using brackets.

Maps can contain arrays, and arrays can contain maps:

```lyric
def main() {
    map app = {
        "name": "MyApp",
        "users": [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob",   "role": "user"}
        ],
        "settings": {
            "theme": "dark",
            "language": "en"
        }
    }

    print(app["name"])                      # MyApp
    print(app["users"][0]["name"])          # Alice
    print(app["settings"]["theme"])         # dark
}
```

```output
MyApp
Alice
dark
```

---

## 10. Strings

A **string** is text data, such as a name, a message, or a sentence. In programs, strings are used for anything human-readable: user input, printed output, file content, and labels. Even when something looks like a number (for example `"123"`), it is still text if it is inside quotes, so Lyric treats it as a string.

### 10.1 String Literals

A **string literal** is text you write directly in your code by putting it inside quotes. In Lyric, you can use either double quotes (`"..."`) or single quotes (`'...'`). Both create the same `str` value, so pick one style and stay consistent to keep your code easy to read.

```lyric
def main() {
    str a = "double quotes"
    str b = 'single quotes'
    print("Using double quotes:", a)
    print("Using single quotes:", b)
    print("Both styles produce a string — no difference in the result")
}
```

```output
Using double quotes: double quotes
Using single quotes: single quotes
Both styles produce a string — no difference in the result
```

### 10.2 Escape Sequences

Escape sequences are special codes you place inside a string to represent characters that are hard to type directly or would otherwise be interpreted as part of the string syntax. They start with a backslash (`\`), which tells Lyric: "the next character has a special meaning."

Beginners often get tripped up here because some characters have two roles. For example, `"` can be either:
- the character that ends a string, or
- a quote mark you want to display as text.

Escape sequences solve this ambiguity. `\"` means "put a quote character in the string", not "end the string." The same idea applies to new lines (`\n`) and tabs (`\t`): they are instructions for formatting text output.

Think of it this way: escape sequences let you control *how text is stored and printed* without breaking the string itself.

| Sequence | Meaning            |
|----------|--------------------|
| `\n`     | Newline            |
| `\t`     | Tab                |
| `\r`     | Carriage return    |
| `\\`     | Literal backslash  |
| `\"`     | Literal `"`        |
| `\'`     | Literal `'`        |

```lyric
def main() {
    print("Line one\nLine two\nLine three")
    print("Column1\tColumn2\tColumn3")
    print("He said \"hello\"")
}
```

```output
Line one
Line two
Line three
Column1 Column2 Column3
He said "hello"
```

### 10.3 String Operations

Operators can behave differently depending on the type of data they are used with. This is important for beginners because the symbol may look the same, but the result can change based on the values:
- `int + int` performs numeric addition (`2 + 3` becomes `5`)
- `str + str` performs concatenation (`"Ly" + "ric"` becomes `"Lyric"`)

In this section, you will use `+` and `*` with strings. With strings, `+` joins text together and `*` repeats text a number of times.

```lyric
def main() {
    str first = "Hello"
    str second = "World"

    # Concatenation
    str full = first + ", " + second + "!"
    print("Concatenated:", full)

    # Repetition
    str border = "=" * 30
    print("\"=\" repeated 30 times:", border)

    str text = "Lyric"
    print("text =", text)
}
```

```output
Concatenated: Hello, World!
"=" repeated 30 times: ==============================
text = Lyric
```

### 10.4 Checking Membership in Strings

Sometimes you need to check whether a word or piece of text appears inside a larger string. The `in` operator answers that question and returns `True` or `False`.

In this example, Lyric checks whether `"quick"` and `"slow"` appear in the sentence. The first check succeeds, and the second check fails, so the `else` branch runs.

```lyric
def main() {
    str sentence = "The quick brown fox"

    if "quick" in sentence
        print("Found 'quick'")
    end

    if "slow" in sentence
        print("Found 'slow'")
    else
        print("'slow' not found")
    end
}
```

```output
Found 'quick'
'slow' not found
```

---

## 11. Classes and Inheritance

A **class** is a way to define your own custom data type. It groups related data (called fields) and related behavior (called methods) in one place.

Why this matters for beginners:
- Without classes, related values and logic are scattered across many variables and functions.
- With classes, you can model real things (like a rectangle, user, or product) as one unit.
- This makes code easier to read, reuse, and maintain as programs grow.

### 11.1 Defining a Class

In this first example, `Rectangle` stores width and height, then provides methods to calculate area and perimeter. You create an instance, set its fields, and call its method to print a summary. Class definitions end with `+++`.

```lyric
class Rectangle:
    width  = 0
    height = 0

    def area() {
        return self.width * self.height
    }

    def perimeter() {
        return 2 * (self.width + self.height)
    }

    def describe() {
        print("Rectangle", self.width, "x", self.height)
        print("  Area:", self.area())
        print("  Perimeter:", self.perimeter())
    }
+++

def main() {
    obj r = Rectangle()
    r.width  = 5
    r.height = 3
    r.describe()
}
```

```output
Rectangle 5 x 3
  Area: 15
  Perimeter: 16
```

**Key rules:**
- Fields are declared at the class body level with default values.
- Methods are `def` functions inside the class.
- Inside a method, access instance fields with `self.fieldname`.
- Call other methods with `self.method()`.
- Class bodies end with `+++` on its own line.

### 11.2 Constructors

A **constructor** is a special method that runs automatically when you create a new object from a class.

Why constructors are useful:
- They set up the object with valid starting values right away.
- They reduce repeated setup code after each object creation.
- They make object creation clearer, because required data is provided up front.

In Lyric, if you define a method with the **same name as the class**, it acts as the constructor and is called automatically when you create an instance:

```lyric
class Point:
    x = 0
    y = 0

    def Point(px, py) {
        self.x = px
        self.y = py
    }

    def to_string() {
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    }
+++

def main() {
    obj p = Point(3, 7)
    print(p.to_string())   # (3, 7)
    print(p.x)             # 3
}
```

```output
(3, 7)
3
```

### 11.3 Inheritance

**Inheritance** lets one class reuse another class's fields and methods.
In Lyric, a child class uses `based on ParentClass` to inherit behavior from a parent class.

Why inheritance is useful:
- You avoid rewriting common code in multiple classes.
- You keep shared behavior in one place, making updates easier.
- Child classes can still customize behavior by overriding specific methods.

In this example, `Dog` and `Cat` both inherit from `Animal`, so they share `describe()` while each class defines its own `speak()` behavior.

```lyric
class Animal:
    name = "Unknown"

    def speak() {
        print(self.name, "makes a sound")
    }

    def describe() {
        print("Animal:", self.name)
    }
+++

class Dog based on Animal:
    breed = "Mixed"

    def speak() {
        print(self.name, "barks!")
    }

    def fetch() {
        print(self.name, "fetches the ball")
    }
+++

class Cat based on Animal:
    indoor = True

    def speak() {
        print(self.name, "meows")
    }
+++

def main() {
    obj dog = Dog()
    dog.name  = "Rex"
    dog.breed = "Labrador"

    obj cat = Cat()
    cat.name = "Whiskers"

    dog.speak()    # Rex barks!
    dog.fetch()    # Rex fetches the ball
    dog.describe() # Animal: Rex  (inherited from Animal)

    cat.speak()    # Whiskers meows
    cat.describe() # Animal: Whiskers (inherited)
}
```

```output
Rex barks!
Rex fetches the ball
Animal: Rex
Whiskers meows
Animal: Whiskers
```

Child classes **override** parent methods by redefining them (as `Dog.speak()` does above).

### 11.4 Type Checking

When you have objects that share a common parent class, you sometimes need to find out exactly what type an object is at runtime. Lyric gives you two tools for this. `type()` returns the object's own class name as a string — useful for debugging or printing. `isinstance()` asks a broader question: "is this object an instance of a given class **or any class that inherits from it**?" This is especially handy when you accept a parent type (like `Animal`) but need to check whether the actual object is a specific child (like `Dog`).

```lyric
def main() {
    obj dog = Dog()
    dog.name = "Max"

    print("type(dog):", type(dog))
    print("isinstance(dog, Dog):", isinstance(dog, Dog))
    print("isinstance(dog, Animal) — Dog inherits from Animal:", isinstance(dog, Animal))
    print("isinstance(dog, Cat):", isinstance(dog, Cat))
}
```

```output
type(dog): Dog
isinstance(dog, Dog): True
isinstance(dog, Animal) — Dog inherits from Animal: True
isinstance(dog, Cat): False
```

### 11.5 Access Modifiers

By default, every method and attribute on a class is accessible from anywhere in your program. That is fine for small scripts, but as your classes grow you often want to hide internal details so that outside code cannot accidentally break them. **Access modifiers** let you control who can see and use each part of a class. Lyric supports three levels: `public` means anyone can access it (this is the default if you leave the keyword off), `private` means only the class itself can use it — code outside the class will get an error if it tries, and `protected` means the class and any child classes that inherit from it can use it, but outside code cannot.

This first example shows access modifiers on **methods**. The `deposit` and `get_balance` methods are `public`, so outside code can call them. The `apply_fee` method is `private`, so only other methods inside `BankAccount` can call it — if `main` tried to call `account.apply_fee()` directly, Lyric would raise an error.

```lyric
class BankAccount:
    balance = 0.0

    public def deposit(flt amount) {
        self.balance += amount
    }

    public def get_balance() {
        return self.balance
    }

    private def apply_fee() {
        self.balance -= 5.0
    }
+++

def main() {
    obj account = BankAccount()
    account.deposit(100.0)
    print(account.get_balance())   # 100.0
}
```

```output
100.0
```

Access modifiers also work on **class attributes**. In this example, `name` is `public` so it can be read and changed from anywhere, but `password` is `private` so only the `User` class itself can access it. The `public` method `check_password` provides a safe way to verify the password without exposing it directly.

```lyric
class User:
    public str name = ""
    private str password = ""

    def User(str n, str p) {
        self.name = n
        self.password = p
    }

    public def check_password(str attempt) {
        return attempt == self.password
    }
+++

def main() {
    obj user = User("Alice", "secret123")

    print("Name:", user.name)                          # works — name is public
    print("Password correct:", user.check_password("secret123"))  # works — method is public
    # print(user.password)                             # would fail — password is private
}
```

```output
Name: Alice
Password correct: True
```

---

## 12. Exception Handling

Sometimes your program will run into a problem it cannot handle normally — dividing by zero, accessing an array index that does not exist, or trying to open a file that is missing. When this happens, Lyric raises an **exception**: the normal flow of the program stops immediately and, if you have not prepared for it, the program crashes with an error message. **Exception handling** is how you prepare for these situations. You wrap the risky code in a `try` block, and if anything goes wrong inside it, execution jumps straight to the `catch` block where you can respond to the error — log a message, use a default value, or try a different approach. An optional `finally` block runs afterward no matter what, whether the code succeeded or failed. In Lyric, the whole structure is closed with `fade` instead of `end`.

### 12.1 Basic try / catch

The simplest form of exception handling is `try` / `catch`. You put the code that might fail inside `try`, and the code that should run if something goes wrong inside `catch`. If no error occurs, the `catch` block is skipped entirely. If an error does occur, Lyric stops executing the `try` block at the point of failure — any lines after the error are never reached — and jumps directly into `catch`.

```lyric
def main() {
    try:
        arr items = [1, 2, 3]
        print("Attempting to access index 10 of a 3-element array...")
        var x = items[10]
        print("This line will never be reached")
    catch:
        print("Error caught! The array only has indexes 0, 1, and 2")
    fade
}
```

```output
Attempting to access index 10 of a 3-element array...
Error caught! The array only has indexes 0, 1, and 2
```

### 12.2 Try / Catch / Finally

Sometimes you need a piece of code to run no matter what — whether the `try` block succeeded or the `catch` block handled an error. That is what `finally` is for. A common real-world example is closing a file: you want to make sure the file gets closed whether reading it worked or not, because leaving files open can cause problems. The `finally` block always executes after `try` (and `catch` if it ran), so it is the perfect place for cleanup work like this.

```lyric
def read_config(str path) {
    dsk f = disk(path)
    try:
        str content = f.read()
        print("Config loaded:", content)
    catch:
        print("Could not read config file:", path)
    finally:
        f.close()
        print("File handle closed")
    fade
}

def main() {
    read_config("settings.txt")
}
```

```output
Could not read config file: settings.txt
File handle closed
```

### 12.3 Raising Exceptions

So far you have seen exceptions that Lyric raises automatically — like accessing an index that does not exist. But sometimes your own code needs to signal that something is wrong. The `raise` keyword lets you do exactly that: you choose an exception type that describes the problem and Lyric immediately stops the current function and looks for a `catch` block to handle it, just as if the error had come from the language itself. This is useful for enforcing rules in your program — for example, rejecting an input that is out of range before it can cause a harder-to-find bug later.

```lyric
def validate_age(int age) {
    if age < 0
        raise ValueErrorLyric
    end
    if age > 150
        raise ValueErrorLyric
    end
    return age
}

def main() {
    try:
        validate_age(-5)
    catch:
        print("Invalid age provided")
    fade

    try:
        validate_age(25)
        print("Age is valid")
    catch:
        print("This won't run")
    fade
}
```

```output
Invalid age provided
Age is valid
```

Lyric provides the following built-in exception types you can use with `raise`:

| Exception | When to use it |
|---|---|
| `ValueError` | A value is the right type but outside the acceptable range or otherwise invalid — like a negative age or an empty string where one is required |
| `TypeError` | An operation received the wrong type — like passing a string to a function that expects an integer |
| `IndexError` | An array or tuple index is out of bounds — like accessing index 10 in a 3-element array |
| `KeyError` | A map lookup used a key that does not exist |
| `ZeroDivisionError` | A division or modulo operation has zero as its divisor |
| `AttributeError` | An object does not have the attribute or method you tried to access |
| `NameError` | A variable name was used before it was declared or assigned |
| `RuntimeError` | A general-purpose error for anything that does not fit the categories above |
| `Error` | A generic catch-all exception |

### 12.4 Exceptions in Classes

Exception handling works exactly the same way inside a class method as it does in a regular function — you use `try`, `catch`, and `fade` just like before. This is useful because a class often manages a resource or enforces its own rules, and the method itself is the best place to decide how to handle errors. In the example below, a `Wallet` class uses `raise` to reject invalid deposits and wraps withdrawal logic in a `try` / `catch` so it can print a helpful message instead of crashing when something goes wrong.

```lyric
class Wallet:
    private flt balance = 0.0

    public def deposit(flt amount) {
        if amount <= 0
            raise ValueErrorLyric
        end
        self.balance += amount
        print("Deposited", amount, "— balance is now", self.balance)
    }

    public def withdraw(flt amount) {
        if amount > self.balance
            raise RuntimeErrorLyric
        end
        self.balance -= amount
        print("Withdrew", amount, "— balance is now", self.balance)
    }
+++

def main() {
    obj w = Wallet()
    w.deposit(50.0)

    try:
        w.deposit(-10.0)
    catch:
        print("Deposit rejected: amount must be positive")
    fade

    try:
        w.withdraw(100.0)
    catch:
        print("Withdrawal rejected: not enough funds")
    fade

    w.withdraw(20.0)
}
```

```output
Deposited 50.0 — balance is now 50.0
Deposit rejected: amount must be positive
Withdrawal rejected: not enough funds
Withdrew 20.0 — balance is now 30.0
```

---

## 13. Regular Expressions

A **regular expression** (often shortened to **regex**) is a special string that describes a pattern of text you want to find. Instead of searching for one exact word, a regex lets you describe a shape — "one or more digits", "a word followed by a space and another word", "anything that looks like an email address" — and the language will find every piece of text that matches. Regular expressions are widely used across almost all programming languages for tasks like validating user input, searching through text, and replacing patterns.

If you have never worked with regular expressions before, they can look intimidating at first. The good news is that you only need a handful of building blocks to handle most common tasks, and the syntax is the same across nearly every language. For a hands-on, beginner-friendly guide to learning regex from scratch, [RegexOne](https://regexone.com/) is one of the best resources available — it teaches you through interactive exercises that let you practice each concept as you learn it.

Lyric has built-in support for regular expressions through the `rex` type and the `regex()` function.

### 13.1 Creating a Pattern

```lyric
rex pattern = regex("/hello/")
rex numbers = regex("/\d+/")
rex email   = regex("/[\w.]+@[\w.]+/")
```

Pass optional flags as a second argument:

| Flag | Meaning                       |
|------|-------------------------------|
| `i`  | Case-insensitive matching     |
| `m`  | Multiline mode                |
| `s`  | Dot matches newlines          |

```lyric
rex ci_pattern = regex("/hello/", "i")
```

### 13.2 Matching and Searching

Once you have a pattern, you need a way to test it against some text. Lyric gives you two methods for this: `search()` scans through the entire string and returns the first match it finds anywhere, while `match()` only checks whether the pattern matches right at the beginning of the string. Both return a match object if they succeed or `None` if they don't, so you can use an `if` statement to check the result. When your pattern contains **groups** — sections wrapped in parentheses `()` — you can pull out individual pieces of the match with `.group(1)`, `.group(2)`, and so on. `.group(0)` always gives you the full match.

```lyric
def main() {
    rex pattern = regex("/(\d{4})-(\d{2})-(\d{2})/")
    var text = "The event is on 2025-12-31 at noon."

    var match = pattern.search(text)

    if match
        print("Full match:", match.group(0))   # 2025-12-31
        print("Year:",       match.group(1))   # 2025
        print("Month:",      match.group(2))   # 12
        print("Day:",        match.group(3))   # 31
    else
        print("No date found")
    end
}
```

```output
Full match: 2025-12-31
Year: 2025
Month: 12
Day: 31
```

### 13.3 Finding All Matches

`search()` stops after the first match, but sometimes you need every match in the text. The `findall()` method does exactly that — it scans through the entire string and returns an array containing every piece of text that matched the pattern. This is useful any time you want to extract all occurrences of something, like every word in a sentence, every number in a log file, or every email address on a page.

```lyric
def main() {
    rex word_pattern = regex("/\w+/")
    str sentence = "Lyric is expressive and clear"

    arr words = word_pattern.findall(sentence)

    print("Sentence:", sentence)
    print("Words found:")
    for str word in words
        print(" -", word)
    done
    print("Total word count:", words.len())
}
```

```output
Sentence: Lyric is expressive and clear
Words found:
 - Lyric
 - is
 - expressive
 - and
 - clear
Total word count: 5
```

### 13.4 Replacing Text

Finding patterns is useful, but often you want to find them and swap them out for something else. The `replace()` method takes two arguments — the text to search through and the string to substitute in place of every match. It returns a new string with all the replacements made; the original string is not changed. In this example, every vowel in the string is replaced with an asterisk.

```lyric
def main() {
    rex vowels = regex("/[aeiou]/", "i")
    var original = "Hello, World!"
    var replaced = vowels.replace(original, "*")
    print(replaced)
}
```

```output
H*ll*, W*rld!
```

### 13.5 Practical Example — Parsing HTML Titles

This example ties everything together into a real-world task: extracting the title from an HTML string. The pattern uses a group `(.*?)` to capture whatever text sits between the `<title>` and `</title>` tags. The `?` after `*` makes it **non-greedy**, meaning it captures as little as possible rather than as much as possible — important when there could be other tags later in the string. We then use `search()` to find the match and `.group(1)` to pull out just the captured title text.

```lyric
rex title_pattern = regex("/<title>(.*?)<\/title>/")

def main() {
    str html = "<html><head><title>My Page</title></head></html>"
    var match = title_pattern.search(html)

    if match
        print("Title:", match.group(1))
    else
        print("No title found")
    end
}
```

```output
Title: My Page
```

---

## 14. File I/O

So far every value in your programs has lived in memory — the moment the program ends, everything disappears. **File I/O** (input/output) is how your program reads data from files on disk and writes data back to them, so information can survive after the program finishes. This is essential for anything that needs to save its work: configuration files, logs, user data, exported reports, and more.

Lyric handles files through a dedicated type called `dsk` (short for **disk**). You create a file handle by calling `disk("path/to/file")`, which gives you an object that represents that file. From there you can call methods like `.write()`, `.read()`, `.readlines()`, and `.close()` to interact with the file. Always remember to call `.close()` when you are done — this tells the operating system you are finished with the file and ensures all your data is safely saved.

### 14.1 Writing to a File

The simplest file operation is writing text to a file. You create a `dsk` handle pointing to the file you want, call `.write()` with the text you want to store, and then `.close()` to finish. If the file does not exist yet, Lyric creates it for you. If it already exists, `.write()` replaces its contents entirely — see [section 14.4](#144-appending-to-a-file) for how to add to a file without erasing what was already there.

```lyric
def main() {
    dsk f = disk("output.txt")
    f.write("Hello, file!")
    f.close()

    print("File written")
}
```

```output
File written
```

### 14.2 Reading from a File

Reading is the opposite of writing — you open a file and pull its contents into your program. The `.read()` method loads the entire file as a single string, which you can then print, search through, split into pieces, or process however you need. This is the simplest way to get data out of a file when you want everything at once.

```lyric
def main() {
    dsk f = disk("output.txt")
    str content = f.read()
    f.close()

    print("Contents of output.txt:")
    print(content)
}
```

```output
Contents of output.txt:
Hello, file!
```

### 14.3 Reading Line by Line

Sometimes you need to work with a file one line at a time — for example, processing a log file entry by entry or reading a list where each item is on its own line. The `.readlines()` method reads the entire file but splits it into an array where each element is one line. You can then loop through the array with a `for` loop, check how many lines there are with `.len()`, or access a specific line by index.

```lyric
def main() {
    dsk f = disk("output.txt")
    arr lines = f.readlines()
    f.close()

    print("Number of lines:", lines.len())
    print("Contents line by line:")
    for str line in lines
        print(" >", line)
    done
}
```

```output
Number of lines: 1
Contents line by line:
 > Hello, file!
```

### 14.4 Appending to a File

In section 14.1 you learned that `.write()` replaces the entire contents of a file. But what if you want to add new data to the end without erasing what is already there? That is what `.append()` does — it opens the file, jumps to the end, and adds your new text after everything that already exists. This is exactly how a log file works: each new entry is appended so the history is never lost.

```lyric
def main() {
    dsk f = disk("log.txt")
    f.write("First line\n")
    f.close()

    f.append("Second line\n")
    f.append("Third line\n")

    str content = f.read()
    f.close()

    print("log.txt now contains:")
    print(content)
}
```

```output
log.txt now contains:
First line
Second line
Third line
```

### 14.5 File Operators: `->`, `->>`, and `<-`

You have already learned to read and write files using methods like `.write()`, `.read()`, and `.append()`. Those work perfectly fine, but Lyric also offers **arrow operators** — a shorthand syntax that lets you do the same things in fewer characters. Think of the arrows as showing the direction data flows: `->` pushes data into a file (write), `->>` pushes data onto the end of a file (append), and `<-` pulls data out of a file (read). You do not have to use them — the methods from earlier sections do the same job — but many Lyric programmers prefer them because they make file operations feel as natural as moving data from one place to another.

| Operator | Meaning                          |
|----------|----------------------------------|
| `x -> f` | Overwrite file `f` with value `x`|
| `x ->> f`| Append value `x` to file `f`    |
| `x <- f` | Read file `f` into variable `x`  |

```lyric
def main() {
    dsk myfile = disk("notes.txt")

    # Overwrite the file
    str line1 = "First note"
    print line1 -> myfile

    # Append to the file
    str line2 = "Second note"
    print line2 ->> myfile

    str line3 = "Third note"
    print line3 ->> myfile

    myfile.close()

    # Read everything back
    str content
    dsk reader = disk("notes.txt")
    content <- reader
    reader.close()

    print("notes.txt contains:")
    print(content)
}
```

```output
notes.txt contains:
First note
Second note
Third note
```

**Note:** `"text" ->> f` appends the raw string (no newline), while `print "text" ->> f` appends the string followed by a newline character.

Arrays and maps can also be written to files:

```lyric
def main() {
    dsk f = disk("data.txt")
    arr numbers = [1, 2, 3, 4, 5]
    numbers ->> f
    f.close()

    # Read lines back into an array
    arr lines
    dsk reader = disk("data.txt")
    lines <- reader
    reader.close()

    print("Lines read back from file:", lines.len())
    print("First line:", lines[0])
}
```

```output
Lines read back from file: 1
First line: [1, 2, 3, 4, 5]
```

### 14.6 File Utility Methods

Beyond reading and writing, you often need to manage files themselves — check whether a file exists before trying to read it, find out how large it is, make a backup copy, rename it, or delete it when it is no longer needed. The `dsk` type provides utility methods for all of these tasks so you can handle them directly from Lyric without shelling out to the operating system.

```lyric
def main() {
    dsk f = disk("temp.txt")

    # Check existence
    print("Exists before write:", f.exists())

    f.write("some data")
    f.close()

    print("Exists after write:", f.exists())

    # File size in bytes
    print("File size:", f.size(), "bytes")

    # Copy and move
    f.copy("temp_copy.txt")
    f.move("temp_renamed.txt")

    # Delete
    dsk copy = disk("temp_copy.txt")
    copy.delete()

    dsk renamed = disk("temp_renamed.txt")
    renamed.delete()

    print("Cleaned up — both files deleted")
}
```

```output
Exists before write: False
Exists after write: True
File size: 9 bytes
Cleaned up — both files deleted
```

---

## 15. Shell Execution

Sometimes you need to reach outside your program and interact with the operating system — run a terminal command, call another program, or automate a task you would normally type into a shell. Most programming languages provide a way to do this, and Lyric is no different. Lyric's `exec()` function lets you pass a command as a string, the operating system runs it, and Lyric gets back a **return code** (also called an **exit code**): a number that tells you whether the command succeeded or failed. By convention, `0` means success and any other number means something went wrong. You can check this code with an `if` statement to decide what your program should do next.

### 15.1 exec()

The `exec()` function takes a shell command as a string, runs it, and returns the exit code as an integer. In this example, the `echo` command prints text to the terminal and always succeeds, so `exec` returns `0`. We store that return code in a variable and then check it — if it is `0`, we know the command worked.

```lyric
def main() {
    int rc = exec("echo Hello from the shell")
    print("Exit code:", rc)

    if rc == 0
        print("Command succeeded")
    end
}
```

```output
Hello from the shell
Exit code: 0
Command succeeded
```

### 15.2 Capturing Output

In section 15.1, `exec()` ran a command and gave you back an exit code, but the command's actual output (the text it printed) went straight to the terminal. Often you want to capture that output inside your program so you can work with it — store it, search through it, or display it later. The `->` operator after an `exec()` call redirects the command's output into a string variable instead of letting it print to the screen.

```lyric
def main() {
    str output
    exec("echo Hello World") -> output
    print("Captured:", output)
}
```

```output
Captured: Hello World
```

### 15.3 Piping Between Commands

If you have used a terminal before, you may have seen the `|` (pipe) character. A pipe takes the output of one command and feeds it directly as input to the next command, like a chain of workers passing data down a line. In Lyric, you can pipe between `exec()` calls the same way. The first command runs, its output flows into the second command, and you can capture the final result with `->`. You can also pipe straight into `print` to display the output without storing it in a variable.

```lyric
def main() {
    str result
    exec("echo hello world") | exec("cat") -> result
    print(result)

    # Pipe to print directly
    exec("echo Piped directly to print") | print
}
```

```output
hello world
Piped directly to print
```

You can chain multiple pipes — the output flows from left to right through each command. In this example, `echo` produces a sentence, `tr` splits the words onto separate lines by replacing spaces with newlines, and `wc -l` counts the number of lines:

```lyric
def main() {
    str out
    exec("echo hello world") | exec("tr ' ' '\n'") | exec("wc -l") -> out
    print(out)
}
```

```output
2
```

### 15.4 Conditional Exec Chains: `&&` and `||`

Sometimes you want to run a command only if the previous one succeeded, or provide a backup command if it failed. The `&&` operator runs the second command only if the first one succeeds (returns exit code 0), while `||` runs the second command only if the first one fails (returns a non-zero exit code). If the first command in a `&&` chain fails, the second command is skipped entirely — this is called short-circuiting.

```lyric
def main() {
    # Run second only if first succeeds
    str out1
    exec("echo step-one") && exec("echo step-two") -> out1
    print(out1)   # step-two

    # Run second only if first fails
    str out2
    exec("exit 1") || exec("echo fallback") -> out2
    print(out2)   # fallback

    # Short-circuits: if first fails, second doesn't run
    str out3
    exec("exit 1") && exec("echo skipped") -> out3
    print(out3)   # (empty)
}
```

```output
step-two
fallback

```

### 15.5 Redirecting Exec Output to a File

You can send the output of a shell command directly into a file using the `->>` (append) operator. This is useful for building log files or saving results from multiple commands. Each `exec()` call appends its output to the file, and then you can read the file back to see everything that was written.

```lyric
def main() {
    dsk logfile = disk("run.log")

    exec("echo Build started") ->> logfile
    exec("echo Compiling...") ->> logfile
    exec("echo Done") ->> logfile

    logfile.close()

    str content
    dsk reader = disk("run.log")
    content <- reader
    reader.close()
    print(content)

    reader.delete()
}
```

```output
Build started
Compiling...
Done
```

---

## 16. Importing Lyric Modules

As your programs grow, you will want to split your code across multiple files to keep things organized and reusable. Lyric's `import` statement lets you load functions, classes, and variables from other `.ly` files into your program, so you can build a library of tools and use them wherever you need without copying and pasting code.

### 16.1 Whole-Module Import (Namespace Access)

When you write `import module`, Lyric loads the entire file and creates a **namespace object** bound to the module name. You then access everything inside that module through dot notation — for example `utils.greet()` or `utils.MAX_SIZE` — which keeps your scope clean and makes it clear where each function or variable came from.

```lyric
# utils.ly
int MAX_SIZE = 100

def greet(str name) {
    print("Hello, " + name + "!")
}

class Counter
    def init(int start) {
        self.value = start
    }

    def increment() {
        self.value += 1
    }
+++
```

```lyric
# main.ly
import utils

def main() {
    utils.greet("Alice")
    print("Max size:", utils.MAX_SIZE)

    obj c = utils.Counter(0)
    c.increment()
    print("Counter:", c.value)
}
```

```output
Hello, Alice!
Max size: 100
Counter: 1
```

This mirrors Python's `import math` pattern — the module name acts as a
namespace that keeps your scope clean.

### 16.2 Selective Import

If you only need a few specific things from a module, you can use a selective import by adding a semicolon after the module name followed by a comma-separated list of the names you want. The listed names are pulled directly into your scope so you can use them without the module prefix, which keeps your code shorter when you only need one or two items from a large module.

```lyric
# main.ly
import utils; greet, Counter

def main() {
    greet("Bob")           # Direct access, no "utils." prefix
    obj c = Counter(10)
    c.increment()
    print("Counter:", c.value)
}
```

```output
Hello, Bob!
Counter: 11
```

This mirrors Python's `from utils import greet, Counter` pattern.

### 16.3 Module Search Path

Lyric looks for modules in the following locations, in order:

1. The current working directory
2. The directory containing the script being executed
3. Directories listed in the `LYRIC_PATH` environment variable

### 16.4 What Can Be Imported

Only **functions**, **classes**, and **module-level variables** (declared at
the top level of the file, outside any function or class) can be imported.

---

## 17. Importing Python Modules

Lyric does not yet have its own native standard library. A dedicated Lyric standard library is planned for a future release. When it arrives, it will become the primary and recommended way to access common functionality within Lyric programs.

For now, `importpy` provides access to a curated subset of Python's standard library and selected third-party modules. The following modules are currently whitelisted and may be imported directly:

- `collections`
- `datetime`
- `http.server`
- `json`
- `math`
- `os`
- `random`
- `requests`
- `sys`
- `time`

These modules have been reviewed to ensure they align with Lyric's runtime model and intended use.

Modules that are not on the whitelist are blocked by default. However, modules that are not explicitly blacklisted may be imported by running Lyric with the `--unsafe` flag. This flag enables broader Python interoperability and is intended for advanced users who understand the implications of stepping outside Lyric's controlled environment.

Certain Python modules remain fully blacklisted and cannot be imported under any circumstances. These include modules that interact directly with CPython internals — such as debuggers, bytecode manipulation tools, pickle serialization, and raw memory access — which are incompatible with Lyric's runtime model. If a blocked module is imported, Lyric will report the restriction clearly. See the [Language Specification](/specification.html#security-blacklist) for the complete list and technical details.

In a future version of Lyric, once the native standard library is available, the use of `importpy` may require explicitly enabling a `--interop` flag. This would make Python interoperability an intentional opt-in feature, clearly separated from Lyric's core standard environment.

### 17.1 Whole-Module Import

The basic form of `importpy` imports an entire Python module under its name, just like a whole-module Lyric import. You then access its functions, constants, and classes using dot notation — for example `math.sqrt()` or `math.pi`. This is the simplest way to start using Python functionality in your Lyric programs.

```lyric
importpy math

def main() {
    flt root = math.sqrt(16)
    print("Square root of 16:", root)

    print("Pi:", math.pi)
    print("floor(3.7) — rounds down:", math.floor(3.7))
    print("ceil(3.2) — rounds up:", math.ceil(3.2))

    flt angle = math.pi / 4
    print("sin(π/4):", math.sin(angle))
    print("cos(π/4):", math.cos(angle))
}
```

```output
Square root of 16: 4.0
Pi: 3.141592653589793
floor(3.7) — rounds down: 3
ceil(3.2) — rounds up: 4
sin(π/4): 0.7071067811865476
cos(π/4): 0.7071067811865476
```

### 17.2 Selective Import

Just like with Lyric module imports, you can selectively import specific names from a Python module by adding a semicolon after the module name followed by a comma-separated list. The selected names are pulled directly into your scope so you can use them without the module prefix, which keeps your code shorter and cleaner when you only need a few items from a large module.

```lyric
# Bind sqrt and pi directly into scope — no "math." prefix needed
importpy math; sqrt, pi

def main() {
    print("Square root of 16:", sqrt(16.0))
    print("Pi:", pi)
}
```

```output
Square root of 16: 4.0
Pi: 3.141592653589793
```

Selective import also works with dotted module names:

```lyric
importpy http.server; HTTPServer, SimpleHTTPRequestHandler

def main() {
    tup addr = ("0.0.0.0", 8080)
    var server = HTTPServer(addr, SimpleHTTPRequestHandler)
    print("Server created on port 8080")
    server.serve_forever()
}
```

```output
Server created on port 8080
```

Both functions and classes can be selectively imported. Blacklist rules still apply — you cannot selectively import from a blacklisted module.

### 17.3 Multiple Modules

You can import as many Python modules as you need by placing each `importpy` statement on its own line at the top of your file. Each module is loaded independently and accessed through its own namespace, so there is no conflict between names from different modules.

```lyric
importpy math
importpy os
importpy datetime

def main() {
    print("sqrt(144):", math.sqrt(144))

    str cwd = os.getcwd()
    print("Current working directory:", cwd)

    var today = datetime.date.today()
    print("Today's date:", today)

    var now = datetime.datetime.now()
    print("Current year:", now.year)
    print("Current month:", now.month)
}
```

```output
sqrt(144): 12.0
Current working directory: C:\Work\lyric\studio\tutorial
Today's date: 2026-03-02
Current year: 2026
Current month: 3
```

### 17.4 Using Python Objects

Python objects returned by `importpy` modules can be stored, passed to
functions, and used just like native Lyric values:

```lyric
importpy math

def apply_func(var func, flt value) {
    return func(value)
}

def main() {
    var sqrt = math.sqrt
    print("sqrt(25.0) passed as a value:", apply_func(sqrt, 25.0))

    arr funcs = [math.sqrt, math.sin, math.cos]
    arr names = ["sqrt", "sin", "cos"]
    int i = 0
    for var f in funcs
        print(names[i] + "(π/4):", f(math.pi / 4))
        i += 1
    done
}
```

```output
sqrt(25.0) passed as a value: 5.0
sqrt(π/4): 0.8862269254527580
sin(π/4): 0.7071067811865476
cos(π/4): 0.7071067811865476
```

### 17.5 Blacklisted Modules

Some Python modules are blocked by Lyric's runtime and cannot be imported with
`importpy`. Examples include `pickle`, `ctypes`, `inspect`, `gc`, `marshal`,
and several others that rely on CPython internals. If you hit a blocked module
you will see a clear error message explaining why. The full blacklist and the
reasoning behind each entry are documented in the
[Language Specification](/specification.html).

---

## 18. Command-Line Arguments

When you run a program from the terminal, you often want to pass in extra information — like which file to process, whether to enable verbose output, or what format to use. These are called **command-line arguments**. The name `getopts` comes from the Unix tradition of "get options" — a standard way for programs to read flags and settings from the command line. Lyric provides `getopts()` as a built-in function so you can easily accept and parse these options in your programs without importing anything.

### 18.1 getopts()

`getopts()` always takes **two arguments**: the short option name (single character, used with `-`) and the long option name (full word, used with `--`). Use `None` for whichever form you don't need. If an option expects a value, add a **colon** (`:`) after the name. Without a colon, the option is treated as a boolean flag that returns `True` or `False`.

```lyric
def main() {
    god verbose = getopts("v", "verbose")    # no colon = boolean flag
    var filename = getopts("f:", "file:")     # colon = expects a value

    if verbose
        print("Verbose mode is ON")
    end

    if filename != False
        print("Processing file:", filename)
    else
        print("No file specified")
    end
}
```

Options that expect a value can be passed with either a space or an equals sign:

```bash
lyric myprogram.ly -v -f config.txt
lyric myprogram.ly -v -f=config.txt
lyric myprogram.ly --verbose --file config.txt
lyric myprogram.ly --verbose --file=config.txt
```

```output
Verbose mode is ON
Processing file: config.txt
```

> **Note:** To see this output, run `lyric myprogram.ly -v -f config.txt` from your terminal.

### 18.2 Short and Long Options

`getopts(short, long)` always takes two arguments:

- **First argument** — the short option name (used with `-`), or `None`
- **Second argument** — the long option name (used with `--`), or `None`

Add a **colon** after either name to indicate it expects a value. Without a colon, the option is a boolean flag.

Short options use a **single dash**: `-v`, `-a`, `-f`
Long options use a **double dash**: `--verbose`, `--file`, `--output`

`getopts()` returns:
- `True` — if the boolean flag was provided
- `False` — if the flag was not provided
- A **string value** — if the option expects a value (colon syntax) and one was given

```lyric
def main() {
    god a       = getopts("a", None)           # -a only, boolean
    god verbose = getopts("v", "verbose")       # -v or --verbose, boolean
    var output  = getopts("o:", "output:")       # -o file or --output=file, expects value
    god x       = getopts("x", None)            # -x only, boolean

    print("a:", a)
    print("verbose:", verbose)
    print("output:", output)
    print("x:", x)
}
```

```output
a: True
verbose: True
output: result.txt
x: False
```

> **Note:** To see this output, run `lyric myprogram.ly -a --verbose --output=result.txt` from your terminal.

### 18.3 Combining getopts with File I/O

This example brings together everything you have learned about `getopts` and file I/O into a small but practical program. It reads an input file, optionally writes the result to an output file, and supports a verbose flag for debugging. If the user forgets to provide an input file, it prints a usage message and exits. Imagine you have a file called `notes.txt` with the following content:

```
Hello from Lyric!
```

The program below reads that file, prepends `"Processed: "` to the content, and either writes the result to an output file or prints it to the screen:

```lyric
def main() {
    var infile  = getopts("i:", "input:")
    var outfile = getopts("o:", "output:")
    god verbose = getopts("v", "verbose")

    if infile == False
        print("Usage: lyric program.ly --input=file.txt [--output=out.txt] [-v]")
        exit(1)
    end

    if verbose
        print("Reading from:", infile)
    end

    str content
    dsk reader = disk(infile)
    content <- reader
    reader.close()

    if outfile != False
        if verbose
            print("Writing to:", outfile)
        end
        str result = "Processed: " + content
        dsk writer = disk(outfile)
        result -> writer
        writer.close()
        print("Done!")
    else
        print(content)
    end
}
```

```output
Reading from: notes.txt
Writing to: result.txt
Done!
```

> **Note:** To see this output, run `lyric program.ly -v -i notes.txt -o result.txt` from your terminal.

---

## 19. Putting It All Together

Now that you have learned the core features of Lyric, let's combine them into a real program. This simple word-frequency counter reads a text file, counts how many times each word appears, and prints the results. It uses many of the features covered in this tutorial: `def main` with typed parameters, `if/else` for control flow, `dsk` for file I/O, `rex` and `regex()` for pattern matching, `map` for storing word counts, `for` loops for iteration, and `arr` for lists.

Imagine you have a file called `sample.txt` with the following content:

```
the cat sat on the mat
the cat sat and the cat played
the mat was on the floor
```

Save the program below as `wordcount.ly`:

```lyric
# a simple word count program

def main(int argc, arr argv) {
    if argc == 0 or argc > 1
        print "usage: wordcount.ly <file>"
        exit()
    end

    str filename = argv[0]

    dsk file = disk(filename)

    str text = file.read()
    file.close()

    rex pattern = regex("/\w+/")
    arr words = pattern.findall(text)

    map counts = {}

    for str word in words
        if word in counts
            counts[word] += 1
        else
            counts[word] = 1
        end
    done

    print counts
}
```

```output
{'the': 6, 'cat': 3, 'sat': 2, 'on': 2, 'mat': 2, 'and': 1, 'played': 1, 'was': 1, 'floor': 1}
```

> **Note:** To see this output, run `lyric wordcount.ly sample.txt` from your terminal.

---

## 20. Standard Library

Lyric ships with a built-in standard library that you can access with `import lyric`. It provides common utilities for working with the file system, dates and times, random numbers, paths, and environment variables — so you can do everyday tasks without reaching for external tools.

Here is a short program that uses several standard library functions together:

```lyric
import lyric

def main() {
    # Date and time
    tup d = lyric.date()
    print("Today:", d[0])
    print("Time:", d[1])

    # Working directory and file listing
    print("Working directory:", lyric.pwd())
    arr files = lyric.ls("*.ly")
    print("Lyric files found:", files)

    # Random numbers
    int roll = lyric.randint(1, 6)
    print("Dice roll:", roll)

    # Environment variables
    str home = lyric.env("HOME")
    print("Home:", home)

    # Path utilities
    str full = lyric.join("src", "main.ly")
    print("Joined path:", full)
}
```

```output
Today: 2026-03-03
Time: 21:45:12
Working directory: /home/user/project
Lyric files found: ['main.ly', 'utils.ly']
Dice roll: 4
Home: /home/user
Joined path: src/main.ly
```

This only scratches the surface. The standard library also includes functions for creating and removing directories, checking whether files exist, formatting dates, seeding the random number generator, and more. Refer to the [Specification](/specification.html#standard-library) for the full standard library reference.

---

## 21. Next Steps

You've now seen the full scope of Lyric's core features. Here are some directions to explore next:

- **Lyric Language Specification** — The formal reference for all syntax and semantics. Visit the [Specification](/specification.html) page for complete details.

- **Combining importpy with native Lyric** — Lyric's experimental Python bridge (`importpy`) lets you pull in whitelisted libraries — from JSON parsing (`json`) to file system operations (`os`) to date and time utilities (`datetime`) — and use them from clean, expressive Lyric code. Run `lyric --whitelist` to see which modules are currently available, or use `lyric --unsafe` if you are feeling adventurous.

- **Follow development** — Lyric is actively evolving. Follow along at [MiraNova Studios](https://miranova.studio/journal.html).

---

## Quick Reference

### Keywords

| Keyword         | Purpose                          |
|-----------------|----------------------------------|
| `def`           | Define a function                |
| `return`        | Return a value from a function   |
| `if / elif / else / end` | Conditional branching |
| `given / for / done` | Loop (for/while)          |
| `break`         | Exit a loop                      |
| `continue`      | Skip to the next iteration       |
| `class / +++`   | Define a class                   |
| `based on`      | Class inheritance                |
| `self`          | Current instance reference       |
| `try / catch / finally / fade` | Exception handling|
| `raise`         | Throw an exception               |
| `import`        | Import a Lyric module            |
| `importpy`      | Import a Python module           |
| `in`            | Membership test / loop iterator  |
| `and / or / not`| Logical operators                |
| `True / False`  | Boolean literals                 |
| `None`          | Null value                       |

### Type Keywords

| Keyword | Type                  |
|---------|-----------------------|
| `int`   | Integer               |
| `flt`   | Float                 |
| `str`   | String                |
| `god`   | Boolean               |
| `bin`   | Boolean (alias)       |
| `var`   | Dynamic (any type)    |
| `arr`   | Array                 |
| `tup`   | Tuple (immutable)     |
| `map`   | Map / dictionary      |
| `obj`   | Object (class instance)|
| `rex`   | Regular expression    |
| `dsk`   | File (disk) handle    |

### Built-in Functions

| Function           | Description                         |
|--------------------|-------------------------------------|
| `print(...)`       | Output values to stdout             |
| `input(prompt)`    | Read a line from stdin              |
| `range(n)`         | Produce integers 0 to n-1           |
| `type(x)`          | Get the type name of a value        |
| `isinstance(x, T)` | Check if x is an instance of T     |
| `int(x)`           | Convert to integer                  |
| `flt(x)`           | Convert to float                    |
| `str(x)`           | Convert to string                   |
| `god(x) / bin(x)`  | Convert to boolean                  |
| `arr(x)`           | Convert to array                    |
| `tup(x)`           | Convert to tuple                    |
| `regex(p, flags)`  | Create a regex pattern              |
| `disk(path)`       | Create a file handle                |
| `exec(cmd)`        | Run a shell command                 |
| `getopts(short, long)` | Read a CLI flag or option (use `None` for unused slot) |
| `exit(code)`       | Exit the program with a code        |

---

## Thank you

Thank you for exploring Lyric. We hope this tutorial gives you a solid foundation to get started programming with Lyric.

