def main() {
    # Run second only if first succeeds
    str out1
    exec("echo step-one") && exec("echo step-two") -> out1
    print(out1)   # step-two

    # Run second only if first fails
    str out2
    exec("exit 1") || exec("echo fallback") -> out2
    print(out2)   # fallback

    # Short-circuits: if first fails, second doesn't run
    str out3
    exec("exit 1") && exec("echo skipped") -> out3
    print(out3)   # (empty)
}
