#!/usr/bin/env python3

import sys
sys.path.append('.')
from lyric.parser import parse
from lyric.interpreter import interpret

# Test simple print with indexing
source = '''
def main() {
    x = [1, 2, 3]
    print(x[0])
}
'''
try:
    program = parse(source, 'test')
    interpret(program)
    print('Simple print with indexing works!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
