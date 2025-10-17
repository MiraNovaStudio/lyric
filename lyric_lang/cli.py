"""
Command-line interface for the Lyric interpreter.
"""

import sys
import os
import argparse
from lyric_lang.parser import parse
from lyric_lang.interpreter import Interpreter
from lyric_lang.errors import LexError, ParseError, RuntimeErrorLyric


def main():
    """Main entry point for the lyric command."""
    parser = argparse.ArgumentParser(description='Lyric Language Interpreter')
    parser.add_argument('--version', action='version', version='Lyric 0.1.9')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with stack traces')
    
    # Allow both subcommand and direct file execution
    parser.add_argument('command_or_file', nargs='?', help='Command (run) or file path to execute')
    parser.add_argument('file', nargs='?', help='Path to the .ly file to run (when using run command)')
    
    args = parser.parse_args()
    
    # Determine the file path and command mode
    if args.command_or_file == 'run':
        # Format: lyric run file_name.ly
        file_path = args.file
        if not file_path:
            print("Error: 'run' command requires a file argument")
            print("Usage: lyric run <file_name.ly>")
            sys.exit(1)
    elif args.command_or_file and not args.command_or_file.startswith('-'):
        # Format: lyric file_name.ly (direct file execution)
        file_path = args.command_or_file
    else:
        # No valid command or file provided
        parser.print_help()
        sys.exit(1)
    
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
        print(f"Traceback (most recent call last):")
        if e.stack_trace:
            for frame in e.stack_trace:
                print(f"  File \"{frame.filename}\", line {frame.line}, in {frame.function_name}")
        print(f"{type(e).__name__}: {e.message}")
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


if __name__ == "__main__":
    main()
