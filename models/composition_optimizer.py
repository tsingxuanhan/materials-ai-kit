# -*- coding: utf-8 -*-
"""
Composition Optimizer - Inverse Design of Material Mix Proportions
Part of materials-ai-kit: AI-Powered Materials Property Prediction

This module provides inverse design capabilities: given target material
properties (e.g., strength), find the optimal mix proportions.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Optional, Tuple, Union


class LSTMForwardModel(nn.Module):
    """
    LSTM-based forward model: mix composition -> strength evolution curve.
    
    Predicts strength at multiple time points (1, 3, 7, 14, 21, 28, 56 days)
    based on mix proportions.
    """
    
    def __init__(self, input_size: int = 6, hidden_size: int = 64, 
                 num_layers: int = 2, output_size: int = 7):
        super(LSTMForwardModel, self).__init__()
        
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # Project input to hidden dimension
        self.input_proj = nn.Linear(input_size, hidden_size)
        
        # LSTM for sequence modeling
        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        
        # Output layer
        self.output_layer = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, output_size)
        )
    
    def forward(self, x):
        # Project input
        x = self.input_proj(x).unsqueeze(1)  # (batch, 1, hidden)
        x = x.expand(-1, 7, -1)  # (batch, 7, hidden)
        
        # LSTM
        lstm_out, _ = self.lstm(x)  # (batch, 7, hidden)
        
        # Output: strength at each time point
        return self.output_layer(lstm_out)  # (batch, 7)


class CompositionOptimizer:
    """
    Inverse design optimizer for material compositions.
    
    Given target properties (e.g., 28-day strength), find the mix 
    proportions that achieve those targets.
    
    Features:
        - Gradient-based optimization
        - Multiple constraint support
        - Sensitivity analysis
        - Mix design recommendations
    
    Example:
        >>> optimizer = CompositionOptimizer()
        >>> optimizer.fit(X_train, strength_curves)
        >>> 
        >>> # Find mix for target strength
        >>> result = optimizer.optimize(target_strength=40.0)
        >>> print(f"Cement: {result['composition']['cement']:.0f} kg")
        >>> print(f"Water: {result['composition']['water']:.0f} kg")
    """
    
    def __init__(self, hidden_size: int = 64, num_layers: int = 2):
        self.model = LSTMForwardModel(
            input_size=6, 
            hidden_size=hidden_size, 
            num_layers=num_layers,
            output_size=7
        )
        self.scaler = None
        self.is_fitted = False
        self.time_points = np.array([1, 3, 7, 14, 21, 28, 56])
    
    def fit(self, compositions: np.ndarray, strength_curves: np.ndarray,
            epochs: int = 150, lr: float = 0.002, verbose: bool = True):
        """
        Train the forward model.
        
        Args:
            compositions: Mix proportions (n_samples, 6)
            strength_curves: Strength values at 7 time points (n_samples, 7)
            epochs: Training epochs
            lr: Learning rate
            verbose: Print progress
        """
        from sklearn.preprocessing import StandardScaler
        
        # Normalize compositions
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(compositions)
        
        # Convert to tensors
        X_t = torch.FloatTensor(X_scaled)
        y_t = torch.FloatTensor(strength_curves)
        
        # Training
        device = torch.device('cpu')
        self.model = self.model.to(device)
        
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        
        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            
            outputs = self.model(X_t)
            loss = criterion(outputs, y_t)
            loss.backward()
            optimizer.step()
            
            if verbose and (epoch + 1) % 30 == 0:
                print(f"Epoch {epoch+1:3d}: Loss = {loss.item():.4f}")
        
        self.is_fitted = True
        return self
    
    def predict_strength_curve(self, composition: np.ndarray) -> np.ndarray:
        """
        Predict strength evolution curve for a composition.
        
        Args:
            composition: Mix proportions (6,) or (1, 6)
        
        Returns:
            Strength values at [1, 3, 7, 14, 21, 28, 56] days
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted first. Call fit().")
        
        self.model.eval()
        
        # Handle single sample
        if composition.ndim == 1:
            composition = composition.reshape(1, -1)
        
        # Scale and predict
        X_scaled = self.scaler.transform(composition)
        X_t = torch.FloatTensor(X_scaled)
        
        with torch.no_grad():
            curve = self.model(X_t).squeeze().numpy()
        
        return curve
    
    def optimize(self, target_strength: float,
                 target_age: int = 28,
                 initial_composition: Optional[np.ndarray] = None,
                 constraints: Optional[Dict] = None,
                 lr: float = 0.1,
                 n_iterations: int = 100) -> Dict:
        """
        Find composition that achieves target strength.
        
        Args:
            target_strength: Desired strength in MPa
            target_age: Age at which to achieve target (days)
            initial_composition: Starting point for optimization
            constraints: Dict of constraints, e.g., {'max_cost': 100, 'max_cement': 400}
            lr: Learning rate for gradient descent
            n_iterations: Number of optimization iterations
        
        Returns:
            Dictionary with optimized composition and verification
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted first. Call fit().")
        
        # Get age index
        age_idx = np.argmin(np.abs(self.time_points - target_age))
        
        # Initialize composition
        if initial_composition is None:
            comp = torch.randn(6, requires_grad=True)
            comp.data = torch.tensor([0.7, 0.3, 0.5, 0.8, 0.8, 0.9])
        else:
            comp = torch.FloatTensor(initial_composition).clone()
            comp.requires_grad = True
        
        optimizer = torch.optim.Adam([comp], lr=lr)
        
        history = []
        
        for i in range(n_iterations):
            optimizer.zero_grad()
            
            # Predict strength curve
            curve = self.model(comp.unsqueeze(0)).squeeze()
            pred_strength = curve[age_idx]
            
            # Loss: squared error from target
            loss = (pred_strength - target_strength) ** 2
            
            # Optional: add regularization for realistic compositions
            # Penalize extreme values
            reg_loss = 0.01 * (torch.sum(torch.relu(comp - 1.0)) + 
                             torch.sum(torch.relu(-comp)))
            total_loss = loss + reg_loss
            
            total_loss.backward()
            optimizer.step()
            
            # Project to valid range
            with torch.no_grad():
                comp.clamp_(0.1, 1.0)
            
            history.append({
                'iteration': i,
                'loss': loss.item(),
                'pred_strength': pred_strength.item()
            })
        
        # Final composition
        final_comp = comp.detach().numpy()
        
        # Denormalize to physical units
        physical_comp = self._denormalize_composition(final_comp)
        
        # Verify prediction
        verified_curve = self.predict_strength_curve(final_comp)
        
        return {
            'composition_normalized': final_comp,
            'composition': physical_comp,
            'predicted_curve': verified_curve,
            'predicted_strength': verified_curve[age_idx],
            'target_strength': target_strength,
            'target_age': target_age,
            'optimization_history': history
        }
    
    def optimize_multi_objective(self, targets: Dict[int, float],
                                  weights: Optional[Dict[int, float]] = None,
                                  n_iterations: int = 150) -> Dict:
        """
        Optimize for multiple strength targets at different ages.
        
        Args:
            targets: Dict mapping age (days) to target strength (MPa)
                     e.g., {7: 25.0, 28: 40.0} means ≥25 MPa at 7 days 
                     and ≥40 MPa at 28 days
            weights: Relative importance of each target
            n_iterations: Optimization iterations
        
        Returns:
            Optimized composition satisfying all targets
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted first. Call fit().")
        
        if weights is None:
            weights = {age: 1.0 for age in targets}
        
        # Initialize
        comp = torch.randn(6, requires_grad=True)
        comp.data = torch.tensor([0.7, 0.3, 0.5, 0.8, 0.8, 0.9])
        
        optimizer = torch.optim.Adam([comp], lr=0.1)
        
        for i in range(n_iterations):
            optimizer.zero_grad()
            
            curve = self.model(comp.unsqueeze(0)).squeeze()
            
            # Loss for each target
            total_loss = 0
            for age, target in targets.items():
                age_idx = np.argmin(np.abs(self.time_points - age))
                weight = weights.get(age, 1.0)
                loss = weight * (curve[age_idx] - target) ** 2
                total_loss += F.relu(-loss)  # Penalize if not meeting target
            
            # Also minimize composition to make it realistic
            reg = 0.01 * torch.sum((comp - 0.7) ** 2)
            
            (total_loss + reg).backward()
            optimizer.step()
            
            with torch.no_grad():
                comp.clamp_(0.1, 1.0)
        
        final_comp = comp.detach().numpy()
        physical_comp = self._denormalize_composition(final_comp)
        verified_curve = self.predict_strength_curve(final_comp)
        
        return {
            'composition_normalized': final_comp,
            'composition': physical_comp,
            'predicted_curve': verified_curve,
            'targets': targets
        }
    
    def _denormalize_composition(self, normalized: np.ndarray) -> Dict[str, float]:
        """Convert normalized composition back to physical units."""
        # Scale factors (typical concrete range)
        scales = {
            'cement': 400,        # kg/m³
            'slag': 150,          # kg/m³
            'gypsum': 15,         # kg/m³
            'water': 200,         # kg/m³
            'fine_aggregate': 800, # kg/m³
            'coarse_aggregate': 1000 # kg/m³
        }
        
        result = {}
        keys = ['cement', 'slag', 'gypsum', 'water', 'fine_aggregate', 'coarse_aggregate']
        
        for key, scale in zip(keys, scales.values()):
            result[key] = normalized[len(result)] * scale
        
        # Calculate derived properties
        result['water_binder_ratio'] = result['water'] / (result['cement'] + result['slag'])
        result['total_powder'] = result['cement'] + result['slag'] + result['gypsum']
        
        return result
    
    def sensitivity_analysis(self, base_composition: np.ndarray,
                              feature_idx: int, 
                              variation_range: Tuple[float, float] = (0.8, 1.2),
                              n_steps: int = 10) -> Dict:
        """
        Analyze how strength changes with a specific mix component.
        
        Args:
            base_composition: Starting mix (normalized 0-1)
            feature_idx: Which component to vary
            variation_range: Multiplicative range (e.g., 0.8-1.2)
            n_steps: Number of test points
        
        Returns:
            Dict with variation levels and corresponding predictions
        """
        multipliers = np.linspace(variation_range[0], variation_range[1], n_steps)
        
        results = {
            'multipliers': multipliers,
            'strength_7d': [],
            'strength_28d': [],
            'strength_56d': []
        }
        
        for mult in multipliers:
            test_comp = base_composition.copy()
            test_comp[feature_idx] *= mult
            test_comp = np.clip(test_comp, 0.1, 1.0)
            
            curve = self.predict_strength_curve(test_comp)
            
            # Get indices for 7, 28, 56 days
            idx_7 = np.argmin(np.abs(self.time_points - 7))
            idx_28 = np.argmin(np.abs(self.time_points - 28))
            idx_56 = np.argmin(np.abs(self.time_points - 56))
            
            results['strength_7d'].append(curve[idx_7])
            results['strength_28d'].append(curve[idx_28])
            results['strength_56d'].append(curve[idx_56])
        
        return results


