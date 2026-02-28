 class Animal:
    name = "Unknown"

    def speak() {
        print(self.name, "makes a sound")
    }

    def describe() {
        print("Animal:", self.name)
    }
+++

class Dog based on Animal:
    breed = "Mixed"

    def speak() {
        print(self.name, "barks!")
    }

    def fetch() {
        print(self.name, "fetches the ball")
    }
+++

class Cat based on Animal:
    indoor = True

    def speak() {
        print(self.name, "meows")
    }
+++

def main() {
    var dog = Dog()
    dog.name  = "Rex"
    dog.breed = "Labrador"

    var cat = Cat()
    cat.name = "Whiskers"

    dog.speak()    # Rex barks!
    dog.fetch()    # Rex fetches the ball
    dog.describe() # Animal: Rex  (inherited from Animal)

    cat.speak()    # Whiskers meows
    cat.describe() # Animal: Whiskers (inherited)
}
