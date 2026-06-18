# -*- coding: utf-8 -*-
"""
Materials-AI-Kit Models
=======================
AI-Powered Materials Science Prediction & Optimization

Modules:
- PropertyPredictor: CNN-based material strength prediction
- CompositionOptimizer: Inverse design for mix proportion optimization
"""

from models.property_predictor import PropertyPredictor
from models.composition_optimizer import CompositionOptimizer

__all__ = ['PropertyPredictor', 'CompositionOptimizer']
__version__ = '4.1.0'
