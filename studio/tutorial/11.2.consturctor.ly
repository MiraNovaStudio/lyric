class Point:
    x = 0
    y = 0

    def Point(px, py) {
        self.x = px
        self.y = py
    }

    def to_string() {
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    }
+++

def main() {
    var p = Point(3, 7)
    print(p.to_string())   # (3, 7)
    print(p.x)             # 3
}
