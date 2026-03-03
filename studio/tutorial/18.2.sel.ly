# Bind sqrt and pi directly into scope — no "math." prefix needed
importpy math; sqrt, pi

def main() {
    print("Square root of 16:", sqrt(16.0))
    print("Pi:", pi)
}
