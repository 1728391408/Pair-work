#!/usr/bin/env python3
"""
性能分析脚本
"""
import cProfile
import pstats
from main import main

if __name__ == "__main__":
    # 使用 cProfile 进行分析
    profiler = cProfile.Profile()
    profiler.enable()

    try:
        # 模拟命令行参数 - 生成1000道题目
        import sys

        sys.argv = ['main.py', '-n', '1000', '-r', '10']
        main()
    except SystemExit:
        pass  # 忽略 argparse 的系统退出

    profiler.disable()

    # 保存分析结果
    profiler.dump_stats('performance.prof')

    # 打印分析结果
    stats = pstats.Stats('performance.prof')
    print("=== 性能分析结果 ===")
    stats.sort_stats('cumulative').print_stats(20)  # 按累计时间排序，显示前20个
