import os
from calculator import Calculator
import re


class FileHandler:
    @staticmethod
    def write_problems_and_answers(problems, answers, problem_path="Exercises.txt", answer_path="Answers.txt"):
        """写入题目到Exercises.txt，答案到Answers.txt"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(problem_path) if os.path.dirname(problem_path) else '.', exist_ok=True)
            os.makedirs(os.path.dirname(answer_path) if os.path.dirname(answer_path) else '.', exist_ok=True)

            # 写入题目
            with open(problem_path, 'w', encoding='utf-8') as f:
                for problem in problems:
                    # 确保格式正确
                    if not problem.strip().endswith('='):
                        problem = problem.strip() + ' ='
                    f.write(problem + '\n')

            # 写入答案
            with open(answer_path, 'w', encoding='utf-8') as f:
                for answer in answers:
                    f.write(str(answer) + '\n')

            return True
        except Exception as e:
            print(f"文件写入错误: {e}")
            return False

    @staticmethod
    def read_file(file_path):
        """读取文件内容，返回每行列表"""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件不存在: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                lines = []
                for line in f:
                    stripped = line.strip()
                    if stripped:  # 只添加非空行
                        lines.append(stripped)
                return lines
        except UnicodeDecodeError:
            # 如果UTF-8失败，尝试其他编码
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    lines = []
                    for line in f:
                        stripped = line.strip()
                        if stripped:
                            lines.append(stripped)
                    return lines
            except Exception as e:
                raise ValueError(f"无法读取文件 {file_path}: {e}")
        except Exception as e:
            raise ValueError(f"读取文件 {file_path} 时出错: {e}")

    @staticmethod
    def check_answers(exercise_file, answer_file, grade_path="Grade.txt"):
        """校验答案，生成评分结果到Grade.txt"""
        try:
            exercises = FileHandler.read_file(exercise_file)
            answers = FileHandler.read_file(answer_file)

            if len(exercises) != len(answers):
                raise ValueError(f"题目数量({len(exercises)})与答案数量({len(answers)})不匹配")

            correct, wrong = [], []

            for idx, (exercise, answer) in enumerate(zip(exercises, answers), 1):
                try:
                    expr = re.sub(r"\s*=\s*$", "", exercise).strip()
                    expr = expr.replace('*', '×').replace('/', '÷')

                    correct_answer = str(Calculator.calculate(expr)).strip()
                    if correct_answer == answer.strip():
                        correct.append(str(idx))
                    else:
                        wrong.append(str(idx))
                except Exception:
                    wrong.append(str(idx))

            correct_str = f"Correct: {len(correct)} ({', '.join(correct)})" if correct else "Correct: 0"
            wrong_str = f"Wrong: {len(wrong)} ({', '.join(wrong)})" if wrong else "Wrong: 0"

            with open(grade_path, 'w', encoding='utf-8') as f:
                f.write(correct_str + '\n' + wrong_str)

            return correct_str, wrong_str

        except Exception as e:
            raise ValueError(f"答案检查失败: {e}")
