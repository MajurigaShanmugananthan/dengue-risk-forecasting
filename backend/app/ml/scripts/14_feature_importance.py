import pandas as pd
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parents[4]

# --------------------------------------------------
# Load model
# --------------------------------------------------
model = joblib.load(
    BASE_DIR / "backend/app/models/random_forest_model.pkl"
)

# --------------------------------------------------
# Load original (unscaled) features
# --------------------------------------------------
X_train = pd.read_csv(BASE_DIR / "data/processed/X_train.csv")

# --------------------------------------------------
# Feature importance
# --------------------------------------------------
importance = pd.DataFrame({
    "Feature": X_train.columns,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

importance.to_csv(
    BASE_DIR / "data/processed/feature_importance.csv",
    index=False
)

print("✅ STEP 14 — Feature importance extracted")
print(importance.head(10))
