# 🧪 Materials-AI-Kit

> AI-Powered Toolkit for Materials Science Research — v4.1

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-4.1-blue.svg)]()

---

## 🌟 Overview

Materials-AI-Kit 是面向材料科学研究者的 AI 工具包，聚焦**低碳建材**与**水泥基体系**。

整合机器学习预测、配合比优化、文献管理和实用脚本，开箱即用。

---

## 📦 结构

```
materials-ai-kit/
├── models/           ← ML 模型（材料性能预测 + 配合比优化）
│   ├── property_predictor.py    # CNN 强度预测
│   └── composition_optimizer.py # 配合比反演设计
├── scripts/          ← 实用脚本集
│   ├── ai/           # AI 辅助（文档生成、代码审查）
│   ├── data/         # 数据处理（特征工程、Pipeline）
│   ├── kb/           # 知识库管理（更新、验证）
│   ├── system/       # 系统监控（GPU、健康检查）
│   └── zotero/       # Zotero 集成（批量导入、论文→KB）
├── demo/             ← 在线演示
└── requirements.txt
```

---

## 🚀 Quick Start

### 材料性能预测

```python
from models import PropertyPredictor

predictor = PropertyPredictor()
result = predictor.predict({
    "cement": 400,
    "water": 180,
    "aggregate": 1200,
    "admixture": 5
})
print(f"预测强度: {result['strength_28d']:.1f} MPa")
```

### 配合比优化

```python
from models import CompositionOptimizer

optimizer = CompositionOptimizer()
mix = optimizer.optimize(
    target_strength=50.0,
    constraints={"water/binder": 0.45, "sand_ratio": 0.35}
)
print(f"最优配合比: {mix}")
```

### 实用脚本

```bash
# 数据处理
python scripts/data/mat_pipeline.py --input data.csv --output features.csv

# 知识库更新
python scripts/kb/kb_update.py --add new_paper.json

# GPU 监控
python scripts/system/gpu_monitor.py

# Zotero 批量导入
python scripts/zotero/zotero_batch.py --collection "cement"
```

---

## 🔗 关联项目

| 项目 | 说明 |
|------|------|
| [agent4science](https://github.com/tsingxuanhan/agent4science) | 多Agent科研框架（核心） |
| [xuanshu-knowledge-base](https://github.com/tsingxuanhan/xuanshu-knowledge-base) | 知识库 v2（524篇论文） |
| [qiu](https://github.com/tsingxuanhan/qiu) | 秋 · 项目指南文档 |
| [xuanshu-ui-gallery](https://github.com/tsingxuanhan/xuanshu-ui-gallery) | UI 风格库 |

---

## 📄 License

MIT
