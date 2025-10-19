from lyric.parser import parse
from lyric.interpreter import evaluate

def test_simple_boolean():
    """Test simple boolean evaluation."""
    source = """
def main() {
    print("Testing boolean operations")
    x = 5
    print("x =", x)
    if x == 5:
        print("x equals 5")
    end
}"""
    
    try:
        ast = parse(source)
        print("Parse successful!")
        
        # Capture print output
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
            output = captured_output.getvalue().strip()
            print("Evaluation result:", result)
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
    test_simple_boolean()
