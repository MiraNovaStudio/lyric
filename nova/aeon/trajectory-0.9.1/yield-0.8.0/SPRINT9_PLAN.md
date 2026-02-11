# Sprint 8 — Inheritance and Access Control

**Target Version:** 0.8.0

## Sprint Goal

Implement single-inheritance support using the "based on" syntax.

**Key Features:**
- Add optional constructors that automatically chain base → child.
- Introduce `public`, `private`, and `protected` access modifiers for class methods.
- All attributes remain public for now.
- Introduce getopts and argument processing


## Task 1 — Implement Inheritance Syntax

Add support for defining a class based on another class.

**Example:**
```lyric
class Entity:
    var id
+++

class Shape based on Entity:
    var size
+++
```

**Implementation:**
- The parser must recognize "based on" as the inheritance operator.
- Each subclass maintains a pointer to its base class in the class metadata.

### Acceptance Criteria:
- Parser recognizes "based on <baseclass>" syntax.
- Runtime correctly links subclasses to their base.
- Method and property lookup checks child first then base.
- Multiple inheritance not allowed (this is single inheritance only).

## Task 2 — Optional Constructors and Automatic Chaining

Constructors remain optional.

**Behavior:**
- If a class has a constructor, it runs automatically when an object is created.
- When inheritance exists, constructors are called automatically in base-to-child order.
- If a base class has no constructor, it is skipped.
- There is no `base()` keyword.

**Example:**
```lyric
class A:
    def A() { print("A") }
+++

class B based on A:
    def B() { print("B") }
+++

class C based on B:
    def C() { print("C") }
+++

var obj = C()
```

**Expected output:**
```
A
B
C
```

### Acceptance Criteria:
- Constructors are optional.
- Automatic constructor chaining always executes base → child.
- Classes without constructors are skipped gracefully.
- No keywords like `base()` or `super()` exist in Lyric.

## Task 3 — Method Resolution and Overriding

Subclass methods may override base methods by using the same name.

**Behavior:**
- When called on a child object, the child method always takes precedence.

### Acceptance Criteria:
- Child methods replace base methods with matching names.
- Base method still accessible internally via explicit reference if needed in future versions (not implemented yet).
- Method lookups work correctly for all inheritance depths.

## Task 4 — Access Control Keywords / Scoping 

Introduce optional visibility modifiers for methods: `public`, `private`, `protected`.

**Rules:**
- If no keyword is present, it defaults to `public`.
- Access control applies only to methods at this stage.
- Attributes remain public and cannot use these keywords.

**Example:**
```lyric
class Person:
    var name
    public def speak() { print("Hi, I am ", self.name) }
    private def think() { print("(thinking silently)") }
    protected def rest() { print("Resting") }
+++
```

### Acceptance Criteria:
- `public`, `private`, `protected` recognized as optional keywords.
- Default visibility = `public`.
- `private` methods callable only from inside same class.
- `protected` methods callable from same class or derived classes.
- All attributes remain public by design.


## Task 5 - getopts support

The goal is to provide convenient getopts support via a built in function 
getopts.  If they want more fine grained support they will use the python
getopts funciton or similar.

**Implementation**
- add the getopts built-in funtion
- getopts("a") will return an option specified with -a
- getopts("verbose") will return an option specified with --verbose
- any option longer than one character will have to use --
- any option which doesn't have an argument will either be true or false
- if a flag is passed that is not defined by getopts throw an error

**Example**

call lyric myProgram.ly -a --verbose --file=myfile
```lyric
def main () {
    god a = getopts("a")
    int v = getopts("verbose")
    str filename = getopts("file")
    int x = getopts("x") # is false because variable was not passed on command line
}
```

### Acceptance criteria

- options are processed and passed when command line options are present
- unit tests are present to test option combinations and corner cases
- actual arguments to the script itself will be implemented in the next task

## Task 6 - Script arguments

The goal is to allow arguments to be passed to the script on the command line.

**Implementation**
- add the ability to specify arguments on the command line in the cli
- the arguments are passed to the main function by user defined parameters to main

**Example**
call lyric myprogram -a arg1 arg2

```lyric
def main(int argc, arr argv) {
    god a = getopts("a")
    if argc == 2
        str var1 = argv[0]
        str var2 = argv[1]
    end
}
```

### Acceptance Criteria

- arguments are processed and passed when command line arguments are present
- unit tests are present to test arguments and argc and argv parameters and corner cases

## Task 7 - File IO

The goal is to add the dsk type and allow file operations on variables of that type

**Implementation**
- add the dsk type to specificy the file, e.g. dsk myfile = "readme.txt"
- add the common file operations on the variable

myfile.open() # default mode is ra, otherwise override with mode='rw' parameter
myfile.readlines()
myfile.write(...)
myfile.append(...)
myfile.delete()
myfile.exists()
myfile.close()
myfile.copy(toPath)
myfile.move(toPath)
myfile.size(),

### Acceptance Criteria

- unit tests are created to test file operations
- the built-in funciton open() is replaced by myfile.open()

## Task 8

have the -h option auto generate a usage help statement unless it is overridden

**Implementation**

lyric myfile.ly -h will autogenerate the help message

- str host = getopts("h") # this will override the -h option

### Acceptance Criteria

- unittests are written to to test auto -h and override -h


## Task 9 - File operators

Add file operators -> ->> and <- to get data to and from the file

dsk myfile = "test.txt"
print "test" ->> myfile

equivalent to str test = "test", test ->> myfile


appends to the string test to myfile

print <- myfile, prints the file

and print "Test" -> myfile, overwrites my file

str myvar <- myfile

loads myvar with the contents of myfile assuming it is not a binary file

same for arr myarr <- myfile loads the array with each line of the file

arr myarr = [1,2,3]

myarr ->> myfile

creates the file
1
2
3

Try to make the operators make sense for each datatype claude (map, god, etc.)

Make sure you match ->> before you match -> so there is no ambiguity.

Do not allow file i/o operators inside of an assignement chat.  So
do not do x = (a + b) -> myfile

Let's start with this and see how it goes

## Task 10

Add the exit() builtin function, allow integer parameters and exit(1) for 
example will exit the program with return code 1


Add the exec("mycomamnd.sh -l") built-in also.  You can use subprocess or os.system on the
backend

Use the > operator to allow redirecting of the output to a variable

str output
like exec("mycommand.sh") > output

output could also be myfile if you want to redirect to a file

similarly you can pipe input to the command with the < operator

str input = "1"

exec("mycommand") < input > output

exec() always returns the return code of the process

int rc = exec("chmod 644 filename.txt")

rc contain 0 the return code of the chmod command example

for now you can always append stderr to stdout so it is just one stream


## Definition of Done

- Inheritance implemented with "based on" syntax.
- Automatic constructor chaining works base → child.
- Constructors are optional and skipped when absent.
- Method overriding confirmed functional.
- `public`/`private`/`protected` modifiers supported for methods
- getopts functions properly
- command line parameters function correctly
