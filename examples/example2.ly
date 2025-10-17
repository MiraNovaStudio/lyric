# Lyric Advanced Example — Inheritance, Access Control, and Typed Functions
# Target: Version 0.3.1 and later

# ---------------------------
# Base class demonstrating constructor and method
# ---------------------------
class Shape:
  var name
  var area

  def Shape(str n) {
    self.name = n
    self.area = 0
    print("Shape created:", self.name)
  }

  public def describe() {
    print("This is a shape named", self.name)
  }

  protected def compute_area() {
    print("Base class has no specific area formula.")
  }
+++

# ---------------------------
# Derived class with inheritance
# ---------------------------
class Rectangle based on Shape:
  var width
  var height

  def Rectangle(int w, int h) {
    self.width = w
    self.height = h
    print("Rectangle initialized — width:", w, "height:", h)
  }

  # This function overrides compute_area() from Shape
  public def compute_area() {
    int area = self.width * self.height
    self.area = area
    print("Computed rectangle area:", area)
  }

  private def log_creation() {
    print("(Rectangle object initialized successfully)")
  }
+++

# ---------------------------
# Example of a typed free function
# ---------------------------
def int square(int a, int b) {
  int area = a * b
  return area
}

# ---------------------------
# Main program
# ---------------------------
def main() {
  print("=== Lyric Advanced Example ===")

  # Test typed function
  int result = square(5, 10)
  print("Area from square():", result)

  # Create base and derived objects
  var s = Shape("GenericShape")
  var r = Rectangle(5, 7)

  # Automatic constructor chaining: Shape() → Rectangle()
  # Both constructors run in sequence.

  s.describe()
  r.describe()

  # Override demonstration
  r.compute_area()

  # Test logical type
  god visible = true
  bin active = false
  print("Visible:", visible, "Active:", active)

  print("Program finished successfully.")
}
