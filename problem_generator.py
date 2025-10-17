import random
import re
from calculator import Calculator
from fraction import Fraction

class DuplicateChecker:
    def __init__(self):
        self.generated_set = set()  # 存储标准化后的题目标识

    def is_duplicate(self, expr):
        """判断题目是否重复：标准化后检查是否已存在"""
        standard_expr = self._standardize(expr)
        if standard_expr in self.generated_set:
            return True
        self.generated_set.add(standard_expr)
        return False

    def _standardize(self, expr):
        """标准化表达式：处理交换律、括号扁平化"""
        expr = expr.replace(" ", "").replace("(", "").replace(")", "")  # 去空格和括号
        
        # 处理加法交换律（如3+2→2+3）
        if '+' in expr and not ('-' in expr or '×' in expr or '÷' in expr):
            terms = sorted(expr.split('+'))
            return '+'.join(terms)
        
        # 处理乘法交换律（如6×8→8×6）
        if '×' in expr and not ('-' in expr or '+' in expr or '÷' in expr):
            terms = sorted(expr.split('×'))
            return '×'.join(terms)
        
        # 处理多运算符（如1+2+3→1+2+3，(1+2)+3→1+2+3）
        # 按运算符优先级标准化（此处简化处理，复杂场景可扩展）
        return expr

class ProblemGenerator:
    def __init__(self, num_range):
        self.num_range = num_range  # 数值范围
        self.operators = ['+', '-', '×', '÷']
        self.duplicate_checker = DuplicateChecker()

    def generate_single_problem(self):
        """生成一道合法且不重复的题目"""
        while True:
            # 随机1-3个运算符
            op_count = random.randint(1, 3)
            # 生成表达式
            expr = self._generate_expression(op_count)
            # 校验合法性（运算无异常）
            if self._is_valid(expr):
                # 检查去重
                if not self.duplicate_checker.is_duplicate(expr):
                    return f"{expr} = "

    def _generate_expression(self, op_count):
        """生成含指定数量运算符的表达式，随机添加括号"""
        # 生成第一个数值
        expr = self._generate_number()
        
        for _ in range(op_count):
            op = random.choice(self.operators)
            num = self._generate_number()
            # 30%概率添加括号（仅对已有多元素的表达式）
            if random.random() < 0.3 and len(re.split(r'[+\-×÷]', expr)) > 1:
                expr = f"({expr}) {op} {num}"
            else:
                expr = f"{expr} {op} {num}"
        return expr

    def _generate_number(self):
        """生成数值范围内的自然数或真分数"""
        # 当 num_range 较小时，避免生成无效范围。
        # 设计原则：整数范围为 0..num_range（包含 num_range），分母至少为 2，且分子 < 分母。
        if self.num_range <= 0:
            return '0'

        num_type = random.choice(['integer', 'fraction'])
        # 当范围过小时，优先生成整数以避免无效分数区间
        if num_type == 'integer' or self.num_range < 2:
            # 自然数（0 到 num_range）
            return str(random.randint(0, self.num_range))

        # 真分数（可带整数部分）
        # 整数部分可以为 0..num_range
        integer_part = random.randint(0, self.num_range)

        # 分母取值范围为 2..max(2, num_range)
        denom_min = 2
        denom_max = max(2, self.num_range)
        denominator = random.randint(denom_min, denom_max)

        # 分子必须小于分母，取 1..denominator-1
        numerator = random.randint(1, denominator - 1)

        if integer_part == 0:
            return f"{numerator}/{denominator}"
        else:
            return f"{integer_part}'{numerator}/{denominator}"

    def _is_valid(self, expr):
        """校验表达式合法性：减法非负、除法真分数、无除零"""
        try:
            Calculator.calculate(expr)
            return True
        except (ValueError, ZeroDivisionError):
            return False
