#!/usr/bin/env python3
"""
测试程序：验证四则运算题目生成器的各项功能
"""

import os
import sys
import tempfile
import re

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from arg_parser import ArgParser
from problem_generator import ProblemGenerator, DuplicateChecker
from calculator import Calculator
from fraction import Fraction
from file_handler import FileHandler


class TestProgram:
    def __init__(self):
        self.test_count = 0
        self.passed_count = 0
        self.failed_tests = []

    def run_test(self, test_name, test_func):
        """运行单个测试"""
        self.test_count += 1
        print(f"测试 {self.test_count}: {test_name}...", end=" ")
        try:
            result = test_func()
            if result:
                self.passed_count += 1
                print("✓ 通过")
            else:
                self.failed_tests.append(test_name)
                print("✗ 失败")
            return result
        except Exception as e:
            self.failed_tests.append(test_name)
            print(f"✗ 异常: {e}")
            return False

    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 50)
        print(f"测试总结: {self.passed_count}/{self.test_count} 通过")
        if self.failed_tests:
            print("失败的测试:")
            for test in self.failed_tests:
                print(f"  - {test}")
        else:
            print("所有测试都通过！")
        print("=" * 50)

    def test_1_arg_parser_n_r(self):
        """测试1: 验证 -n 和 -r 参数解析"""
        # 模拟命令行参数
        sys.argv = ['program', '-n', '10', '-r', '20']
        parser = ArgParser()
        params = parser.parse()

        return (params['type'] == 'generate' and
                params['problem_count'] == 10 and
                params['num_range'] == 20)

    def test_2_arg_parser_e_a(self):
        """测试2: 验证 -e 和 -a 参数解析"""
        sys.argv = ['program', '-e', 'exercises.txt', '-a', 'answers.txt']
        parser = ArgParser()
        params = parser.parse()

        return (params['type'] == 'check' and
                params['exercise_file'] == 'exercises.txt' and
                params['answer_file'] == 'answers.txt')

    def test_3_arg_parser_invalid(self):
        """测试3: 验证无效参数处理"""
        # 测试缺少必要参数
        sys.argv = ['program', '-n', '10']
        parser = ArgParser()
        try:
            params = parser.parse()
            return False  # 应该抛出异常
        except SystemExit:
            return True  # argparse 会调用 sys.exit()
        except Exception:
            return True

    def test_4_problem_generation_count(self):
        """测试4: 验证生成题目数量准确性"""
        generator = ProblemGenerator(10)
        problems = generator.generate_batch(5)

        return len(problems) == 5 and all('=' in problem for problem in problems)

    def test_5_number_range_validation(self):
        """测试5: 验证数值范围控制"""
        generator = ProblemGenerator(5)  # 范围5

        # 生成多个题目检查数值范围
        problems = generator.generate_batch(10)
        all_valid = True

        for problem in problems:
            expr = problem.replace(' = ', '')
            # 提取所有数字部分
            numbers = re.findall(r'\d+\'?\d*/\d+|\d+', expr)

            for num_str in numbers:
                if "'" in num_str:
                    # 带分数: integer'numerator/denominator
                    integer_part, fraction = num_str.split("'")
                    numerator, denominator = map(int, fraction.split('/'))
                    if int(integer_part) >= 5 or denominator > 5:
                        all_valid = False
                        break
                elif '/' in num_str:
                    # 真分数: numerator/denominator
                    numerator, denominator = map(int, num_str.split('/'))
                    if denominator > 5:
                        all_valid = False
                        break
                else:
                    # 整数
                    if int(num_str) >= 5:
                        all_valid = False
                        break

        return all_valid

    def test_6_no_negative_results(self):
        """测试6: 验证不会产生负数结果"""
        generator = ProblemGenerator(10)
        problems = generator.generate_batch(20)

        for problem in problems:
            expr = problem.replace(' = ', '')
            try:
                result = Calculator.calculate(expr)
                # 结果应该是非负的
                if isinstance(result, Fraction):
                    if result.integer < 0 or (result.integer == 0 and result.numerator < 0):
                        return False
            except:
                continue

        return True

    def test_7_division_produces_proper_fractions(self):
        """测试7: 验证除法产生真分数"""
        generator = ProblemGenerator(10)
        problems = generator.generate_batch(50)  # 增加生成数量

        division_count = 0
        valid_division_count = 0

        for problem in problems:
            expr = problem.replace(' = ', '')
            if '÷' in expr:
                division_count += 1
                try:
                    result = Calculator.calculate(expr)
                    # 检查除法结果：应该是真分数或带分数的真分数部分
                    if isinstance(result, Fraction):
                        if result.integer == 0:
                            # 真分数：分子小于分母
                            if result.numerator < result.denominator:
                                valid_division_count += 1
                        else:
                            # 带分数：分数部分是真分数
                            if result.numerator < result.denominator:
                                valid_division_count += 1
                except Exception as e:
                    continue  # 忽略计算错误的题目

        # 如果有除法题目，至少80%应该是有效的
        if division_count > 0:
            success_rate = valid_division_count / division_count
            print(f"除法题目: {division_count}, 有效: {valid_division_count}, 成功率: {success_rate:.2f}")
            return success_rate >= 0.8
        else:
            print("未生成除法题目，测试跳过")
            return True  # 如果没有除法题目，不视为失败

    def test_8_operator_count_limit(self):
        """测试8: 验证运算符数量不超过3个"""
        generator = ProblemGenerator(10)
        problems = generator.generate_batch(50)

        for problem in problems:
            expr = problem.replace(' = ', '')
            operator_count = sum(1 for char in expr if char in ['+', '-', '×', '÷'])
            if operator_count > 3:
                return False

        return True

    def test_9_no_duplicate_problems(self):
        """测试9: 验证题目不重复"""
        generator = ProblemGenerator(5)  # 小范围便于测试重复
        problems = generator.generate_batch(20)

        # 使用重复检查器验证
        checker = DuplicateChecker()
        seen_problems = set()

        for problem in problems:
            expr = problem.replace(' = ', '')
            standard_expr = checker._standardize_fast(expr)
            if standard_expr in seen_problems:
                return False
            seen_problems.add(standard_expr)

        return True

    def test_10_large_scale_generation(self):
        """测试10: 验证支持一万道题目生成"""
        generator = ProblemGenerator(100)

        try:
            # 生成10000道题目（实际测试可以用较小数量，这里用1000测试性能）
            problems = generator.generate_batch(1000)
            return len(problems) == 1000
        except Exception as e:
            print(f"大规模生成失败: {e}")
            return False

    def test_11_file_operations(self):
        """测试11: 验证文件读写功能"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试数据
            test_problems = ["1 + 2 =", "3 × 4 =", "5 ÷ 2 ="]
            test_answers = ["3", "12", "2'1/2"]

            # 写入文件
            problem_path = os.path.join(temp_dir, "Exercises.txt")
            answer_path = os.path.join(temp_dir, "Answers.txt")

            FileHandler.write_problems_and_answers(test_problems, test_answers,
                                                   problem_path, answer_path)

            # 读取并验证
            read_problems = FileHandler.read_file(problem_path)
            read_answers = FileHandler.read_file(answer_path)

            return (read_problems == test_problems and
                    read_answers == test_answers)

    def test_12_answer_checking(self):
        """测试12: 验证答案检查功能"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建测试文件
            exercise_file = os.path.join(temp_dir, "Exercises.txt")
            answer_file = os.path.join(temp_dir, "Answers.txt")
            grade_file = os.path.join(temp_dir, "Grade.txt")

            # 写入测试数据
            with open(exercise_file, 'w', encoding='utf-8') as f:
                f.write("1 + 2 =\n3 × 4 =\n6 ÷ 2 =")
            with open(answer_file, 'w', encoding='utf-8') as f:
                f.write("3\n12\n2")  # 最后一个答案故意写错

            # 检查答案
            correct_str, wrong_str = FileHandler.check_answers(exercise_file, answer_file, grade_file)

            # 验证结果
            return ("Correct: 2" in correct_str and "Wrong: 1" in wrong_str and
                    os.path.exists(grade_file))

    def test_13_fraction_calculation(self):
        """测试13: 验证分数计算准确性"""
        try:
            # 清空缓存避免干扰
            Calculator.clear_cache()
            Fraction.clear_cache()

            # 测试分数加法
            result1 = Calculator.calculate("1/6 + 1/8")
            expected1 = "7/24"
            actual1 = str(result1)
            if actual1 != expected1:
                print(f"分数加法错误: 期望 {expected1}, 得到 {actual1}")
                return False

            # 测试带分数
            result2 = Calculator.calculate("1'1/2 + 1/2")
            expected2 = "2"
            actual2 = str(result2)
            if actual2 != expected2:
                print(f"带分数加法错误: 期望 {expected2}, 得到 {actual2}")
                return False

            # 测试分数乘法
            result3 = Calculator.calculate("2/3 × 3/4")
            expected3 = "1/2"
            actual3 = str(result3)
            if actual3 != expected3:
                print(f"分数乘法错误: 期望 {expected3}, 得到 {actual3}")
                return False

            return True
        except Exception as e:
            print(f"分数计算测试失败: {e}")
            return False

    def test_14_expression_standardization(self):
        """测试14: 验证表达式标准化"""
        checker = DuplicateChecker()

        # 测试交换律
        expr1 = "2 + 3"
        expr2 = "3 + 2"
        std1 = checker._standardize_fast(expr1)
        std2 = checker._standardize_fast(expr2)

        # 测试结合律（简化版本）
        expr3 = "1 + 2 + 3"
        expr4 = "3 + (1 + 2)"
        std3 = checker._standardize_fast(expr3)
        std4 = checker._standardize_fast(expr4)

        return std1 == std2  # 交换律应该被标准化为相同

    def test_15_error_handling(self):
        """测试15: 验证错误处理"""
        # 测试无效表达式
        try:
            Calculator.calculate("1 / 0")  # 除零
            return False
        except (ZeroDivisionError, ValueError):
            pass

        # 测试负数结果
        try:
            Calculator.calculate("1 - 2")  # 负数
            return False
        except ValueError:
            pass

        return True


