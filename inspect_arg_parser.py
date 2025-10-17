import importlib
import os
import traceback

print('cwd:', os.getcwd())
print('\nReading file content (first 3000 chars):')
with open('d:/jiedui/arg_parser.py', 'r', encoding='utf-8') as f:
    print(f.read()[:3000])

print('\nAttempting to import arg_parser:')
try:
    m = importlib.import_module('arg_parser')
    print('module:', m)
    print('module file:', getattr(m, '__file__', None))
    names = [name for name in dir(m) if not name.startswith('__')]
    print('exported names:', names)
    print('\nHas ArgParser:', hasattr(m, 'ArgParser'))
    if hasattr(m, 'ArgParser'):
        print('ArgParser object:', m.ArgParser)
except Exception as e:
    print('import error:', type(e), e)
    traceback.print_exc()
