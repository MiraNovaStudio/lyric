def main() {
    map person = {"name": "Alice", "age": 30, "city": "Boston"}
    map scores = {"math": 95, "english": 88}
    map config = {"debug": True, "version": "0.8.4"}
    map empty  = {}

    print("person's name:", person["name"])
    print("person's city:", person["city"])
    print("math score:", scores["math"])
    print("debug mode:", config["debug"])
}
