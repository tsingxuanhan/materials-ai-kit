# -*- coding: utf-8 -*-
"""
Property Predictor - CNN-based Material Strength Prediction
Part of materials-ai-kit: AI-Powered Materials Property Prediction

This module provides a clean interface for predicting material properties
using trained CNN models.
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Union, Dict, List, Optional


class CNN1D(nn.Module):
    """
    1D Convolutional Neural Network for Property Prediction.
    
    Architecture:
        Input -> Conv1d -> BatchNorm -> ReLU -> MaxPool
             -> Conv1d -> BatchNorm -> ReLU -> MaxPool
             -> Flatten -> FC -> ReLU -> Dropout -> FC -> Output
    """
    
    def __init__(self, n_features: int = 6, hidden_channels: int = 64):
        super(CNN1D, self).__init__()
        
        self.conv_block1 = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        
        self.conv_block2 = nn.Sequential(
            nn.Conv1d(in_channels=32, out_channels=hidden_channels, kernel_size=3, padding=1),
            nn.BatchNorm1d(hidden_channels),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2)
        )
        
        self.fc = nn.Sequential(
            nn.Linear(hidden_channels, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 1)
        )
    
    def forward(self, x):
        # Reshape: (batch, n_features) -> (batch, 1, n_features)
        x = x.unsqueeze(1)
        
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        
        # Flatten: (batch, hidden_channels, seq_len) -> (batch, hidden_channels)
        x = x.squeeze(-1)
        
        return self.fc(x)


class PropertyPredictor:
    """
    High-level interface for material property prediction.
    
    Features:
        - Automatic feature scaling
        - Single sample or batch prediction
        - Confidence estimation
        - Feature importance analysis
    
    Example:
        >>> predictor = PropertyPredictor()
        >>> predictor.fit(X_train, y_train)
        >>> strength = predictor.predict({
        ...     'cement': 350, 'slag': 50, 'gypsum': 10,
        ...     'water': 180, 'fine_aggregate': 700, 'coarse_aggregate': 1000
        ... })
        >>> print(f"Predicted strength: {strength:.1f} MPa")
    """
    
    def __init__(self, hidden_channels: int = 64):
        self.model = CNN1D(n_features=6, hidden_channels=hidden_channels)
        self.scaler = None
        self.is_fitted = False
        
        # Statistics for prediction intervals
        self.train_std = None
    
    def fit(self, X: np.ndarray, y: np.ndarray, 
            epochs: int = 100, lr: float = 0.001, 
            val_split: float = 0.2,
            verbose: bool = True) -> Dict:
        """
        Train the model on provided data.
        
        Args:
            X: Feature matrix (n_samples, 6) with columns:
               [cement, slag, gypsum, water, fine_aggregate, coarse_aggregate]
            y: Target values (n_samples,) - typically 28-day strength in MPa
            epochs: Number of training epochs
            lr: Learning rate
            val_split: Fraction of data for validation
            verbose: Print training progress
        
        Returns:
            Dictionary with training history
        """
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        
        # Initialize scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Split for validation
        if val_split > 0:
            X_train, X_val, y_train, y_val = train_test_split(
                X_scaled, y, test_size=val_split, random_state=42
            )
        else:
            X_train, y_train = X_scaled, y
            X_val, y_val = X_train, y_train
        
        # Move to tensors
        X_train_t = torch.FloatTensor(X_train)
        y_train_t = torch.FloatTensor(y_train).reshape(-1, 1)
        X_val_t = torch.FloatTensor(X_val)
        y_val_t = torch.FloatTensor(y_val).reshape(-1, 1)
        
        # Training setup
        device = torch.device('cpu')
        self.model = self.model.to(device)
        
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=10
        )
        
        history = {'train_loss': [], 'val_loss': []}
        best_val_loss = float('inf')
        best_state = None
        
        for epoch in range(epochs):
            # Train
            self.model.train()
            optimizer.zero_grad()
            train_pred = self.model(X_train_t)
            train_loss = criterion(train_pred, y_train_t)
            train_loss.backward()
            optimizer.step()
            
            # Validate
            self.model.eval()
            with torch.no_grad():
                val_pred = self.model(X_val_t)
                val_loss = criterion(val_pred, y_val_t).item()
            
            scheduler.step(val_loss)
            history['train_loss'].append(train_loss.item())
            history['val_loss'].append(val_loss)
            
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_state = self.model.state_dict().copy()
            
            if verbose and (epoch + 1) % 20 == 0:
                print(f"Epoch {epoch+1:3d}: "
                      f"Train Loss={train_loss.item():.4f}, "
                      f"Val Loss={val_loss:.4f}")
        
        # Load best model
        self.model.load_state_dict(best_state)
        self.is_fitted = True
        self.train_std = np.std(y_train)
        
        return history
    
    def predict(self, X: Union[np.ndarray, Dict]) -> np.ndarray:
        """
        Predict material properties.
        
        Args:
            X: Either:
               - numpy array of shape (n_samples, 6)
               - dict with keys: cement, slag, gypsum, water, 
                                 fine_aggregate, coarse_aggregate
        
        Returns:
            Predicted values in original units
        """
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before prediction. Call fit() first.")
        
        self.model.eval()
        
        # Convert dict to array if needed
        if isinstance(X, dict):
            X = np.array([[
                X.get('cement', 0),
                X.get('slag', 0),
                X.get('gypsum', 0),
                X.get('water', 0),
                X.get('fine_aggregate', 0),
                X.get('coarse_aggregate', 0)
            ]])
        
        # Scale and predict
        X_scaled = self.scaler.transform(X)
        X_t = torch.FloatTensor(X_scaled)
        
        with torch.no_grad():
            predictions = self.model(X_t).squeeze().numpy()
        
        return predictions
    
    def predict_with_interval(self, X: Union[np.ndarray, Dict], 
                               confidence: float = 0.95) -> Dict:
        """
        Predict with prediction intervals.
        
        Args:
            X: Input features
            confidence: Confidence level (0-1)
        
        Returns:
            Dictionary with 'mean', 'lower', 'upper' predictions
        """
        from scipy import stats
        
        mean_pred = self.predict(X)
        
        # Approximate prediction interval using training std
        z = stats.norm.ppf((1 + confidence) / 2)
        margin = z * self.train_std
        
        if isinstance(mean_pred, np.ndarray) and mean_pred.ndim > 0:
            lower = mean_pred - margin
            upper = mean_pred + margin
        else:
            lower = mean_pred - margin
            upper = mean_pred + margin
        
        return {
            'mean': mean_pred,
            'lower': np.maximum(lower, 0),  # Strength can't be negative
            'upper': upper
        }
    
    def feature_importance(self, X_sample: Optional[np.ndarray] = None) -> Dict:
        """
        Estimate feature importance via gradient magnitude.
        
        Args:
            X_sample: Sample for gradient computation (uses mean if None)
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        feature_names = ['cement', 'slag', 'gypsum', 'water', 
                        'fine_aggregate', 'coarse_aggregate']
        
        if X_sample is None:
            # Use mean values from training data
            X_sample = self.scaler.mean_
        
        X_t = torch.FloatTensor(X_sample, requires_grad=True)
        
        self.model.eval()
        output = self.model(X_t.unsqueeze(0))
        
        # Compute gradients
        output.backward()
        gradients = X_t.grad.abs().detach().numpy()
        
        # Normalize to sum to 1
        importance = gradients / gradients.sum()
        
        return dict(zip(feature_names, importance))
    
    def save(self, path: str):
        """Save model to disk."""
        torch.save({
            'model_state': self.model.state_dict(),
            'scaler_mean': self.scaler.mean_,
            'scaler_scale': self.scaler.scale_,
            'train_std': self.train_std
        }, path)
    
    @classmethod
    def load(cls, path: str) -> 'PropertyPredictor':
        """Load model from disk."""
        from sklearn.preprocessing import StandardScaler
        
        checkpoint = torch.load(path, map_location='cpu')
        
        predictor = cls()
        predictor.model.load_state_dict(checkpoint['model_state'])
        
        predictor.scaler = StandardScaler()
        predictor.scaler.mean_ = checkpoint['scaler_mean']
        predictor.scaler.scale_ = checkpoint['scaler_scale']
        
        predictor.train_std = checkpoint.get('train_std', 5.0)
        predictor.is_fitted = True
        
        return predictor


