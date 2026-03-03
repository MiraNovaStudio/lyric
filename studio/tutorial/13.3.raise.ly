def validate_age(int age) {
    if age < 0
        raise ValueErrorLyric
    end
    if age > 150
        raise ValueErrorLyric
    end
    return age
}

def main() {
    try:
        validate_age(-5)
    catch:
        print("Invalid age provided")
    fade

    try:
        validate_age(25)
        print("Age is valid")
    catch:
        print("This won't run")
    fade
}
