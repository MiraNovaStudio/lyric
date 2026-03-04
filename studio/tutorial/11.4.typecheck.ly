class Animal:
    name = "Unknown"

    def speak() {
        print(self.name, "makes a sound")
    }

+++

class Dog based on Animal:

    def speak() {
        print(self.name, "barks!")
    }

+++

class Cat based on Animal:

    def speak() {
        print(self.name, "meows")
    }

+++

def main() {
    var dog = Dog()
    dog.name = "Max"

    print("type(dog):", type(dog))
    print("isinstance(dog, Dog):", isinstance(dog, Dog))
    print("isinstance(dog, Animal) — Dog inherits from Animal:", isinstance(dog, Animal))
    print("isinstance(dog, Cat):", isinstance(dog, Cat))
}
