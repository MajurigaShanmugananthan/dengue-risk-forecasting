import pandas as pd
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]

model = joblib.load(
    BASE_DIR / "backend/app/models/random_forest_model.pkl"
)

X_test = pd.read_csv(BASE_DIR / "data/processed/X_test_scaled.csv")
y_test = pd.read_csv(BASE_DIR / "data/processed/y_test.csv").squeeze()

y_pred = model.predict(X_test)

results = X_test.copy()
results["Actual_Risk"] = y_test.values
results["Predicted_Risk"] = y_pred

results.to_csv(
    BASE_DIR / "data/processed/predictions_test_set.csv",
    index=False
)

print("✅ STEP 15 — Predictions saved")
