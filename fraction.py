class Fraction:
    # 添加分数对象缓存
    _fraction_cache = {}

    def __init__(self, numerator, denominator=1, integer=0):
        """初始化分数"""
        # 立即检查分母是否为0
        if denominator == 0:
            raise ZeroDivisionError("分母不能为0")

        self.integer = integer
        self.numerator = numerator
        self.denominator = denominator
        self._simplify_fast()

    def _simplify_fast(self):
        """快速化简分数"""
        # 如果分子为0，直接设为0
        if self.numerator == 0:
            self.integer = 0
            self.denominator = 1
            return

        # 假分数转为带分数
        if self.numerator >= self.denominator:
            self.integer += self.numerator // self.denominator
            self.numerator = self.numerator % self.denominator

        # 如果分子为0，调整整数部分
        if self.numerator == 0:
            self.denominator = 1
            return

        # 快速约分
        gcd_val = self._gcd_fast(abs(self.numerator), self.denominator)
        if gcd_val > 1:
            self.numerator //= gcd_val
            self.denominator //= gcd_val

    @staticmethod
    def _gcd_fast(a, b):
        """快速计算最大公约数"""
        while b:
            a, b = b, a % b
        return a

    def __add__(self, other):
        """分数加法"""
        if isinstance(other, int):
            other = Fraction(other, 1)

        # 转为假分数计算
        num1 = self.integer * self.denominator + self.numerator
        den1 = self.denominator

        num2 = other.integer * other.denominator + other.numerator
        den2 = other.denominator

        # 通分相加
        new_numerator = num1 * den2 + num2 * den1
        new_denominator = den1 * den2

        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        """分数减法"""
        if isinstance(other, int):
            other = Fraction(other, 1)

        num1 = self.integer * self.denominator + self.numerator
        den1 = self.denominator

        num2 = other.integer * other.denominator + other.numerator
        den2 = other.denominator

        # 检查结果是否为负数
        if num1 * den2 < num2 * den1:
            raise ValueError("减法结果不能为负数")

        new_numerator = num1 * den2 - num2 * den1
        new_denominator = den1 * den2

        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        """分数乘法"""
        if isinstance(other, int):
            other = Fraction(other, 1)

        num1 = self.integer * self.denominator + self.numerator
        den1 = self.denominator

        num2 = other.integer * other.denominator + other.numerator
        den2 = other.denominator

        new_numerator = num1 * num2
        new_denominator = den1 * den2

        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        """分数除法"""
        if isinstance(other, int):
            other = Fraction(other, 1)

        # 检查除数是否为0
        if other.integer == 0 and other.numerator == 0:
            raise ZeroDivisionError("除数不能为0")

        # 转为假分数计算
        num1 = self.integer * self.denominator + self.numerator
        den1 = self.denominator

        num2 = other.integer * other.denominator + other.numerator
        den2 = other.denominator

        # 乘以倒数
        new_numerator = num1 * den2
        new_denominator = den1 * num2

        # 检查分母是否为0
        if new_denominator == 0:
            raise ZeroDivisionError("除数不能为0")

        result = Fraction(new_numerator, new_denominator)

        # 检查结果是否为真分数
        if result.integer > 0:
            # 带分数：确保分数部分是真分数
            if result.numerator >= result.denominator:
                raise ValueError("除法结果必须为真分数")
        else:
            # 真分数：分子必须小于分母
            if result.numerator >= result.denominator:
                raise ValueError("除法结果必须为真分数")

        return result

    def __str__(self):
        """格式化输出"""
        if self.integer != 0:
            if self.numerator == 0:
                return str(self.integer)
            else:
                return f"{self.integer}'{self.numerator}/{self.denominator}"
        else:
            if self.numerator == 0:
                return "0"
            else:
                return f"{self.numerator}/{self.denominator}"

    @staticmethod
    def from_str(s):
        """从字符串解析分数"""
        # 检查缓存
        if s in Fraction._fraction_cache:
            return Fraction._fraction_cache[s]

        try:
            if "'" in s:
                # 带分数: intergenerational/denominator
                integer_part, frac_part = s.split("'")
                numerator, denominator = map(int, frac_part.split("/"))
                result = Fraction(numerator, denominator, int(integer_part))
            elif "/" in s:
                # 真分数: numerator/denominator
                numerator, denominator = map(int, s.split("/"))
                result = Fraction(numerator, denominator)
            else:
                # 整数
                result = Fraction(int(s), 1)

            Fraction._fraction_cache[s] = result
            return result
        except Exception as e:
            raise ValueError(f"无法解析分数: {s}, 错误: {e}")

    @staticmethod
    def clear_cache():
        """清空分数缓存"""
        Fraction._fraction_cache.clear()
