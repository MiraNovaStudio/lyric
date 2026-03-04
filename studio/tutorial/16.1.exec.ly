def main() {
    int rc = exec("echo Hello from the shell")
    print("Exit code:", rc)   # 0

    if rc == 0
        print("Command succeeded")
    end
}
