def main() {
    map app = {
        "name": "MyApp",
        "users": [
            {"name": "Alice", "role": "admin"},
            {"name": "Bob",   "role": "user"}
        ],
        "settings": {
            "theme": "dark",
            "language": "en"
        }
    }

    print(app["name"])                      # MyApp
    print(app["users"][0]["name"])          # Alice
    print(app["settings"]["theme"])         # dark
}
