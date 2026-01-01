import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import confusion_matrix

BASE_DIR = Path(__file__).resolve().parents[4]

model = joblib.load(
    BASE_DIR / "backend/app/models/random_forest_model.pkl"
)

X_test = pd.read_csv(BASE_DIR / "data/processed/X_test_scaled.csv")
y_test = pd.read_csv(BASE_DIR / "data/processed/y_test.csv").squeeze()

y_pred = model.predict(X_test)

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix – Dengue Risk")
plt.tight_layout()

plt.savefig(BASE_DIR / "docs/confusion_matrix.png")
plt.show()

print("✅ STEP 16 — Confusion matrix saved")
