"""
Machine Learning Training Pipeline
Project: Machine Learning-Based Component-Wise Manufacturing Time and Cost Prediction for Laptops

Author: 5th-Semester CSE Student Project
Description:
    Trains two separate regression models:
    - Model A: Predicts 'Actual_Time_Minutes'
    - Model B: Predicts 'Actual_Cost_INR'
    Uses a 70% Training / 30% Testing split, ColumnTransformer preprocessing,
    RandomForestRegressor, and baseline Linear Regression comparison.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score


def resolve_paths():
    """Resolve file paths relative to script directory or working directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "data", "laptop_manufacturing_assembly_dataset_600_rows.csv"),
        os.path.join(script_dir, "..", "laptop_manufacturing_assembly_dataset_600_rows.csv"),
        os.path.join(os.getcwd(), "data", "laptop_manufacturing_assembly_dataset_600_rows.csv"),
        os.path.join(os.getcwd(), "laptop_manufacturing_assembly_dataset_600_rows.csv"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            data_path = os.path.abspath(p)
            break
    else:
        raise FileNotFoundError(
            "Could not locate 'laptop_manufacturing_assembly_dataset_600_rows.csv'. "
            "Please ensure the dataset file is placed in data/ or the current directory."
        )

    models_dir = os.path.join(script_dir, "models")
    outputs_dir = os.path.join(script_dir, "outputs")
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(outputs_dir, exist_ok=True)

    return data_path, models_dir, outputs_dir


def load_and_validate_data(data_path):
    """Load CSV dataset and perform thorough quality validation."""
    print("=" * 70)
    print("STEP 1: LOADING & INSPECTING DATASET")
    print(f"Data source: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape[0]} rows, {df.shape[1]} columns")

    expected_cols = [
        "Component_Type", "Process_Type", "Material", "Length_mm",
        "Width_mm", "Height_mm", "Production_Quantity",
        "Manufacturing_Process", "Complexity_Level", "Machine_Type",
        "Shift_Type", "Actual_Time_Minutes", "Actual_Cost_INR"
    ]
    missing_cols = [c for c in expected_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    # Check missing values
    null_counts = df.isnull().sum()
    total_nulls = null_counts.sum()
    print(f"Total null / missing values: {total_nulls}")
    if total_nulls > 0:
        print("Warning: Missing values found, dropping incomplete rows...")
        df = df.dropna().reset_index(drop=True)

    # Check duplicates
    dups = df.duplicated().sum()
    print(f"Duplicate rows detected: {dups}")
    if dups > 0:
        df = df.drop_duplicates().reset_index(drop=True)

    # Validate numeric ranges
    numeric_checks = {
        "Length_mm": df["Length_mm"] > 0,
        "Width_mm": df["Width_mm"] > 0,
        "Height_mm": df["Height_mm"] > 0,
        "Production_Quantity": df["Production_Quantity"] > 0,
        "Complexity_Level": df["Complexity_Level"] > 0,
        "Actual_Time_Minutes": df["Actual_Time_Minutes"] > 0,
        "Actual_Cost_INR": df["Actual_Cost_INR"] > 0,
    }
    for col_name, valid_mask in numeric_checks.items():
        invalid_cnt = (~valid_mask).sum()
        if invalid_cnt > 0:
            raise ValueError(f"Found {invalid_cnt} non-positive values in column '{col_name}'!")

    print("Data validation successful: All records are strictly positive and valid.")
    print("=" * 70)
    return df


def train_and_evaluate(df, models_dir, outputs_dir):
    """
    Train Model A (Time) and Model B (Cost) using 70/30 train/test split.
    Save models and evaluation metrics.
    """
    print("\nSTEP 2: FEATURE ENGINEERING & TRAIN-TEST SPLIT (70/30)")

    categorical_features = [
        "Component_Type", "Process_Type", "Material",
        "Manufacturing_Process", "Machine_Type", "Shift_Type"
    ]
    numerical_features = [
        "Length_mm", "Width_mm", "Height_mm",
        "Production_Quantity", "Complexity_Level"
    ]
    feature_cols = categorical_features + numerical_features

    X = df[feature_cols].copy()
    y_time = df["Actual_Time_Minutes"].copy()
    y_cost = df["Actual_Cost_INR"].copy()

    # Fixed random state for 100% reproducibility across runs
    RANDOM_STATE = 42
    TEST_SIZE = 0.30

    X_train, X_test, y_time_train, y_time_test, y_cost_train, y_cost_test = train_test_split(
        X, y_time, y_cost, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    print(f"Total dataset size : {len(df)} rows")
    print(f"Training set (70%) : {len(X_train)} rows")
    print(f"Testing set (30%)  : {len(X_test)} rows")

    # Build preprocessing pipeline
    # Categorical: OneHotEncoder with handle_unknown='ignore' prevents runtime crash on new categories
    # Numerical: StandardScaler
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_features),
            ("num", StandardScaler(), numerical_features),
        ]
    )

    print("\nSTEP 3: MODEL TRAINING (Model A: Time, Model B: Cost)")

    # Model A: Random Forest for Time
    time_rf_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1))
    ])

    # Model B: Random Forest for Cost
    cost_rf_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=RANDOM_STATE, n_jobs=-1))
    ])

    # Baseline Models: Linear Regression for academic comparison
    time_lr_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])
    cost_lr_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])

    print("Fitting models strictly on Training data (avoiding data leakage)...")
    time_rf_pipeline.fit(X_train, y_time_train)
    cost_rf_pipeline.fit(X_train, y_cost_train)

    time_lr_pipeline.fit(X_train, y_time_train)
    cost_lr_pipeline.fit(X_train, y_cost_train)
    print("Model fitting complete.")

    print("\nSTEP 4: MODEL EVALUATION ON HELD-OUT TEST DATA (180 samples)")

    # Predictions
    y_time_rf_pred = time_rf_pipeline.predict(X_test)
    y_cost_rf_pred = cost_rf_pipeline.predict(X_test)

    y_time_lr_pred = time_lr_pipeline.predict(X_test)
    y_cost_lr_pred = cost_lr_pipeline.predict(X_test)

    # Metrics calculation
    metrics = {
        "split_info": {
            "total_samples": int(len(df)),
            "train_samples": int(len(X_train)),
            "test_samples": int(len(X_test)),
            "train_ratio": 0.70,
            "test_ratio": 0.30,
            "random_state": RANDOM_STATE
        },
        "time_model": {
            "random_forest": {
                "mae": float(mean_absolute_error(y_time_test, y_time_rf_pred)),
                "rmse": float(root_mean_squared_error(y_time_test, y_time_rf_pred)),
                "r2_score": float(r2_score(y_time_test, y_time_rf_pred))
            },
            "linear_baseline": {
                "mae": float(mean_absolute_error(y_time_test, y_time_lr_pred)),
                "rmse": float(root_mean_squared_error(y_time_test, y_time_lr_pred)),
                "r2_score": float(r2_score(y_time_test, y_time_lr_pred))
            }
        },
        "cost_model": {
            "random_forest": {
                "mae": float(mean_absolute_error(y_cost_test, y_cost_rf_pred)),
                "rmse": float(root_mean_squared_error(y_cost_test, y_cost_rf_pred)),
                "r2_score": float(r2_score(y_cost_test, y_cost_rf_pred))
            },
            "linear_baseline": {
                "mae": float(mean_absolute_error(y_cost_test, y_cost_lr_pred)),
                "rmse": float(root_mean_squared_error(y_cost_test, y_cost_lr_pred)),
                "r2_score": float(r2_score(y_cost_test, y_cost_lr_pred))
            }
        }
    }

    # Print results to terminal
    print("=" * 70)
    print("EVALUATION RESULTS (Held-Out Test Set: 180 rows)")
    print("=" * 70)
    print(f"{'Target / Model':<35} | {'MAE':<10} | {'RMSE':<10} | {'R² Score':<10}")
    print("-" * 70)
    tf_m = metrics["time_model"]["random_forest"]
    print(f"{'Time Model (Random Forest)':<35} | {tf_m['mae']:<10.2f} | {tf_m['rmse']:<10.2f} | {tf_m['r2_score']:<10.4f}")
    tl_m = metrics["time_model"]["linear_baseline"]
    print(f"{'Time Model (Linear Regression Baseline)':<35} | {tl_m['mae']:<10.2f} | {tl_m['rmse']:<10.2f} | {tl_m['r2_score']:<10.4f}")
    print("-" * 70)
    cf_m = metrics["cost_model"]["random_forest"]
    print(f"{'Cost Model (Random Forest)':<35} | {cf_m['mae']:<10.2f} | {cf_m['rmse']:<10.2f} | {cf_m['r2_score']:<10.4f}")
    cl_m = metrics["cost_model"]["linear_baseline"]
    print(f"{'Cost Model (Linear Regression Baseline)':<35} | {cl_m['mae']:<10.2f} | {cl_m['rmse']:<10.2f} | {cl_m['r2_score']:<10.4f}")
    print("=" * 70)

    # Extract feature importances from Random Forest models
    fitted_preprocessor = time_rf_pipeline.named_steps["preprocessor"]
    transformed_feature_names = fitted_preprocessor.get_feature_names_out()

    time_rf_reg = time_rf_pipeline.named_steps["regressor"]
    cost_rf_reg = cost_rf_pipeline.named_steps["regressor"]

    time_importances = sorted(
        [{"feature": f.replace("cat__", "").replace("num__", ""), "importance": float(imp)}
         for f, imp in zip(transformed_feature_names, time_rf_reg.feature_importances_)],
        key=lambda x: x["importance"], reverse=True
    )
    cost_importances = sorted(
        [{"feature": f.replace("cat__", "").replace("num__", ""), "importance": float(imp)}
         for f, imp in zip(transformed_feature_names, cost_rf_reg.feature_importances_)],
        key=lambda x: x["importance"], reverse=True
    )

    feature_importances_data = {
        "time_feature_importances": time_importances,
        "cost_feature_importances": cost_importances
    }

    # Save artifacts
    print("\nSTEP 5: SAVING TRAINED ARTIFACTS")
    time_model_path = os.path.join(models_dir, "time_model.pkl")
    cost_model_path = os.path.join(models_dir, "cost_model.pkl")
    metrics_path = os.path.join(outputs_dir, "evaluation_metrics.json")
    importance_path = os.path.join(outputs_dir, "feature_importances.json")
    test_preds_path = os.path.join(outputs_dir, "test_predictions.csv")
    metadata_path = os.path.join(outputs_dir, "metadata.json")

    joblib.dump(time_rf_pipeline, time_model_path)
    joblib.dump(cost_rf_pipeline, cost_model_path)
    print(f"Saved Time Model : {time_model_path}")
    print(f"Saved Cost Model : {cost_model_path}")

    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Saved Evaluation Metrics : {metrics_path}")

    with open(importance_path, "w") as f:
        json.dump(feature_importances_data, f, indent=2)
    print(f"Saved Feature Importances : {importance_path}")

    # Save test set actual vs predicted for interactive web visualizations
    test_eval_df = X_test.copy()
    test_eval_df["Actual_Time_Minutes"] = y_time_test.values
    test_eval_df["Predicted_Time_Minutes"] = y_time_rf_pred
    test_eval_df["Time_Error"] = y_time_rf_pred - y_time_test.values

    test_eval_df["Actual_Cost_INR"] = y_cost_test.values
    test_eval_df["Predicted_Cost_INR"] = y_cost_rf_pred
    test_eval_df["Cost_Error"] = y_cost_rf_pred - y_cost_test.values
    test_eval_df.to_csv(test_preds_path, index=False)
    print(f"Saved Test Predictions : {test_preds_path}")

    # Extract component profiles for intelligent UI auto-filling
    profiles = {}
    for comp, group in df.groupby("Component_Type"):
        profiles[comp] = {
            "Process_Type": group["Process_Type"].mode()[0],
            "Material": group["Material"].mode()[0],
            "Length_mm": int(group["Length_mm"].median()),
            "Width_mm": int(group["Width_mm"].median()),
            "Height_mm": int(group["Height_mm"].median()),
            "Manufacturing_Process": group["Manufacturing_Process"].mode()[0],
            "Complexity_Level": float(group["Complexity_Level"].mode()[0]),
            "Machine_Type": group["Machine_Type"].mode()[0],
            "Default_Quantity": 1
        }

    metadata = {
        "categorical_columns": categorical_features,
        "numerical_columns": numerical_features,
        "unique_values": {col: sorted(df[col].unique().tolist()) for col in categorical_features},
        "component_profiles": profiles
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved Metadata & Profiles: {metadata_path}")

    print("\nTraining Pipeline Completed Successfully!")
    return metrics


if __name__ == "__main__":
    data_path, models_dir, outputs_dir = resolve_paths()
    dataset = load_and_validate_data(data_path)
    train_and_evaluate(dataset, models_dir, outputs_dir)
