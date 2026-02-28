def main() {
    map capitals = {"France": "Paris", "Japan": "Tokyo", "Brazil": "Brasília"}

    given country in capitals
        print(country, "->", capitals[country])
    done
}
