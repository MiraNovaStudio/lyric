def main() {
    rex vowels = regex("/[aeiou]/", "i")
    var original = "Hello, World!"
    var replaced = vowels.replace(original, "*")
    print(replaced)   # H*ll*, W*rld!
}
