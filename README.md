# Materials-AI-Kit

> AI-Powered Toolkit for Materials Science Research — v4.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/Version-4.0-blue.svg)]()

## Overview

Materials-AI-Kit is a comprehensive AI toolkit designed for materials scientists and researchers, focusing on **low-carbon building materials** and **cement-based systems**. It integrates machine learning, multi-agent automation, and intelligent memory into traditional materials research workflows.

**What's New in v4.0:**
- 🔬 **AI+Materials Breakthroughs**: DPA4 atomic model integration, MatterGen crystal generation support
- 🧠 **3-Layer Memory System**: Core (active) → Recall (searchable) → Archival (compressed), with Sleeptime consolidation
- 🤖 **Agent4Science Integration**: Multi-agent collaboration via A2A networking with autonomous goal decomposition
- 🔍 **Multi-Hop RAG**: Chain-of-reasoning retrieval across knowledge domains
- 🛡️ **Safety Guardrails**: Injection detection, anti-pattern blocking, quality dials

## 🎮 Live Demo

Try the interactive AI Workstation demo with Liquid Glass design:

**[Open Demo](demo/index.html)** (Download and open in browser)

Features:
- Dashboard with 4 Agent status & API resource allocation
- Agent orchestration (Miner/Assayer/Caster/Artisan)
- Workflow pipeline with DAG visualization
- Knowledge base browser with domain files
- Model training playground (CNN/GNN/LSTM)
- Mix design prediction for cementitious materials

> All interactions use simulated data. Connect to real backend APIs for full functionality.

## Features

### ML Models

| Model | Description |
|-------|-------------|
| **PropertyPredictor** | CNN-based strength prediction with confidence intervals |
| **CompositionOptimizer** | Inverse design for target properties |
| **LSTMForwardModel** | Strength evolution curve prediction |

### 3-Layer Memory System (v4.0)

```
┌──────────────────────────────────────────────┐
│               Memory Manager                  │
│  ┌──────────┐  ┌───────────┐  ┌───────────┐ │
│  │  Core    │  │  Recall   │  │  Archival  │ │
│  │(Working) │  │(Episodic) │  │(Long-term) │ │
│  │ ~4K ctx  │  │ Semantic  │  │ Compressed │ │
│  │ Active   │  │ Search    │  │ Scored     │ │
│  └──────────┘  └───────────┘  └───────────┘ │
│        + Sleeptime Consolidation              │
│        + Multi-Hop RAG                        │
└──────────────────────────────────────────────┘
```

```python
from models.vector_memory import NGramTFIDFProvider, PersistentVectorStore

# Create semantic memory
provider = NGramTFIDFProvider()
memory = PersistentVectorStore(provider=provider)

# Index materials knowledge
memory.add("SSC requires min 70% GGBS, max 5% clinker", metadata={"type": "composition"})
memory.add("Nano SiO₂ improves early strength by 20-30%", metadata={"type": "admixture"})

# Semantic search — "silica nanoparticle" now matches "nano SiO₂"!
results = memory.search("ground granulated blast furnace slag cement", top_k=5)
```

### Multi-Hop RAG (v4.0)

Chain-of-reasoning retrieval that connects knowledge across domains:

```python
from multi_hop_rag import MultiHopRAG

rag = MultiHopRAG(memory_store=memory)

# Multi-hop query: connects cement chemistry → nano modification → durability
answer = rag.query(
    "How does nano-SiO₂ modification affect SSC durability in chloride environments?"
)
# Retrieves: SSC composition → SiO₂ pozzolanic reaction → Chloride binding mechanism
```

### AI-Enabled Tools

| Tool | Description |
|------|-------------|
| **Literature Search** | Semantic search and summarization |
| **Code Generation** | Scripts for common materials science tasks |
| **Concept Explanation** | Domain-specific tutoring |
| **Property Prediction** | CNN-based strength prediction |
| **Mix Optimization** | Inverse design for target properties |
| **Cross-Domain Transfer** | Apply insights from related fields (ceramics → cement) |

### Knowledge Base