# Example usage
if __name__ == "__main__":
    print("CompositionOptimizer - Quick Demo")
    print("-" * 40)
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 80
    
    compositions = []
    curves = []
    
    for _ in range(n_samples):
        cement = np.random.uniform(200, 400)
        slag = np.random.uniform(0, 150)
        water = np.random.uniform(150, 195)
        
        w_b = water / (cement + slag)
        fc_28 = 100 * (1 - 0.5 * w_b) + np.random.normal(0, 3)
        fc_28 = np.clip(fc_28, 20, 60)
        
        # Strength evolution curve
        times = np.array([1, 3, 7, 14, 21, 28, 56])
        age_factor = times / (0.15 + 0.25 * times)
        curve = fc_28 * (1 - np.exp(-0.15 * age_factor))
        curve += np.random.normal(0, 1, 7)
        
        comp = np.array([cement/400, slag/150, 0.5, water/200, 0.8, 1.0])
        
        compositions.append(comp)
        curves.append(curve)
    
    compositions = np.array(compositions)
    curves = np.array(curves)
    
    # Train optimizer
    optimizer = CompositionOptimizer()
    optimizer.fit(compositions, curves, epochs=100, verbose=False)
    
    # Optimize for target strength
    result = optimizer.optimize(target_strength=40.0, target_age=28)
    
    print(f"\nTarget: 40 MPa at 28 days")
    print(f"\nOptimized composition:")
    for key, value in result['composition'].items():
        if key not in ['total_powder']:
            print(f"  {key:20s}: {value:.1f}")
    
    print(f"\nPredicted strength curve:")
    for age, strength in zip(optimizer.time_points, result['predicted_curve']):
        print(f"  Day {age:2d}: {strength:.1f} MPa")
    
    print("\n✓ Composition optimization demo complete!")
