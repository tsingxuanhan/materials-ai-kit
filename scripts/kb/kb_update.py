#!/usr/bin/env python3
"""KB批量更新脚本"""
import os
import sys
from pathlib import Path

KB_DIR = Path(os.environ.get("KB_DIR", "C:/Users/ASUS/Desktop/knowledge_bases"))

def update_kb_entries(kb_name, entries):
    """向指定KB追加条目"""
    kb_path = KB_DIR / kb_name
    if not kb_path.exists():
        print(f"Error: {kb_path} not found")
        return

    with open(kb_path, 'a', encoding='utf-8') as f:
        for entry in entries:
            f.write(f"\n### {entry['title']}\n")
            f.write(f"- **作者**: {entry.get('authors', 'Unknown')}\n")
            f.write(f"- **方法**: {entry.get('method', '')}\n")
            f.write(f"- **要点**: {entry.get('summary', '')}\n")
    print(f"Added {len(entries)} entries to {kb_name}")

if __name__ == "__main__":
    print(f"KB Directory: {KB_DIR}")
    print(f"KB files: {list(KB_DIR.glob('**/*.md'))}")
    print("Usage: python kb_update.py")
