def main() {
    arr scores = [85, 92, 78, 95, 88]
    int total = 0
    var score

    given score in scores
        total = total + score
    done

    print("Total:", total)
    print("Count:", scores.len())
}
