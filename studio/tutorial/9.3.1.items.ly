def main() {
    map prices = {"apple": 1.20, "banana": 0.50, "cherry": 2.99}

    given pair in prices.items()
        print(pair[0], "costs", pair[1])
    done
}
