#!/usr/bin/env python3
"""
Lyric Language CLI
Command-line interface for the Lyric programming language.
"""

import sys
import os
from pathlib import Path


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric [--version] [run <file.ly>]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.1")
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file.ly>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        
        # Validate file path
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        
        if not file_path.endswith('.ly'):
            print(f"Error: File '{file_path}' is not a .ly file")
            sys.exit(1)
        
        print("execution not implemented")
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric [--version] [run <file.ly>]")
        sys.exit(1)


if __name__ == "__main__":
    main()
