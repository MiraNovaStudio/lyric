def main() {
    rex pattern = regex("/(\d{4})-(\d{2})-(\d{2})/")
    var text = "The event is on 2025-12-31 at noon."

    var match = pattern.search(text)

    if match
        print("Full match:", match.group(0))   # 2025-12-31
        print("Year:",       match.group(1))   # 2025
        print("Month:",      match.group(2))   # 12
        print("Day:",        match.group(3))   # 31
    else
        print("No date found")
    end
}
