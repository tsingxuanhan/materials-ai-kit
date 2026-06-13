# agent4science · 科研Agent框架

> 开源的多智能体科研自动化框架。让AI团队帮你做文献调研、数据分析、代码生成。

## 一句话定位

**科研界的AI团队** — 不是单个AI助手，而是4个AI分工协作。

## 仓库信息

- **地址**: `github.com/tsingxuanhan/agent4science`
- **可见性**: 公开（Public）
- **当前版本**: v3.2
- **在线Demo**: [Hub控制面板](https://tsingxuanhan.github.io/agent4science/)（支持云端预览+一键本地化）

## 适用场景

✅ **文献调研**
- "帮我找2024年关于低碳水泥的最新论文"
- "总结这10篇论文的核心方法"

✅ **数据验证**
- "检查这个实验数据有没有异常值"
- "交叉验证这两组数据是否一致"

✅ **代码生成**
- "写一个Python脚本处理CSV数据"
- "用PyTorch搭一个简单的CNN模型"

✅ **概念解释**
- "用通俗的话解释什么是碱激发混凝土"
- "对比GNN和CNN在材料科学中的应用"

## 核心架构

### 四角色Agent

```
         ┌──────────────┐
         │  用户请求     │
         └──────┬───────┘
                ↓
    ┌───────────────────────┐
    │   Orchestrator        │  ← 编排调度
    │   (任务分配)          │
    └───────┬───────────────┘
            │
    ┌───────┴───────┬───────┬───────┐
    ↓               ↓       ↓       ↓
┌────────┐    ┌────────┐ ┌────────┐ ┌────────┐
│ Miner  │    │Assayer │ │ Caster │ │Artisan │
│ 矿工   │    │ 试金   │ │ 铸师   │ │ 匠人   │
│文献搜索│    │数据验证│ │代码生成│ │领域问答│
└────────┘    └────────┘ └────────┘ └────────┘
    ↓               ↓       ↓       ↓
    └───────┬───────┴───────┴───────┘
            ↓
    ┌───────────────┐
    │  整合结果      │
    │  返回用户      │
    └───────────────┘
```

**角色分工**：

| Agent | 模型 | 职责 | 典型任务 |
|-------|------|------|---------|
| Miner | DeepSeek Pro | 文献搜索 | 搜论文、找资料、信息收集 |
| Assayer | DeepSeek Flash | 数据验证 | 交叉核对、异常检测、事实核查 |
| Caster | DeepSeek Pro | 代码生成 | 写脚本、搭模型、数据处理 |
| Artisan | DeepSeek Flash | 领域问答 | 概念解释、方案建议、专家咨询 |

### A2A协作网络

Agent之间可以直接通信，不必每次都经过Orchestrator：

```python
# Miner发现某篇论文很重要，直接通知Assayer验证
miner.send_to(assayer, "这篇论文的数据需要验证: ...")

# Assayer验证通过，直接交给Caster生成代码
assayer.send_to(caster, "数据已验证，请生成处理脚本: ...")
```

**优势**：
- 减少Orchestrator瓶颈
- Agent间直接协作，效率更高
- 支持能力发现和自动路由

### 向量记忆（v3.1.1）

语义搜索，不是关键词匹配：

```python
# 传统搜索：必须精确匹配关键词
search("ground granulated blast furnace slag")  # 只能匹配完全一样的词

# 语义搜索：理解意思就行
search("GGBS水泥")  # 能匹配到 "ground granulated blast furnace slag"
search("矿渣粉")    # 也能匹配到！
```

**技术实现**：NGram TF-IDF（不依赖HuggingFace，国内直接用）

## 目录结构

```
agent4science/
├── README.md                  # 项目说明
├── requirements.txt           # 依赖包
│
├── crew/                      # Agent团队
│   ├── __init__.py
│   ├── miner.py              # 矿工Agent
│   ├── assayer.py            # 试金Agent
│   ├── caster.py             # 铸师Agent
│   ├── artisan.py            # 匠人Agent
│   ├── base_agent.py         # Agent基类
│   ├── orchestrator.py       # 编排调度
│   ├── handoff.py            # 任务交接
│   ├── checkpoint.py         # 检查点
│   ├── memory.py             # 记忆管理
│   ├── vector_memory.py      # 向量检索
│   └── observability.py      # 可观测性
│
├── gateway/                   # A2A网关
│   ├── a2a_protocol.py       # A2A协议实现
│   ├── a2a_gateway.py        # A2A网关
│   └── handoff.py            # Handoff桥接
│
├── tools/                     # 工具集
│   ├── web_search.py         # 联网搜索
│   ├── code_exec.py          # 代码执行
│   ├── file_ops.py           # 文件操作
│   ├── browser.py            # 浏览器控制
│   └── ...
│
├── mcp_server/                # MCP服务器
│   └── mcp_server.py         # Model Context Protocol
│
├── observability/             # 可观测性
│   └── observability.py      # 日志/指标/追踪
│
├── examples/                  # 示例
│   ├── quickstart.py         # 快速开始
│   └── legacy/               # 旧版示例
│
└── docs/                      # 文档
    └── ...
```

## 核心文件说明

### crew/orchestrator.py

任务编排器，决定哪个Agent处理什么任务：

```python
class Orchestrator:
    def route(self, task):
        # 分析任务类型
        if "搜索" in task or "找" in task:
            return self.miner
        elif "验证" in task or "检查" in task:
            return self.assayer
        elif "代码" in task or "脚本" in task:
            return self.caster
        else:
            return self.artisan  # 默认交给匠人
```

### crew/vector_memory.py

向量记忆，核心是NGram TF-IDF：

```python
class NGramTFIDFProvider:
    def encode(self, text):
        # 把文本转为向量（n-gram + TF-IDF）
        # "混凝土" → [0.12, 0.34, ...]
        # "concrete" → [0.11, 0.33, ...]  # 语义接近！
        return vector
```

### gateway/a2a_protocol.py

A2A协议，Agent间直接通信：

```python
class A2AProtocol:
    def send(self, from_agent, to_agent, message):
        # Agent间直接传递消息
        # 不经过Orchestrator，减少延迟
        pass
```

## 在线Demo

**Hub控制面板**：[https://tsingxuanhan.github.io/agent4science/](https://tsingxuanhan.github.io/agent4science/)

功能：
- 📊 实时查看4个Agent状态
- 🔀 任务编排可视化
- 🧠 知识库浏览
- 🎛️ 模型资源分配
- 🔧 快速命令面板

**两种模式**：
- **云端模式**：模拟数据，无需部署，直接预览
- **本地模式**：连接你的真实Agent后端

点击页面上的「一键本地化」按钮，可以把Demo下载到本地。

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/tsingxuanhan/agent4science.git
cd agent4science
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API Key

```bash
export DEEPSEEK_API_KEY="sk-xxx"
export DEEPSEEK_ENDPOINT="https://api.deepseek.com"
```

### 4. 运行示例

```bash
python examples/quickstart.py
```

### 5. 打开控制面板

```bash
# 方式1：直接用浏览器打开
open docs/hub.html

# 方式2：启动本地服务器
python -m http.server 8080
# 然后访问 http://localhost:8080/docs/hub.html
```

## 与其他仓库的关系

```
agent4science (公开)
    ↓ 包含
crew/ 目录
    ↓ 是
xuan-hub (私有) 的子集
```

**agent4science** 是 **xuan-hub** 的公开子集：
- xuan-hub 包含完整实现（82个文件，34K行）
- agent4science 只包含核心Agent框架（13个文件，3.5K行）
- 想体验完整功能 → 用 xuan-hub
- 只想用Agent协作 → agent4science 够用

## 设计哲学

1. **角色明确** — 每个Agent只做一件事，做到极致
2. **A2A优先** — Agent间直接协作，减少中心化瓶颈
3. **国内友好** — DeepSeek API，不依赖外网
4. **轻量部署** — 最小化依赖，笔记本就能跑

## 技术亮点

- ✅ A2A协议：Agent间直接通信，不必经过Orchestrator
- ✅ 语义搜索：NGram TF-IDF，中英混合支持
- ✅ 检查点恢复：崩溃后从上次断点继续
- ✅ 可观测性：OpenTelemetry追踪，日志/指标/链路全有
- ✅ MCP支持：Model Context Protocol，标准化工具调用
