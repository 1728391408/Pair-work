from calculator import Calculator


class FileHandler:
    @staticmethod
    def write_problems_and_answers(problems, answers, problem_path="Exercises.txt", answer_path="Answers.txt"):
        """写入题目到Exercises.txt，答案到Answers.txt"""
        # 写入题目：为避免在某些终端出现 Unicode 显示问题，
        # 在写入时将乘除符号规范为 ASCII 字符 '*' 和 '/'
        safe_problems = [p.replace('×', '*').replace('÷', '/') for p in problems]
        with open(problem_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(safe_problems))
        # 写入答案
        with open(answer_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(answers))

    @staticmethod
    def read_file(file_path):
        """读取文件内容，返回每行列表"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            raise FileNotFoundError(f"文件不存在: {file_path}")

    @staticmethod
    def check_answers(exercise_file, answer_file, grade_path="Grade.txt"):
        """校验答案，生成评分结果到Grade.txt"""
        # 读取题目和答案
        exercises = FileHandler.read_file(exercise_file)
        answers = FileHandler.read_file(answer_file)

        if len(exercises) != len(answers):
            raise ValueError("题目数量与答案数量不匹配")

        correct = []  # 正确题目编号
        wrong = []  # 错误题目编号

        for idx, (exercise, answer) in enumerate(zip(exercises, answers), 1):
            # 提取表达式（去除末尾的等号及多余空白，防止不同空格格式导致匹配失败）
            import re
            expr = re.sub(r"\s*=\s*$", "", exercise).strip()
            try:
                # 计算正确答案
                correct_answer = str(Calculator.calculate(expr))
                # 对比用户答案
                if correct_answer == answer.strip():
                    correct.append(str(idx))
                else:
                    wrong.append(str(idx))
            except Exception:
                # 题目本身错误，归为错误
                wrong.append(str(idx))

        # 生成评分结果
        correct_str = f"Correct: {len(correct)} ({', '.join(correct)})" if correct else f"Correct: 0 ()"
        wrong_str = f"Wrong: {len(wrong)} ({', '.join(wrong)})" if wrong else f"Wrong: 0 ()"

        # 写入Grade.txt
        with open(grade_path, 'w', encoding='utf-8') as f:
            f.write(correct_str + '\n' + wrong_str)

        return correct_str, wrong_str