- Paper metadata extraction and indexing
- Citation network analysis
- Domain knowledge organization
- Semantic vector search
- **4 knowledge domains**: Materials Science, AI/ML, Chemistry, General

### Zotero Integration

- One-click import from Zotero library
- Metadata synchronization
- Tag-based organization

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                         │
│            (Demo / API / AgentOS)                         │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Agent4Science (Multi-Agent Layer)          │   │
│  │  Miner ── Assayer ── Caster ── Artisan            │   │
│  │  Planner ── Executor ── Researcher ── Reviewer     │   │
│  └──────────────────────┬───────────────────────────┘   │
│                          │                                │
│  ┌──────────────────────┼───────────────────────────┐   │
│  │        Safety & Quality Layer                      │   │
│  │  Guardrails │ Quality Dials │ Circuit Breaker     │   │
│  └──────────────────────┼───────────────────────────┘   │
│                          │                                │
│  ┌──────────────────────┼───────────────────────────┐   │
│  │        Memory Layer (3-Layer + Sleeptime)          │   │
│  │  Core │ Recall │ Archival │ Multi-Hop RAG         │   │
│  └──────────────────────┼───────────────────────────┘   │
│                          │                                │
│  ┌──────────────────────┼───────────────────────────┐   │
│  │          ML Models & Data Pipeline                 │   │
│  │  Predictor │ Optimizer │ Feature Engineer          │   │
│  └────────────────────────────────────────────────────┘   │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
git clone https://github.com/tsingxuanhan/materials-ai-kit.git
cd materials-ai-kit
pip install -r requirements.txt
```

### Property Prediction

```python
from models.property_predictor import PropertyPredictor

predictor = PropertyPredictor()

test_mix = {
    'cement': 350, 'slag': 50, 'gypsum': 10,
    'water': 175, 'fine_aggregate': 750, 'coarse_aggregate': 1000
}

result = predictor.predict_with_interval(test_mix)
print(f"Predicted: {result['mean']:.1f} MPa (95% CI: {result['lower']:.1f}-{result['upper']:.1f})")
```

### Mix Optimization

```python
from models.composition_optimizer import CompositionOptimizer

optimizer = CompositionOptimizer()
optimizer.fit(X_train, strength_curves)

result = optimizer.optimize(target_strength=40.0, target_age=28)
print(f"Optimized: Cement={result['composition']['cement']:.0f} kg/m³")
```

### Semantic Knowledge Search

```python
from models.vector_memory import NGramTFIDFProvider, PersistentVectorStore

provider = NGramTFIDFProvider()
memory = PersistentVectorStore(provider=provider, persist_path="./kb_memory.json")

documents = [
    ("LC3: 50% limestone + 50% calcined clay, 5-30% OPC", {"type": "binder"}),
    ("SSC: min 70% GGBS, 10-15% gypsum, max 5% clinker", {"type": "binder"}),
    ("Nano SiO₂ improves early strength by 20-30%", {"type": "admixture"}),
]

for content, meta in documents:
    memory.add(content, metadata=meta)

results = memory.search("ground slag gypsum limestone blend", top_k=3)
for r in results:
    print(f"[{r.score:.3f}] {r.entry.content}")
```

## Research Domains

| Domain | Focus Areas |
|--------|-------------|
| **Low-Carbon Cement** | SSC, MBCMs, LC3 systems |
| **Supplementary Cementitious** | Fly ash, slag, silica fume |
| **Nano-Modification** | SiO₂, TiO₂, CNTs |
| **Concrete Durability** | Chloride, sulfate, freeze-thaw |
| **AI-Driven Design** | DPA4, MatterGen, inverse design |

## Project Structure

```
materials-ai-kit/
├── models/                        # ML models & memory
│   ├── __init__.py
│   ├── composition_optimizer.py   # Inverse design
│   ├── property_predictor.py      # CNN prediction
│   └── vector_memory.py           # NGram semantic memory
├── demo/                          # Interactive Liquid Glass demo
├── README.md
└── requirements.txt
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Materials-AI-Kit — AI-powered materials research, from data to design*
