# Lyric

Lyric is an experimental interpreted programming language built in Python, featuring strict type declarations, classes with inheritance, Python interoperability, and exception handling.

**Version:** 1.1.1 (Alpha)  
**Docs:** [lyric-lang.org](https://lyric-lang.org)  
**Source:** [GitHub](https://github.com/aeonath/lyric-lang)  

## Install

```bash
pip install lyric-lang
```

Requires Python 3.10+.

## Usage

```bash
lyric program.ly          # run a file
lyric -i                  # interactive REPL
lyric -i "print 2 + 2"    # evaluate an expression
```

## Example

Hello world program.

```lyric
def main() {
    print "Hello World"
}
```

## Bugs

Bug reports and feedback are welcome at [GitHub Issues](https://github.com/aeonath/lyric-lang/issues).

---

Copyright (c) 2026 MiraNova Studios. Licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).
