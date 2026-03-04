# main.ly
import utils

def main() {
    utils.greet("Alice")
    print("Max size:", utils.MAX_SIZE)

    obj c = utils.Counter(0)
    c.increment()
    print("Counter:", c.value)
}
