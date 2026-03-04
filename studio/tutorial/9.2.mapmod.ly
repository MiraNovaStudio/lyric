def main() {
    map info = {"language": "Lyric"}
    print("Before changes:", info)

    info["version"] = "0.8.4"      # add a new key
    info["language"] = "Lyric 2"   # update existing key

    print("After adding 'version' and updating 'language':", info)
}
