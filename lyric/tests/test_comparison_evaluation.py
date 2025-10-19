from lyric.parser import parse
from lyric.interpreter import evaluate

def test_comparison_evaluation():
    """Test evaluating a comparison."""
    source = """
def main() {
    x = 5
    if x == 5:
        print("x equals 5")
    else:
        print("x does not equal 5")
    end
}"""
    
    try:
        ast = parse(source)
        print("Parse successful!")
        print("AST statements:", len(ast.statements))
        
        # Capture print output
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        try:
            result = evaluate(ast)
            output = captured_output.getvalue().strip()
            print("Evaluation result:", result)
            print("Output:", output)
        except Exception as eval_error:
            print("Evaluation error:", eval_error)
        finally:
            sys.stdout = old_stdout
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_comparison_evaluation()
