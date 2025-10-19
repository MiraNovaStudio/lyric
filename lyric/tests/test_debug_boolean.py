from lyric.parser import parse
from lyric.interpreter import evaluate

def test_debug_boolean():
    """Debug boolean operations step by step."""
    source = """
def main() {
    print("Starting test")
    x = 5
    print("x =", x)
    if x == 5:
        print("x equals 5")
    else:
        print("x does not equal 5")
    end
    print("Test complete")
}"""
    
    try:
        ast = parse(source)
        print("Parse successful!")
        print("Number of statements:", len(ast.statements))
        
        # Create interpreter and check functions
        from lyric.interpreter import Interpreter
        interpreter = Interpreter()
        
        # Evaluate statements
        for i, statement in enumerate(ast.statements):
            print(f"Evaluating statement {i}: {type(statement).__name__}")
            result = interpreter._evaluate_statement(statement)
            print(f"Statement {i} result: {result}")
        
        print("Functions defined:", list(interpreter.functions.keys()))
        
        # Capture print output
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            # Call main function
            if "main" in interpreter.functions:
                print("Calling main function...")
                interpreter._call_function("main", [])
            else:
                print("Main function not found!")
            
            output = captured_output.getvalue().strip()
            print("Output:", repr(output))
        except Exception as eval_error:
            print("Evaluation error:", eval_error)
            import traceback
            traceback.print_exc()
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        print("Error:", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_debug_boolean()
