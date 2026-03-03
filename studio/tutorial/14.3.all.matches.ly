def main() {
    rex word_pattern = regex("/\w+/")
    str sentence = "Lyric is expressive and clear"

    arr words = word_pattern.findall(sentence)
    str word

    print("Sentence:", sentence)
    print("Words found:")
    for word in words
        print(" -", word)
    done
    print("Total word count:", words.len())
}
