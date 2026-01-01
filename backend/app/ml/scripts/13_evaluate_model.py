import pandas as pd
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import joblib

BASE_DIR = Path(__file__).resolve().parents[4]

# --------------------------------------------------
# Load model
# --------------------------------------------------
model = joblib.load(
    BASE_DIR / "backend/app/models/random_forest_model.pkl"
)

# --------------------------------------------------
# Load test data
# --------------------------------------------------
X_test = pd.read_csv(BASE_DIR / "data/processed/X_test_scaled.csv")
y_test = pd.read_csv(BASE_DIR / "data/processed/y_test.csv").squeeze()

# --------------------------------------------------
# Predict
# --------------------------------------------------
y_pred = model.predict(X_test)

print("\n📊 Classification Report")
print(classification_report(y_test, y_pred))

print("🧩 Confusion Matrix")
print(confusion_matrix(y_test, y_pred))