def load_pretrained_model(path: str) -> PropertyPredictor:
    """
    Load a pretrained property predictor model.
    
    Args:
        path: Path to saved model file
    
    Returns:
        Loaded PropertyPredictor instance
    """
    return PropertyPredictor.load(path)


# Example usage
if __name__ == "__main__":
    # Quick demo
    print("PropertyPredictor - Quick Demo")
    print("-" * 40)
    
    # Generate synthetic data
    np.random.seed(42)
    n_samples = 100
    X = np.random.uniform([200, 0, 5, 150, 600, 900],
                          [400, 150, 15, 190, 850, 1050],
                          (n_samples, 6))
    
    # Generate realistic strength values
    w_b = X[:, 3] / (X[:, 0] + X[:, 1])
    y = 60 * (1 - 0.5 * w_b) + 0.02 * X[:, 0] + np.random.normal(0, 3, n_samples)
    
    # Train
    predictor = PropertyPredictor()
    history = predictor.fit(X, y, epochs=50, verbose=False)
    
    print(f"Final validation loss: {history['val_loss'][-1]:.4f}")
    
    # Predict
    test_mix = {
        'cement': 350, 'slag': 50, 'gypsum': 10,
        'water': 175, 'fine_aggregate': 750, 'coarse_aggregate': 1000
    }
    
    result = predictor.predict_with_interval(test_mix)
    print(f"\nTest mix: {test_mix['cement']:.0f} kg cement, W/B={test_mix['water']/(test_mix['cement']+test_mix['slag']):.2f}")
    print(f"Predicted strength: {result['mean']:.1f} MPa "
          f"(95% CI: {result['lower']:.1f} - {result['upper']:.1f} MPa)")
    
    print("\nFeature importance:")
    for feat, imp in predictor.feature_importance().items():
        print(f"  {feat:20s}: {imp:.3f}")
