# This file demonstrates different types of errors in Lyric
# Each section will cause a different type of error

def main() {
    print("Testing error reporting...")
    
    # This should cause a runtime error - undefined variable
    print("About to access undefined variable...")
    print(undefined_variable)
}

# Uncomment one of the following sections to test different error types:

# Lex Error Example (unexpected character):
# def bad_syntax() {
#     @invalid_character = 42
# }

# Parse Error Example (missing end):
# def incomplete_function() {
#     if true:
#         print("This will cause a parse error")
#     # Missing 'end'
# }

# Runtime Error Example (calling undefined function):
# def call_undefined() {
#     undefined_function()
# }

# Runtime Error Example (wrong argument count):
# def wrong_args() {
#     isinstance(42)  # Missing second argument
# }
