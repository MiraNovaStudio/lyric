# Lyric syntax demonstration
# Exercises core language features for syntax highlighting, folding, and testing.

# ---------------------------
# Example 1 — Class and Methods
# ---------------------------
class Person:
  var name
  var age

  def Person(str n, int a) {
    self.name = n
    self.age = a
    print("Created person:", self.name)
  }

  def greet() {
    print("Hi, my name is", self.name, "and I am", self.age, "years old.")
  }

  def birthday() {
    self.age = self.age + 1
    print("Happy birthday,", self.name, "now you are", self.age)
  }
+++

# ---------------------------
# Example 2 — Exception Handling
# ---------------------------
def flt divide(int a, int b) {
  if b == 0:
    raise "Division by zero"
  end
  return a / b
}

def safe_division():
  try:
    flt result = divide(10, 0)
    print("Result:", result)
  catch:
    print("Caught a division error — cannot divide by zero.")
  finally:
    print("Exiting safe_division()")
  fade
}

# ---------------------------
# Example 3 — Main Program
# ---------------------------
def main() {
  str message = "Hello from Lyric!"
  print(message)

  # Instantiate a Person
  var p = Person("Aeonath", 41)
  p.greet()
  p.birthday()

  # Try dividing safely
  safe_division()

  # Conditional test
  int number = 5
  if number > 0:
    print("Positive number")
  else:
    print("Non-positive number")
  end

  # Simple loop
  given i in range(3):
    print("Loop iteration", i)
  done

  print("Program completed successfully.")
}
