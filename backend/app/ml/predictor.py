import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import shap

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[3]
MODEL_DIR = BASE_DIR / "backend/app/models"

# --------------------------------------------------
# Load model & scaler
# --------------------------------------------------
rf_model = joblib.load(MODEL_DIR / "random_forest_model.pkl")
scaler = joblib.load(BASE_DIR / "data/processed/scaler.pkl")

FEATURES = list(rf_model.feature_names_in_)

# --------------------------------------------------
# SHAP Explainer
# --------------------------------------------------
rf_explainer = shap.TreeExplainer(rf_model)

# --------------------------------------------------
# USER-FRIENDLY NAMES (FINAL VERSION)
# --------------------------------------------------
FRIENDLY_NAMES = {
    "prcp": "Heavy rainfall increases mosquito breeding",
    "tavg": "High temperature supports mosquito growth",
    "tmin": "Warm nights help mosquitoes survive",
    "tmax": "Hot daytime weather increases activity",
    "wspd": "Wind conditions affect mosquito movement",

    "Latitude": "Your location influences dengue risk",
    "Longitude": "Environmental conditions in your area",

    "Dengue_Cases_lag_1": "Recent dengue cases nearby",
    "Dengue_Cases_lag_2": "Cases reported in recent weeks",
    "Dengue_Cases_lag_3": "Ongoing dengue spread",
    "Dengue_Cases_lag_4": "Past dengue trends in your area",

    "prcp_lag_1": "Recent rainfall created breeding sites",
    "prcp_lag_2": "Previous rainfall increased risk",
    "prcp_lag_3": "Sustained rainfall supports mosquitoes",

    "tavg_lag_1": "Recent temperature trend supports spread",
    "tavg_lag_2": "Temperature pattern affects mosquito growth",
    "tavg_lag_3": "Sustained warm weather increases risk",
    "tavg_lag_4": "Previous weather conditions influenced risk"
}

# --------------------------------------------------
# Prediction Function
# --------------------------------------------------
def predict_dengue_risk(input_data: dict, model_type: str = "rf"):

    df = pd.DataFrame([input_data])

    # Ensure all features exist
    for col in FEATURES:
        if col not in df.columns:
            df[col] = 0

    df = df[FEATURES]
    df_scaled = scaler.transform(df)

    # -------------------------
    # Prediction
    # -------------------------
    prediction = rf_model.predict(df_scaled)[0]
    probabilities = rf_model.predict_proba(df_scaled)[0]

    explanations = []

    # -------------------------
    # SHAP Explainability
    # -------------------------
    try:
        shap_values = rf_explainer.shap_values(df_scaled)

        if isinstance(shap_values, list):
            shap_values = shap_values[prediction]

        shap_array = np.array(shap_values).flatten()
        feature_impact = dict(zip(FEATURES, shap_array))

        # Top 5 important features
        top_features = sorted(
            feature_impact.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]

        print("SHAP SUCCESS:", top_features)

        for feature, value in top_features:
            friendly = FRIENDLY_NAMES.get(feature, None)

            # ❌ Skip unknown technical features
            if friendly is None:
                continue

            # ✅ Add clean explanation
            if value > 0:
                explanations.append(f"{friendly}")
            else:
                explanations.append(f"{friendly}")

        # ✅ Limit to top 3 (clean UI)
        explanations = explanations[:3]

    except Exception as e:
        print("SHAP FAILED:", e)
        explanations = []

    # -------------------------
    # Fallback (never empty)
    # -------------------------
    if len(explanations) == 0:
        explanations = [
            "Weather conditions 🌦️ influenced mosquito activity",
            "Recent dengue trends 🦟 affected the prediction"
        ]

    # -------------------------
    # Alert Logic
    # -------------------------
    if prediction == 2:
        alert = True
        alert_message = "🚨 High dengue risk detected! Take precautions."
    elif prediction == 1:
        alert = False
        alert_message = "⚠️ Moderate dengue risk. Stay cautious."
    else:
        alert = False
        alert_message = "✅ Low dengue risk. Stay safe."

    # -------------------------
    # Response
    # -------------------------
    return {
        "risk_level": int(prediction),
        "low_risk_prob": float(probabilities[0]),
        "medium_risk_prob": float(probabilities[1]),
        "high_risk_prob": float(probabilities[2]),
        "alert": bool(alert),
        "alert_message": alert_message,
        "explanations": explanations
    }