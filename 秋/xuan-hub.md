# xuan-hub · 核心AI工作站

> 铉枢的私有核心仓库，包含完整的AI工作站实现。

## 一句话定位

**从"AI聊天"到"AI工作"** — 不是对话机器人，而是能干活的AI团队。

## 仓库信息

- **地址**: `github.com/tsingxuanhan/xuan-hub`
- **可见性**: 私有（Private）
- **当前版本**: v4.3（34,246行代码）
- **技术栈**: Python 3.9+ / DeepSeek API / MiMo API

## 核心概念

### 四角色Agent团队

| 角色 | 代号 | 职责 | 模型 |
|------|------|------|------|
| 矿工 | Miner | 文献搜索、数据收集 | DeepSeek Pro |
| 试金 | Assayer | 数据验证、交叉核对 | DeepSeek Flash |
| 铸师 | Caster | 方案生成、代码编写 | DeepSeek Pro |
| 匠人 | Artisan | 成果整合、领域问答 | DeepSeek Flash |

### 记忆系统（Letta 3层架构）

```
┌─────────────────┐
│  Core Memory    │  ← 核心记忆：你是谁、我是谁、当前任务
├─────────────────┤
│  Recall Memory  │  ← 回忆记忆：最近对话、短期上下文
├─────────────────┤
│  Archival Memory│  ← 归档记忆：长期知识、经验沉淀
└─────────────────┘
```

### 思想结晶（v4.3新增）

不是存原始数据，而是提炼推理过程中的智慧：

```
推理过程 → 提炼思想 → 存入结晶库
    ↓
下次遇到类似问题 → 直接调用结晶 → 跳过重复思考
```

**例子**：
- 第一次：花10分钟推理"为什么混凝土开裂"
- 提炼结晶：存储"温度应力+收缩→开裂"的核心逻辑
- 下次遇到：0.1秒调出结晶，直接给答案

## 目录结构

```
xuan-hub/
├── base_agent.py              # Agent基类（2533行，核心中的核心）
├── config.py                  # 配置管理
│
├── agents/                    # 四角色Agent
│   ├── miner.py              #   矿工
│   ├── assayer.py            #   试金
│   ├── caster.py             #   铸师
│   ├── artisan.py            #   匠人
│   └── domains/              #   领域知识（材料/AI/通用）
│
├── memory/                    # 记忆系统
│   ├── core_memory.py        #   核心记忆
│   ├── recall_memory.py      #   回忆记忆
│   ├── archival_memory.py    #   归档记忆
│   ├── vector_memory.py      #   向量检索（1683行）
│   ├── sleeptime.py          #   睡眠整理
│   └── multi_hop_rag.py      #   多跳RAG
│
├── v4.2模块/                  # Agora启发优化
│   ├── knowledge_library.py  #   领域知识库
│   ├── hypothesis_engine.py  #   假说引擎
│   ├── discovery_exploitation.py  # 发现-剥削探索
│   ├── self_healing.py       #   自修复循环
│   ├── succinct_comm.py      #   通信极简
│   └── structured_pattern_memory.py  # 模式记忆
│
├── v4.3模块/                  # Thought-Retriever启发
│   ├── thought_crystallization.py   # 思想结晶
│   ├── abstraction_hierarchy.py     # 抽象层级
│   └── confidence_filter.py  #   置信度门控
│
├── tools/                     # 工具生态（20+工具）
│   ├── code_exec.py          #   代码执行
│   ├── web_search.py         #   联网搜索
│   ├── browser.py            #   浏览器控制
│   ├── file_ops.py           #   文件操作
│   ├── git_ops.py            #   Git操作
│   └── ...
│
├── control-panel/             # 液态玻璃UI控制面板
│   ├── index.html            #   主页（Agent状态）
│   ├── models.html           #   模型管理
│   ├── monitor.html          #   系统监控
│   ├── commands.html         #   快速命令
│   ├── css/
│   └── js/
│
├── api-proxy/                 # API代理
│   └── proxy.py              #   DeepSeek/MiMo路由
│
├── demo/                      # Demo演示
│   └── previews/             #   截图预览
│
└── archive/                   # 历史归档
    ├── 20250525_backup/      #   v3.x备份
    └── 20260601_backup/      #   v3.3备份
```

## 核心文件说明

### base_agent.py（2533行）

Agent的"大脑"，所有Agent都继承它：

```python
class BaseAgent:
    def chat(self, message)        # 普通对话
    def react(self, task)          # 推理+行动（ReAct模式）
    def review(self, output)       # 自我审查
    def chat_with_review(self, msg) # 对话+审查（最常用）
```

**关键能力**：
- 模式切换：chat / react / review
- Guardrails安全护栏
- 质量检查
- 记忆读写

### vector_memory.py（1683行）

向量记忆系统，核心是NGram TF-IDF：

```python
# 不依赖HuggingFace，纯Python实现
provider = NGramTFIDFProvider()
memory = PersistentVectorStore(provider=provider)

# 语义搜索（不是关键词匹配）
memory.add("混凝土开裂原因")
memory.add("cement crack causes")
results = memory.search("为什么水泥会裂")  # 能匹配到！
```

**为什么不用OpenAI Embedding？**
- 外网不通
- 要钱
- NGram效果够用，还快

### thought_crystallization.py（687行，v4.3新增）

思想结晶引擎：

```python
class ThoughtCrystallizer:
    def crystallize(self, reasoning_text):
        # 从推理过程中提炼思想钻石
        return ThoughtDiamond(
            core_idea="核心思想",
            reasoning_chain=["步骤1", "步骤2", ...],
            confidence=0.85,
            applicable_domain="适用领域"
        )
```

**设计灵感**：Thought-Retriever论文（TMLR 2026）— "存思想不存数据"

## 版本演进

| 版本 | 日期 | 核心变更 | 代码量 |
|------|------|---------|--------|
| v3.1.1 | 2025.05 | 向量记忆 | 13文件/3.5K行 |
| v3.2 | 2025.05 | 四角色架构 | 13文件/3.5K行 |
| v3.3 | 2025.06 | 安全加固 | 13文件/4K行 |
| v4.0 | 2026.05 | AI工作站 | 68文件/25K行 |
| v4.1 | 2026.06.12 | 检查点+目标验证 | 71文件/28K行 |
| v4.2 | 2026.06.12 | 知识库+假说引擎 | 78文件/32K行 |
| v4.3 | 2026.06.13 | 思想结晶 | 82文件/34K行 |

**关键跳跃**：v3.3 → v4.0，从4K行暴增到25K行，从"Agent框架"变成"完整工作站"。

## 技术亮点

1. **国内友好**
   - DeepSeek API（国内直连，不用翻墙）
   - MiMo API（小米开源，便宜）
   - NGram TF-IDF（不依赖HuggingFace）

2. **轻量部署**
   - 3.8GB内存就能跑（笔记本够用）
   - 纯Python，无Docker依赖
   - API代理自带限流

3. **智能检索**
   - 语义搜索（不是关键词匹配）
   - 中英混合支持（"混凝土"能匹配"concrete"）
   - 多跳推理（A→B→C的链式搜索）

4. **安全可控**
   - API Key环境变量管理
   - Guardrails输入输出校验
   - 熔断器防止API滥用

## 如何使用

详见 [快速开始](快速开始.md)