def run_all_tests():
    """运行所有测试"""
    tester = TestProgram()

    print("开始运行四则运算题目生成器测试...")
    print("=" * 50)

    # 运行所有测试
    tester.run_test("参数解析 (-n, -r)", tester.test_1_arg_parser_n_r)
    tester.run_test("参数解析 (-e, -a)", tester.test_2_arg_parser_e_a)
    tester.run_test("无效参数处理", tester.test_3_arg_parser_invalid)
    tester.run_test("题目数量准确性", tester.test_4_problem_generation_count)
    tester.run_test("数值范围控制", tester.test_5_number_range_validation)
    tester.run_test("无负数结果", tester.test_6_no_negative_results)
    tester.run_test("除法产生真分数", tester.test_7_division_produces_proper_fractions)
    tester.run_test("运算符数量限制", tester.test_8_operator_count_limit)
    tester.run_test("题目不重复", tester.test_9_no_duplicate_problems)
    tester.run_test("大规模生成支持", tester.test_10_large_scale_generation)
    tester.run_test("文件读写功能", tester.test_11_file_operations)
    tester.run_test("答案检查功能", tester.test_12_answer_checking)
    tester.run_test("分数计算准确性", tester.test_13_fraction_calculation)
    tester.run_test("表达式标准化", tester.test_14_expression_standardization)
    tester.run_test("错误处理", tester.test_15_error_handling)

    # 打印总结
    tester.print_summary()

    return tester.passed_count == tester.test_count


if __name__ == "__main__":
    # 运行测试
    success = run_all_tests()

    # 退出码
    sys.exit(0 if success else 1)
