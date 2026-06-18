#!/usr/bin/env python3
"""Zotero批量导入 — 从CSV/JSON导入文献到Zotero"""
import json
import sys

def import_from_json(json_path, zotero_dir):
    """从JSON文件批量导入Zotero条目（生成BibTeX中间文件）"""
    with open(json_path, 'r', encoding='utf-8') as f:
        papers = json.load(f)

    bib_entries = []
    for p in papers:
        entry = f"""@article{{{p.get('key', 'paper')},
  title = {{{p['title']}}},
  author = {{{p.get('authors', 'Unknown')}}},
  year = {{{p.get('year', '2024')}}},
  journal = {{{p.get('journal', '')}}}
}}
"""
        bib_entries.append(entry)

    output_path = json_path.replace('.json', '.bib')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(bib_entries))

    print(f"Generated {len(bib_entries)} BibTeX entries -> {output_path}")
    print(f"Import to Zotero: File -> Import -> {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python zotero_batch.py <papers.json>")
        sys.exit(1)
    import_from_json(sys.argv[1], None)
