class Rectangle:
    width  = 0
    height = 0

    def area() {
        return self.width * self.height
    }

    def perimeter() {
        return 2 * (self.width + self.height)
    }

    def describe() {
        print("Rectangle", self.width, "x", self.height)
        print("  Area:", self.area())
        print("  Perimeter:", self.perimeter())
    }
+++

def main() {
    var r = Rectangle()
    r.width  = 5
    r.height = 3
    r.describe()
}
