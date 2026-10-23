"""
Root Entrypoint for Training Pipeline
Runs laptop_prediction_project/train_model.py seamlessly.
"""
import sys
import os

project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "laptop_prediction_project")
sys.path.insert(0, project_dir)

from train_model import resolve_paths, load_and_validate_data, train_and_evaluate

if __name__ == "__main__":
    data_path, models_dir, outputs_dir = resolve_paths()
    dataset = load_and_validate_data(data_path)
    train_and_evaluate(dataset, models_dir, outputs_dir)
