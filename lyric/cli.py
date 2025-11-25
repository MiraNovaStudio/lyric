# Lyric Programming Language
# Copyright (c) 2025 MiraNova Studios
# Designed and Architected by Michael (Aeonath) and ChatGPT
# Implemented by Claude
# Licensed under the GNU General Public License v3.0

"""Command-line interface for Lyric interpreter."""

import sys
import os
from lyric.errors import LexError, ParseError, RuntimeErrorLyric, SyntaxErrorLyric, NameErrorLyric
from lyric.parser import parse, Parser
from lyric.lexer import tokenize
from lyric.interpreter import evaluate, Interpreter


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly> | lyric -i [code]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "--version":
        print("Lyric 0.7.0")
    elif command == "--help":
        print("Lyric Language Interpreter")
        print("")
        print("Usage:")
        print("  lyric --version                    Show version information")
        print("  lyric --help                       Show this help message")
        print("  lyric run <file.ly>               Run a Lyric source file")
        print("  lyric <file.ly>                   Run a Lyric source file (shorthand)")
        print("  lyric -i [code]                   Interactive mode (REPL) or execute immediate code")
        print("")
        print("Examples:")
        print("  lyric run hello.ly")
        print("  lyric hello.ly")
        print('  lyric -i "print(2 + 2)"')
        print("  lyric -i                           Start REPL")
        sys.exit(0)
    elif command == "-i":
        # Interactive/Immediate mode
        if len(sys.argv) > 2:
            # Execute immediate code passed as argument
            code = ' '.join(sys.argv[2:])
            _execute_immediate(code)
        else:
            # Start REPL
            _start_repl()
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
        print("Usage: lyric --version | lyric --help | lyric run <file.ly> | lyric <file.ly> | lyric -i [code]")
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
        
        # Execute the program, passing the source file path for relative imports
        evaluate(ast, source_file=file_path)
        
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


def _execute_immediate(code: str):
    """Execute immediate code in interactive mode (no main() required)."""
    try:
        # Create parser with interactive mode enabled
        tokens = tokenize(code)
        parser = Parser(tokens)
        parser._interactive_mode = True  # Mark as interactive mode
        parser.is_top_level = False  # Disable top-level restrictions
        ast = parser.parse()
        
        # Execute the code
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
    except (LexError, ParseError, SyntaxErrorLyric) as e:
        if hasattr(e, 'line') and e.line > 0:
            print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"Error: {e}")
        sys.exit(1)
    except (RuntimeErrorLyric, NameErrorLyric) as e:
        if hasattr(e, 'line') and e.line > 0:
            print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
        else:
            print(f"{e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def _start_repl():
    """Start interactive REPL (Read-Eval-Print Loop)."""
    print("Lyric 0.7.0 Interactive Mode")
    print('Type "exit()" or press Ctrl+C to quit')
    print()
    
    interpreter = Interpreter()
    buffer = []
    in_block = False
    block_depth = 0
    
    while True:
        try:
            # Show prompt
            if in_block:
                line = input("...   ")
            else:
                line = input("lyric> ")
            
            # Check for exit command
            if line.strip() in ('exit()', 'quit()', 'exit', 'quit'):
                print("Goodbye!")
                break
            
            # Add line to buffer
            buffer.append(line)
            
            # Check if we're in a block (function, class, control structure)
            stripped = line.strip()
            if stripped:
                # Check for block start
                if any(keyword in stripped for keyword in ['def ', 'class ', 'if ', 'given ', 'for ', 'try:', 'catch:', 'finally:']):
                    in_block = True
                    block_depth += 1
                
                # Track braces and block ends
                if '{' in line:
                    block_depth += line.count('{')
                if '}' in line:
                    block_depth -= line.count('}')
                if stripped in ('end', 'done', 'fade', '+++'):
                    block_depth -= 1
                
                # Check if block is complete
                if in_block and block_depth <= 0:
                    in_block = False
                    block_depth = 0
            
            # If not in block, execute the buffer
            if not in_block and buffer:
                code = '\n'.join(buffer)
                buffer = []
                
                try:
                    # Parse and execute (with top-level restrictions disabled)
                    tokens = tokenize(code)
                    parser = Parser(tokens)
                    parser._interactive_mode = True  # Mark as interactive mode
                    parser.is_top_level = False  # Disable top-level restrictions in REPL
                    ast = parser.parse()
                    
                    # Execute using the persistent interpreter
                    interpreter.evaluate(ast)
                    
                except (LexError, ParseError, SyntaxErrorLyric) as e:
                    if hasattr(e, 'line') and e.line > 0:
                        print(f"Error [line {e.line}]: {e.args[0] if e.args else str(e)}")
                    else:
                        print(f"Error: {e}")
                except (RuntimeErrorLyric, NameErrorLyric) as e:
                    if hasattr(e, 'line') and e.line > 0:
                        print(f"Runtime error [line {e.line}]: {e.args[0] if e.args else str(e)}")
                    else:
                        print(f"{e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    import traceback
                    traceback.print_exc()
        
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
            buffer = []
            in_block = False
            block_depth = 0
            continue
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()