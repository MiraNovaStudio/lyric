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


## Task 4 - add a module whitelist for importpy

Hi Claude, we need to add a module whitelist for importpy.  This is modules that we know are safe.  Initially add modules we are using in our unit tests to the whitelist along with math, time, and datetime.  We will be writing separate unit tests for each module in the whitelist in a subsequent task.  Add a --unsafe flag which will allow importpy of modules that are not in the whitelist and not in the blacklist.  Blacklist modules can never be imported even with --unsafe.  Also add a --blacklist flag and --whitelist flag that will print out the current blacklist and whitelist reqpectiveley.


## Taks 5 - add the obj type

Currently when instantating classes in Lyric we need to use the var type, for example

var account = BankAccount()

where BankAccount is a class in lyric.  We need to add the object type (obj) to the language so
we can do 

obj account = BankAccount()

This should be a primitive type in lyric like int str and arr etc.  

Do not update the old unit tests to use obj, var should still work as normal (it is dynamic and can be any type)

Write the new unit tests to test that obj type works correctly.


