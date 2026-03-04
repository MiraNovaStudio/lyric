def main() {
    map data = {"a": 1, "b": 2, "c": 3}

    arr keys = data.keys()
    print("Keys:", keys)

    arr vals = data.values()
    print("Values:", vals)

    var x = data.get("z", 0)
    print("get(\"z\", 0) — key doesn't exist, so default is returned:", x)

    int removed = data.pop("b")
    print("Removed key \"b\", its value was:", removed)
    print("Map after pop:", data)

    map extra = {"d": 4, "e": 5}
    data.update(extra)
    print("After merging {d:4, e:5}, total keys:", data.len())

    map copy = data.copy()
    copy.clear()
    print("After clearing the copy, its length is:", copy.len())
}
