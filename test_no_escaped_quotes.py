#!/usr/bin/env python3

import sys
sys.path.append('.')
from lyric.parser import parse
from lyric.interpreter import interpret

# Test without escaped quotes
source = '''
def main() {
    y = {"key": "value", "number": 42}
    print("y[key] =", y["key"])
}
'''
try:
    program = parse(source, 'test')
    interpret(program)
    print('No escaped quotes case works!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
