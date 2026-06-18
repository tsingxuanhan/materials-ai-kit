#!/usr/bin/env python3
"""材料特征工程 — 从成分/结构计算描述符"""
import numpy as np
import pandas as pd

def composition_features(formula):
    """从化学式提取基本成分特征（示例）"""
    import re
    elements = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula)
    features = {}
    for elem, count in elements:
        count = float(count) if count else 1.0
        features[f"elem_{elem}"] = count
    features["num_elements"] = len(elements)
    return features

def statistical_features(X):
    """统计特征：均值、方差、偏度、峰度"""
    return {
        "mean": np.mean(X),
        "std": np.std(X),
        "skew": float(pd.Series(X).skew()),
        "kurtosis": float(pd.Series(X).kurtosis()),
        "min": np.min(X),
        "max": np.max(X),
        "range": np.max(X) - np.min(X),
    }

def generate_features(df, formula_col="formula"):
    """从DataFrame生成特征矩阵"""
    features_list = []
    for _, row in df.iterrows():
        feats = composition_features(row[formula_col])
        features_list.append(feats)
    return pd.DataFrame(features_list)

if __name__ == "__main__":
    # 示例
    df = pd.DataFrame({"formula": ["BaTiO3", "SrTiO3", "CaTiO3"]})
    feats = generate_features(df)
    print(feats)
