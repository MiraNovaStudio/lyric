SPRINT 7 — CLASS SYSTEM IMPLEMENTATION
Target Version: 0.2.8

Sprint Goal:
Implement the Lyric class system with constructor support, instance methods, and the self keyword.
Add an alternative alias for the god type called bin.
This sprint will focus only on defining, instantiating, and using classes.
Inheritance and access control (public/private/protected) will be handled in Sprint 8.

TASK 1 — IMPLEMENT CLASS DEFINITION SYNTAX
Classes begin with the keyword class and terminate with +++.
Example syntax:

class Person:
var name
def Person() {
print("Hello, I am ", self.name)
}
+++

The parser must recognize class blocks and store defined methods and attributes within a class object.
Each class should have its own namespace for variables and methods.

ACCEPTANCE CRITERIA:
• class keyword and +++ terminator recognized.
• Parser correctly groups code between class and +++.
• Methods and variables defined inside class are attached to class scope.
• Nested or multiple class definitions in one file supported.

TASK 2 — ADD CONSTRUCTOR RECOGNITION
If a method name matches the class name, it is treated as the constructor.
Constructors run automatically on object instantiation.
The interpreter should translate def ClassName() to Python’s init() under the hood.

Example:
class Person:
var name
def Person() {
self.name = "Unknown"
print("Person created")
}
+++

ACCEPTANCE CRITERIA:
• Constructor executes automatically upon object creation.
• Constructor can access and modify instance variables through self.
• Only one constructor allowed per class (raise error if multiple found).
• Constructor can accept parameters (def Person(str name), etc.).

TASK 3 — ADD OBJECT INSTANTIATION AND SELF KEYWORD
Add ability to create objects and call methods on them.
Use standard function-call syntax for instantiation:

var p = Person()
p.Person()

The self keyword must automatically reference the instance object in all class methods.
Example:
class Person:
var name
def Person() {
self.name = "Unknown"
}
def greet() {
print("Hello, I am ", self.name)
}
+++

var user = Person()
user.greet()

ACCEPTANCE CRITERIA:
• Objects can be instantiated with parentheses syntax.
• self references the instance correctly within all methods.
• Instance variables retain their values between method calls.
• Calling methods on object instances executes correctly.
• Error handling works if a method or property does not exist.

TASK 4 — ADD CLASS METHOD AND PROPERTY ACCESS
Methods and variables inside classes should be accessible via dot notation.
Example:
var p = Person()
p.name = "Michael"
p.greet()

ACCEPTANCE CRITERIA:
• Dot notation works for property access and method calls.
• Assigning to an undeclared property raises an error.
• Properties persist across method calls for the same instance.
• Parser handles chained access correctly (p.address.city).

TASK 5 — ADD ALTERNATIVE TYPE NAME BIN FOR GOD TYPE
Introduce bin as an alias for god.
Both types represent true/false values.
Internally, both map to the same boolean implementation.
If god becomes widely accepted, bin may be deprecated in a future release.

Example:
god flag1 = true
bin flag2 = false
print(flag1, flag2)

ACCEPTANCE CRITERIA:
• bin recognized as a valid type keyword.
• bin and god behave identically.
• Type enforcement and logical operations work with both.
• Documentation updated noting bin is an alias for god.

TASK 6 — DOCUMENTATION AND CHANGELOG UPDATES
Update README.md and CHANGELOG.md to describe:
• class definition and +++ terminator.
• Constructor syntax (def ClassName()).
• self keyword behavior and usage examples.
• bin type alias for god.
Include multiple examples of class creation, property assignment, and method calling.

ACCEPTANCE CRITERIA:
• Documentation includes syntax and examples for class, self, and bin.
• CHANGELOG updated for version 0.2.2.

DEFINITION OF DONE
• Class syntax implemented and parser recognizes class and +++.
• Constructors function automatically when instances are created.
• self keyword works correctly inside all class methods.
• Dot notation works for accessing methods and variables.
• bin alias for god implemented and documented.
• All new features tested and verified through example programs.
• Documentation and CHANGELOG updated.
• Version bumped to 0.2.8 and committed.