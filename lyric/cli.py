# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the MIT License with Source Attribution

"""Command-line interface for Lyric interpreter."""

import sys
import os
from lyric.errors import LexError, ParseError, RuntimeErrorLyric, SyntaxErrorLyric, NameErrorLyric
from lyric.parser import parse
from lyric.interpreter import evaluate


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.5.0")
    elif command == "--help":
        print("Lyric Language Interpreter")
        print("")
        print("Usage:")
        print("  lyric --version                    Show version information")
        print("  lyric --help                       Show this help message")
        print("  lyric run <file.ly>               Run a Lyric source file")
        print("  lyric <file.ly>                   Run a Lyric source file (shorthand)")
        print("")
        print("Examples:")
        print("  lyric run hello.ly")
        print("  lyric hello.ly")
        sys.exit(0)
    elif command == "run":
        if len(sys.argv) < 3:
            print("Usage: lyric run <file.ly>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        _execute_file(file_path)
    elif command.endswith('.ly'):
        # Treat as shorthand for "lyric run <file.ly>"
        file_path = command
        _execute_file(file_path)
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly>")
        sys.exit(1)


def _remove_shebang(source: str) -> str:
    """Remove shebang line from source code if present."""
    lines = source.splitlines()
    
    # Check if first line is a shebang
    if lines and lines[0].startswith('#!'):
        # Remove the shebang line
        return '\n'.join(lines[1:])
    
    return source


def _execute_file(file_path: str):
    """Execute a Lyric source file."""
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
        
        # Remove shebang line if present
        source = _remove_shebang(source)
        
        # Parse the source code
        ast = parse(source)
        
        # Execute the program
        evaluate(ast)
        
    except (LexError, ParseError, SyntaxErrorLyric) as e:
        # Syntax/lexical errors
        if hasattr(e, 'line') and e.line > 0:
            print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except (RuntimeErrorLyric, NameErrorLyric) as e:
        # Runtime errors
        if hasattr(e, 'line') and e.line > 0:
            print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"{e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()