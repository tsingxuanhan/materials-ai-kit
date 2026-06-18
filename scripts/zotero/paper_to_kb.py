#!/usr/bin/env python3
"""论文→KB — 从论文PDF提取结构化信息写入知识库"""
import sys

def extract_paper_info(pdf_path):
    """
    从PDF提取论文结构化信息。
    依赖: Stirling PDF API (http://127.0.0.1:8081)
    """
    print(f"Processing: {pdf_path}")
    print("Step 1: Upload to Stirling PDF for text extraction")
    print("Step 2: Parse title, authors, abstract, methods")
    print("Step 3: Generate KB entry in standard format")
    print("\nNote: This is a template. Full implementation needs:")
    print("  - Stirling PDF API integration")
    print("  - NLP for section parsing")
    print("  - KB format rendering")

def generate_kb_entry(info):
    """生成标准KB条目"""
    return f"""### {info.get('title', 'Untitled')}
- **作者**: {info.get('authors', 'Unknown')}
- **年份**: {info.get('year', '')}
- **方法**: {info.get('method', '')}
- **材料**: {info.get('materials', '')}
- **关键结果**: {info.get('results', '')}
- **代码**: {info.get('code_url', '未提供')}
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python paper_to_kb.py <paper.pdf>")
        sys.exit(1)
    extract_paper_info(sys.argv[1])
