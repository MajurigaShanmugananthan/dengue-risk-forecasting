import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import joblib

BASE_DIR = Path(__file__).resolve().parents[4]

# --------------------------------------------------
# Load scaled features & labels
# --------------------------------------------------
X_train = pd.read_csv(BASE_DIR / "data/processed/X_train_scaled.csv")
y_train = pd.read_csv(BASE_DIR / "data/processed/y_train.csv").squeeze()

# --------------------------------------------------
# Train model
# --------------------------------------------------
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# --------------------------------------------------
# Save model
# --------------------------------------------------
MODEL_DIR = BASE_DIR / "backend/app/models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_DIR / "random_forest_model.pkl")

print("✅ STEP 12 — Random Forest model trained")
