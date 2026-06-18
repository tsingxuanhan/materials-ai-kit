#!/usr/bin/env python3
"""材料数据Pipeline — 集成MLflow实验追踪"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import mlflow
import mlflow.sklearn

# MLflow配置
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("mat-prop-prediction")

def run_pipeline(data_path, target_col, test_size=0.2):
    """运行完整的材料性质预测pipeline"""
    with mlflow.start_run():
        # 1. 加载数据
        df = pd.read_csv(data_path)
        X = df.drop(columns=[target_col])
        y = df[target_col]

        # 2. 分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )

        # 3. 训练
        model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42
        )
        model.fit(X_train, y_train)

        # 4. 评估
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # 5. 日志
        mlflow.log_params({"model": "RF", "n_estimators": 100})
        mlflow.log_metrics({"mae": mae, "r2": r2})
        mlflow.sklearn.log_model(model, "model")

        print(f"MAE: {mae:.4f}, R2: {r2:.4f}")
        return model, {"mae": mae, "r2": r2}

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python mat_pipeline.py <data.csv> <target_column>")
        sys.exit(1)
    run_pipeline(sys.argv[1], sys.argv[2])
