"""
Command-line interface for the Lyric interpreter.
"""

import sys
import os
import argparse
from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import LexError, ParseError, RuntimeErrorLyric


def main():
    """Main entry point for the lyric command."""
    parser = argparse.ArgumentParser(description='Lyric Language Interpreter')
    parser.add_argument('--version', action='version', version='Lyric 0.0.4')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a Lyric program')
    run_parser.add_argument('file', help='Path to the .ly file to run')
    run_parser.add_argument('--debug', action='store_true', help='Enable debug mode with stack traces')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        file_path = args.file
        
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

            # Parse the source code
            program = parse(source, file_path)

            # Create interpreter with debug mode
            interpreter = Interpreter(debug_mode=args.debug)
            
            # Execute the program
            interpreter.interpret(program)

        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            sys.exit(1)
        except LexError as e:
            print(str(e))
            sys.exit(1)
        except ParseError as e:
            print(str(e))
            sys.exit(1)
        except RuntimeErrorLyric as e:
            print(str(e))
            if args.debug and e.stack_trace:
                print()
                print(e.format_debug_info())
            sys.exit(1)
        except Exception as e:
            print(f"Error in '{file_path}': {e}")
            if args.debug:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
