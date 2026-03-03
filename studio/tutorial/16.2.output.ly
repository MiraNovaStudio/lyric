def main() {
    str output
    exec("echo Hello World") -> output
    print("Captured:", output)   # Hello World

    str listing
    exec("ls -la") -> listing
    print(listing)
}
