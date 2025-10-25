class Person:
    var name
    var age
    
    def init(str name, int age) {
        self.name = name
        self.age = age
        print("Person created with init():", self.name, "age", self.age)
    }
+++

def main() {
    person = Person("Bob", 25)
    print("Person name:", person.name)
    print("Person age:", person.age)
}
