def main() {
    str out
    exec("echo step1") | exec("cat") | exec("cat") -> out
    print(out)   # step1
}
