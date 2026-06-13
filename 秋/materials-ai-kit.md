# materials-ai-kit · 建材AI工具包

> 面向材料科学研究者的AI工具包。用机器学习预测材料性能、优化配方、挖掘文献。

## 一句话定位

**材料科学的AI助手** — 从"试错法"到"AI预测"，让实验设计更聪明。

## 仓库信息

- **地址**: `github.com/tsingxuanhan/materials-ai-kit`
- **可见性**: 公开（Public）
- **当前版本**: v4.0
- **研究领域**: 低碳水泥、碱激发混凝土、胶凝材料

## 适用场景

✅ **性能预测**
- "这组配方的28天抗压强度是多少？"
- "预测这个混凝土的耐久性"

✅ **配方优化**
- "我要强度40MPa、碳排放最低的配方"
- "逆向设计：目标性能→最优配比"

✅ **文献挖掘**
- "找2024年关于GGBS水泥的最新研究"
- "总结矿渣粉活性的影响因素"

## 核心功能

### 1. CNN强度预测（PropertyPredictor）

```
输入：配合物成分（水泥、矿渣、粉煤灰、水灰比等）
模型：CNN学习成分→性能的映射
输出：预测强度 + 置信区间
```

**用途**：
- 不用做实验，直接预测强度
- 置信区间告诉你预测的可信度

### 2. LSTM强度演化（LSTMForwardModel）

```
输入：早期强度（3天、7天）
模型：LSTM时间序列预测
输出：完整强度曲线（3/7/28/56/90天）
```

**用途**：
- 只用3天、7天数据，预测28天强度
- 提前判断混凝土是否达标，不用等28天

### 3. 配方优化（CompositionOptimizer）

```
目标：强度≥40MPa，碳排放最低
约束：成本≤500元/m³，工作性≥180mm
算法：遗传算法搜索最优解
输出：最优配方
```

**用途**：
- 逆向设计：从目标性能反推最优配比
- 多目标优化：同时考虑强度、成本、碳排放

### 4. 向量记忆（语义搜索）

```python
memory.add("碱激发混凝土需要min 70% GGBS")
results = memory.search("矿渣粉用量")
# 能匹配到 "GGBS"（GGBS = 矿渣粉）
```

**优势**：
- 中英混合支持（"矿渣粉" ↔ "GGBS"）
- 缩写识别（"Nano SiO₂" ↔ "纳米二氧化硅"）
- 不需要精确关键词，理解语义

## 目录结构

```
materials-ai-kit/
├── README.md
├── requirements.txt
├── models/
│   ├── property_predictor.py    # CNN强度预测
│   ├── lstm_model.py            # LSTM强度演化
│   └── composition_optimizer.py # 配方优化
├── pytorch_demos/
│   ├── cnn_demo.py
│   └── lstm_demo.py
├── data/
│   ├── sample_compositions.csv
│   └── strength_curves.csv
└── docs/
```

## 数据来源

模型训练数据：
- **237篇SCI论文**：低碳水泥、碱激发混凝土、LC3、地聚合物
- **实验数据**：配合物成分 + 力学性能 + 耐久性指标
- **主要体系**：普通水泥、矿渣水泥、碱激发混凝土、LC3、地聚合物

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/tsingxuanhan/materials-ai-kit.git
cd materials-ai-kit
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：`torch`、`numpy`、`pandas`、`scikit-learn`

### 3. 运行Demo

```bash
python pytorch_demos/cnn_demo.py
```

## 与其他仓库的关系

```
materials-ai-kit (建材工具包)
    ↓ 集成
agent4science (Agent框架)
    ↓ 底层
xuan-hub (核心工作站)
```

- **materials-ai-kit**：建材领域专用工具
- **agent4science**：通用Agent框架
- **xuan-hub**：完整工作站（包含上面两者）

**使用建议**：
- 只做建材研究 → materials-ai-kit
- 需要Agent协作 → agent4science
- 想要完整体验 → xuan-hub

## 局限性

- ⚠️ 仅适用于胶凝材料体系（水泥、混凝土）
- ⚠️ 预测精度依赖训练数据范围
- ⚠️ 逆向设计可能有多个解，需要人工筛选
- ⚠️ 未考虑所有耐久性指标（如抗冻性、抗渗性）
