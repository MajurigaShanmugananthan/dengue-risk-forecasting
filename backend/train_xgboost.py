import pandas as pd
from pathlib import Path
import joblib
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# --------------------------------------------------
# Correct project root
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]  # dengue_project

# --------------------------------------------------
# Load data
# --------------------------------------------------
X = pd.read_csv(BASE_DIR / "data/processed/X_train_scaled.csv")
y = pd.read_csv(BASE_DIR / "data/processed/y_train.csv").squeeze()

# Encode labels for XGBoost
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# --------------------------------------------------
# Train XGBoost model
# --------------------------------------------------
model = XGBClassifier(
    objective="multi:softprob",
    num_class=3,
    n_estimators=200,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="mlogloss",
    random_state=42
)

model.fit(X_train, y_train)

# --------------------------------------------------
# Evaluate
# --------------------------------------------------
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# --------------------------------------------------
# Save model
# --------------------------------------------------
MODEL_DIR = BASE_DIR / "backend/app/models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_DIR / "xgboost_model.pkl")
joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")

print("✅ STEP 13 — XGBoost model trained successfully")
