"""
Command-line interface for the Lyric interpreter.
"""

import sys
import os
from pathlib import Path
from lyric.lexer import tokenize
from lyric.parser import parse
from lyric.interpreter import interpret
from lyric.errors import LexError, ParseError, RuntimeErrorLyric


def main():
    """Main entry point for the lyric command."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric run <file>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.0.2")
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        
        # Validate that file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        
        # Check if it's a .ly file
        if not file_path.endswith('.ly'):
            print(f"Error: Expected .ly file, got '{file_path}'")
            sys.exit(1)
        
        # Read and execute the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Tokenize the source code
            tokens = tokenize(source)
            
            # Parse the source code
            program = parse(source)
            
            # Execute the program
            interpret(program)
            
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        except LexError as e:
            print(f"Lexical Error in '{file_path}': {e}")
            sys.exit(1)
        except ParseError as e:
            print(f"Parse Error in '{file_path}': {e}")
            sys.exit(1)
        except RuntimeErrorLyric as e:
            print(f"Runtime Error in '{file_path}': {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error in '{file_path}': {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric run <file>")
        sys.exit(1)


if __name__ == "__main__":
    main()
