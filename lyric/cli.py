"""
Command-line interface for the Lyric interpreter.
"""

import sys
import os
from pathlib import Path


def main():
    """Main entry point for the lyric command."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric run <file>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.1")
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        
        # Validate that file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        
        # Check if it's a .lyr file
        if not file_path.endswith('.lyr'):
            print(f"Error: Expected .lyr file, got '{file_path}'")
            sys.exit(1)
        
        print("execution not implemented")
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric run <file>")
        sys.exit(1)


if __name__ == "__main__":
    main()
