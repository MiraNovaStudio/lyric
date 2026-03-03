# main.ly
import utils; greet, Counter

def main() {
    greet("Bob")           # Direct access, no "utils." prefix
    obj c = Counter(10)
    c.increment()
    print("Counter:", c.value)
}
