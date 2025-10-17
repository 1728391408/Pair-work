from pathlib import Path
p = Path('d:/jiedui/Exercises.txt')
b = p.read_bytes()
print('bytes (hex first 120):', b[:120].hex())
print('\nraw bytes repr:')
print(repr(b[:200]))
print('\ntry utf-8 decode:')
try:
    s = b.decode('utf-8')
    print(s)
    print('\ncode points of first 200 chars:')
    print([hex(ord(c)) for c in s[:200]])
except Exception as e:
    print('utf8 decode error', e)
    try:
        s = b.decode('gbk')
        print('\nGBK decode:')
        print(s)
        print([hex(ord(c)) for c in s[:200]])
    except Exception as e2:
        print('gbk decode error', e2)
