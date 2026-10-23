"""
Unit and Integration Verification Script
Project: Machine Learning-Based Component-Wise Manufacturing Time and Cost Prediction for Laptops

Author: 5th-Semester CSE Student Project
Description:
    Verifies that:
    1. Saved models load correctly.
    2. Model inputs produce valid, positive predictions for both targets.
    3. Handles unknown categories safely without crashing.
    4. Evaluates predictions on test data and verifies metrics.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_tests():
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE")
    print("=" * 60)

    # 1. Check artifact presence
    time_model_path = os.path.join(BASE_DIR, "models", "time_model.pkl")
    cost_model_path = os.path.join(BASE_DIR, "models", "cost_model.pkl")
    metrics_path = os.path.join(BASE_DIR, "outputs", "evaluation_metrics.json")
    test_preds_path = os.path.join(BASE_DIR, "outputs", "test_predictions.csv")

    assert os.path.exists(time_model_path), f"Missing {time_model_path}"
    assert os.path.exists(cost_model_path), f"Missing {cost_model_path}"
    assert os.path.exists(metrics_path), f"Missing {metrics_path}"
    assert os.path.exists(test_preds_path), f"Missing {test_preds_path}"
    print("[PASS] All 4 model and output artifacts exist.")

    # 2. Load models
    time_model = joblib.load(time_model_path)
    cost_model = joblib.load(cost_model_path)
    print("[PASS] Both Random Forest pipelines loaded successfully via joblib.")

    # 3. Test single prediction: Manufacturing component (Laptop Casing)
    sample_mfg = pd.DataFrame([{
        "Component_Type": "Laptop_Casing",
        "Process_Type": "Manufacturing",
        "Material": "Aluminum",
        "Length_mm": 320,
        "Width_mm": 220,
        "Height_mm": 8,
        "Production_Quantity": 50,
        "Manufacturing_Process": "CNC_Machining",
        "Complexity_Level": 1.3,
        "Machine_Type": "CNC_Machine",
        "Shift_Type": "Day"
    }])
    pred_time_mfg = time_model.predict(sample_mfg)[0]
    pred_cost_mfg = cost_model.predict(sample_mfg)[0]
    assert pred_time_mfg > 0, "Time prediction must be positive"
    assert pred_cost_mfg > 0, "Cost prediction must be positive"
    print(f"[PASS] Manufacturing Sample: Time = {pred_time_mfg:.2f} mins, Cost = INR {pred_cost_mfg:.2f}")

    # 4. Test single prediction: Assembly operation (RAM Installation)
    sample_asm = pd.DataFrame([{
        "Component_Type": "RAM_Installation",
        "Process_Type": "Assembly",
        "Material": "Purchased_Electronics",
        "Length_mm": 70,
        "Width_mm": 30,
        "Height_mm": 3,
        "Production_Quantity": 20,
        "Manufacturing_Process": "Slot_Insertion",
        "Complexity_Level": 1.0,
        "Machine_Type": "Assembly_Workstation",
        "Shift_Type": "Day"
    }])
    pred_time_asm = time_model.predict(sample_asm)[0]
    pred_cost_asm = cost_model.predict(sample_asm)[0]
    assert pred_time_asm > 0, "Time prediction must be positive"
    assert pred_cost_asm > 0, "Cost prediction must be positive"
    print(f"[PASS] Assembly Sample: Time = {pred_time_asm:.2f} mins, Cost = INR {pred_cost_asm:.2f}")

    # 5. Test unknown categorical value robustness
    sample_unseen = pd.DataFrame([{
        "Component_Type": "Unseen_Component",
        "Process_Type": "Custom_Process",
        "Material": "Titanium_Alloy",
        "Length_mm": 150,
        "Width_mm": 100,
        "Height_mm": 10,
        "Production_Quantity": 10,
        "Manufacturing_Process": "Laser_Sintering",
        "Complexity_Level": 1.2,
        "Machine_Type": "3D_Printer",
        "Shift_Type": "Morning"
    }])
    pred_time_unseen = time_model.predict(sample_unseen)[0]
    pred_cost_unseen = cost_model.predict(sample_unseen)[0]
    assert pred_time_unseen > 0, "Unseen category time prediction must be positive"
    assert pred_cost_unseen > 0, "Unseen category cost prediction must be positive"
    print(f"[PASS] Unknown Category Robustness: Handled safely without error! (Time: {pred_time_unseen:.2f} min, Cost: INR {pred_cost_unseen:.2f})")

    # 6. Verify metrics against saved test set predictions
    test_df = pd.read_csv(test_preds_path)
    assert len(test_df) == 180, f"Expected 180 test rows (30%), got {len(test_df)}"

    recalc_mae_time = mean_absolute_error(test_df["Actual_Time_Minutes"], test_df["Predicted_Time_Minutes"])
    recalc_r2_time = r2_score(test_df["Actual_Time_Minutes"], test_df["Predicted_Time_Minutes"])
    recalc_mae_cost = mean_absolute_error(test_df["Actual_Cost_INR"], test_df["Predicted_Cost_INR"])
    recalc_r2_cost = r2_score(test_df["Actual_Cost_INR"], test_df["Predicted_Cost_INR"])

    with open(metrics_path, "r") as f:
        saved_metrics = json.load(f)

    expected_mae_time = saved_metrics["time_model"]["random_forest"]["mae"]
    expected_r2_time = saved_metrics["time_model"]["random_forest"]["r2_score"]
    expected_mae_cost = saved_metrics["cost_model"]["random_forest"]["mae"]
    expected_r2_cost = saved_metrics["cost_model"]["random_forest"]["r2_score"]

    assert np.isclose(recalc_mae_time, expected_mae_time, atol=1e-3), "Recalculated Time MAE does not match!"
    assert np.isclose(recalc_r2_time, expected_r2_time, atol=1e-3), "Recalculated Time R2 does not match!"
    assert np.isclose(recalc_mae_cost, expected_mae_cost, atol=1e-3), "Recalculated Cost MAE does not match!"
    assert np.isclose(recalc_r2_cost, expected_r2_cost, atol=1e-3), "Recalculated Cost R2 does not match!"

    print("[PASS] Test Set Metrics strictly verified on 180 held-out samples:")
    print(f"   Time Model -> MAE: {recalc_mae_time:.2f} mins, R2: {recalc_r2_time:.4f}")
    print(f"   Cost Model -> MAE: INR {recalc_mae_cost:.2f}, R2: {recalc_r2_cost:.4f}")

    print("=" * 60)
    print("ALL TESTS PASSED SUCCESSFULLY! [100% OK]")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
