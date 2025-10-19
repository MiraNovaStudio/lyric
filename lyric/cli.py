"""Command-line interface for Lyric interpreter."""

import sys
import os
from lyric.errors import LexError, ParseError, RuntimeErrorLyric

def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric run <file.ly>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.1")
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file.ly>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        
        print("execution not implemented")
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric run <file.ly>")
        sys.exit(1)
