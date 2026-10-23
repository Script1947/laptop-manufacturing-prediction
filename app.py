"""
Root Entrypoint
"""
import sys
import os

project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "laptop_prediction_project")
sys.path.insert(0, project_dir)

with open(os.path.join(project_dir, "app.py"), "r", encoding="utf-8") as f:
    code = compile(f.read(), os.path.join(project_dir, "app.py"), 'exec')
    exec(code, globals())
