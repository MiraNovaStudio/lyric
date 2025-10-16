#!/usr/bin/env python3

import sys
sys.path.append('.')
from lyric.lexer import tokenize

# Test the tokenization of indexing
source = 'y["key"]'
tokens = tokenize(source, 'test')
print('Indexing tokens:', [f'{t.type}:{t.value}' for t in tokens])
