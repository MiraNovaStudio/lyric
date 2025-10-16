# This file demonstrates parse errors (syntax errors)

def main() {
    print("About to cause a parse error...")
    
    # This will cause a parse error - missing 'end'
    if true:
        print("This will cause a parse error")
    # Missing 'end' keyword
}
