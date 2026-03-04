def main() {
    if 5
        print("5 is truthy — any non-zero number counts as True")
    end

    if not 0
        print("0 is falsy — zero counts as False")
    end

    if "hello"
        print("\"hello\" is truthy — non-empty strings count as True")
    end

    if not ""
        print("\"\" is falsy — empty strings count as False")
    end
}
