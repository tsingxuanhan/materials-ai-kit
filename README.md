<div align="center">

# 🧪 Materials-AI-Kit

> AI-Powered Toolkit for Materials Science Research — v4.2

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)]()
[![Version](https://img.shields.io/badge/Version-4.2-blue.svg)]()

</div>

---

## 🌟 Overview

Materials-AI-Kit 是面向材料科学研究者的 AI 工具包，聚焦**低碳建材**与**水泥基体系**。

整合机器学习预测、配合比优化、文献管理和实用脚本，开箱即用。配合 [NexusFlow](https://github.com/tsingxuanhan/NexusFlow) 多智能体框架使用可实现自动化科研工作流。

> **最新基准**：NexusFlow 在跨框架对比中得分 92/100（vs AutoGen 88 / CrewAI 85），复杂任务 94.4 分。详见 [agent4science 对比报告](https://github.com/tsingxuanhan/agent4science/blob/main/reports/horizontal_comparison_summary.md)。

---

## 📦 结构

```
materials-ai-kit/
├── models/           ← ML 模型
│   ├── property_predictor.py    # CNN 强度预测（28d 抗压强度）
│   └── composition_optimizer.py # 配合比反演设计（约束优化）
├── scripts/          ← 实用脚本集
│   ├── ai/           # AI 辅助（文档生成、代码审查）
│   ├── data/         # 数据处理（特征工程、Pipeline）
│   ├── kb/           # 知识库管理（更新、验证）
│   ├── system/       # 系统监控（GPU、健康检查）
│   └── zotero/       # Zotero 集成（批量导入、论文→KB）
├── demo/             ← 在线演示面板
└── requirements.txt
```

---

## 🚀 Quick Start

### 材料性能预测

```python
from models import PropertyPredictor

predictor = PropertyPredictor()
result = predictor.predict({
    "cement": 400,      # kg/m³
    "water": 180,       # kg/m³
    "aggregate": 1200,  # kg/m³
    "admixture": 5,     # kg/m³
    "fly_ash": 80,      # kg/m³ (粉煤灰掺量)
    "slag": 120         # kg/m³ (矿渣掺量)
})
print(f"预测 28d 强度: {result['strength_28d']:.1f} MPa")
print(f"CO₂ 排放: {result['co2_kg_m3']:.1f} kg/m³")
```

### 配合比优化

```python
from models import CompositionOptimizer

optimizer = CompositionOptimizer()
mix = optimizer.optimize(
    target_strength=50.0,        # MPa
    constraints={
        "water/binder": 0.45,    # 最大水胶比
        "sand_ratio": 0.35,      # 砂率
        "min_fly_ash": 50,       # 最小粉煤灰掺量 kg/m³
        "max_co2": 300           # 最大碳排放 kg/m³
    },
    objective="minimize_co2"     # 优化目标
)
print(f"最优配合比: {mix}")
print(f"预计强度: {mix.strength:.1f} MPa")
print(f"预计碳排放: {mix.co2:.1f} kg/m³")
```

### 实用脚本

```bash
# 数据处理 Pipeline
python scripts/data/mat_pipeline.py --input data.csv --output features.csv

# 知识库更新
python scripts/kb/kb_update.py --add new_paper.json

# GPU 监控
python scripts/system/gpu_monitor.py

# Zotero 批量导入
python scripts/zotero/zotero_batch.py --collection "cement"

# 知识库验证
python scripts/kb/kb_validate.py --check-links
```

---

## 🔬 研究聚焦

本工具包特别关注以下低碳建材方向：

| 方向 | 工具支持 | 说明 |
|------|---------|------|
| **SSC（煅烧粘土石灰石水泥）** | 配合比优化 | LC3 体系配比设计 |
| **纳米改性混凝土** | 性能预测 | 纳米 SiO₂/TiO₂ 掺量优化 |
| **固废利用** | 数据 Pipeline | 煤矸石/粉煤灰/矿渣活性评估 |
| **AI 辅助设计** | ML 模型 | CNN 强度预测 + 约束优化 |

---

## 📊 Demo

在线演示面板展示材料性能预测和配合比优化效果：

```bash
# 本地运行 Demo
cd demo && python -m http.server 8080
# 访问 http://localhost:8080
```

---

## 🔗 关联项目

| 项目 | 说明 | 最近更新 |
|------|------|---------|
| [NexusFlow](https://github.com/tsingxuanhan/NexusFlow) | 群体智能引擎（CDoL 认知分工，10-Agent） | 2026-07-14 |
| [agent4science](https://github.com/tsingxuanhan/agent4science) | 学术工具集 & 知识库入口 | 2026-07-15 |
| [xuanshu-knowledge-base](https://github.com/tsingxuanhan/xuanshu-knowledge-base) | 知识库 v2（524 篇论文 / 30 分类） | 2026-06-15 |
| [xuanshu-ui-gallery](https://github.com/tsingxuanhan/xuanshu-ui-gallery) | UI 风格库（6 种 CSS 主题） | 2026-06-14 |
| [qiu](https://github.com/tsingxuanhan/qiu) | 秋 · 项目指南文档 | 2026-06-13 |

---

## 🌐 生态导航

```
🏛️ XuanHub 开源生态
├── 🔬 NexusFlow                 ← 核心 AGI 框架 (v2.8, CDoL+端边云)
├── 📚 xuanshu-knowledge-base    ← 知识库 (524篇 / 30分类)
├── 🧪 materials-ai-kit          ← 材料AI工具包（本仓库）
├── 🧰 agent4science             ← 学术工具集 & 评估引擎
├── 🎨 xuanshu-ui-gallery        ← UI风格库 (6种CSS主题)
└── 📖 qiu                       ← 项目指南
```

---

## 📄 License

MIT
