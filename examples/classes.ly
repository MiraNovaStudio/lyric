# Basic class and object usage

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

def main() {
  var p = Person("Lyric", 1)
  p.greet()
  p.birthday()
}