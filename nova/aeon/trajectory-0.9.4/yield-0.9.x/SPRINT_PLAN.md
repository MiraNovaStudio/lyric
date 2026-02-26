# SPrint Plan


# Task 1 - Blacklist Python modules that do not make sense in Lyric

“If a stdlib module relies on CPython bytecode, frames, object identity, or interpreter internals, it must be blacklisted for Lyric.”

At a minimum the following modules should be blacklisted.

```
pdb
trace
traceback
faulthandler
inspect
dis
marshal
pickle
pickletools
copyreg
code
codeop
compile
eval
exec
types.CodeType
importlib._bootstrap
importlib._bootstrap_external
zipimport
runpy
modulefinder
gc
weakref
sys.getrefcount
ctypes
cffi
_ctypes
mmap
```

If a module is blacklisted, the program should print out an error message saying the module is blacklisted and
does not work with lyric.  Include this message so that the user knows why the module doesn't work with lyric

```
If a stdlib module relies on CPython bytecode, frames, object identity, or interpreter internals, it must be blacklisted for Lyric.”
```

Create unit test as usual in the proper tests/ directory for the sprint.  

## Task 2 - redirect and append stderr to stdout for command output operators and command pipelines

When dealing with command output, the entirety of stdout and stderr will be considered the output of the program.  So if we have exec(mycmd) -> myvar, then both stdout and stderr are captured into the variable.  The same is true for our command pipelines exec(mycmd) | exec(mycmd2)


## Task 3 - update function definition syntax regarding return types

Claude our current syntax requires return types for functions to be specifed as follows

```
int def add(int a, int b) {
      return a + b
  }
```

The int def here is redundant.  If a return type is specified, the function would be int add(), if no return type is specified the function would be def add().  There is no reason to have int def add().  

Please udpate the code to recognize functions with return types in the form int myfunc(), str myfunc() etc. or simply def myfunc().

Please update the unit tests to honor this new syntax.  int def add() should not parse chat.




