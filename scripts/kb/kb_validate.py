#!/usr/bin/env python3
"""KB格式校验脚本"""
import os
import sys
import re
from pathlib import Path

KB_DIR = Path(os.environ.get("KB_DIR", "C:/Users/ASUS/Desktop/knowledge_bases"))

def validate_kb(filepath):
    """校验KB文件格式"""
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    if not content.strip():
        errors.append("空文件")

    for i, line in enumerate(lines, 1):
        if '\t' in line:
            errors.append(f"L{i}: Tab缩进(应用空格)")
        if line.rstrip() != line and line.strip():
            errors.append(f"L{i}: 行尾空格")

    return errors

def main():
    md_files = list(KB_DIR.glob("**/*.md"))
    total = 0
    for f in md_files:
        errs = validate_kb(f)
        status = "✅" if not errs else "❌"
        print(f"{status} {f.relative_to(KB_DIR)} ({len(errs)} issues)")
        total += len(errs)
    print(f"\nTotal: {len(md_files)} files, {total} issues")
    sys.exit(1 if total else 0)

if __name__ == "__main__":
    main()
