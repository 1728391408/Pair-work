import re
from fraction import Fraction


class Calculator:
    # 添加表达式结果缓存
    _calc_cache = {}

    @staticmethod
    def calculate(expr):
        """计算表达式结果，处理括号优先级（带缓存）"""
        expr = expr.replace(" ", "")  # 移除空格

        # 检查缓存
        if expr in Calculator._calc_cache:
            return Calculator._calc_cache[expr]

        try:
            result = Calculator._eval_recursive(expr)
            Calculator._calc_cache[expr] = result
            return result
        except Exception as e:
            raise ValueError(f"表达式计算失败: {str(e)}")

    @staticmethod
    def calculate_cached(expr):
        """专门用于校验的快速计算（不抛详细异常）"""
        expr_clean = expr.replace(" ", "")
        if expr_clean in Calculator._calc_cache:
            return Calculator._calc_cache[expr_clean]

        try:
            result = Calculator._eval_recursive(expr_clean)
            Calculator._calc_cache[expr_clean] = result
            return result
        except:
            raise ValueError("无效表达式")

    @staticmethod
    def _eval_recursive(expr):
        """递归解析表达式：先算括号，再按优先级运算"""
        # 处理括号（从最内层开始）
        if '(' in expr:
            left = expr.rfind('(')  # 最后一个左括号（最内层）
            right = expr.find(')', left)  # 对应右括号
            inner_result = Calculator._eval_recursive(expr[left + 1:right])
            # 替换括号内容为结果，继续计算
            return Calculator._eval_recursive(expr[:left] + str(inner_result) + expr[right + 1:])

        # 按运算优先级计算：加减最后算，乘除先算
        if '+' in expr or '-' in expr:
            # 拆分表达式（保留运算符）
            parts = re.split(r'([+-])', expr)
            parts = [p for p in parts if p.strip()]  # 去除空字符
            result = Fraction.from_str(parts[0])
            for i in range(1, len(parts), 2):
                op = parts[i]
                num = Fraction.from_str(parts[i + 1])
                if op == '+':
                    result += num
                else:
                    result -= num
            return result

        # 支持 Unicode 运算符和 ASCII 运算符
        if '×' in expr or '÷' in expr or '*' in expr or '/' in expr:
            # 先把 ASCII 运算符规范化为 Unicode，以便重用现有分割逻辑
            expr_norm = expr.replace('*', '×').replace('/', '÷')
            parts = re.split(r'([×÷])', expr_norm)
            parts = [p for p in parts if p.strip()]
            result = Fraction.from_str(parts[0])
            for i in range(1, len(parts), 2):
                op = parts[i]
                num = Fraction.from_str(parts[i + 1])
                if op == '×':
                    result *= num
                else:
                    result /= num
            return result

        # 单一数值
        return Fraction.from_str(expr)

    @staticmethod
    def clear_cache():
        """清空计算缓存"""
        Calculator._calc_cache.clear()
