#!/usr/bin/env python3
"""文档自动生成 — 从Python文件生成Markdown文档"""
import ast
import sys

def generate_doc(filepath):
    """从Python文件提取docstring生成文档"""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()

    tree = ast.parse(source)
    doc = ast.get_docstring(tree)
    if doc:
        print(f"# {filepath}\n\n{doc}\n")

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_doc = ast.get_docstring(node)
            args = [a.arg for a in node.args.args]
            sig = f"{node.name}({', '.join(args)})"
            print(f"## {sig}\n")
            if func_doc:
                print(f"{func_doc}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_doc.py <file.py>")
        sys.exit(1)
    generate_doc(sys.argv[1])
