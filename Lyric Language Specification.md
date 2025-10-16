# Lyric Language Specification  
**Version:** 0.1  
**Author:** Michael Stone & ChatGPT  
**Date:** October 2025  

---

## 🌙 Overview

**Lyric** is a modern, beginner-friendly programming language designed for simplicity, readability, and elegance.  
It blends Python’s clean structure with a touch of natural language rhythm — code that reads like thought and feels like poetry.  

Lyric minimizes syntax noise, avoids redundant symbols, and introduces symbolic elegance (`+++`, `done`, `end`) to clarify program flow.  

---

## 🧭 Design Philosophy

> *Readable like pseudocode, structured like Python, expressive like poetry.*

1. **Clarity before cleverness** — syntax must express intent plainly.  
2. **Simplicity over completeness** — features exist only when they add clarity.  
3. **Visual harmony** — indentation and rhythm matter.  
4. **Consistency** — similar constructs end with parallel patterns (`end`, `done`, `+++`).  
5. **Braces only where needed** — functions use braces; everything else uses natural terminators.

---

## 🧩 Syntax Summary

| Construct | Open | Close | Notes |
|------------|-------|--------|-------|
| Conditional | `if`, `else if`, `else` | `end` | Replaces `elif` with `else if` |
| Loop | `given` | `done` | Unifies `for` and `while` |
| Function | `def` | `{ ... }` | Only construct using braces |
| Class | `class` | `+++` | Symbolic closure (adds class to program) |
| Try/Except | `try`, `except`, `finally` | implicit | Structured inside `{}` |
| Import | `import` | — | Simplified single-line import |
| Entry Point | `main()` | — | Required start of every program |

---

## 🔹 Basic Structure

Every Lyric program starts execution in a **main function**.  
There is no `__name__` or hidden runtime boilerplate.

```lyric
def main() {
	print("Hello, world!")
}


## ⚙️ Core Constructs

### Conditionals

- Uses else if instead of elif
- Block introduced by : and closed by end

```lyric
if x > 0:
	print("positive")
else if x < 0:
	print("negative")
else:
	print("zero")
end

### Loops
- given replaces both for and while
- Ends with done

given i in range(5):
	print(i)
done

given n > 0:
	print(n)
	n -= 1
done


### Functions
- Braces used only for functions
-Indentation purely stylistic, not structural

def greet(name) {
	print("Hello,", name)
}

### Classes
- +++ closes a class, symbolizing addition of a structure to the program
- Classes are lightweight containers for variables and functions

class Player:
	name = "Guest"

	def greet() {
		print("Hello,", self.name)
	}
+++

### Importing
- from … import … replaced with direct or semicolon syntax

import math
import random.randint
import random; randint, randrange
import os as system

### FIle I/o
- given reads naturally with iterables
- Explicit and readable file handling

def main() {
	total = 0
	given line in open("numbers.txt"):
		total += int(line.strip())
	done
	print("Total:", total)
}

### Error Handling
- Uses familiar Python-style exception handling
- Syntax simplified: except: ErrorType:

def main() {
	try:
		n = int(input("Enter a number: "))
		print("Half:", n / 2)
	except: ValueError:
		print("Invalid input")
	finally:
		print("Done")
}

### Class

class Counter:
	value = 0

	def Counter(start) {
		self.value = start
	}

	def increment() {
		self.value += 1
	}

	def get_string() {
		return str(self.value)
	}
+++

def main() {
	c = Counter()
	given i in range(3):
		c.increment()
	done
	print("Count:", c)
}

## NOTES
🚫 Omitted in v0.1

To maintain simplicity:

No comprehensions ([x for x in y])

No lambdas

No decorators

No context managers (with)

No async/await

No type hints

Lyric is about learning and clarity, not syntax density.

## Example Program

import math

def area(radius) {
	return math.pi * radius * radius
}

def main() {
	r = 5
	print("Area:", area(r))
}

### Output

Area: 78.5398


### Closing Thoughts

Lyric is designed to teach, inspire, and simplify.
It’s a bridge between thought and execution — a language that emphasizes intent, not ceremony.

“Code should not only work — it should sing.” 🎵


