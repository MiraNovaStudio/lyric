def main() {
    str result
    exec("echo hello world") | exec("cat") -> result
    print(result)   # hello world

    # Pipe to print directly
    exec("echo Piped directly to print") | print
}
