def main() {
    map capitals = {"France": "Paris", "Japan": "Tokyo", "Brazil": "Brasília"}

    var country
    given country in capitals
        print(country, "->", capitals[country])
    done
}
