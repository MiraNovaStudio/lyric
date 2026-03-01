def main() {
    int i
    print("range(1, 6) — from 1 up to (but not including) 6:")
    given i in range(1, 6)
        print(" ", i)
    done

    print("range(0, 10, 2) — even numbers from 0 to 8:")
    given i in range(0, 10, 2)
        print(" ", i)
    done
}
