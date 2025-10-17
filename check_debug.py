from calculator import Calculator
from pathlib import Path

p_ex = Path('d:/jiedui/Exercises.txt')
p_ans = Path('d:/jiedui/Answers.txt')
ex_lines = [l.strip() for l in p_ex.read_text(encoding='utf-8').splitlines() if l.strip()]
ans_lines = [l.strip() for l in p_ans.read_text(encoding='utf-8').splitlines() if l.strip()]

import re

for i, (ex, an) in enumerate(zip(ex_lines, ans_lines), 1):
    expr = re.sub(r"\s*=\s*$", "", ex).strip()
    try:
        calc = Calculator.calculate(expr)
        calc_str = str(calc)
    except Exception as e:
        calc_str = f'<ERROR: {e}>'
    print(f"{i}. expr= {expr}")
    print(f"   file_answer= {repr(an)}")
    print(f"   calc_answer= {repr(calc_str)}")
    print(f"   equal? {calc_str == an}")
    print()
