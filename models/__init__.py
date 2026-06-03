# -*- coding: utf-8 -*-
"""
Materials-AI-Kit Models Module
AI-Powered Materials Science ML Models

Provides:
- PropertyPredictor: CNN-based strength prediction
- CompositionOptimizer: Inverse design for mix optimization
- VectorMemory: NGram TF-IDF semantic search (v3.1.1)
"""

# Property Prediction
from .property_predictor import PropertyPredictor, load_pretrained_model

# Composition Optimization
from .composition_optimizer import CompositionOptimizer

# Vector Memory (v3.1.1)
from .vector_memory import (
    NGramTFIDFProvider,
    PersistentVectorStore,
    MemoryEntry,
    MemoryTier,
    SearchResult
)

__all__ = [
    # Property Prediction
    'PropertyPredictor',
    'load_pretrained_model',
    # Composition Optimization
    'CompositionOptimizer',
    # Vector Memory
    'NGramTFIDFProvider',
    'PersistentVectorStore',
    'MemoryEntry',
    'MemoryTier',
    'SearchResult'
]
