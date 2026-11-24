#!/usr/bin/env python3
"""递归统计目录下的文件数量，并按扩展名分组计数。

用法: python file_stats.py [目录]   # 省略目录时统计当前目录
"""

import os
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "pycache", "__pycache__"}  # 扫描时跳过的目录名
SKIP_FILES = {".gitkeep"}                                # 仅占位用，不参与统计
NO_EXT = "(无扩展名)"


def count_files(root: Path) -> tuple[int, Counter]:
    """遍历 root 下所有文件，返回 (文件总数, 扩展名计数)。"""
    total, counter = 0, Counter()
    for dirpath, dirs, files in os.walk(root):
        # 原地修改 dirs，os.walk 就不会再递归进入这些目录（真正的剪枝）
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            full = os.path.join(dirpath, name)
            if name in SKIP_FILES or not os.path.isfile(full):
                continue
            # 没有后缀的文件（如 Makefile、.env）单独归为一类
            counter[os.path.splitext(name)[1].lower() or NO_EXT] += 1
            total += 1
    return total, counter


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()
    if not root.is_dir():
        print(f"目录不存在: {root}")
        return 1

    total, counter = count_files(root)
    print(f"目录: {root.resolve()}")
    print(f"文件总数: {total}")
    print("\n按扩展名统计:")
    # 数量多的排前面，数量相同时按扩展名排序，保证输出稳定
    for ext, num in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {ext:<14} {num:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
