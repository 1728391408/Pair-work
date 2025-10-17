"""
arg_parser.py

向后兼容的命令行参数解析模块。

提供：
- ArgParser 类（项目中 main.py 期待的接口）
- build_arg_parser / parse_args 供通用用途
"""
from __future__ import annotations

import argparse
from typing import List, Optional

__all__ = ["build_arg_parser", "parse_args", "ArgParser"]


def build_arg_parser(prog: Optional[str] = None) -> argparse.ArgumentParser:
    """构建并返回一个通用的 ArgumentParser（通用版本，与项目兼容）。"""
    parser = argparse.ArgumentParser(prog=prog, description="通用命令行参数解析器")

    # 常见输入/输出/配置
    parser.add_argument("-c", "--config", type=str, help="配置文件路径")
    parser.add_argument("-i", "--input", type=str, help="输入文件或目录")
    parser.add_argument("-o", "--output", type=str, help="输出文件或目录")

    # 日志与运行模式
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="增加日志详细级别，使用 -v 或 -vv（越多越详细）")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", help="显式设置日志级别（优先于 -v）")
    parser.add_argument("--dry-run", action="store_true", help="仅打印将要执行的操作，不进行写入")

    # 并发与性能相关
    parser.add_argument("-w", "--workers", type=int, default=1, help="并发工作线程/进程数（默认: 1）")

    # 版本信息
    parser.add_argument("--version", action="version", version="%(prog)s 0.1")

    return parser


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """解析传入参数（若 args 为 None，则解析 sys.argv）。"""
    parser = build_arg_parser()
    return parser.parse_args(args)


class ArgParser:
    """向后兼容的参数解析类，提供与原项目中相同的接口。

    用法：
        arg_parser = ArgParser()
        params = arg_parser.parse()
    返回的 params 为字典，包含：
        - 生成模式: {'type': 'generate', 'problem_count': int, 'num_range': int}
        - 校验模式: {'type': 'check', 'exercise_file': str, 'answer_file': str}
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="小学四则运算题目生成与校验程序")
        self._add_arguments()

    def _add_arguments(self):
        # 生成题目所需参数
        self.parser.add_argument('-n', type=int, help='生成题目的个数（正整数）')
        self.parser.add_argument('-r', type=int, help='数值范围（自然数，必须提供）')
        # 校验答案所需参数
        self.parser.add_argument('-e', help='题目文件路径（如Exercises.txt）')
        self.parser.add_argument('-a', help='答案文件路径（如Answers.txt）')

    def parse(self):
        """解析命令行参数并返回项目期望的字典格式。"""
        args = self.parser.parse_args()
        # 校验参数组合合法性
        if getattr(args, 'e', None) and getattr(args, 'a', None):
            return {'type': 'check', 'exercise_file': args.e, 'answer_file': args.a}
        elif getattr(args, 'n', None) and getattr(args, 'r', None):
            if args.n < 1:
                raise ValueError("参数-n必须为正整数")
            if args.r < 1:
                raise ValueError("参数-r必须为自然数")
            return {'type': 'generate', 'problem_count': args.n, 'num_range': args.r}
        else:
            self.parser.error("生成题目需提供-n和-r参数；校验答案需提供-e和-a参数")


if __name__ == "__main__":
    # 方便单独测试解析器
    ap = ArgParser()
    params = ap.parse()
    print(params)