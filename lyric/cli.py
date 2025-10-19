"""Command-line interface for Lyric interpreter."""

import sys
import os
from lyric.errors import LexError, ParseError, RuntimeErrorLyric
from lyric.parser import parse
from lyric.interpreter import evaluate


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric run <file.ly>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.0.1")
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file.ly>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        
        # Check file extension
        if not file_path.endswith('.ly'):
            print(f"Error: File '{file_path}' is not a .ly file")
            sys.exit(1)
        
        try:
            # Read and execute the file
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse the source code
            ast = parse(source)
            
            # Execute the program
            evaluate(ast)
            
        except LexError as e:
            print(f"Lexical error: {e}")
            sys.exit(1)
        except ParseError as e:
            print(f"Parse error: {e}")
            sys.exit(1)
        except RuntimeErrorLyric as e:
            print(f"Runtime error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric run <file.ly>")
        sys.exit(1)
