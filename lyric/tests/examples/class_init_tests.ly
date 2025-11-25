# Class and Constructor Tests for Sprint 3
# Tests class definitions, init() methods, and instance creation
#
# NOTE: As of Sprint 8, len(), append(), keys(), and values() are now methods
# on arr and map objects, not standalone functions.

# Test 1: Basic class with init() method
class Person
    def init(str name, int age) {
        self.name = name
        self.age = age
        self.greeting = "Hello, I'm " + name
    }
+++

# Test 2: Class instantiation with init()
var person1 = Person("Alice", 30)
var person2 = Person("Bob", 25)

# Test 3: Access instance variables
var alice_name = person1.name
var alice_age = person1.age
var alice_greeting = person1.greeting

# Test 4: Class with multiple methods
class BankAccount
    def init(str owner, flt initial_balance) {
        self.owner = owner
        self.balance = initial_balance
        self.transactions = []
    }
    
    def deposit(flt amount) {
        self.balance = self.balance + amount
        self.transactions.append("Deposit: " + str(amount))
    }
    
    def withdraw(flt amount) {
        if self.balance >= amount
            self.balance = self.balance - amount
            self.transactions.append("Withdrawal: " + str(amount))
        else
            print("Insufficient funds")
        end
    }
+++

# Test 5: Bank account usage
var account = BankAccount("Alice", 1000.0)
account.deposit(500.0)
account.withdraw(200.0)
var current_balance = account.balance

# Test 6: Class with typed parameters
class Calculator
    def init(str name) {
        self.name = name
        self.history = []
    }
    
    def add(int a, int b) {
        var result = a + b
        self.history.append(str(a) + " + " + str(b) + " = " + str(result))
        return result
    }
    
    def multiply(int a, int b) {
        var result = a * b
        self.history.append(str(a) + " * " + str(b) + " = " + str(result))
        return result
    }
+++

# Test 7: Calculator usage
var calc = Calculator("MyCalculator")
var sum_result = calc.add(5, 10)
var product_result = calc.multiply(3, 7)
var history_length = calc.history.len()

# Test 8: Class with complex init()
class Student
    def init(str name, int student_id, var grades) {
        self.name = name
        self.id = student_id
        self.grades = grades
        self.average = 0.0
        self.calculate_average()
    }
    
    def calculate_average() {
        if self.grades.len() > 0
            var total = 0
            var count = self.grades.len()
            # Note: This would need a loop to sum grades, simplified for now
            self.average = 85.0  # Placeholder
        end
    }
+++

# Test 9: Student with grades
var student_grades = [85, 92, 78, 96]
var student = Student("Charlie", 12345, student_grades)
var student_name = student.name
var student_id = student.id
var student_avg = student.average

# Test 10: Class inheritance simulation (using composition)
class Employee
    def init(str name, int employee_id, flt salary) {
        self.name = name
        self.id = employee_id
        self.salary = salary
        self.department = "General"
    }
    
    def promote(flt raise_amount) {
        self.salary = self.salary + raise_amount
        print("Employee promoted! New salary:", self.salary)
    }
+++

var employee = Employee("David", 67890, 50000.0)
employee.promote(5000.0)
var new_salary = employee.salary
