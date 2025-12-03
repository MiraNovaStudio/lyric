# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the GNU General Public License v3.0

"""Tests for access control keywords: public, private, protected (Sprint 9 Task 4)."""

from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric
import pytest
import io
import sys


def test_public_method_accessible_from_outside():
    """Test that public methods can be called from outside the class."""
    source = """
class Person
    var name
    public def speak() {
        print("Hello from", self.name)
    }
+++

def main() {
    var person = Person()
    person.name = "Alice"
    person.speak()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Hello from Alice" in output
    finally:
        sys.stdout = old_stdout


def test_public_method_default_visibility():
    """Test that methods without visibility modifier default to public."""
    source = """
class Person
    var name
    def greet() {
        print("Hi from", self.name)
    }
+++

def main() {
    var person = Person()
    person.name = "Bob"
    person.greet()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Hi from Bob" in output
    finally:
        sys.stdout = old_stdout


def test_private_method_not_accessible_from_outside():
    """Test that private methods cannot be called from outside the class."""
    source = """
class Person
    var name
    private def secret() {
        print("Secret method")
    }
+++

def main() {
    var person = Person()
    person.secret()
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "private method" in str(exc_info.value).lower()
    assert "secret" in str(exc_info.value)


def test_protected_method_not_accessible_from_outside():
    """Test that protected methods cannot be called from outside the class."""
    source = """
class Person
    var name
    protected def internal() {
        print("Internal method")
    }
+++

def main() {
    var person = Person()
    person.internal()
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "protected method" in str(exc_info.value).lower()
    assert "internal" in str(exc_info.value)


def test_private_method_accessible_from_public_method():
    """Test that private methods can be called from public methods within the same class."""
    source = """
class Calculator
    private def compute() {
        print("Computing...")
        return 42
    }
    
    public def getResult() {
        var result = self.compute()
        print("Result:", result)
        return result
    }
+++

def main() {
    var calc = Calculator()
    var value = calc.getResult()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Computing..." in output
        assert "Result: 42" in output
    finally:
        sys.stdout = old_stdout


def test_protected_method_accessible_from_public_method():
    """Test that protected methods can be called from public methods within the same class."""
    source = """
class Base
    protected def helper() {
        print("Helper called")
        return 100
    }
    
    public def work() {
        var val = self.helper()
        print("Work done:", val)
        return val
    }
+++

def main() {
    var myobj = Base()
    var result = myobj.work()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Helper called" in output
        assert "Work done: 100" in output
    finally:
        sys.stdout = old_stdout


def test_multiple_visibility_modifiers_in_class():
    """Test that a class can have methods with different visibility levels."""
    source = """
class Example
    public def publicMethod() {
        print("Public method")
    }
    
    private def privateMethod() {
        print("Private method")
    }
    
    protected def protectedMethod() {
        print("Protected method")
    }
    
    def defaultMethod() {
        print("Default (public) method")
    }
+++

def main() {
    var myobj = Example()
    myobj.publicMethod()
    myobj.defaultMethod()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Public method" in output
        assert "Default (public) method" in output
    finally:
        sys.stdout = old_stdout


def test_private_method_in_constructor():
    """Test that private methods can be called from constructors."""
    source = """
class Person
    var name
    
    private def initialize(str n) {
        print("Initializing with:", n)
        self.name = n
    }
    
    def Person(str n) {
        self.initialize(n)
    }
    
    public def getName() {
        return self.name
    }
+++

def main() {
    var person = Person("Charlie")
    var n = person.getName()
    print("Name is:", n)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Initializing with: Charlie" in output
        assert "Name is: Charlie" in output
    finally:
        sys.stdout = old_stdout


def test_visibility_with_typed_methods():
    """Test that visibility modifiers work with typed method declarations."""
    source = """
class Math
    private int compute(int x) {
        return x * 2
    }
    
    public int calculate(int x) {
        var result = self.compute(x)
        return result + 10
    }
+++

def main() {
    var math = Math()
    var value = math.calculate(5)
    print("Value:", value)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Value: 20" in output
    finally:
        sys.stdout = old_stdout


def test_protected_method_accessible_in_derived_class():
    """Test that protected methods are accessible from derived classes."""
    source = """
class Base
    protected def helper() {
        print("Base helper")
        return 42
    }
+++

class Child based on Base
    public def useHelper() {
        var val = self.helper()
        print("Used helper, got:", val)
        return val
    }
+++

def main() {
    var child = Child()
    var result = child.useHelper()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Base helper" in output
        assert "Used helper, got: 42" in output
    finally:
        sys.stdout = old_stdout


def test_private_method_not_accessible_in_derived_class():
    """Test that private methods are NOT accessible from derived classes."""
    source = """
class Base
    private def secret() {
        print("Secret")
        return 99
    }
+++

class Child based on Base
    public def trySecret() {
        var val = self.secret()
        return val
    }
+++

def main() {
    var child = Child()
    var result = child.trySecret()
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "private method" in str(exc_info.value).lower()
    assert "secret" in str(exc_info.value)


def test_public_method_accessible_in_derived_class():
    """Test that public methods are accessible from derived classes."""
    source = """
class Base
    public def greet() {
        print("Hello from Base")
        return "base"
    }
+++

class Child based on Base
    public def callGreet() {
        var msg = self.greet()
        print("Called greet, got:", msg)
        return msg
    }
+++

def main() {
    var child = Child()
    var result = child.callGreet()
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Hello from Base" in output
        assert "Called greet, got: base" in output
    finally:
        sys.stdout = old_stdout


def test_visibility_applies_only_to_methods_not_attributes():
    """Test that attributes remain public regardless of method visibility."""
    source = """
class Person
    var name
    var age
    private def secret() {
        print("Secret")
    }
+++

def main() {
    var person = Person()
    person.name = "Alice"
    person.age = 30
    print("Name:", person.name)
    print("Age:", person.age)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Name: Alice" in output
        assert "Age: 30" in output
    finally:
        sys.stdout = old_stdout


def test_method_override_preserves_visibility():
    """Test that overriding a method can change its visibility."""
    source = """
class Base
    protected def process() {
        print("Base process")
        return 1
    }
+++

class Child based on Base
    public def process() {
        print("Child process")
        return 2
    }
+++

def main() {
    var child = Child()
    var result = child.process()
    print("Result:", result)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Child process" in output
        assert "Result: 2" in output
    finally:
        sys.stdout = old_stdout


def test_error_message_includes_class_name():
    """Test that access error messages include the class name."""
    source = """
class SecretKeeper
    private def getSecret() {
        return "secret123"
    }
+++

def main() {
    var keeper = SecretKeeper()
    var s = keeper.getSecret()
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    error_msg = str(exc_info.value).lower()
    assert "secretkeeper" in error_msg
    assert "getsecret" in error_msg
    assert "private" in error_msg


def test_private_attribute_not_accessible_from_outside():
    """Test that private attributes cannot be accessed from outside the class."""
    source = """
class BankAccount
    private var balance = 1000
    public var accountNumber = "12345"
+++

def main() {
    var account = BankAccount()
    print(account.balance)
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "private attribute" in str(exc_info.value).lower()
    assert "balance" in str(exc_info.value)


def test_protected_attribute_not_accessible_from_outside():
    """Test that protected attributes cannot be accessed from outside the class."""
    source = """
class Employee
    protected var salary = 50000
    public var name = "John"
+++

def main() {
    var emp = Employee()
    print(emp.salary)
}
"""
    with pytest.raises(RuntimeErrorLyric) as exc_info:
        ast = parse(source)
        evaluate(ast)
    
    assert "protected attribute" in str(exc_info.value).lower()
    assert "salary" in str(exc_info.value)


def test_private_attribute_accessible_from_same_class():
    """Test that private attributes can be accessed from within the same class."""
    source = """
class BankAccount
    private var balance = 1000
    
    public def getBalance() {
        return self.balance
    }
+++

def main() {
    var account = BankAccount()
    var bal = account.getBalance()
    print("Balance:", bal)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Balance: 1000" in output
    finally:
        sys.stdout = old_stdout


def test_protected_attribute_accessible_in_derived_class():
    """Test that protected attributes are accessible from derived classes."""
    source = """
class Employee
    protected var salary = 50000
    public var name = "John"
+++

class Manager based on Employee
    public def getSalary() {
        return self.salary
    }
+++

def main() {
    var mgr = Manager()
    var sal = mgr.getSalary()
    print("Salary:", sal)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Salary: 50000" in output
    finally:
        sys.stdout = old_stdout


def test_public_attribute_accessible_everywhere():
    """Test that public attributes are accessible from everywhere."""
    source = """
class Person
    public var name = "Alice"
    private var ssn = "123-45-6789"
+++

def main() {
    var p = Person()
    print("Name:", p.name)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Name: Alice" in output
    finally:
        sys.stdout = old_stdout


def test_mixed_visibility_attributes_and_methods():
    """Test a class with mixed visibility for both attributes and methods."""
    source = """
class SecureData
    private var secret = "classified"
    protected var internal = "internal-use"
    public var publicInfo = "public"
    
    private def getSecret() {
        return self.secret
    }
    
    public def getPublicInfo() {
        return self.publicInfo
    }
    
    public def accessSecretViaMethod() {
        return self.getSecret()
    }
+++

def main() {
    var data = SecureData()
    print("Public:", data.publicInfo)
    var secretData = data.accessSecretViaMethod()
    print("Secret via method:", secretData)
}
"""
    old_stdout = sys.stdout
    sys.stdout = captured_output = io.StringIO()
    
    try:
        ast = parse(source)
        evaluate(ast)
        output = captured_output.getvalue()
        assert "Public: public" in output
        assert "Secret via method: classified" in output
    finally:
        sys.stdout = old_stdout

