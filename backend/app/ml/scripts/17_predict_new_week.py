import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

model = joblib.load(
    BASE_DIR / "backend/app/models/random_forest_model.pkl"
)

scaler = joblib.load(
    BASE_DIR / "data/processed/scaler.pkl"
)

def predict_risk(new_data_df):
    scaled = scaler.transform(new_data_df)
    return model.predict(scaled)

print("✅ STEP 17 — Prediction function ready")
