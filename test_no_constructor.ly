class Point:
    var x
    var y
    
    def move(int dx, int dy) {
        self.x = self.x + dx
        self.y = self.y + dy
    }
+++

def main() {
    point = Point()
    point.x = 10
    point.y = 20
    print("Point:", point.x, point.y)
    point.move(5, 5)
    print("After move:", point.x, point.y)
}
