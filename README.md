# Materials-AI-Kit

> AI-Powered Toolkit for Materials Science Research

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![arXiv](https://img.shields.io/badge/arXiv-materials.XXXXX-orange.svg)](https://arxiv.org)

## Overview

Materials-AI-Kit is a comprehensive AI toolkit designed for materials scientists and researchers, focusing on **low-carbon building materials** and **cement-based systems**. It integrates machine learning capabilities into traditional materials research workflows.

## 🎮 Live Demo

Try the interactive AI Workstation demo with Liquid Glass design:

**[Open Demo](demo/index.html)** (Download and open in browser)

Features:
- Dashboard with 4 Agent status & API resource allocation
- Agent orchestration (Miner/Assayer/Foundry/Artisan)
- Workflow pipeline with DAG visualization
- Knowledge base browser with domain files
- Model training playground (CNN/GNN/LSTM)
- Mix design prediction for cementitious materials

> All interactions use simulated data. Connect to real backend APIs for full functionality.

## Features

### Data Processing Pipeline
- Automated data cleaning and normalization
- Feature engineering for material properties
- Batch processing with progress tracking

### AI-Enabled Tools
- **Literature Search**: Semantic search and summarization
- **Code Generation**: Scripts for common materials science tasks
- **Concept Explanation**: Domain-specific tutoring
- **Property Prediction**: CNN-based strength prediction
- **Mix Optimization**: Inverse design for target properties

### Knowledge Base
- Paper metadata extraction and indexing
- Citation network analysis
- Domain knowledge organization

### Zotero Integration
- One-click import from Zotero library
- Metadata synchronization
- Tag-based organization

## Architecture

```mermaid
graph TB
    subgraph "Data Layer"
        KB[Knowledge Base] --> MP[Mat Pipeline]
        ZT[Zotero Import] --> KB
    end
    
    subgraph "AI Layer"
        MP --> LS[Literature Search]
        MP --> CG[Code Generator]
        MP --> CT[Concept Tutor]
        MP --> PP[Property Predictor]
        MP --> MO[Mix Optimizer]
    end
    
    subgraph "Output Layer"
        LS --> RP[Reports]
        CG --> CODE[Code Snippets]
        CT --> ANS[Answers]
        PP --> PRED[Predictions]
        MO --> DES[Designs]
    end
```

## Quick Start

### Installation

```bash
git clone https://github.com/tsingxuanhan/materials-ai-kit.git
cd materials-ai-kit
pip install -r requirements.txt
```

### Basic Usage

#### Property Prediction

```python
from models.property_predictor import PropertyPredictor
import numpy as np

# Load or train model
predictor = PropertyPredictor()
# predictor.fit(X_train, y_train)  # Train on your data

# Predict strength
test_mix = {
    'cement': 350, 'slag': 50, 'gypsum': 10,
    'water': 175, 'fine_aggregate': 750, 'coarse_aggregate': 1000
}

result = predictor.predict_with_interval(test_mix)
print(f"Predicted: {result['mean']:.1f} MPa (95% CI: {result['lower']:.1f}-{result['upper']:.1f})")
```

#### Mix Optimization

```python
from models.composition_optimizer import CompositionOptimizer

optimizer = CompositionOptimizer()
optimizer.fit(X_train, strength_curves)

# Find mix for target strength
result = optimizer.optimize(target_strength=40.0, target_age=28)
print(f"Optimized: Cement={result['composition']['cement']:.0f} kg/m³")
```

## Project Structure

```
materials-ai-kit/
├── ai/                      # AI-enabled tools
├── data/                    # Data processing
├── kb/                      # Knowledge base
├── models/                  # ML models (NEW)
│   ├── __init__.py
│   ├── composition_optimizer.py  # Inverse design
│   └── property_predictor.py     # CNN prediction
├── system/                  # System utilities
├── zotero/                  # Zotero integration
├── demo/                    # Interactive demo
├── README.md
└── requirements.txt
```

## Research Domains

The toolkit focuses on:

| Domain | Focus Areas |
|--------|-------------|
| Low-Carbon Cement | SSC, MBCMs, LC3 systems |
| Supplementary Cementitious | Fly ash, slag, silica fume |
| Nano-Modification | SiO₂, TiO₂, CNTs |
| Concrete Durability | Chloride, sulfate, freeze-thaw |

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

MIT License - See [LICENSE](LICENSE) for details.
