from arg_parser import ArgParser
from problem_generator import ProblemGenerator
from file_handler import FileHandler
from calculator import Calculator


def main():
    try:
        # 解析参数
        arg_parser = ArgParser()
        params = arg_parser.parse()

        if params['type'] == 'generate':
            # 生成题目模式
            problem_count = params['problem_count']
            num_range = params['num_range']

            print(f"正在生成{problem_count}道{num_range}以内的题目...")
            generator = ProblemGenerator(num_range)
            problems = []
            answers = []

            for _ in range(problem_count):
                problem = generator.generate_single_problem()
                problems.append(problem)
                # 计算答案
                import re
                expr = re.sub(r"\s*=\s*$", "", problem).strip()
                answer = str(Calculator.calculate(expr))
                answers.append(answer)

            # 写入文件
            FileHandler.write_problems_and_answers(problems, answers)
            print("生成完成！")
            print(f"题目已保存至：Exercises.txt")
            print(f"答案已保存至：Answers.txt")

        elif params['type'] == 'check':
            # 校验答案模式
            exercise_file = params['exercise_file']
            answer_file = params['answer_file']

            print(f"正在校验{exercise_file}与{answer_file}...")
            correct_str, wrong_str = FileHandler.check_answers(exercise_file, answer_file)
            print("校验完成！")
            print(f"结果已保存至：Grade.txt")
            print(correct_str)
            print(wrong_str)

    except Exception as e:
        print(f"程序出错：{str(e)}")


if __name__ == "__main__":
    main()
