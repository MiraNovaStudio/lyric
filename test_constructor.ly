class Person:
    var name
    var age
    
    def Person(str name, int age) {
        self.name = name
        self.age = age
        print("Person created:", self.name, "age", self.age)
    }
+++

def main() {
    person = Person("Alice", 30)
    print("Person name:", person.name)
    print("Person age:", person.age)
}