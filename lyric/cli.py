#!/usr/bin/env python3
"""
Lyric Language CLI
Command-line interface for the Lyric programming language.
"""

import sys
import os
from pathlib import Path
from lyric.lexer import Lexer
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import LexError, ParseError, RuntimeErrorLyric


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
        
        # Execute the Lyric program
        try:
            with open(file_path, 'r') as f:
                source_code = f.read()
            
            # Lexical analysis
            lexer = Lexer(source_code)
            tokens = lexer.tokenize()
            
            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Interpretation
            interpreter = Interpreter()
            interpreter.interpret(ast)
            
        except LexError as e:
            print(f"Lexical Error: {e}")
            sys.exit(1)
        except ParseError as e:
            print(f"Parse Error: {e}")
            sys.exit(1)
        except RuntimeErrorLyric as e:
            print(f"Runtime Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        print("Usage: lyric [--version] [run <file.ly>]")
        sys.exit(1)


if __name__ == "__main__":
    main()
