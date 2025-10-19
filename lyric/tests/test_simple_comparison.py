from lyric.parser import parse

def test_simple_comparison():
    """Test parsing a simple comparison."""
    source = "x == 5"
    try:
        ast = parse(source)
        print("Parse successful!")
        print("AST:", ast)
    except Exception as e:
        print("Parse error:", e)

if __name__ == "__main__":
    test_simple_comparison()
