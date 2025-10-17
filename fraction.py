class Fraction:
    def __init__(self, numerator, denominator=1, integer=0):
        """初始化分数：integer（整数部分）、numerator（分子）、denominator（分母）"""
        self.integer = integer  # 带分数整数部分
        self.numerator = numerator  # 分子
        self.denominator = denominator  # 分母
        self._simplify()  # 初始化时自动化简

    def _simplify(self):
        """化简分数为最简形式，分离带分数整数部分"""
        if self.denominator == 0:
            raise ZeroDivisionError("分母不能为0")
        
        # 假分数转为带分数（分子≥分母时）
        if self.numerator >= self.denominator:
            self.integer += self.numerator // self.denominator
            self.numerator = self.numerator % self.denominator
        
        # 约分（通过最大公约数）
        gcd_val = self._gcd(abs(self.numerator), self.denominator)
        if gcd_val != 0:
            self.numerator //= gcd_val
            self.denominator //= gcd_val

    @staticmethod
    def _gcd(a, b):
        """计算最大公约数"""
        while b:
            a, b = b, a % b
        return a

    # 四则运算重载
    def __add__(self, other):
        """分数加法"""
        if isinstance(other, int):
            other = Fraction(other)
        # 统一转为假分数计算
        self_total = self.integer * self.denominator + self.numerator
        other_total = other.integer * other.denominator + other.numerator
        new_denominator = self.denominator * other.denominator
        new_numerator = self_total * other.denominator + other_total * self.denominator
        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        """分数减法（确保结果非负）"""
        if isinstance(other, int):
            other = Fraction(other)
        self_total = self.integer * self.denominator + self.numerator
        other_total = other.integer * other.denominator + other.numerator
        if self_total < other_total:
            raise ValueError("减法结果不能为负数")
        new_denominator = self.denominator * other.denominator
        new_numerator = self_total * other.denominator - other_total * self.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        """分数乘法"""
        if isinstance(other, int):
            other = Fraction(other)
        self_total = self.integer * self.denominator + self.numerator
        other_total = other.integer * other.denominator + other.numerator
        new_numerator = self_total * other_total
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        """分数除法（确保结果为真分数）"""
        if isinstance(other, int):
            other = Fraction(other)
        # 检查除数为0
        other_total = other.integer * other.denominator + other.numerator
        if other_total == 0:
            raise ZeroDivisionError("除数不能为0")
        # 乘以倒数
        reciprocal = Fraction(other.denominator, other.numerator, other.integer)
        result = self * reciprocal
        # 检查结果是否为真分数
        if result.numerator % result.denominator == 0:
            raise ValueError("除法结果必须为真分数")
        return result

    def __str__(self):
        """格式化输出：带分数（如2'3/8）或真分数（如3/5）"""
        if self.integer != 0:
            return f"{self.integer}'{self.numerator}/{self.denominator}" if self.numerator != 0 else str(self.integer)
        else:
            return f"{self.numerator}/{self.denominator}" if self.numerator != 0 else "0"

    @staticmethod
    def from_str(s):
        """从字符串解析分数（支持自然数、真分数、带分数）"""
        if "'" in s:
            # 带分数（如2'3/8）
            integer_part, frac_part = s.split("'")
            numerator, denominator = map(int, frac_part.split("/"))
            return Fraction(numerator, denominator, int(integer_part))
        elif "/" in s:
            # 真分数（如3/5）
            numerator, denominator = map(int, s.split("/"))
            return Fraction(numerator, denominator)
        else:
            # 自然数（如5）
            return Fraction(int(s), 1)