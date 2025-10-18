import random
import re
from calculator import Calculator


class DuplicateChecker:
    def __init__(self):
        self.generated_set = set()
        self._expr_cache = {}  # 缓存标准化结果

    def is_duplicate(self, expr):
        """判断题目是否重复：标准化后检查是否已存在"""
        standard_expr = self._standardize_fast(expr)
        if standard_expr in self.generated_set:
            return True
        self.generated_set.add(standard_expr)
        return False

    def _standardize_fast(self, expr):
        """快速标准化表达式"""
        if expr in self._expr_cache:
            return self._expr_cache[expr]

        # 快速移除空格和括号
        clean_expr = expr.translate(str.maketrans('', '', ' ()'))

        # 只对简单表达式进行排序（单运算符）
        if clean_expr.count('+') == 1 and clean_expr.count('×') == 0 and clean_expr.count(
                '-') == 0 and clean_expr.count('÷') == 0:
            parts = clean_expr.split('+')
            if all(part.replace('/', '').isdigit() for part in parts):  # 处理分数
                result = '+'.join(sorted(parts))
                self._expr_cache[expr] = result
                return result

        # 处理乘法交换律
        if clean_expr.count('×') == 1 and clean_expr.count('+') == 0 and clean_expr.count(
                '-') == 0 and clean_expr.count('÷') == 0:
            parts = clean_expr.split('×')
            if all(part.replace('/', '').isdigit() for part in parts):
                result = '×'.join(sorted(parts))
                self._expr_cache[expr] = result
                return result

        self._expr_cache[expr] = clean_expr
        return clean_expr


class ProblemGenerator:
    def __init__(self, num_range):
        if num_range < 1:
            raise ValueError("数值范围必须大于0")
        self.num_range = num_range
        self.operators = ['+', '-', '×', '÷']
        self.duplicate_checker = DuplicateChecker()
        self.number_pool = self._precompute_number_pool()

    def _precompute_number_pool(self):
        """预生成常用数值池，确保数值在范围内"""
        pool = []

        # 整数 (0 到 num_range-1)
        for i in range(self.num_range):
            pool.append(str(i))

        # 分数（分母范围：2 到 num_range，分子：1 到 分母-1）
        if self.num_range >= 2:
            for denom in range(2, self.num_range + 1):
                for num in range(1, denom):
                    # 确保分数值小于范围
                    if num < denom:  # 真分数
                        pool.append(f"{num}/{denom}")

        return pool

    def _is_number_in_range(self, num_str):
        """检查数值是否在范围内"""
        if num_str.isdigit():
            return int(num_str) < self.num_range
        elif '/' in num_str:
            if "'" in num_str:
                # 带分数
                integer_part, fraction = num_str.split("'")
                numerator, denominator = map(int, fraction.split('/'))
                return (int(integer_part) < self.num_range and
                        numerator < denominator <= self.num_range)
            else:
                # 真分数
                numerator, denominator = map(int, num_str.split('/'))
                return numerator < denominator <= self.num_range
        return True

    def generate_single_problem(self):
        """生成一道合法且不重复的题目"""
        attempts = 0
        max_attempts = 100  # 增加尝试次数

        while attempts < max_attempts:
            # 随机1-3个运算符
            op_count = random.randint(1, 3)
            expr = self._generate_expression_optimized(op_count)

            # 校验所有数值都在范围内
            if not self._check_all_numbers_in_range(expr):
                attempts += 1
                continue

            # 快速校验合法性
            if self._is_valid_fast(expr):
                if not self.duplicate_checker.is_duplicate(expr):
                    return f"{expr} = "

            attempts += 1

        # 如果尝试次数过多，返回一个简单的保底题目
        simple_num = random.randint(1, max(1, self.num_range - 1))
        return f"{simple_num} + {simple_num} = "

    def _check_all_numbers_in_range(self, expr):
        """检查表达式中所有数值都在范围内"""
        # 分割表达式获取所有数字部分
        parts = re.split(r'[+\-×÷()\s]', expr)
        numbers = [p for p in parts if p and not p.isspace()]

        for num in numbers:
            if not self._is_number_in_range(num):
                return False
        return True

    def _generate_expression_optimized(self, op_count):
        """优化表达式生成"""
        parts = [random.choice(self.number_pool)]

        for i in range(op_count):
            op = random.choice(self.operators)
            num = random.choice(self.number_pool)

            # 简化括号逻辑
            if i > 0 and random.random() < 0.3:
                parts[-1] = f"({parts[-1]})"

            parts.append(op)
            parts.append(num)

        return ' '.join(parts)

    def _is_valid_fast(self, expr):
        """快速校验表达式合法性"""
        try:
            result = Calculator.calculate_cached(expr)

            # 检查除法运算的结果
            if '÷' in expr or '/' in expr:
                # 对于除法，确保结果是真分数或带分数的真分数部分
                if hasattr(result, 'integer'):
                    if result.integer > 0:
                        # 带分数：分数部分必须是真分数
                        if result.numerator >= result.denominator:
                            return False
                    else:
                        # 真分数：分子必须小于分母
                        if result.numerator >= result.denominator:
                            return False
                # 添加对整数结果的处理
                elif isinstance(result, int) and result > 0:
                    # 整数结果也是合法的
                    return True

            return True
        except (ValueError, ZeroDivisionError):
            return False

    def generate_batch(self, count):
        """批量生成题目"""
        results = []
        attempts = 0
        max_total_attempts = count * 5

        while len(results) < count and attempts < max_total_attempts:
            problem = self.generate_single_problem()
            if problem and problem not in results:
                results.append(problem)
            attempts += 1

        return results
