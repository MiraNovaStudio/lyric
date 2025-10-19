SPRINT 8 — INHERITANCE AND ACCESS CONTROL
Target Version: 0.3.1

Sprint Goal:
Implement single-inheritance support using the “based on” syntax.
Add optional constructors that automatically chain base → child.
Introduce public, private, and protected access modifiers for class methods.
All attributes remain public for now.

TASK 1 — IMPLEMENT INHERITANCE SYNTAX
Add support for defining a class based on another class.
Example:
class Entity:
var id
+++

class Shape based on Entity:
var size
+++

The parser must recognize “based on” as the inheritance operator.
Each subclass maintains a pointer to its base class in the class metadata.

ACCEPTANCE CRITERIA:
• Parser recognizes “based on <baseclass>” syntax.
• Runtime correctly links subclasses to their base.
• Method and property lookup checks child first then base.
• Multiple inheritance not allowed (this is single inheritance only).

TASK 2 — OPTIONAL CONSTRUCTORS AND AUTOMATIC CHAINING
Constructors remain optional.
If a class has a constructor, it runs automatically when an object is created.
When inheritance exists, constructors are called automatically in base-to-child order.
If a base class has no constructor, it is skipped.
There is no base() keyword.

Example:
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

Expected output:
A
B
C

ACCEPTANCE CRITERIA:
• Constructors are optional.
• Automatic constructor chaining always executes base → child.
• Classes without constructors are skipped gracefully.
• No keywords like base() or super() exist in Lyric.

TASK 3 — METHOD RESOLUTION AND OVERRIDING
Subclass methods may override base methods by using the same name.
When called on a child object, the child method always takes precedence.

ACCEPTANCE CRITERIA:
• Child methods replace base methods with matching names.
• Base method still accessible internally via explicit reference if needed in future versions (not implemented yet).
• Method lookups work correctly for all inheritance depths.

TASK 4 — ACCESS CONTROL KEYWORDS
Introduce optional visibility modifiers for methods: public, private, protected.
If no keyword is present, it defaults to public.
Access control applies only to methods at this stage.
Attributes remain public and cannot use these keywords.

Example:
class Person:
var name
public def speak() { print("Hi, I am ", self.name) }
private def think() { print("(thinking silently)") }
protected def rest() { print("Resting") }
+++

ACCEPTANCE CRITERIA:
• public, private, protected recognized as optional keywords.
• Default visibility = public.
• private methods callable only from inside same class.
• protected methods callable from same class or derived classes.
• All attributes remain public by design.

TASK 5 — UPDATE DOCUMENTATION AND CHANGELOG
Update README.md and CHANGELOG.md to include:
• based on syntax for inheritance.
• constructor chaining behavior.
• method overriding rules.
• optional visibility modifiers (public, private, protected).
• note that attributes are always public in this version.

ACCEPTANCE CRITERIA:
• Documentation shows examples of base and derived classes.
• Examples demonstrate automatic constructor order and visibility rules.
• CHANGELOG updated for version 0.2.9.

DEFINITION OF DONE
• Inheritance implemented with “based on” syntax.
• Automatic constructor chaining works base → child.
• Constructors are optional and skipped when absent.
• Method overriding confirmed functional.
• public/private/protected modifiers supported for methods.
• Documentation and CHANGELOG updated.
• Version bumped to 0.3.1 and committed.