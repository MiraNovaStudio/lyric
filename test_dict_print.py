#!/usr/bin/env python3

import sys
sys.path.append('.')
from lyric.parser import parse
from lyric.interpreter import interpret

# Test print with dictionary indexing
source = '''
def main() {
    y = {"key": "value"}
    print(y["key"])
}
'''
try:
    program = parse(source, 'test')
    interpret(program)
    print('Print with dictionary indexing works!')
except Exception as e:
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
