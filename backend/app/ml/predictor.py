import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

model = joblib.load(BASE_DIR / "data/processed/random_forest_model.pkl")
scaler = joblib.load(BASE_DIR / "data/processed/scaler.pkl")

FEATURES = list(model.feature_names_in_)

def predict_dengue_risk(input_data: dict):
    """
    input_data: JSON from API
    """

    # Create DataFrame with correct columns
    df = pd.DataFrame([input_data])

    # Add missing features as 0
    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns EXACTLY as training
    df = df[FEATURES]

    # Scale
    df_scaled = scaler.transform(df)

    # Predict
    prediction = model.predict(df_scaled)[0]
    probabilities = model.predict_proba(df_scaled)[0]

    return {
        "risk_level": int(prediction),
        "low_risk_prob": float(probabilities[0]),
        "medium_risk_prob": float(probabilities[1]),
        "high_risk_prob": float(probabilities[2])
    }
