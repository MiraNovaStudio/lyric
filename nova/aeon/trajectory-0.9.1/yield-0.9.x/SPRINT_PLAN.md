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

