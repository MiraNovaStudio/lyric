def main() {
    # Find the first even number greater than 5
    print("Searching for the first even number greater than 5:")
    given i in range(20)
        if i <= 5
            continue   # skip anything 5 or under
        end
        if i % 2 == 0
            print("Found it:", i)
            break      # stop as soon as we find one
        end
    done
}
