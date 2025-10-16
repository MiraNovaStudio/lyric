# This file demonstrates lex errors (unexpected characters)

def main() {
    print("About to cause a lex error...")
    
    # This will cause a lex error - unexpected character '@'
    @invalid_character = 42
}
