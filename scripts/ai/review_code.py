#!/usr/bin/env python3
"""代码审查 — 使用Codex CLI或API进行代码审查"""
import subprocess
import sys
import os

def review_with_codex(filepath, api_key=None):
    """使用Codex CLI审查代码文件"""
    api_key = api_key or os.environ.get("MIMO_API_KEY")
    if not api_key:
        print("Error: Set MIMO_API_KEY environment variable")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    prompt = f"""Review the following Python code for bugs, security issues, 
and style problems. Output a concise review report.

```python
{code}
```"""

    result = subprocess.run(
        ["codex", "exec", prompt],
        capture_output=True, text=True,
        env={**os.environ, "OPENAI_API_KEY": api_key}
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review_code.py <file.py>")
        sys.exit(1)
    review_with_codex(sys.argv[1])
