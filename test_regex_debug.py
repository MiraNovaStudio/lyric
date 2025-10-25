#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lyric', 'lyric'))

from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter

def test_regex_literal():
    print("Testing regex literal syntax...")
    
    # Test 1: Basic regex literal
    print("\n1. Testing basic regex literal...")
    try:
        code = 'rex pattern = /hello/'
        print(f"Code: {code}")
        
        tokens = tokenize(code)
        print(f"Tokens: {[(t.type, t.value) for t in tokens]}")
        
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST: {ast}")
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        print("✅ Parse and evaluation successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Complex regex
    print("\n2. Testing complex regex...")
    try:
        code = 'rex email = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/'
        print(f"Code: {code}")
        
        tokens = tokenize(code)
        print(f"Tokens: {[(t.type, t.value) for t in tokens]}")
        
        parser = Parser(tokens)
        ast = parser.parse()
        print(f"AST: {ast}")
        
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        print("✅ Parse and evaluation successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_regex_literal()
